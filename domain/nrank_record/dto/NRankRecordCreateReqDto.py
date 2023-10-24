class NRankRecordCreateReqDto():
    
    class IncludedKeywordAndMallName():
        keyword = None
        mall_name = None
        
        def __init__(self, req):
            self.keyword = req.get('keyword', None)
            self.mall_name = req.get('mall_name', None)
    
    class IncludedRecordIdAndRecordInfoId():
        record_id = None
        record_info_id = None

        def __init__(self, req):
            self.record_id = req.get('record_id', None)
            self.record_info_id = req.get('record_info_id', None)

    class IncludedRecordIds():
        record_ids = []
        
        def __init__(self, req):
            self.record_ids = req.get('record_ids', [])

    class IncludedCategoryId():
        nrank_record_category_id = None

        def __init__(self, req):
            self.nrank_record_category_id = req.get('nrank_record_category_id', None)
