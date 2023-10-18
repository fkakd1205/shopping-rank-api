import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import uuid
from fake_useragent import UserAgent
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientOSError, ClientHttpProxyError
import requests
from flask import request

from domain.nrank_record_detail.dto.NRankRecordDetailDto import NRankRecordDetailDto
from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel
from domain.nrank_record_detail.repository.NRankRecordDetailRepository import NRankRecordDetailRepository
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_detail.dto.NRankRecordDetailCreateReqDto import NRankRecordDetailCreateReqDto
from domain.nrank_record_detail.dto.NRankRecordDetailSearchReqDto import NRankRecordDetailSearchReqDto

from enums.NRankRecordStatusEnum import NRankRecordStatusEnum
from enums.YnEnum import YnEnum
from enums.NRankRecordInfoStatusEnum import NRankRecordInfoStatusEnum
from exception.types.CustomException import *
from exception.types.CustomException import CustomInvalidValueException
from decorators import transactional
from config.server.ServerConfig import config
from utils import DateTimeUtils, ProxyUtils

NAVER_SHOPPING_RANK_URL = "https://search.shopping.naver.com/search/all"
DEFAULT_PAGINGSIZE = 80

# 랭킹 조회 요청 타임아웃 = 60초
TOTAL_REQUEST_TIMEOUT_SIZE = 60
UNIT_REQUEST_TIMEOUT_SIZE = 30

# 랭킹 조회 가능 시간 = 10분
SEARCHABLE_DIFF_SECONDS = 60 * 10

