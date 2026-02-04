import math

def paginate(items, page: int, page_size: int):
    page = max(1, int(page))
    page_size = min(100, max(1, int(page_size)))
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items[start:end],
        "pages": math.ceil(total / page_size) if page_size else 1
    }
