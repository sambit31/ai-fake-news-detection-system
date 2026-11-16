
from api.evidence_search import search_evidence
from api.evidence_fetch import fetch_evidence

claim = (
    "The Indian government announced a new "
    "education scheme on Monday"
)

print("\n========== SEARCHING SOURCES ==========")

search_results = search_evidence(claim, max_results=5)

print("Search results:", len(search_results))

print("\n========== FETCHING ACTUAL WEBPAGES ==========")

sources = fetch_evidence(search_results, max_pages=3)

if not sources:
    print("No webpage content could be retrieved.")

for index, source in enumerate(sources, start=1):
    print(f"\n========== SOURCE {index} ==========")
    print("Title:", source["title"])
    print("URL:", source["url"])
    print("Extracted text:")
    print(source["text"][:1500])
