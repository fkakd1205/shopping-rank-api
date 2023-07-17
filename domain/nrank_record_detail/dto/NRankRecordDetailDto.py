class NRankRecordDetailDto():
    def __init__(self):
        self.id = None
        self.mall_name = None      # 스토어명
        self.rank = 0               # 노출 순위
        self.product_title = None      # 상품명
        self.price = 0      # 가격
        self.page = 0       # 노출 페이지
        self.mall_product_id = None     # 상품 id
        
        self.advertising_yn = 'n'      # 광고 여부
        self.included_ad_rank = 0     # 광고 포함 노출 순위
        self.price_comparision_yn = 'n'     # 가격 비교 여부
        self.comparision_rank = 0        # 가격 비교 순위
        self.low_mall_count = 0       # 가격비교 쇼핑몰 개수
        
        self.review_count = 0    # 리뷰 개수
        self.score_info = 0      # 리뷰 평점
        self.registration_date = None        # 등록일
        self.thumbnail_url = None      # 썸네일 이미지
        self.purchase_count = 0      # 구매 건수
        self.keep_count = 0      # 찜 개수
        self.delivery_fee = 0        # 배송비

        self.category1_name = None       # 카테고리1
        self.category2_name = None       # 카테고리2
        self.category3_name = None       # 카테고리3
        self.category4_name = None       # 카테고리4
        
        self.nrank_record_id = None

    @staticmethod
    def to_dto(entity):
        dto = NRankRecordDetailDto()
        dto.id = entity.id
        dto.mall_name = entity.mall_name
        dto.rank = entity.rank
        dto.product_title = entity.product_title
        dto.price = entity.price
        dto.page = entity.page
        dto.mall_product_id = entity.mall_product_id
        dto.advertising_yn = entity.advertising_yn
        dto.included_ad_rank = entity.included_ad_rank
        dto.price_comparision_yn = entity.price_comparision_yn
        dto.comparision_rank = entity.comparision_rank
        dto.low_mall_count = entity.low_mall_count
        dto.review_count = entity.review_count
        dto.score_info = entity.score_info
        dto.registration_date = str(entity.registration_date)
        dto.thumbnail_url = entity.thumbnail_url
        dto.purchase_count = entity.purchase_count
        dto.keep_count = entity.keep_count
        dto.delivery_fee = entity.delivery_fee
        dto.category1_name = entity.category1_name
        dto.category2_name = entity.category2_name
        dto.category3_name = entity.category3_name
        dto.category4_name = entity.category4_name
        dto.nrank_record_id = entity.nrank_record_id
        return dto.__dict__