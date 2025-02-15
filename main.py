#!/usr/bin/env python3
import argparse
import json
from modules import subdomain, urlcollector, regexfilter
from utils import logger
from utils.helper import filter_urls_by_status  # Hàm lọc URL theo status

def main():
    parser = argparse.ArgumentParser(
    description="AutoRecon Pro - Tool thu thập thông tin và kiểm thử bảo mật\n"
                "Flow: (1) Subdomain Enumeration (subfinder + HTTPX) ->\n"
                "      (2) Endpoint Collection (Waybackurls & Urlfinder) ->\n"
                "      (3) Regex Filtering & Categorization ->\n"
                "      (4) Lưu kết quả theo category trong 1 file JSON\n"
                "      (5) (Tùy chọn) Lọc từng category (status 200, giới hạn số lượng) và lưu vào JSON.",
    formatter_class=argparse.RawDescriptionHelpFormatter
)
    parser.add_argument("--domain", required=True, help="Domain mục tiêu (ví dụ: example.com)")
    parser.add_argument("--subenum", action="store_true", help="Kích hoạt liệt kê subdomain (Subfinder + HTTPX)")
    parser.add_argument("--collect", action="store_true", help="Kích hoạt thu thập URL endpoint từ các subdomain sống")
    parser.add_argument("--limit", type=int, default=100, help="Giới hạn số URL cho mỗi category (mặc định: 100)")
    parser.add_argument("--filter-status", action="store_true", help="Chỉ giữ các URL có status 200 (áp dụng cho endpoint)")
    parser.add_argument("--verbose", action="store_true", help="Kích hoạt chế độ log chi tiết")
    parser.add_argument("--output", help="Đường dẫn file lưu kết quả JSON")
    parser.add_argument("--threads", type=int, default=10, help="Số luồng xử lý song song cho urlfinder")
    args = parser.parse_args()

    if args.verbose:
        logger.enable_verbose()

    result = {}
    domain = args.domain

    # Bước 1: Subdomain Enumeration
    alive_subdomains = []
    if args.subenum:
        logger.log("Bắt đầu liệt kê subdomain (subfinder + HTTPX)...")
        alive_subdomains = subdomain.enumerate_subdomains(domain)
        result['subdomains'] = alive_subdomains
        logger.log(f"Đã tìm được {len(alive_subdomains)} subdomain sống.")
    else:
        logger.log("Không kích hoạt subenum. Sử dụng domain gốc để thu thập endpoint.")
        alive_subdomains = [domain]
        result['subdomains'] = alive_subdomains

    # Bước 2: Endpoint Collection
    urls = []
    if args.collect and alive_subdomains:
        logger.log("Bắt đầu thu thập URL từ các subdomain sống...")
        urls = urlcollector.collect_urls(alive_subdomains, threads=args.threads)
        result['urls'] = urls
        logger.log(f"Thu thập được tổng cộng {len(urls)} URL từ các subdomain.")
    else:
        logger.log("Không thu thập URL vì không có subdomain sống hoặc tùy chọn --collect không được bật.")

    # Bước 3: Regex Filtering & Categorization
    logger.log("Phân loại URL theo regex...")
    categorized = regexfilter.filter_urls(urls)
    result['categorized'] = categorized
    for category, url_list in categorized.items():
        logger.log(f"Category '{category}': {len(url_list)} URL.")

    # Bước 4: Lưu kết quả phân loại theo category vào 1 file JSON (chứa toàn bộ dữ liệu)
    # Nếu bật tùy chọn filter-status, thực hiện lọc từng category và lưu kết quả vào key riêng
    if args.filter_status:
        logger.log("Lọc từng category để chỉ giữ các URL có status 200 và giới hạn số lượng...")
        filtered_categorized = {}
        for category, url_list in categorized.items():
            filtered_urls = filter_urls_by_status(url_list, limit=args.limit, expected_status=200)
            filtered_categorized[category] = filtered_urls
            logger.log(f"Category '{category}' sau lọc: {len(filtered_urls)} URL.")
        result['categorized_filtered'] = filtered_categorized

    # Lưu kết quả tổng hợp ra file JSON nếu tham số --output được chỉ định
    if args.output:
        logger.log(f"Lưu kết quả vào file {args.output} ...")
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            logger.log("Lưu kết quả JSON thành công.")
        except Exception as e:
            logger.log(f"Lỗi khi lưu kết quả JSON: {e}")

if __name__ == "__main__":
    main()
