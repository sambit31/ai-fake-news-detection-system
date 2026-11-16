from api.ai_fact_checker import extract_claims

article = """
The Indian government announced a new education scheme
on Monday. Under this scheme, students from eligible
families will receive financial assistance.
The government stated that the programme will begin
in January 2027.
"""

claims = extract_claims(article)

print("\n========== EXTRACTED CLAIMS ==========")

for index, item in enumerate(claims, start=1):
    print(f"\nClaim {index}: {item['claim']}")
    print(f"Importance: {item['importance']}")