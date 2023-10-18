class NRankRecordInfoCreateReqDto():

    class IncludedRecordInfoId():
        record_info_id = None

        def __init__(self, req):
            self.record_info_id = req.get('record_info_id', None)

    class IncludedRecordIds():
        record_ids = []

        def __init__(self, req):
            self.record_ids = req.get('record_ids', [])
