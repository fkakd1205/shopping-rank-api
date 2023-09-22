from dataclasses import dataclass

@dataclass
class NRankRecordDetailCreateReqDto():
    keyword = None
    mall_name = None
    page_size = None
    record_id = None
    record_info_id = None
    ad_product_unit = 0
    total_ad_products = {}
    workspace_id = None