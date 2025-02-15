# modules/urlcollector.py

import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import logger

def run_command(cmd):
    """
    Chạy lệnh shell và trả về danh sách các dòng output.
    Nếu không có output, log thông báo và trả về danh sách rỗng.
    """
    try:
        logger.log(f"Running command: {cmd}")
        process = subprocess.run(
            cmd,
            shell=True,
            universal_newlines=True,
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False
        )
        output = process.stdout
        if output:
            return output.strip().splitlines()
        else:
            logger.log(f"Command '{cmd}' returned exit code {process.returncode} with no output.")
            return []
    except Exception as e:
        logger.log(f"Exception running command '{cmd}': {e}")
        return []

def collect_urls_wayback(alive_subdomains):
    """
    Thu thập URL từ Waybackurls cho tất cả các subdomain.
    Ghi danh sách các subdomain sống vào file tạm và chạy một lần lệnh.
    """
    filename = "subdomains.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for sub in alive_subdomains:
                f.write(sub + "\n")
    except Exception as e:
        logger.log(f"Error writing to file {filename}: {e}")
        return []
    
    # Chạy lệnh để lấy URL từ waybackurls cho tất cả các subdomain
    cmd = f"cat {filename} | /root/go/bin/waybackurls"
    results = run_command(cmd)
    return results

def collect_url_for_subdomain(sub):
    """
    Thu thập URL từ urlfinder cho 1 subdomain.
    """
    urls = set()
    cmd = f"/root/go/bin/urlfinder -d {sub}"
    results = run_command(cmd)
    urls.update(results)
    return urls

def collect_urls_urlfinder(alive_subdomains, threads=10):
    """
    Thu thập URL từ urlfinder cho tất cả các subdomain chạy song song.
    Sử dụng ThreadPoolExecutor để tăng tốc độ thu thập.
    """
    all_urls = set()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(collect_url_for_subdomain, sub): sub for sub in alive_subdomains}
        for future in as_completed(futures):
            all_urls.update(future.result())
    return list(all_urls)

def collect_urls(alive_subdomains, threads=10):
    """
    Hàm tổng hợp thu thập URL từ cả Waybackurls và urlfinder.
    Kết quả trả về là hợp nhất của các URL từ cả hai nguồn.
    """
    logger.log("Thu thập URL từ Waybackurls cho tất cả subdomain...")
    urls_wayback = collect_urls_wayback(alive_subdomains)
    logger.log(f"Waybackurls thu thập được {len(urls_wayback)} URL.")

    logger.log("Thu thập URL từ urlfinder cho tất cả subdomain (song song)...")
    urls_urlfinder = collect_urls_urlfinder(alive_subdomains, threads=threads)
    logger.log(f"Urlfinder thu thập được {len(urls_urlfinder)} URL.")

    all_urls = set(urls_wayback) | set(urls_urlfinder)
    logger.log(f"Tổng cộng thu thập được {len(all_urls)} URL từ cả hai nguồn.")
    return list(all_urls)
