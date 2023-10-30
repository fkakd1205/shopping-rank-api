from enums.PageSortDirectionEnum import PageSortDirectionEnum

DEFAULT_SIZE_20 = 20
MAX_SIZE_100 = 100

class PageableReqDto():
    """pagenation request dto
    
    sort_column, sort_direction, page, size
    """
    def __init__(self, pageable):
        self.sort_column = pageable.get('sort_column')
        self.sort_direction = PageSortDirectionEnum(pageable.get('sort_direction') or 'desc')
        self.page = int(pageable.get('page')) or 1
        self.size = int(pageable.get('size')) or 0

    class Size20To100():
        DEFAULT_SIZE = 20
        MAX_SIZE = 100

        def __init__(self, pageable):
            self.sort_column = pageable.get('sort_column')
            self.sort_direction = PageSortDirectionEnum(pageable.get('sort_direction') or 'desc')
            self.page = int(pageable.get('page')) or 1
            self.size = int(pageable.get('size')) or self.DEFAULT_SIZE

            if(self.size > self.MAX_SIZE):
                self.size = self.MAX_SIZE
            elif(self.size < self.DEFAULT_SIZE):
                self.size = self.DEFAULT_SIZE
