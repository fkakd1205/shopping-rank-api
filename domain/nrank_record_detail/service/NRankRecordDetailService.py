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
from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel

from exception.types.CustomException import *
from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomException import CustomInvalidValueException
from utils.db.v2.QueryUtils import transactional

PROXY_REQUEST_URL = "http://kr.smartproxy.com:10000"
NAVER_SHOPPINT_RANK_URL = "https://search.shopping.naver.com/search/all"
DEFAULT_PAGINGSIZE = 80

TOTAL_REQUEST_TIMEOUT_SIZE = 60
UNIT_REQUEST_TIMEOUT_SIZE = 30

# 랭킹 조회 가능 시간 = 1시간
SEARCHABLE_DIFF_SECONDS = 60 * 60

class NRankRecordDetailService():

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
                        url=NAVER_SHOPPINT_RANK_URL,
                        proxy=PROXY_REQUEST_URL,
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

                if (item['mallName'] == create_req_dto.mall_name):
                    model = NRankRecordDetailModel()
                    model.id = detail_id
                    model.mall_name = create_req_dto.mall_name
                    model.rank = int(item['rank'])
                    model.product_title = item['productTitle']
                    model.price = item['price']
                    # rank % 80 결과가 40보다 작으면 (page_index * 2) - 1, 40보다 크면 (page_index * 2)
                    model.page = ((page_index * 2) - 1) if ((model.rank % DEFAULT_PAGINGSIZE) <= (DEFAULT_PAGINGSIZE / 2)) else (page_index * 2)
                    model.mall_product_id = item['mallProductId']
                    model.included_ad_rank = included_ad_rank
                    model.review_count = item['reviewCount']
                    model.score_info = item['scoreInfo']
                    model.registration_date = item['openDate']
                    model.thumbnail_url = item['imageUrl']
                    model.purchase_count = item['purchaseCnt']
                    model.keep_count = item.get('keepCnt', 0)
                    model.delivery_fee = item['deliveryFeeContent']
                    model.category1_name = item['category1Name']
                    model.category2_name = item['category2Name']
                    model.category3_name = item['category3Name']
                    model.category4_name = item['category4Name']
                    model.nrank_record_info_id = create_req_dto.record_info_id

                    if('adId' in item):
                        model.advertising_yn = 'y'
                        model.thumbnail_url = item.get('adImageUrl', model.thumbnail_url)
                        model.page = None
                        model.rank = 0
                        model.included_ad_rank = included_ad_rank

                    models.append(model)

                # 가격비교 쇼핑몰 검색
                # item['lowMallList'] = null or []
                if (item['lowMallList'] is not None):
                    # 가격비교 상품들의 공통 필드
                    comparition_rank = 0
                    rank = int(item['rank'])
                    product_title = item['productTitle']
                    review_count = item['reviewCount']
                    score_info = item['scoreInfo']
                    registration_date = item['openDate']
                    thumbnail_url = item['imageUrl']
                    purchase_count = item['purchaseCnt']
                    keep_count = item.get('keepCnt', 0)
                    delivery_fee = item['deliveryFeeContent']
                    category1_name = item['category1Name']
                    category2_name = item['category2Name']
                    category3_name = item['category3Name']
                    category4_name = item['category4Name']
                    low_mall_count = item['mallCount']
                    page = ((page_index * 2) - 1) if ((rank % DEFAULT_PAGINGSIZE) <= (DEFAULT_PAGINGSIZE / 2)) else (page_index * 2)

                    for low_item in item['lowMallList']:
                        comparition_rank += 1
                        if (low_item['name'] == create_req_dto.mall_name):
                            model = NRankRecordDetailModel()
                            model.id = uuid.uuid4()
                            model.mall_name = create_req_dto.mall_name
                            model.rank = rank
                            model.included_ad_rank = included_ad_rank
                            model.price_comparision_yn = 'y'
                            model.comparision_rank = comparition_rank
                            model.product_title = product_title
                            model.price = low_item['price']
                            model.page = page
                            model.mall_product_id = low_item['mallPid']
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

    @transactional
    def create_list(self, create_req_dto):
        """search naver shopping ranking and create rank details
        
        + nrank_record_info의 created_at으로 랭킹 조회 가능 시간 제한
        1. nrank_record_info 초기화
        2. nrank_record 조회
        3. 랭킹 조회 가능 시간 검사
        4. (2)에서 조회된 keyword & mallname으로 랭킹 검사
        5. 광고 상품 순위 설정
        6. nrank_record_detail 저장
        7. 조회된 결과로 nrank_record_info 설정 및 저장
        8. nrank_record의 current_nrank_record_info_id 업데이트
        """
        nrank_record_detail_repository = NRankRecordDetailRepository()
        nrank_record_info_repository = NRankRecordInfoRepository()
        nrank_record_repository = NRankRecordRepository()

        # 1.
        record_info_model = NRankRecordInfoModel()
        record_info_model.id = uuid.uuid4()
        record_info_model.nrank_record_id = create_req_dto.record_id

        # 2.
        record_model = nrank_record_repository.search_one(create_req_dto.record_id)
        # 3.
        last_info_model = nrank_record_info_repository.search_one(record_model.current_nrank_record_info_id)
        self.checkSearchableTime(last_info_model)

        create_req_dto.keyword = record_model.keyword
        create_req_dto.mall_name = record_model.mall_name

        # 4.
        create_req_dto.record_info_id = record_info_model.id
        results = asyncio.run(self.request_shopping_ranking(create_req_dto))
        # 5.
        updated_results = self.updateRankForAdProduct(create_req_dto, results)
        
        # 6.
        nrank_record_detail_repository.bulk_save(updated_results)

        # 7.
        record_info_model.rank_detail_unit = len(results) - create_req_dto.ad_product_unit
        record_info_model.ad_rank_detail_unit = create_req_dto.ad_product_unit
        self.create_nrank_record_info(record_info_model, updated_results)

        # 8.
        record_model.current_nrank_record_info_id = create_req_dto.record_info_id
        nrank_record_repository.save(record_model)
    
    def checkSearchableTime(self, last_info_model):
        last_searched_at = last_info_model.created_at
        diff = DateTimeUtils.get_current_datetime() - last_searched_at

        if(SEARCHABLE_DIFF_SECONDS > diff.seconds):
            raise CustomMethodNotAllowedException("요청 가능 시간이 아닙니다. 잠시 후 시도해주세요.")

    def updateRankForAdProduct(self, create_req_dto, results):
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

    def create_nrank_record_info(self, record_info, results):
        nrank_record_info_repository = NRankRecordInfoRepository()
        ad_thumbnail_url = None
        thumbnail_url = None
        
        # 1. 일반상품 썸네일 / 2. 광고상품 썸네일
        for result in results:
            if (result.advertising_yn == 'y' and ad_thumbnail_url is None):
                ad_thumbnail_url = result.thumbnail_url
            elif(result.advertising_yn == 'n'):
                thumbnail_url = result.thumbnail_url
                break
        
        record_info.thumbnail_url = ad_thumbnail_url if (thumbnail_url is None) else thumbnail_url
        record_info.created_at = DateTimeUtils.get_current_datetime()
        nrank_record_info_repository.save(record_info)

    def search_list_by_record_info_id(self, record_info_id):
        nrank_record_detail_repository = NRankRecordDetailRepository()
        
        detail_entities = nrank_record_detail_repository.search_list_by_record_info_id(record_info_id)
        detail_dtos = list(map(lambda entity: NRankRecordDetailDto.to_dto(entity), detail_entities))
        return detail_dtos