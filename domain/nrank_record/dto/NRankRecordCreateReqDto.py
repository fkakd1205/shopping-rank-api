class NRankRecordCreateReqDto():
    class IncludedIds():
        ids = None
        
        def __init__(self, req):
            self.ids = req.get('ids', None)

    class IncludedCategoryId():
        nrank_record_category_id = None

        def __init__(self, req):
            self.nrank_record_category_id = req.get('nrank_record_category_id', None)
