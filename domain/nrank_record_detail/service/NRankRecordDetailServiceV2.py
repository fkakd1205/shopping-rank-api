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
from domain.nrank_record_detail.repository.NRankRecordDetailRepositoryV2 import NRankRecordDetailRepository
from domain.nrank_record.repository.NRankRecordRepositoryV2 import NRankRecordRepository

PROXY_REQUEST_URL = "http://kr.smartproxy.com:10000"
NAVER_SHOPPINT_RANK_URL = "https://search.shopping.naver.com/search/all"
DEFAULT_PAGINGSIZE = 80

TOTAL_REQUEST_TIMEOUT_SIZE = 60
UNIT_REQUEST_TIMEOUT_SIZE = 30

class NRankRecordDetailService():

    def __init__(self, page_size = 0):
        self.keyword = None
        self.mall_name = None
        self.page_size = page_size

    def set_request_info(self):
        body = request.get_json()
        self.keyword = body['keyword']
        self.mall_name = body['mall_name']
        self.nrank_record_id = body['nrank_record_id']

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

    async def search_page_and_create_rank_models(self, page_index):
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
                    model.nrank_record_id = self.nrank_record_id

                    if('adId' in item):
                        model.thumbnail_url = item.get('adImageUrl', model.thumbnail_url)
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
                            model.nrank_record_id = self.nrank_record_id
                            models.append(model)

                result.extend(models)
            return result
        except KeyError as e:
            pass
            # raise CustomException(f"not found value for {e}")
        except AttributeError as e:
            pass
            # raise CustomException(e)

    async def create_list(self):
        nRankRecordDetailRepository = NRankRecordDetailRepository()
        results = []

        self.set_request_info()

        # pageSize 만큼 비동기 요청
        rank_entities = [self.search_page_and_create_rank_models(i+1) for i in range(self.page_size)]
        tasks = asyncio.gather(*rank_entities)

        # 전체 요청시간이 TOTAL_REQUEST_TIMEOUT_SIZE를 초과한다면 기다리지 않고 예외처리
        try:
            await asyncio.wait_for(tasks, timeout=TOTAL_REQUEST_TIMEOUT_SIZE)
        except asyncio.TimeoutError:
            tasks.cancel()
            raise TimeoutError("request time out")
        
        for result in tasks.result():
            results.extend(result)
        
        # TODO :: bulk_save 성공한다면 bulk_delete 실행. bulk_delete 성공한다면 nrank_record update 실행
        nRankRecordDetailRepository.bulk_delete(self.nrank_record_id)
        nRankRecordDetailRepository.bulk_save(results)
        self.update_nrank_record_last_searched_at()

    def update_nrank_record_last_searched_at(self):
        nRankRecordRepository = NRankRecordRepository()

        entity = nRankRecordRepository.search_one(self.nrank_record_id)
        nRankRecordRepository.change_last_searched_at(entity)
        

    def search_list_by_record_id(self, record_id):
        nRankRecordDetailRepository = NRankRecordDetailRepository()
        
        detail_entities = nRankRecordDetailRepository.search_list_by_record_id(record_id)
        detail_dtos = list(map(lambda entity: NRankRecordDetailDto.to_dto(entity), detail_entities))
        return detail_dtos