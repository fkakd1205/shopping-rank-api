class NRankRecordDetailSearchReqDto:

    class IncludedRecordInfoIds():
        def __init__(self, req):
            self.record_info_ids = req.get('record_info_ids', [])
            
