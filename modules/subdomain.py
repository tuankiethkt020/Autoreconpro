import subprocess
import tempfile
import os
from utils import logger
from urllib.parse import urlparse

def run_command(cmd):
    try:
        logger.log(f"Running command: {cmd}")
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True, errors="replace")
        return output.strip().splitlines()
    except subprocess.CalledProcessError as e:
        logger.log(f"Error running command '{cmd}': {e}")
        return []

def enumerate_subdomains(domain):
    # Bước 1: Chạy subfinder để thu thập subdomain
    subfinder_cmd = f"subfinder -d {domain} -silent"
    subfinder_results = run_command(subfinder_cmd)
    subdomains = set(subfinder_results)
    logger.log(f"Subfinder tìm được {len(subdomains)} subdomain.")

    # Nếu không có subdomain nào thu được, trả về danh sách rỗng
    if not subdomains:
        return []

    # Bước 2: Kiểm tra tính sống của các subdomain bằng httpx
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp:
        for sub in subdomains:
            tmp.write(sub + "\n")
        tmp_filename = tmp.name

    # Lệnh httpx sử dụng file danh sách subdomain
    httpx_cmd = f"/usr/local/bin/httpx -silent -mc 200 -title -tech-detect -status-code -location -retries 5 -l {tmp_filename}"
    httpx_results = run_command(httpx_cmd)
    os.unlink(tmp_filename)

    alive_subdomains = set()
    for line in httpx_results:
        # Giả sử mỗi dòng có định dạng:
        # https://subdomain.example.com [200] [...] [...]
        tokens = line.split()
        if tokens:
            url = tokens[0]
            parsed = urlparse(url)
            if parsed.netloc:
                alive_subdomains.add(parsed.netloc)
    logger.log(f"httpx xác nhận {len(alive_subdomains)} subdomain sống.")
    return list(alive_subdomains)
