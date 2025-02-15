# AutoRecon Pro

AutoRecon Pro là tool tự động thu thập thông tin phục vụ kiểm thử bảo mật với các tính năng:

- **Subdomain Enumeration:**  
  - Kết hợp **Subfinder** và **HTTPX** để liệt kê và kiểm tra tính khả dụng của subdomain.

- **URL Collection:**  
  - Thu thập URL endpoint từ **WaybackURLs** và **URLFinder**.
  - **Regex Filtering & Categorization:** Phân loại URL thành các nhóm:
    - `/info`: URL chứa file `.js`
    - `/sensitive`: URL chứa file `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`
    - `/backup`: URL chứa file `.bak`, `.bk`
    - `others`: Các URL không khớp

- **JavaScript Analysis:**  
  - Tải file JS từ URL và phân tích bằng **jsleak** và **JSLinkFinder** để tìm các endpoint ẩn và secret (token, API key,...).

## Yêu cầu hệ thống

- **Hệ điều hành:** Linux/macOS/Windows (nên dùng Linux cho CLI tool)
- **Python:** 3.8+
- **Các công cụ CLI cần cài đặt và đảm bảo nằm trong PATH:**
  - [Subfinder](https://github.com/projectdiscovery/subfinder)
  - [HTTPX](https://github.com/projectdiscovery/httpx)
  - [WaybackURLs](https://github.com/tomnomnom/waybackurls)
  - [URLFinder](https://github.com/ProjectScanner/urlfinder)
  - [jsleak](https://github.com/nahamsec/jsleak)
  - [JSLinkFinder](https://github.com/nahamsec/JSLinkFinder)

## Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/YourUsername/AutoReconPro.git
   cd AutoReconPro
