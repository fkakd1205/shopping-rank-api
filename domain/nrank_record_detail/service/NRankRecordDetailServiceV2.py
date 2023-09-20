import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import uuid
from fake_useragent import UserAgent
import copy
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientOSError, ClientHttpProxyError

from domain.nrank_record_detail.dto.NRankRecordDetailDto import NRankRecordDetailDto
from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel
from domain.nrank_record_detail.repository.NRankRecordDetailRepository import NRankRecordDetailRepository
from domain.nrank_record.repository.NRankRecordRepository import NRankRecordRepository
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_detail.dto.NRankRecordDetailCreateReqDto import NRankRecordDetailCreateReqDto

from enums.NRankRecordStatusEnum import NRankRecordStatusEnum
from enums.YnEnum import YnEnum
from enums.NRankRecordInfoStatusEnum import NRankRecordInfoStatusEnum
from exception.types.CustomException import *
from utils import DateTimeUtils, ProxyUtils
from exception.types.CustomException import CustomInvalidValueException
from decorators import transactional

NAVER_SHOPPING_RANK_URL = "https://search.shopping.naver.com/search/all"
DEFAULT_PAGINGSIZE = 80

# 랭킹 조회 요청 타임아웃 = 60초
TOTAL_REQUEST_TIMEOUT_SIZE = 60
UNIT_REQUEST_TIMEOUT_SIZE = 30

# 랭킹 조회 가능 시간 = 10분
SEARCHABLE_DIFF_SECONDS = 60 * 10

