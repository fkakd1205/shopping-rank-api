class NRankRecordDetailCreateReqDto():

    class RequestNRank():
        def __init__(self, req):
            self.keyword = req.get('keyword', None)
            self.mall_name = req.get('mall_name', None)
            self.page_size = req.get('page_size', None)
            self.record_id = req.get('record_id', None)
            self.record_info_id = req.get('record_info_id', None)
            self.ad_product_unit = req.get('ad_product_unit', 0)
            self.total_ad_products = req.get('total_ad_products', {})
            self.workspace_id = req.get('workspace_id', None)
    
    class RankResult():
        def __init__(self, req):
            self.create_req_dto = req.get('create_req_dto', None)
            self.nrank_record_details = req.get('nrank_record_details', [])