class NRankRecordCreateReqDto():
    
    class IncludedKeywordAndMallName():
        keyword = None
        mall_name = None
        
        def __init__(self, req):
            self.keyword = req.get('keyword', None)
            self.mall_name = req.get('mall_name', None)
        

    class IncludedRecordIds():
        record_ids = None
        
        def __init__(self, req):
            self.record_ids = req.get('record_ids', None)

    class IncludedCategoryId():
        nrank_record_category_id = None

        def __init__(self, req):
            self.nrank_record_category_id = req.get('nrank_record_category_id', None)
