class NRankRecordCategoryCreateReqDto():

    class IncludedName():
        def __init__(self, req):
            self.name = req.get('name', None)