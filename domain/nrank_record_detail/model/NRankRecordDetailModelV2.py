from utils.db.v2.DBUtils import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime

class NRankRecordDetailModel(Base):
    __tablename__ = 'nrank_record_detail'

    cid = Column("cid", BigInteger, primary_key=True, autoincrement=True)
    id = Column("id", String(36), unique=True, nullable=False)
    mall_name = Column("mall_name", String(50), nullable=False)
    rank = Column("rank", Integer, nullable=False)
    product_title = Column("product_title", String(200), nullable=False)
    price = Column("price", Integer, nullable=True)
    page = Column("page", Integer, nullable=False)
    mall_product_id = Column("mall_product_id", String(15), nullable=True)

    advertising_yn = Column("advertising_yn", String(1), nullable=False)
    included_ad_rank = Column("included_ad_rank", Integer, nullable=True)
    price_comparision_yn = Column("price_comparision_yn", String(1), nullable=False)
    comparision_rank = Column("comparision_rank", Integer, nullable=True)
    low_mall_count = Column("low_mall_count", Integer, nullable=True)

    review_count = Column("review_count", Integer, nullable=True)
    score_info = Column("score_info", String(5), nullable=True)
    registration_date = Column("registration_date", DateTime(timezone=True), nullable=True)
    thumbnail_url = Column("thumbnail_url", String(600), nullable=True)
    purchase_count = Column("purchase_count", Integer, nullable=True)
    keep_count = Column("keep_count", Integer, nullable=True)
    delivery_fee = Column("delivery_fee", Integer, nullable=True)

    category1_name = Column("category1_name", String(30), nullable=True)
    category2_name = Column("category2_name", String(30), nullable=True)
    category3_name = Column("category3_name", String(30), nullable=True)
    category4_name = Column("category4_name", String(30), nullable=True)

    nrank_record_info_id = Column("nrank_record_info_id", String(36), nullable=False)

    def __init__(self):
        self.id = None
        self.mall_name = None
        self.rank = 0               # 노출 순위
        self.product_title = None      # 상품명
        self.price = 0      # 가격
        self.page = 0       # 노출 페이지
        self.mall_product_id = None     # 상품 id
        
        self.advertising_yn = 'n'      # 광고 여부
        self.included_ad_rank = 0     # 실제 순위
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
        
        self.nrank_record_info_id = None
