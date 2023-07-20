from flask import request
import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import uuid
from fake_useragent import UserAgent

from aiohttp.client_exceptions import ClientProxyConnectionError, ClientOSError, ClientHttpProxyError

from domain.nrank_record_detail.dto.NRankRecordDetailDto import NRankRecordDetailDto
from domain.nrank_record_detail.model.NRankRecordDetailModel import NRankRecordDetailModel
from domain.nrank_record_detail.repository.NRankRecordDetailRepositoryV3 import NRankRecordDetailRepository
from domain.nrank_record.repository.NRankRecordRepositoryV3 import NRankRecordRepository
from domain.nrank_record_info.dto.NRankRecordInfoDto import NRankRecordInfoDto
from domain.nrank_record_info.repository.NRankRecordInfoRepository import NRankRecordInfoRepository
from domain.nrank_record_info.model.NRankRecordInfoModel import NRankRecordInfoModel

from utils.date.DateTimeUtils import DateTimeUtils
from exception.types.CustomInvalidValueException import CustomInvalidValueException

PROXY_REQUEST_URL = "http://kr.smartproxy.com:10000"
NAVER_SHOPPINT_RANK_URL = "https://search.shopping.naver.com/search/all"
DEFAULT_PAGINGSIZE = 80

TOTAL_REQUEST_TIMEOUT_SIZE = 60
UNIT_REQUEST_TIMEOUT_SIZE = 30

class NRankRecordDetailService():

    def __init__(self, page_size = 0, record_id = None):
        self.keyword = None
        self.mall_name = None
        self.page_size = page_size
        self.record_id = record_id
        self.record_info_id = None

    def set_request_info(self, record_model):
        self.keyword = record_model.keyword
        self.mall_name = record_model.mall_name

    async def get_current_page_response(self, page_index):
        params = {
            'frm': 'NVSHTTL',
            'pagingIndex': page_index,
            'pagingSize': DEFAULT_PAGINGSIZE,
            'query': self.keyword,
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
                        proxy = PROXY_REQUEST_URL,
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

    async def search_page_and_get_rank_models(self, page_index):
        # get response by naver ranking page
        searchResponse = await asyncio.create_task(self.get_current_page_response(page_index))

        try:
            # 한 페이지에 여러 상품이 노출될 수 있으므로 list 반환
            result = []
            included_ad_rank = DEFAULT_PAGINGSIZE * (page_index-1)
            for responseObj in searchResponse: 
                models = []
                item = responseObj['item']
                included_ad_rank += 1

                if (item['mallName'] == self.mall_name):
                    model = NRankRecordDetailModel()
                    model.id = uuid.uuid4()
                    model.mall_name = self.mall_name
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
                    model.nrank_record_info_id = self.record_info_id

                    if('adId' in item):
                        model.thumbnail_url = item.get('adImageUrl', model.thumbnail_url)
                        model.page = None
                        # TODO :: 광고 상품 순위 설정
                        model.rank = 0
                        model.advertising_yn = 'y'

                    models.append(model)
                    # continue

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
                        if (low_item['name'] == self.mall_name):
                            model = NRankRecordDetailModel()
                            model.id = uuid.uuid4()
                            model.mall_name = self.mall_name
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
                            model.nrank_record_info_id = self.record_info_id
                            models.append(model)

                result.extend(models)
            return result
        except KeyError as e:
            raise CustomInvalidValueException(f"not found value for {e}")
        except AttributeError as e:
            raise CustomInvalidValueException(e)

    def create_list(self):
        nRankRecordDetailRepository = NRankRecordDetailRepository()
        nRankRecordRepository = NRankRecordRepository()
        record_model = nRankRecordRepository.search_one(self.record_id)
        self.set_request_info(record_model)

        record_info_dto = NRankRecordInfoDto()
        record_info_dto.id = uuid.uuid4()
        record_info_dto.nrank_record_id = self.record_id

        self.record_info_id = record_info_dto.id
        results = asyncio.run(self.request_shopping_ranking())

        # 1. 랭킹 조회가 완료되면 nrank_record_detail 생성, nrank_record_info 생성. nrank_record의 current_nrank_record_id 업데이트
        nRankRecordDetailRepository.bulk_save(results)
        self.create_nrank_record_info(record_info_dto, results)
        record_model.current_nrank_record_info_id = self.record_info_id
        nRankRecordRepository.save(record_model)

    async def request_shopping_ranking(self):
        results = []

        # pageSize 만큼 비동기 요청
        rank_entities = [self.search_page_and_get_rank_models(i+1) for i in range(self.page_size)]
        tasks = asyncio.gather(*rank_entities)

        # 전체 요청시간이 TOTAL_REQUEST_TIMEOUT_SIZE를 초과한다면 기다리지 않고 예외처리
        try:
            await asyncio.wait_for(tasks, timeout=TOTAL_REQUEST_TIMEOUT_SIZE)
        except asyncio.TimeoutError:
            tasks.cancel()
            raise TimeoutError("request time out")
        
        for result in tasks.result():
            results.extend(result)

        return results

    def create_nrank_record_info(self, record_info_dto, results):
        nRankRecordInfoRepository = NRankRecordInfoRepository()
        ad_thumbnail_url = None
        thumbnail_url = None
        
        # 1. 일반상품 썸네일 / 2. 광고상품 썸네일
        for result in results:
            if (result.advertising_yn == 'y' and ad_thumbnail_url is None):
                ad_thumbnail_url = result.thumbnail_url
            else:
                thumbnail_url = result.thumbnail_url
                break
        
        record_info_dto.thumbnail_url = ad_thumbnail_url if (thumbnail_url is None) else thumbnail_url
        record_info_dto.created_at = DateTimeUtils.get_current_datetime()
        model = NRankRecordInfoModel.to_model(record_info_dto)
        nRankRecordInfoRepository.save(model)

    def search_list_by_record_info_id(self, record_info_id):
        nRankRecordDetailRepository = NRankRecordDetailRepository()
        
        detail_entities = nRankRecordDetailRepository.search_list_by_record_info_id(record_info_id)
        detail_dtos = list(map(lambda entity: NRankRecordDetailDto.to_dto(entity), detail_entities))
        return detail_dtos