"""Simple Ollama connectivity checker.

Usage:
  python scripts/check_ollama_host.py

It reads OLLAMA_HOST and OLLAMA_MODEL from the environment (falls back to defaults).
It performs an HTTP probe to the Ollama REST API (/v1/models) and optionally
tries to instantiate the Python Ollama client if the package is installed.

This script is safe to run locally to verify the ngrok/remote URL you provided.
"""
import os
import sys
import json
import socket
from urllib.parse import urlparse

try:
    import requests
except Exception:
    print("The 'requests' package is required. Install with: pip install requests")
    sys.exit(1)


def http_probe(host_url: str):
    url = host_url.rstrip('/') + '/v1/models'
    print(f"HTTP probe -> {url}")
    try:
        r = requests.get(url, timeout=10)
        print(f"Status: {r.status_code}")
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text[:1000])
    except Exception as e:
        print(f"HTTP probe failed: {e}")


def http_probe_with_default_headers(host_url: str):
    url = host_url.rstrip('/') + '/v1/models'
    headers = {
        "ngrok-skip-browser-warning": "true",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": host_url,
    }
    print(f"HTTP probe with headers -> {url}")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        try:
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(r.text[:1000])
    except Exception as e:
        print(f"HTTP probe with headers failed: {e}")


def tcp_probe(host_url: str):
    p = urlparse(host_url)
    host = p.hostname
    port = p.port or (443 if p.scheme == 'https' else 80)
    print(f"TCP probe -> {host}:{port}")
    try:
        with socket.create_connection((host, port), timeout=5):
            print("TCP: OK")
    except Exception as e:
        print(f"TCP probe failed: {e}")


def try_ollama_client(host_url: str):
    try:
        from ollama import Client as OllamaClient
    except Exception as e:
        print(f"ollama python client not available: {e}")
        return
    print("ollama python package found — trying to instantiate client...")
    try:
        client = OllamaClient(host=host_url)
        # Try a common method; different versions may expose different APIs.
        for method in ('list_models', 'models', 'get_models'):
            if hasattr(client, method):
                try:
                    fn = getattr(client, method)
                    res = fn()
                    print(f"Client.{method}() -> {type(res)}")
                    try:
                        print(json.dumps(res, indent=2, default=str)[:2000])
                    except Exception:
                        print(res)
                    return
                except Exception as e:
                    print(f"Client.{method}() failed: {e}")
        # Fallback: print repr
        print(repr(client))
    except Exception as e:
        print(f"Could not instantiate OllamaClient: {e}")


def main():
    host = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'phi')
    print(f"OLLAMA_HOST={host}")
    print(f"OLLAMA_MODEL={model}")
    print('\n-- TCP probe --')
    tcp_probe(host)
    print('\n-- HTTP probe --')
    http_probe(host)
    print('\n-- HTTP probe with default headers (like main/llm.py) --')
    http_probe_with_default_headers(host)
    print('\n-- Ollama client check --')
    try_ollama_client(host)


if __name__ == '__main__':
    main()
