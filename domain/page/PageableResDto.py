from dataclasses import dataclass

@dataclass
class PageableResDto():
    """pagenation response dto
    
    number, size, content
    """
    class TotalSize():
        def __init__(self, total_size):
            self.total_size = total_size
