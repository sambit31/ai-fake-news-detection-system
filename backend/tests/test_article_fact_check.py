
from api.article_fact_check import fact_check_article


article = """
The Indian government announced a new education scheme
on Monday. Under this scheme, students from eligible
families will receive financial assistance.

The government stated that the programme will begin
in January 2027. The initiative aims to improve access
to higher education and support students from
economically weaker backgrounds.
"""


print("\n========== ARTICLE FACT CHECK ==========")

report = fact_check_article(article)

print("\n========== SUMMARY ==========")
print("Total claims:", report["summary"]["total_claims"])
print("Supported:", report["summary"]["supported"])
print("Contradicted:", report["summary"]["contradicted"])
print(
    "Insufficient evidence:",
    report["summary"]["insufficient_evidence"]
)

print("\n========== CLAIM RESULTS ==========")

for item in report["claims"]:

    print("\nClaim:", item["claim"])
    print("Importance:", item["importance"])
    print("Verdict:", item["verdict"])
    print("Explanation:", item["explanation"])

    print("\nSources reviewed:")

    if not item["sources_reviewed"]:
        print("No sources found.")

    for source in item["sources_reviewed"]:
        print("Title:", source["title"])
        print("URL:", source["url"])
        print("Status:", source["status"])

    print("\nSources used for verification:")

    if not item["sources_used"]:
        print("No directly used sources.")

    for source in item["sources_used"]:
        print("Title:", source["title"])
        print("URL:", source["url"])
