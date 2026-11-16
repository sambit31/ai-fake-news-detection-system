
import os
from pathlib import Path

from dotenv import load_dotenv
from tavily import TavilyClient


# --------------------------------------------------
# ENVIRONMENT CONFIGURATION
# --------------------------------------------------

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"

load_dotenv(dotenv_path=ENV_PATH)


# --------------------------------------------------
# SEARCH CLIENT
# --------------------------------------------------

def create_search_client():

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is missing. "
            "Add it to the backend .env file."
        )

    return TavilyClient(api_key=api_key)


# --------------------------------------------------
# SEARCH QUERY IMPROVEMENT
# --------------------------------------------------

def build_search_query(claim: str) -> str:
    """
    Improve claim searches by encouraging discovery
    of authoritative sources and primary records.

    This does not assume that a particular website
    is authoritative for every subject.
    """

    return (
        f"{claim.strip()} "
        "official records primary sources "
        "authoritative government institutional sources"
    )


# --------------------------------------------------
# SEARCH SINGLE CLAIM
# --------------------------------------------------

def search_evidence(
    claim: str,
    max_results: int = 5,
    client=None
) -> list:
    """
    Search for candidate evidence using Tavily.

    Search results are candidates, NOT verified evidence.
    Actual webpage content must still be fetched
    and evaluated by the evidence verifier.
    """

    if not claim or not claim.strip():
        raise ValueError("Claim cannot be empty.")

    if max_results < 1:
        raise ValueError("max_results must be at least 1.")

    search_client = client or create_search_client()

    improved_query = build_search_query(claim)

    try:

        response = search_client.search(
            query=improved_query,
            max_results=max_results,
            search_depth="advanced"
        )

    except Exception as error:

        raise RuntimeError(
            f"Tavily search failed: "
            f"{type(error).__name__}: {error}"
        ) from error

    results = response.get("results", [])

    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("content", "")
        }
        for item in results
        if item.get("url")
    ]


# --------------------------------------------------
# SEARCH MULTIPLE CLAIMS
# --------------------------------------------------

def search_claims(
    claims: list,
    max_results: int = 5
) -> list:
    """
    Search multiple claims using one shared Tavily client.
    """

    all_results = []

    client = create_search_client()

    for item in claims:

        claim_text = item.get("claim", "").strip()

        if not claim_text:
            continue

        results = search_evidence(
            claim_text,
            max_results=max_results,
            client=client
        )

        all_results.append({
            "claim": claim_text,
            "evidence": results
        })

    return all_results
