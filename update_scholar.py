
import os
import re
import requests

SCHOLAR_ID = "36WXELIAAAAJ"
API_KEY = os.environ["SERPAPI_API_KEY"]

url = "https://serpapi.com/search.json"

params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

print("Fetching Google Scholar metrics...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

stats = data.get("cited_by", {}).get("table", [])

citations = stats[0]["citations"]["all"]
hindex = stats[1]["h_index"]["all"]
i10index = stats[2]["i10_index"]["all"]

print(f"Citations: {citations}")
print(f"h-index: {hindex}")
print(f"i10-index: {i10index}")

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

replacement = f"""## 📊 Research Highlights

📚 **Citations:** {citations}

📈 **h-index:** {hindex}

⭐ **i10-index:** {i10index}

🌍 **Google Scholar**  
https://scholar.google.com/citations?user={SCHOLAR_ID}
"""

pattern = r"## 📊 Research Highlights.*?(?=\n---)"

new_readme = re.sub(
    pattern,
    replacement,
    readme,
    flags=re.S
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated successfully.")
