class NRankRecordSearchFilter():
    def __init__(self, filter):
        self.search_condition = filter.get('search_condition')
        self.search_query = filter.get('search_query')
        self.search_category_id = filter.get('search_category_id')
        self.search_status = filter.get('search_status')
        