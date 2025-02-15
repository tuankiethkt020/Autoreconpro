import os
import subprocess
from utils import logger
from concurrent.futures import ThreadPoolExecutor
import requests

def download_js(url):
    try:
        logger.log(f"Downloading JS file from: {url}")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Lấy tên file từ URL
            filename = url.split("/")[-1]
            if not filename.endswith(".js"):
                filename = "downloaded.js"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            return filename
        else:
            logger.log(f"Failed to download {url}: HTTP {response.status_code}")
    except Exception as e:
        logger.log(f"Exception downloading {url}: {e}")
    return None

def analyze_js_file(filepath):
    results = {}
    
    # Phân tích với jsleak
    cmd_jsleak = f"jsleak {filepath}"
    try:
        logger.log(f"Analyzing {filepath} with jsleak...")
        jsleak_output = subprocess.check_output(cmd_jsleak, shell=True, universal_newlines=True)
        results['jsleak'] = jsleak_output.strip()
    except Exception as e:
        results['jsleak'] = f"Error: {e}"
    
    # Phân tích với JSLinkFinder (giả sử JSLinkFinder.py có thể chạy được)
    cmd_jslinkfinder = f"python3 JSLinkFinder.py -i {filepath} -o cli"
    try:
        logger.log(f"Analyzing {filepath} with JSLinkFinder...")
        jslink_output = subprocess.check_output(cmd_jslinkfinder, shell=True, universal_newlines=True)
        results['jslinkfinder'] = jslink_output.strip()
    except Exception as e:
        results['jslinkfinder'] = f"Error: {e}"

    return results

def analyze_js_files(urls, threads=5):
    # Lọc các URL chứa file .js
    js_urls = [url for url in urls if ".js" in url.lower()]
    analysis_results = {}
    
    def process_url(url):
        js_file = download_js(url)
        if js_file:
            result = analyze_js_file(js_file)
            try:
                os.remove(js_file)
            except Exception as e:
                logger.log(f"Error removing file {js_file}: {e}")
            return (url, result)
        else:
            return (url, "Download failed")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(process_url, url): url for url in js_urls}
        for future in futures:
            url, result = future.result()
            analysis_results[url] = result
    return analysis_results
