from dataclasses import dataclass

@dataclass
class PageableResDto():
    """pagenation response dto
    
    number, size, content
    """
    number = 0
    size = 0
    content = None

    class TotalSize():
        def __init__(self, total_size):
            self.total_size = total_size
