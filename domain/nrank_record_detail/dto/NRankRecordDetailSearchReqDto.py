class NRankRecordDetailSearchReqDto:
    
    class IncludedRecordIdAndRecordInfoId():
        record_id = None
        record_info_id = None

        def __init__(self, req):
            self.record_id = req.get('record_id', None)
            self.record_info_id = req.get('record_info_id', None)

    class IncludedRecordInfoIds():
        record_info_ids = []

        def __init__(self, req):
            self.record_info_ids = req.get('record_info_ids', [])
            
