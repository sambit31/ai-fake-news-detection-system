
from api.evidence_search import search_evidence

claim = "The Indian government announced a new education scheme on Monday."

print("Testing application evidence search...")
results = search_evidence(claim, max_results=5)

print("\nResults found:", len(results))

for index, item in enumerate(results, start=1):
    print(f"\nSource {index}")
    print("Title:", item["title"])
    print("URL:", item["url"])
    print("Snippet:", item["snippet"][:200])
