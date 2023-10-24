class NRankRecordCategoryCreateReqDto():

    class IncludedName():
        name = None
    
        def __init__(self, req):
            self.name = req.get('name', None)