import json
import os
import re

import requests

SCHOLAR_ID = "36WXELIAAAAJ"
API_KEY = os.environ["SERPAPI_API_KEY"]

URL = "https://serpapi.com/search.json"

print("Fetching Google Scholar metrics...")

response = requests.get(
    URL,
    params={
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "api_key": API_KEY,
    },
    timeout=30,
)

response.raise_for_status()

data = response.json()

if "error" in data:
    raise RuntimeError(data["error"])

try:
    stats = data["cited_by"]["table"]

    citations = stats[0]["citations"]["all"]
    h_index = stats[1]["h_index"]["all"]
    i10_index = stats[2]["i10_index"]["all"]

except Exception as e:
    print(json.dumps(data, indent=2))
    raise RuntimeError("Unexpected SerpAPI response format.") from e

print(f"Citations : {citations}")
print(f"h-index   : {h_index}")
print(f"i10-index : {i10_index}")

# --------------------------------------------------------
# Save metrics.json
# --------------------------------------------------------

metrics = {
    "citations": citations,
    "h_index": h_index,
    "i10_index": i10_index,
}

with open("metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print("metrics.json updated.")

# --------------------------------------------------------
# Update README
# --------------------------------------------------------

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

replacement = f"""
<!-- SCHOLAR_STATS_START -->

📚 **Citations:** **{citations}**

📈 **h-index:** **{h_index}**

⭐ **i10-index:** **{i10_index}**

🌍 **Google Scholar**  
https://scholar.google.com/citations?user={SCHOLAR_ID}

<!-- SCHOLAR_STATS_END -->
"""

pattern = (
    r"<!-- SCHOLAR_STATS_START -->.*?<!-- SCHOLAR_STATS_END -->"
)

new_readme = re.sub(
    pattern,
    replacement.strip(),
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated successfully.")
