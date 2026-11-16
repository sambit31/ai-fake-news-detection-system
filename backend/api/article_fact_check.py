
from api.ai_fact_checker import extract_claims
from api.evidence_search import (
    create_search_client,
    search_evidence
)
from api.evidence_fetch import fetch_page
from api.evidence_verifier import verify_claim


def fact_check_article(
    article_text: str,
    max_claims: int = 5,
    max_search_results: int = 5,
    max_pages_per_claim: int = 3
) -> dict:

    if not article_text or len(article_text.strip()) < 50:
        raise ValueError("Article text is too short.")

    # STEP 1: Extract factual claims
    extracted_claims = extract_claims(article_text)
    extracted_claims = extracted_claims[:max_claims]

    claim_results = []

    # STEP 2: Create one shared Tavily client
    search_client = create_search_client()

    # STEP 3: Process each extracted claim
    for index, item in enumerate(extracted_claims, start=1):

        claim_text = item.get("claim", "").strip()
        importance = item.get("importance", "medium")

        if not claim_text:
            continue

        print(
            f"\nFact-checking claim {index}/{len(extracted_claims)}"
        )
        print("Claim:", claim_text)

        # STEP 4: Search for candidate sources
        try:
            search_results = search_evidence(
                claim_text,
                max_results=max_search_results,
                client=search_client
            )

        except Exception as error:
            print("Search error:", error)

            search_results = []

        print("Search results:", len(search_results))

        # STEP 5: Fetch actual webpage content
        fetched_sources = []
        sources_reviewed = []

        for search_item in search_results[:max_pages_per_claim]:

            url = search_item.get("url", "").strip()

            if not url:
                continue

            try:
                fetched = fetch_page(url)

                if fetched.get("success"):

                    fetched_sources.append(fetched)

                    sources_reviewed.append({
                        "title": fetched.get("title", ""),
                        "url": fetched.get("url", url),
                        "status": "FETCHED"
                    })

                else:
                    sources_reviewed.append({
                        "title": search_item.get("title", ""),
                        "url": url,
                        "status": "FETCH_FAILED",
                        "error": fetched.get(
                            "error",
                            "Unknown error"
                        )
                    })

            except Exception as error:

                sources_reviewed.append({
                    "title": search_item.get("title", ""),
                    "url": url,
                    "status": "FETCH_FAILED",
                    "error": str(error)
                })

        print("Fetched sources:", len(fetched_sources))

        # STEP 6: Verify claims using actual webpage content
        try:
            verification = verify_claim(
                claim=claim_text,
                sources=fetched_sources,
                article_context=article_text
            )

        except Exception as error:

            print("Verification error:", error)

            verification = {
                "verdict": "INSUFFICIENT_EVIDENCE",
                "explanation": (
                    "The claim could not be verified because "
                    "the verification process encountered an error."
                ),
                "sources_used": []
            }

        claim_results.append({
            "claim_number": index,
            "claim": claim_text,
            "importance": importance,
            "verdict": verification.get(
                "verdict",
                "INSUFFICIENT_EVIDENCE"
            ),
            "explanation": verification.get(
                "explanation",
                "No verification explanation was returned."
            ),
            "sources_used": verification.get("sources_used", []),
            "sources_reviewed": sources_reviewed
        })

    # STEP 7: Calculate verdict counts
    summary = {
        "total_claims": len(claim_results),
        "supported": 0,
        "contradicted": 0,
        "insufficient_evidence": 0
    }

    for result in claim_results:

        verdict = result["verdict"]

        if verdict == "SUPPORTED":
            summary["supported"] += 1

        elif verdict == "CONTRADICTED":
            summary["contradicted"] += 1

        else:
            summary["insufficient_evidence"] += 1

    return {
        "summary": summary,
        "claims": claim_results
    }