class NRankRecordDetailService():

    @transactional
    def search_list_by_record_info_id(self, record_info_id):
        nrankRecordDetailRepository = NRankRecordDetailRepository()
        detail_entities = nrankRecordDetailRepository.search_list_by_record_info_id(record_info_id)
        detail_dtos = list(map(lambda entity: NRankRecordDetailDto.to_dto(entity), detail_entities))
        return detail_dtos
    
    @transactional
    def create_list(self, req_dto):
        """search naver shopping ranking and create rank details
        
        + nrank_record_info의 created_at으로 랭킹 조회 가능 시간 제한
        1. nrank_record_info 조회 및 상태 검사
        2. nrank_record 조회
        3. 랭킹 조회 가능 시간 검사
        4. (2)에서 조회된 keyword & mallname으로 랭킹 조회
        5. 광고 상품 순위 설정
        6. nrank_record_detail 저장
        7. 조회된 결과로 nrank_record_info 설정 및 저장
        8. nrank_record의 current_nrank_record_info_id 업데이트
        """
        create_req_dto = NRankRecordDetailCreateReqDto()
        create_req_dto.page_size = req_dto['page_size']
        create_req_dto.record_id = req_dto['record_id']
        create_req_dto.record_info_id = req_dto['record_info_id']

        nrankRecordDetailRepository = NRankRecordDetailRepository()
        nrankRecordInfoRepository = NRankRecordInfoRepository()
        nrankRecordRepository = NRankRecordRepository()
        current_datetime = DateTimeUtils.get_current_datetime()

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
                self.checkSearchableTime(last_info_model.created_at)

        # 4.
        create_req_dto.record_info_id = record_info_model.id
        results = asyncio.run(self.request_shopping_ranking(create_req_dto))

        # 5.
        updated_results = self.updateRankForAdProduct(create_req_dto, results)
        
        # 6.
        nrankRecordDetailRepository.bulk_save(updated_results)

        # 7.
        record_info_model.rank_detail_unit = len(results) - create_req_dto.ad_product_unit
        record_info_model.ad_rank_detail_unit = create_req_dto.ad_product_unit
        record_info_model.thumbnail_url = self.get_thumbnail_by_rank_results(updated_results)
        record_info_model.status = NRankRecordInfoStatusEnum.COMPLETE.value
        nrankRecordInfoRepository.save(record_info_model)

        # 8.
        record_model.current_nrank_record_info_id = create_req_dto.record_info_id
        record_model.status = NRankRecordStatusEnum.COMPLETE.value
        record_model.status_updated_at = current_datetime
        nrankRecordRepository.save(record_model)
    
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

        try:
            # 한 페이지에 스토어의 여러 상품이 노출될 수 있으므로 list로 반환
            result = []
            included_ad_rank = DEFAULT_PAGINGSIZE * (page_index-1)
            for responseObj in searchResponse: 
                models = []
                item = responseObj['item']
                included_ad_rank += 1
                detail_id =  uuid.uuid4()
                
                if ('adId' in item):
                    create_req_dto.total_ad_products[included_ad_rank] = detail_id

                if (item.get('mallName') == create_req_dto.mall_name):
                    model = NRankRecordDetailModel()
                    model.id = detail_id
                    model.mall_name = create_req_dto.mall_name
                    model.rank = int(item.get('rank') or 0)
                    model.product_title = item.get('productTitle') or ''
                    model.price = item.get('price') or None
                    # rank % 80 결과가 40보다 작으면 (page_index * 2) - 1, 40보다 크면 (page_index * 2)
                    model.page = ((page_index * 2) - 1) if ((model.rank % DEFAULT_PAGINGSIZE) <= (DEFAULT_PAGINGSIZE / 2)) else (page_index * 2)
                    model.mall_product_id = item.get('mallProductId') or None
                    model.review_count = item.get('reviewCount') or None
                    model.score_info = item.get('scoreInfo') or None
                    model.registration_date = item.get('openDate') or None
                    model.thumbnail_url = item.get('imageUrl') or None
                    model.purchase_count = item.get('purchaseCnt') or None
                    model.keep_count = item.get('keepCnt') or None
                    model.delivery_fee = item.get('deliveryFeeContent') or None
                    model.category1_name = item.get('category1Name') or None
                    model.category2_name = item.get('category2Name') or None
                    model.category3_name = item.get('category3Name') or None
                    model.category4_name = item.get('category4Name') or None
                    model.nrank_record_info_id = create_req_dto.record_info_id

                    if('adId' in item):
                        model.advertising_yn = YnEnum.Y.value
                        # 광고상품의 썸네일은 'adImageUrl', 없다면 'imageUrl'로 결정
                        model.thumbnail_url = item.get('adImageUrl', model.thumbnail_url)
                        model.page = None
                        model.rank = 0
                        model.included_ad_rank = included_ad_rank

                    models.append(model)

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
                    page = ((page_index * 2) - 1) if ((rank % DEFAULT_PAGINGSIZE) <= (DEFAULT_PAGINGSIZE / 2)) else (page_index * 2)

                    for low_item in item['lowMallList']:
                        comparition_rank += 1
                        if (low_item.get('name') == create_req_dto.mall_name):
                            model = NRankRecordDetailModel()
                            model.id = uuid.uuid4()
                            model.mall_name = create_req_dto.mall_name
                            model.rank = rank
                            model.included_ad_rank = included_ad_rank
                            model.price_comparision_yn = YnEnum.Y.value
                            model.comparision_rank = comparition_rank
                            model.product_title = product_title
                            model.price = low_item.get('price') or None
                            model.page = page
                            model.mall_product_id = low_item.get('mallPid') or None
                            model.review_count = review_count
                            model.score_info = score_info
                            model.registration_date = registration_date
                            model.thumbnail_url = thumbnail_url
                            model.purchase_count = purchase_count
                            model.keep_count = keep_count
                            model.delivery_fee = delivery_fee
                            model.category1_name = category1_name
                            model.category2_name = category2_name
                            model.category3_name = category3_name
                            model.category4_name = category4_name
                            model.low_mall_count = low_mall_count
                            model.nrank_record_info_id = create_req_dto.record_info_id
                            models.append(model)

                result.extend(models)
            return result
        except KeyError as e:
            raise CustomInvalidValueException(f"not found value for {e}")
        except AttributeError as e:
            raise CustomInvalidValueException(e)

    def checkSearchableTime(self, last_searched_at):
        """check store rank searchable time
        
        last_searched_at -- created_at of nrank record info 
        """
        diff = DateTimeUtils.get_current_datetime() - last_searched_at
        if(SEARCHABLE_DIFF_SECONDS > diff.seconds):
            raise CustomMethodNotAllowedException("요청 가능 시간이 아닙니다. 잠시 후 시도해주세요.")
        
    def updateRankForAdProduct(self, create_req_dto, results):
        """update rank for advertisement product

        광고 상품들끼리의 순위를 계산
        광고 상품 개수를 구한다
        """
        # 순위별로 광고상품 정렬
        sorted_ad_products = dict(sorted(create_req_dto.total_ad_products.items()))
        
        # 광고상품 순위 설정된 results
        updated_results = copy.deepcopy(results)
        ad_detail_ids = sorted_ad_products.values()
        for idx, ad_detail_id in enumerate(ad_detail_ids):
            for result in updated_results:
                if(result.id == ad_detail_id):
                    result.rank = idx + 1
                    create_req_dto.ad_product_unit += 1
        return updated_results

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
