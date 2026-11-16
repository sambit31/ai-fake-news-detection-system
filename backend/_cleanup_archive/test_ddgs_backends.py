
from ddgs import DDGS

query = "India government education scheme"

backends = ["duckduckgo", "brave", "google", "bing"]

for backend in backends:
    print(f"\n========== TESTING {backend.upper()} ==========")

    try:
        with DDGS(timeout=15) as client:
            results = client.text(
                query,
                backend=backend,
                max_results=3
            )

        print("Results:", len(results))

        for result in results:
            print("Title:", result.get("title"))
            print("URL:", result.get("href"))

    except Exception as error:
        print("Error:", type(error).__name__, repr(error))
