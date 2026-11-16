
import ddgs
from ddgs import DDGS

print("DDGS package version:", getattr(ddgs, "__version__", "Unknown"))
print("Testing direct search...")

try:
    with DDGS() as ddgs_client:
        results = ddgs_client.text(
            "India government education scheme",
            max_results=5
        )

        results = list(results)

        print("Results found:", len(results))

        for index, item in enumerate(results, start=1):
            print(f"\nSource {index}")
            print("Title:", item.get("title"))
            print("URL:", item.get("href"))

except Exception as error:
    print("\nSEARCH ERROR")
    print("Error type:", type(error).__name__)
    print("Error details:", repr(error))
