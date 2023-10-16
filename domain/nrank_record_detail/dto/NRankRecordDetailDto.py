from dataclasses import dataclass

from enums.YnEnum import YnEnum

@dataclass
class NRankRecordDetailDto():
    id = None
    mall_name = None      # 스토어명
    rank = 0               # 노출 순위
    product_title = None      # 상품명
    price = 0      # 가격
    page = 0       # 노출 페이지
    item_id = None     # item id
    mall_product_id = None     # 상품 id
        
    advertising_yn = YnEnum.N.value      # 광고 여부
    included_ad_rank = 0     # 광고 포함 노출 순위
    price_comparision_yn = YnEnum.N.value     # 가격 비교 여부
    comparision_rank = 0        # 가격 비교 순위
    low_mall_count = 0       # 가격비교 쇼핑몰 개수
        
    review_count = 0    # 리뷰 개수
    score_info = 0      # 리뷰 평점
    registration_date = None        # 등록일
    thumbnail_url = None      # 썸네일 이미지
    purchase_count = 0      # 구매 건수
    keep_count = 0      # 찜 개수
    delivery_fee = 0        # 배송비

    category1_name = None       # 카테고리1
    category2_name = None       # 카테고리2
    category3_name = None       # 카테고리3
    category4_name = None       # 카테고리4
        
    nrank_record_info_id = None
    deleted_flag = False

    @staticmethod
    def to_dto(model):
        dto = NRankRecordDetailDto()
        dto.id = model.id
        dto.mall_name = model.mall_name
        dto.rank = model.rank
        dto.product_title = model.product_title
        dto.price = model.price
        dto.page = model.page
        dto.item_id = model.item_id
        dto.mall_product_id = model.mall_product_id
        dto.advertising_yn = model.advertising_yn
        dto.included_ad_rank = model.included_ad_rank
        dto.price_comparision_yn = model.price_comparision_yn
        dto.comparision_rank = model.comparision_rank
        dto.low_mall_count = model.low_mall_count
        dto.review_count = model.review_count
        dto.score_info = model.score_info
        dto.registration_date = model.registration_date
        dto.thumbnail_url = model.thumbnail_url
        dto.purchase_count = model.purchase_count
        dto.keep_count = model.keep_count
        dto.delivery_fee = model.delivery_fee
        dto.category1_name = model.category1_name
        dto.category2_name = model.category2_name
        dto.category3_name = model.category3_name
        dto.category4_name = model.category4_name
        dto.nrank_record_info_id = model.nrank_record_info_id
        dto.deleted_flag = model.deleted_flag
        return dto.__dict__
    
    # TODO :: dataclass 사용 시 default값 안채워짐. 확인해보기
    class AnalysisByDatetime():
        def __init__(self):
            self.datetime = None
            self.advertising_yn = 'n'
            self.price_comparision_yn = 'n'
            self.rank = None
            self.comparision_rank = None