class NRankRecordInfoCreateReqDto():

    class IncludedRecordIds():
        record_ids = []

        def __init__(self, req):
            self.record_ids = req.get('record_ids', [])
