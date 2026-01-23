import requests
import os
import re
import sys

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
SCHOLAR_ID = os.environ.get("SCHOLAR_ID")

if not SERPAPI_KEY or not SCHOLAR_ID:
    print("❌ Missing environment variables.")
    sys.exit(1)


def get_scholar_metrics():
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        cites = data["cited_by"]["table"][0]["citations"]["all"]
        h_index = data["cited_by"]["table"][1]["h_index"]["all"]
        i10_index = data["cited_by"]["table"][2]["i10_index"]["all"]
        return cites, h_index, i10_index
    except Exception as e:
        print("❌ Failed to parse Scholar data")
        print(data)
        sys.exit(1)


def update_index(citations, hindex, i10index):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r"\{\{CITATIONS\}\}", str(citations), content)
    content = re.sub(r"\{\{HINDEX\}\}", str(hindex), content)
    content = re.sub(r"\{\{I10INDEX\}\}", str(i10index), content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    cites, h, i10 = get_scholar_metrics()
    print("✔ Citations:", cites)
    print("✔ H-index:", h)
    print("✔ i10-index:", i10)
    update_index(cites, h, i10)
    print("✅ index.html updated successfully")


if __name__ == "__main__":
    main()
