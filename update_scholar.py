import requests
import re

# Your Google Scholar User ID
GSCHOLAR_ID = "tuwg40gAAAAJ"

# SerpAPI endpoint
API_URL = "https://serpapi.com/search"

def get_metrics():
    params = {
        "engine": "google_scholar_author",
        "author_id": GSCHOLAR_ID,
        "api_key": os.environ["SERPAPI_KEY"]
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    # Extract metrics
    citations = data.get("cited_by", {}).get("table", [{}])[0].get("citations", "N/A")
    h_index = data.get("cited_by", {}).get("table", [{}])[1].get("h_index", "N/A")
    i10_index = data.get("cited_by", {}).get("table", [{}])[2].get("i10_index", "N/A")

    return citations, h_index, i10_index


def update_html(citations, h_index, i10_index):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = re.sub(r"\{\{CITATIONS\}\}", str(citations), html)
    html = re.sub(r"\{\{HINDEX\}\}", str(h_index), html)
    html = re.sub(r"\{\{I10INDEX\}\}", str(i10_index), html)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    try:
        citations, hindex, i10 = get_metrics()
        print("Fetched:", citations, hindex, i10)
        update_html(citations, hindex, i10)
        print("index.html updated successfully.")
    except Exception as e:
        print("Error:", e)
