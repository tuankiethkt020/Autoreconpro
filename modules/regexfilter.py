import re

patterns = {
    "info": re.compile(r".*\.js(\?.*)?$", re.IGNORECASE),
    "sensitive": re.compile(r".*\.(pdf|docx?|xlsx?|xls)(\?.*)?$", re.IGNORECASE),
    "backup": re.compile(r".*\.(bak|bk)(\?.*)?$", re.IGNORECASE),
    "config": re.compile(r".*\.(env|ini|json|yaml|yml|xml)(\?.*)?$", re.IGNORECASE),
    "database": re.compile(r".*\.(sql|db|sqlite)(\?.*)?$", re.IGNORECASE),
    "log": re.compile(r".*\.log(\?.*)?$", re.IGNORECASE),
    "archive": re.compile(r".*\.(zip|tar\.gz|rar|7z)(\?.*)?$", re.IGNORECASE),
    "phpinfo": re.compile(r".*phpinfo\.php(\?.*)?$", re.IGNORECASE),
    "admin": re.compile(r".*/admin(\/|\?|\b).*", re.IGNORECASE),
    "source": re.compile(r".*\.(zip|tar\.gz|rar|7z|git)(\?.*)?$", re.IGNORECASE),
    # Các pattern cho API:
    "api": re.compile(r".*(/api/|api=)(\?.*)?$", re.IGNORECASE),
    "swagger": re.compile(r".*(swagger|openapi)(\?.*)?$", re.IGNORECASE),
    "graphql": re.compile(r".*/graphql(\?.*)?$", re.IGNORECASE),
    "graph": re.compile(r".*/graph(\?.*)?$", re.IGNORECASE)
}

def filter_urls(urls):
    filtered = {
        "info": [],
        "sensitive": [],
        "backup": [],
        "config": [],
        "database": [],
        "log": [],
        "archive": [],
        "phpinfo": [],
        "admin": [],
        "source": [],
        "api": [],
        "swagger": [],
        "graphql": [],
        "graph": [],
        "others": []
    }
    for url in urls:
        matched = False
        for category, pattern in patterns.items():
            if pattern.search(url):
                filtered[category].append(url)
                matched = True
                break
        # if not matched:
        #     filtered["others"].append(url)
    return filtered
