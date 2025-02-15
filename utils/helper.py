import httpx
from concurrent.futures import ThreadPoolExecutor, as_completed

def filter_urls_by_status(urls, limit=100, expected_status=200, timeout=5, max_workers=10):
    """
    Lọc các URL mà trả về status code bằng expected_status (mặc định 200).
    Chỉ trả về tối đa limit URL.
    """
    filtered = []

    def check_url(url):
        try:
            response = httpx.get(url, timeout=timeout)
            if response.status_code == expected_status:
                return url
        except Exception:
            return None
        return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            result = future.result()
            if result:
                filtered.append(result)
                if len(filtered) >= limit:
                    break
    return filtered
