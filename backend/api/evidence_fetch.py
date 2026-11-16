
import ipaddress
import socket
from urllib.parse import urljoin, urlparse

import httpx
import trafilatura


MAX_REDIRECTS = 5
MAX_PAGE_SIZE = 5 * 1024 * 1024

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EvidenceResearchBot/1.0)"
}


def is_public_url(url: str) -> bool:
    """Allow only HTTP(S) URLs pointing to public IP addresses."""

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if not parsed.hostname:
            return False

        if parsed.username or parsed.password:
            return False

        hostname = parsed.hostname

        # Reject localhost and local hostnames.
        if hostname.lower() == "localhost":
            return False

        addresses = socket.getaddrinfo(
            hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM
        )

        if not addresses:
            return False

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if not ip.is_global:
                return False

        return True

    except (ValueError, socket.gaierror, OSError):
        return False


def fetch_page(url: str) -> dict:
    """Download and extract readable text from a public webpage."""

    current_url = url

    try:
        with httpx.Client(
            timeout=15,
            follow_redirects=False,
            headers=HEADERS
        ) as client:

            for _ in range(MAX_REDIRECTS + 1):

                if not is_public_url(current_url):
                    return {
                        "success": False,
                        "url": current_url,
                        "error": "URL is invalid or points to a non-public address."
                    }

                with client.stream("GET", current_url) as response:

                    if response.status_code in (301, 302, 303, 307, 308):
                        location = response.headers.get("location")

                        if not location:
                            return {
                                "success": False,
                                "url": current_url,
                                "error": "Redirect location missing."
                            }

                        current_url = urljoin(current_url, location)
                        continue

                    response.raise_for_status()

                    content_type = response.headers.get(
                        "content-type", ""
                    ).lower()

                    if "text/html" not in content_type:
                        return {
                            "success": False,
                            "url": current_url,
                            "error": "This source is not an HTML webpage."
                        }

                    chunks = []
                    total_size = 0

                    for chunk in response.iter_bytes():
                        total_size += len(chunk)

                        if total_size > MAX_PAGE_SIZE:
                            return {
                                "success": False,
                                "url": current_url,
                                "error": "Webpage exceeds the 5 MB limit."
                            }

                        chunks.append(chunk)

                    html = b"".join(chunks).decode(
                        "utf-8", errors="replace"
                    )

                    downloaded_url = current_url

                extracted_text = trafilatura.extract(
                    html,
                    include_tables=True,
                    favor_precision=True
                )

                metadata = trafilatura.extract_metadata(html)

                title = (
                    metadata.title
                    if metadata and metadata.title
                    else ""
                )

                if not extracted_text:
                    return {
                        "success": False,
                        "url": downloaded_url,
                        "error": "Could not extract readable webpage text."
                    }

                return {
                    "success": True,
                    "title": title,
                    "url": downloaded_url,
                    "text": extracted_text[:12000]
                }

            return {
                "success": False,
                "url": current_url,
                "error": "Too many redirects."
            }

    except httpx.HTTPStatusError as error:
        return {
            "success": False,
            "url": current_url,
            "error": f"HTTP error: {error.response.status_code}"
        }

    except Exception as error:
        return {
            "success": False,
            "url": current_url,
            "error": str(error)
        }


def fetch_evidence(search_results: list, max_pages: int = 3) -> list:
    """Fetch actual webpage content from search results."""

    extracted_sources = []

    for item in search_results[:max_pages]:

        url = item.get("url", "")

        if not url:
            continue

        result = fetch_page(url)

        if result["success"]:
            extracted_sources.append(result)

    return extracted_sources
