from dataclasses import dataclass

@dataclass
class PageableResDto():
    number = 0
    size = 0
    content = None
    number_of_elements = 0

    # client에서 처리
    # first = False
    # last = False

    @dataclass
    class TotalSize():
        total_size = 0
