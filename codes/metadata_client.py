"""Simple client helpers to call the Metadata Management Flask API.

Provides:
- get_tables(base_url) -> list[dict]: raw response from /tables
- get_table_names(base_url) -> list[str]: list of table names extracted

Uses `requests` and sets a sensible timeout. Designed for use in scripts or tests.
"""
from typing import List, Dict, Any
import requests


DEFAULT_BASE = "http://127.0.0.1:5000"
DEFAULT_TIMEOUT = 5.0


def get_tables(base_url: str = DEFAULT_BASE, timeout: float = DEFAULT_TIMEOUT) -> List[Dict[str, Any]]:
    """Fetch `/tables` from the metadata API and return the parsed JSON list.

    Raises requests.HTTPError on non-2xx responses, or requests.RequestException on network errors.
    """
    url = f"{base_url.rstrip('/')}/tables"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError(f"unexpected /tables response shape: {type(data)}")
    return data


def get_file_names(base_url: str = DEFAULT_BASE, timeout: float = DEFAULT_TIMEOUT) -> List[str]:
    """Return only the table names discovered by the API.

    Example return: ["asset_metadata", "asset_performance", "plant_hierarchy"]
    """
    rows = get_tables(base_url=base_url, timeout=timeout)
    names: List[str] = []
    for r in rows:
        # defensive: accept either dict with 'table' or string elements
        if isinstance(r, dict) and 'table' in r:
            names.append(r['file'])
        elif isinstance(r, str):
            names.append(r)
        else:
            # ignore unexpected rows but keep going
            continue
    return names


if __name__ == '__main__':
    # simple CLI demo
    try:
        tbls = get_file_names()
        print('Details:', tbls)
    except Exception as e:
        print('Error fetching tables:', e)
