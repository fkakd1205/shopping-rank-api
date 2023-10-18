class NRankRecordDetailSearchReqDto:
    
    class IncludedRecordInfoIdsAndMallProductIdAndItemId():
        info_ids = []
        detail_mall_product_id = None
        detail_item_id = None

        def __init__(self, req):
            self.info_ids = req.get('info_ids', [])
            self.detail_mall_product_id = req.get('detail_mall_product_id', None)
            self.detail_item_id = req.get('detail_item_id', None)

    class IncludedRecordIdAndRecordInfoId():
        record_id = None
        record_info_id = None

        def __init__(self, req):
            self.record_id = req.get('record_id', None)
            self.record_info_id = req.get('record_info_id', None)
