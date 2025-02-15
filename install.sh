#!/bin/bash
set -e

# Kiểm tra và tạo virtual environment nếu chưa có
if [ ! -d "venv" ]; then
    echo "[*] Tạo virtual environment..."
    python3 -m venv venv
fi

# Kích hoạt virtual environment
echo "[*] Kích hoạt virtual environment..."
source venv/bin/activate

# Cài đặt các gói Python từ requirements.txt
echo "[*] Cài đặt các gói Python từ requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Hàm kiểm tra lệnh có tồn tại không
command_exists () {
    command -v "$1" >/dev/null 2>&1
}

# Cài đặt subfinder nếu chưa có (sử dụng Go)
if ! command_exists subfinder; then
    echo "[*] subfinder không tồn tại, cài đặt subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
fi

# Cài đặt httpx CLI nếu chưa có (sử dụng Go)
if ! command_exists httpx; then
    echo "[*] httpx không tồn tại, cài đặt httpx CLI..."
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
fi

# Cài đặt waybackurls nếu chưa có (sử dụng Go)
if ! command_exists waybackurls; then
    echo "[*] waybackurls không tồn tại, cài đặt waybackurls..."
    go install -v github.com/tomnomnom/waybackurls@latest
fi

# Cài đặt urlfinder nếu chưa có (sử dụng Go)
if ! command_exists urlfinder; then
    echo "[*] urlfinder không tồn tại, cài đặt urlfinder..."
    go install -v github.com/projectdiscovery/urlfinder/cmd/urlfinder@latest
fi

echo "[*] Cài đặt hoàn tất!"
