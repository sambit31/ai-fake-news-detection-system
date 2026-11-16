
from api.evidence_search import search_evidence
from api.evidence_fetch import fetch_evidence
from api.evidence_verifier import verify_claim

claim = (
    "The Indian government announced a new "
    "education scheme on Monday."
)

print("\n========== STEP 1: SEARCHING ==========")

search_results = search_evidence(claim, max_results=5)
print("Search results:", len(search_results))

print("\n========== STEP 2: FETCHING WEBPAGES ==========")

sources = fetch_evidence(search_results, max_pages=3)
print("Successfully fetched sources:", len(sources))

print("\n========== STEP 3: AI FACT CHECK ==========")

result = verify_claim(claim, sources)

print("\nClaim:", result["claim"])
print("Verdict:", result["verdict"])
print("Explanation:", result["explanation"])

print("\nSources used:")

if not result["sources_used"]:
    print("No sources directly used.")

for source in result["sources_used"]:
    print("\nTitle:", source["title"])
    print("URL:", source["url"])
