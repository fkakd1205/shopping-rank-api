from utils.db.DBUtils import db
import uuid

class NRankRecordDetailModel(db.Model):
    __tablename__ = 'nrank_record_detail'

    cid = db.Column("cid", db.BigInteger, primary_key=True, autoincrement=True)
    id = db.Column("id", db.String(36), unique=True, nullable=False)
    mall_name = db.Column("mall_name", db.String(50), nullable=False)
    rank = db.Column("rank", db.Integer, nullable=False)
    product_title = db.Column("product_title", db.String(200), nullable=False)
    price = db.Column("price", db.Integer, nullable=True)
    page = db.Column("page", db.Integer, nullable=False)
    mall_product_id = db.Column("mall_product_id", db.String(15), nullable=True)

    advertising_yn = db.Column("advertising_yn", db.String(1), nullable=False)
    included_ad_rank = db.Column("included_ad_rank", db.Integer, nullable=True)
    price_comparision_yn = db.Column("price_comparision_yn", db.String(1), nullable=False)
    comparision_rank = db.Column("comparision_rank", db.Integer, nullable=True)
    low_mall_count = db.Column("low_mall_count", db.Integer, nullable=True)

    review_count = db.Column("review_count", db.Integer, nullable=True)
    score_info = db.Column("score_info", db.String(5), nullable=True)
    registration_date = db.Column("registration_date", db.DateTime(timezone=True), nullable=True)
    thumbnail_url = db.Column("thumbnail_url", db.String(600), nullable=True)
    purchase_count = db.Column("purchase_count", db.Integer, nullable=True)
    keep_count = db.Column("keep_count", db.Integer, nullable=True)
    delivery_fee = db.Column("delivery_fee", db.Integer, nullable=True)

    category1_name = db.Column("category1_name", db.String(30), nullable=True)
    category2_name = db.Column("category2_name", db.String(30), nullable=True)
    category3_name = db.Column("category3_name", db.String(30), nullable=True)
    category4_name = db.Column("category4_name", db.String(30), nullable=True)

    nrank_record_info_id = db.Column("nrank_record_info_id", db.String(36), nullable=False)

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
