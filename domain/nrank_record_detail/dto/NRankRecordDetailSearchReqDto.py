class NRankRecordDetailSearchReqDto:

    class IncludedRecordInfoIds():
        record_info_ids = []

        def __init__(self, req):
            self.record_info_ids = req.get('record_info_ids', [])
            
