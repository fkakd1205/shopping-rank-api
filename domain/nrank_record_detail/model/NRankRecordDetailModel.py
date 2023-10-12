from utils import Base
from sqlalchemy import Column, BigInteger, String, Integer, Boolean

from enums.YnEnum import YnEnum

class NRankRecordDetailModel(Base):
    __tablename__ = 'nrank_record_detail'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    mall_name = Column("mall_name", String(50), nullable=False)
    rank = Column("rank", Integer, nullable=False)
    product_title = Column("product_title", String(200), nullable=False)
    price = Column("price", Integer, nullable=True)
    page = Column("page", Integer, nullable=False)
    item_id = Column("item_id", String(15), nullable=True)
    mall_product_id = Column("mall_product_id", String(15), nullable=True)

    advertising_yn = Column("advertising_yn", String(1), nullable=False)
    included_ad_rank = Column("included_ad_rank", Integer, nullable=True)
    price_comparision_yn = Column("price_comparision_yn", String(1), nullable=False)
    comparision_rank = Column("comparision_rank", Integer, nullable=True)
    low_mall_count = Column("low_mall_count", Integer, nullable=True)

    review_count = Column("review_count", Integer, nullable=True)
    score_info = Column("score_info", String(5), nullable=True)
    registration_date = Column("registration_date", String(14), nullable=True)
    thumbnail_url = Column("thumbnail_url", String(600), nullable=True)
    purchase_count = Column("purchase_count", Integer, nullable=True)
    keep_count = Column("keep_count", Integer, nullable=True)
    delivery_fee = Column("delivery_fee", Integer, nullable=True)

    category1_name = Column("category1_name", String(30), nullable=True)
    category2_name = Column("category2_name", String(30), nullable=True)
    category3_name = Column("category3_name", String(30), nullable=True)
    category4_name = Column("category4_name", String(30), nullable=True)

    nrank_record_info_id = Column("nrank_record_info_id", String(36), nullable=False)
    deleted_flag = Column("deleted_flag", Boolean, nullable=False)

    def __init__(self):
        self.id = None
        self.mall_name = None
        self.rank = 0               # 노출 순위
        self.product_title = None      # 상품명
        self.price = 0      # 가격
        self.page = 0       # 노출 페이지
        self.item_id = None     # item id
        self.mall_product_id = None     # 상품 id
        
        self.advertising_yn = YnEnum.N.value      # 광고 여부
        self.included_ad_rank = 0     # 실제 순위
        self.price_comparision_yn = YnEnum.N.value     # 가격 비교 여부
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
        
        self.nrank_record_info_id = None
        self.deleted_flag = False

    def to_model(self, dto):
        model = NRankRecordDetailModel()
        model.id = dto.get('id')
        model.mall_name = dto.get('mall_name')
        model.rank = dto.get('rank')               # 노출 순위
        model.product_title = dto.get('product_title')      # 상품명
        model.price = dto.get('price')      # 가격
        model.page = dto.get('page')       # 노출 페이지
        model.item_id = dto.get('item_id')      # item id
        model.mall_product_id = dto.get('mall_product_id')     # 상품 id
        
        model.advertising_yn = YnEnum(dto.get('advertising_yn', 'n')).value      # 광고 여부
        model.included_ad_rank = dto.get('included_ad_rank')     # 실제 순위
        model.price_comparision_yn = YnEnum(dto.get('price_comparision_yn', 'n')).value     # 가격 비교 여부
        model.comparision_rank = dto.get('comparision_rank')        # 가격 비교 순위
        model.low_mall_count = dto.get('low_mall_count')       # 가격비교 쇼핑몰 개수
        
        model.review_count = dto.get('review_count')    # 리뷰 개수
        model.score_info = dto.get('score_info')      # 리뷰 평점
        model.registration_date = dto.get('registration_date')        # 등록일
        model.thumbnail_url = dto.get('thumbnail_url')      # 썸네일 이미지
        model.purchase_count = dto.get('purchase_count')      # 구매 건수
        model.keep_count = dto.get('keep_count')      # 찜 개수
        model.delivery_fee = dto.get('delivery_fee')        # 배송비

        model.category1_name = dto.get('category1_name')       # 카테고리1
        model.category2_name = dto.get('category2_name')       # 카테고리2
        model.category3_name = dto.get('category3_name')       # 카테고리3
        model.category4_name = dto.get('category4_name')       # 카테고리4
        
        model.nrank_record_info_id = dto.get('nrank_record_info_id')
        model.deleted_flag = dto.get('deleted_flag')
        return model
