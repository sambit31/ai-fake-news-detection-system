
from ddgs import DDGS

claims = [
    "The Indian government announced a new education scheme on Monday.",
    "Students from eligible families will receive financial assistance under the scheme.",
    "The programme will begin in January 2027.",
    "The initiative aims to improve access to higher education and support students from economically weaker backgrounds."
]

with DDGS() as client:
    for index, claim in enumerate(claims, start=1):
        print(f"\n========== CLAIM {index} ==========")
        print(claim)

        try:
            results = list(
                client.text(
                    claim,
                    region="in-en",
                    safesearch="moderate",
                    max_results=5,
                    backend="bing"
                )
            )

            print("Results:", len(results))

            for result in results:
                print("Title:", result.get("title"))
                print("URL:", result.get("href"))

        except Exception as error:
            print("Search error:", repr(error))
