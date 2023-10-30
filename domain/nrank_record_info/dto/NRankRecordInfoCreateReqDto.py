class NRankRecordInfoCreateReqDto():

    class IncludedRecordIds():
        def __init__(self, req):
            self.record_ids = req.get('record_ids', [])