class NRankRecordDetailService():

    @transactional(read_only=True)
    def search_list_by_record_info_id(self, record_info_id):
        nrankRecordDetailRepository = NRankRecordDetailRepository()
        detail_entities = nrankRecordDetailRepository.search_list_by_record_info_id(record_info_id)
        detail_dtos = list(map(lambda entity: NRankRecordDetailDto.to_dto(entity), detail_entities))
        return detail_dtos

    @transactional(read_only=True)
    def nrank_request_setting(self, create_req_dto):
        """naver shopping ranking request setting
        shopping ranking api를 요청하기 전 request dto 세팅
        
        1. nrank_record_info 조회 및 상태 검사
        2. nrank_record 조회
        3. 이전 랭킹 조회 내역이 존재한다면 재조회 가능 시간 검사
        """
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        nrankRecordRepository = NRankRecordRepository()

        # 1.
        record_info_model = nrankRecordInfoRepository.search_one(create_req_dto.record_info_id)
        if((record_info_model is None) or (record_info_model.status != NRankRecordInfoStatusEnum.NONE.value)) :
            raise CustomMethodNotAllowedException("올바르지 않은 요청입니다.")

        # 2.
        record_model = nrankRecordRepository.search_one(create_req_dto.record_id)
        create_req_dto.keyword = record_model.keyword
        create_req_dto.mall_name = record_model.mall_name

        # 3.
        if(record_model.current_nrank_record_info_id):
            last_info_model = nrankRecordInfoRepository.search_one(record_model.current_nrank_record_info_id)
            if(last_info_model):
                self.check_searchable_time(last_info_model.created_at)

        create_req_dto.record_info_id = record_info_model.id
        return create_req_dto

    def request_nrank(self, req_dto, cookies):
        """search naver shopping ranking 요청 및 저장 api 호출"""
        create_req_dto = NRankRecordDetailCreateReqDto.RequestNRank(req_dto)
        results = asyncio.run(self.request_shopping_ranking(create_req_dto))
        ws_id = create_req_dto.workspace_id

        request_url = config['origin']['store-rank-api'] + '/api/v1/nrank-record-details/results'
        request_headers = {
            'wsId': ws_id,
            'referer': config['origin']['store-rank-api'],
            'nrankDirectAccessKey': config['nrankDirectAccessKey'],
            'Content-Type': 'application/json'
        }

        detail_create_req_dto = {
            'create_req_dto': create_req_dto.__dict__,
            'nrank_record_details': results
        }

        # 랭킹 조회 결과를 저장할 api 요청
        requests.post(url=request_url, 
            headers=request_headers,
            cookies=cookies,
            data=json.dumps(detail_create_req_dto),
            verify=False
        )

    @transactional()
    def create_list(self):
        """create rank details
        
        1. 광고 상품 순위 설정
        2. nrank_record_detail 저장
        3. 조회된 결과로 nrank_record_info 설정 및 저장
        4. nrank_record의 current_nrank_record_info_id 업데이트
        """
        nrankRecordDetailRepository = NRankRecordDetailRepository()
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        nrankRecordRepository = NRankRecordRepository()

        # filter 클래스 생성
        body = request.get_json()
        rank_result_dto = NRankRecordDetailCreateReqDto.RankResult(body)
        req_dto = rank_result_dto.create_req_dto
        results = rank_result_dto.nrank_record_details
        current_datetime = DateTimeUtils.get_current_datetime()

        create_req_dto = NRankRecordDetailCreateReqDto.RequestNRank(req_dto)
        record_info_model = nrankRecordInfoRepository.search_one(create_req_dto.record_info_id)
        record_model = nrankRecordRepository.search_one(create_req_dto.record_id)

        # 1.
        if(create_req_dto.total_ad_products):
            self.update_rank_for_ad_product(create_req_dto, results)

        nrank_detail_models = list(map(lambda dto: NRankRecordDetailModel().to_model(dto), results))
            
        # 2.
        nrankRecordDetailRepository.bulk_save(nrank_detail_models)

        # 3.
        record_info_model.rank_detail_unit = len(nrank_detail_models) - create_req_dto.ad_product_unit
        record_info_model.ad_rank_detail_unit = create_req_dto.ad_product_unit
        record_info_model.thumbnail_url = self.get_thumbnail_by_rank_results(nrank_detail_models)
        record_info_model.status = NRankRecordInfoStatusEnum.COMPLETE.value
        nrankRecordInfoRepository.save(record_info_model)

        # 4.
        record_model.current_nrank_record_info_id = create_req_dto.record_info_id
        record_model.status = NRankRecordStatusEnum.COMPLETE.value
        record_model.status_updated_at = current_datetime
        nrankRecordInfoRepository.save(record_model)
    
    async def get_current_page_response(self, page_index, create_req_dto):
        params = {
            'frm': 'NVSHTTL',
            'pagingIndex': page_index,
            'pagingSize': DEFAULT_PAGINGSIZE,
            'query': create_req_dto.keyword,
            'sort': 'rel',
            'productSet': 'total',
        }

        response = None
        productList = []

        # 프록시 서버를 이용해 request 응답이 성공할 때까지 요청을 중단하지 않는다
        while(True):
            headers = {"user-agent": UserAgent().random}
            try:
                async with aiohttp.ClientSession() as session:
                    res = await session.get(
                        url=NAVER_SHOPPING_RANK_URL,
                        proxy=ProxyUtils.PROXY_REQUEST_URL,
                        timeout=UNIT_REQUEST_TIMEOUT_SIZE,
                        headers=headers,
                        params=params
                        )
                    response = await res.text()
            except (ConnectionRefusedError, ClientProxyConnectionError, ClientOSError, ClientHttpProxyError):
                print("proxy connection error")
                continue
            except asyncio.TimeoutError:
                print("proxy connection time out")
                continue
            except aiohttp.ServerDisconnectedError:
                print("server does not accept request")
                continue

            try:
                dom = BeautifulSoup(response, "html.parser")
                resultObj = dom.select_one("#__NEXT_DATA__").text
                productJsonObj = json.loads(resultObj)
                productList = productJsonObj['props']['pageProps']['initialState']['products']['list']
            except (KeyError, AttributeError, UnboundLocalError, TypeError):
                # 응답은 넘어오지만, response attribute가 올바르지 않는다면 다음 프록시 요청
                print("response attribute error")
                continue
                
            return productList

    async def search_page_and_get_rank_models(self, page_index, create_req_dto):
        # get response by naver ranking page
        searchResponse = await asyncio.create_task(self.get_current_page_response(page_index, create_req_dto))
        ad_products = create_req_dto.total_ad_products or {}

        try:
            # 한 페이지에 스토어의 여러 상품이 노출될 수 있으므로 list로 반환
            result = []
            included_ad_rank = DEFAULT_PAGINGSIZE * (page_index-1)
            for responseObj in searchResponse: 
                dtos = []
                item = responseObj['item']
                included_ad_rank += 1
                detail_id = str(uuid.uuid4())
                
                if ('adId' in item):
                    ad_products[included_ad_rank] = detail_id
                    
                if (item.get('mallName') == create_req_dto.mall_name):
                    dto = NRankRecordDetailDto()
                    dto.id = detail_id
                    dto.mall_name = create_req_dto.mall_name
                    dto.rank = int(item.get('rank') or 0)
                    dto.product_title = item.get('productTitle') or ''
                    dto.price = item.get('price') or None
                    # rank % 80 결과가 40보다 작으면 (page_index * 2) - 1, 40보다 크면 (page_index * 2)
                    dto.page = ((page_index * 2) - 1) if ((dto.rank % DEFAULT_PAGINGSIZE) <= (DEFAULT_PAGINGSIZE / 2)) else (page_index * 2)
                    dto.item_id = item.get('id') or None
                    dto.mall_product_id = item.get('mallProductId') or None
                    dto.review_count = item.get('reviewCount') or None
                    dto.score_info = item.get('scoreInfo') or None
                    dto.registration_date = item.get('openDate') or None
                    dto.thumbnail_url = item.get('imageUrl') or None
                    dto.purchase_count = item.get('purchaseCnt') or None
                    dto.keep_count = item.get('keepCnt') or None
                    dto.delivery_fee = item.get('deliveryFeeContent') or None
                    dto.category1_name = item.get('category1Name') or None
                    dto.category2_name = item.get('category2Name') or None
                    dto.category3_name = item.get('category3Name') or None
                    dto.category4_name = item.get('category4Name') or None
                    dto.nrank_record_info_id = create_req_dto.record_info_id

                    if('adId' in item):
                        dto.advertising_yn = YnEnum.Y.value
                        # 광고상품의 썸네일은 'adImageUrl', 없다면 'imageUrl'로 결정
                        dto.thumbnail_url = item.get('adImageUrl', dto.thumbnail_url)
                        dto.page = None
                        dto.rank = 0
                        dto.included_ad_rank = included_ad_rank

                    dtos.append(dto.__dict__)

                # 가격비교 쇼핑몰 검색
                # item['lowMallList'] = null or []
                if (item.get('lowMallList')):
                    # 가격비교 상품들의 공통 필드
                    comparition_rank = 0
                    rank = int(item.get('rank') or 0)
                    product_title = item.get('productTitle') or ''
                    review_count = item.get('reviewCount') or None
                    score_info = item.get('scoreInfo') or None
                    registration_date = item.get('openDate') or None
                    thumbnail_url = item.get('imageUrl') or None
                    purchase_count = item.get('purchaseCnt') or None
                    keep_count = item.get('keepCnt') or None
                    delivery_fee = item.get('deliveryFeeContent') or None
                    category1_name = item.get('category1Name') or None
                    category2_name = item.get('category2Name') or None
                    category3_name = item.get('category3Name') or None
                    category4_name = item.get('category4Name') or None
                    low_mall_count = item.get('mallCount') or None
                    item_id = item.get('id') or None

                    page = ((page_index * 2) - 1) if ((rank % DEFAULT_PAGINGSIZE) <= (DEFAULT_PAGINGSIZE / 2)) else (page_index * 2)

                    for low_item in item['lowMallList']:
                        comparition_rank += 1
                        if (low_item.get('name') == create_req_dto.mall_name):
                            dto = NRankRecordDetailDto()
                            dto.id = str(uuid.uuid4())
                            dto.mall_name = create_req_dto.mall_name
                            dto.rank = rank
                            dto.included_ad_rank = included_ad_rank
                            dto.price_comparision_yn = YnEnum.Y.value
                            dto.comparision_rank = comparition_rank
                            dto.product_title = product_title
                            dto.price = low_item.get('price') or None
                            dto.page = page
                            dto.mall_product_id = low_item.get('mallPid') or None
                            dto.item_id = item_id
                            dto.review_count = review_count
                            dto.score_info = score_info
                            dto.registration_date = registration_date
                            dto.thumbnail_url = thumbnail_url
                            dto.purchase_count = purchase_count
                            dto.keep_count = keep_count
                            dto.delivery_fee = delivery_fee
                            dto.category1_name = category1_name
                            dto.category2_name = category2_name
                            dto.category3_name = category3_name
                            dto.category4_name = category4_name
                            dto.low_mall_count = low_mall_count
                            dto.nrank_record_info_id = create_req_dto.record_info_id
                            dtos.append(dto.__dict__)
                
                create_req_dto.total_ad_products = ad_products
                result.extend(dtos)
            return result
        except KeyError as e:
            raise CustomInvalidValueException(f"not found value for {e}")
        except AttributeError as e:
            raise CustomInvalidValueException(e)

    def check_searchable_time(self, last_searched_at):
        """check store rank searchable time
        
        last_searched_at -- created_at of nrank record info 
        """
        diff = DateTimeUtils.get_current_datetime() - last_searched_at
        if(SEARCHABLE_DIFF_SECONDS > diff.seconds):
            raise CustomMethodNotAllowedException("요청 가능 시간이 아닙니다. 잠시 후 시도해주세요.")
        
    def update_rank_for_ad_product(self, create_req_dto, details):
        """update rank for advertisement product

        광고 상품들끼리의 순위를 계산
        광고 상품 개수를 구한다
        """
        # 순위별로 광고상품 정렬
        sorted_ad_products = dict(sorted(create_req_dto.total_ad_products.items()))

        ad_detail_ids = sorted_ad_products.values()

        # 광고 상품 세팅
        for detail in details:
            for idx, ad_detail_id in enumerate(ad_detail_ids):
                if(detail.get('id') == ad_detail_id):
                    detail['rank'] = idx + 1
                    create_req_dto.ad_product_unit += 1
                    break

    async def request_shopping_ranking(self, create_req_dto):
        """request naver store ranking page
        
        요청 페이지 만큼 비동기 요청 실행
        해당 요청이 TOTAL_REQUEST_TIMEOUT_SIZE보다 오래 걸린다면 예외처리
        """
        ranking_results = []
        # pageSize 만큼 비동기 요청

        rank_entities = [self.search_page_and_get_rank_models(i+1, create_req_dto) for i in range(create_req_dto.page_size)]
        tasks = asyncio.gather(*rank_entities)

        # 전체 요청시간이 TOTAL_REQUEST_TIMEOUT_SIZE를 초과한다면 기다리지 않고 예외처리
        try:
            await asyncio.wait_for(tasks, timeout=TOTAL_REQUEST_TIMEOUT_SIZE)
        except asyncio.TimeoutError:
            tasks.cancel()
            raise CustomTimeoutException("요청 소요시간이 초과되었습니다. 재시도 해주세요.")
        
        for result in tasks.result():
            ranking_results.extend(result)
        return ranking_results

    def get_thumbnail_by_rank_results(self, results):
        """get thumbnail of nrank record
        
        우선순위 1.일반상품 썸네일, 2. 광고상품 썸네일 순으로 대표 썸네일을 반환한다.
        """
        ad_thumbnail_url = None
        thumbnail_url = None
        
        # 1. 일반상품 썸네일 / 2. 광고상품 썸네일
        for result in results:
            if ((result.advertising_yn == YnEnum.Y.value) and (ad_thumbnail_url is None)):
                ad_thumbnail_url = result.thumbnail_url
            elif(result.advertising_yn == YnEnum.N.value):
                thumbnail_url = result.thumbnail_url
                break
        
        return thumbnail_url or ad_thumbnail_url
    
    @transactional(read_only=True)
    def search_list_by_filter(self):
        nRankRecordDetailRepository = NRankRecordDetailRepository()

        body = request.get_json()
        req_dto = NRankRecordDetailSearchReqDto.IncludedRecordInfoIdsAndMallProductIdAndItemId(body)

        if(req_dto.info_ids is None or req_dto.detail_mall_product_id is None):
            raise CustomInvalidValueException("검색이 불가능한 항목입니다.")

        detail_models = nRankRecordDetailRepository.search_list_by_record_info_ids_and_pid_and_iid(req_dto.info_ids, req_dto.detail_mall_product_id, req_dto.detail_item_id)
        detail_dtos = list(map(lambda model: NRankRecordDetailDto.to_dto(model), detail_models))
        return detail_dtos
