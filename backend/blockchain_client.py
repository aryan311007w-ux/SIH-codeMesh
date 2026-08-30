"""
Multi-chain blockchain data client.

Routes requests to the correct chain-specific adapter:
  - EVM chains (Ethereum, BSC, Polygon): Etherscan v2 multi-chain API
  - Tron: TronGrid REST API
  - Bitcoin: Blockstream.info public API (no key required)

All adapters return a normalized list of transaction dicts:
  {
    "hash":        str,
    "from":        str (lower-cased),
    "to":          str (lower-cased),
    "value":       str  (raw integer string, smallest unit),
    "timeStamp":   str  (unix epoch seconds),
    "chain":       str  (chain key, e.g. "ethereum"),
  }
"""

import time
from functools import lru_cache
from typing import List, Dict

import requests

from chains import SUPPORTED_CHAINS

ETHERSCAN_V2_URL = "https://api.etherscan.io/v2/api"
TRONGRID_URL     = "https://api.trongrid.io"
BLOCKSTREAM_URL  = "https://blockstream.info/api"

# Default retry settings for all adapters
_DEFAULT_RETRIES   = 3
_DEFAULT_BACKOFF   = 1.0   # base backoff in seconds, doubles each retry
_RETRY_STATUS_CODES = {429, 500, 502, 503, 504}


class BlockchainClientError(Exception):
    """Raised when the underlying data source fails or rate-limits us."""


# ---------------------------------------------------------------------------
# Shared retry helper
# ---------------------------------------------------------------------------

def _request_with_retry(method, url, retries=_DEFAULT_RETRIES, backoff=_DEFAULT_BACKOFF,
                        timeout=15, _status_codes=None, **kwargs):
    """
    HTTP request with exponential-backoff retry on transient errors.

    Retries on: 429 (rate limit), 500, 502, 503, 504.
    Raises BlockchainClientError if all retries are exhausted.
    """
    _status_codes = _status_codes or _RETRY_STATUS_CODES
    last_exc = None
    last_status = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.request(method, url, timeout=timeout, **kwargs)
        except requests.RequestException as e:
            last_exc = e
            if attempt < retries:
                time.sleep(backoff * (2 ** (attempt - 1)))
                continue
            raise BlockchainClientError(f"Request failed after {retries} attempts: {e}")

        if resp.status_code not in _status_codes:
            return resp

        # Transient error — wait and retry
        last_status = resp.status_code
        if attempt < retries:
            wait = backoff * (2 ** (attempt - 1))
            # Respect Retry-After header if present (e.g. from 429)
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                try:
                    wait = max(wait, float(retry_after))
                except ValueError:
                    pass
            time.sleep(wait)

    raise BlockchainClientError(
        f"{method} {url} failed after {retries} attempts (last status: {last_status})."
    )


# ---------------------------------------------------------------------------
# EVM Adapter (Ethereum, BSC, Polygon — all via Etherscan v2 chainid param)
# ---------------------------------------------------------------------------

class EVMAdapter:
    def __init__(self, api_key: str, chain_id: int, request_delay: float = 0.15):
        self.api_key       = api_key
        self.chain_id      = chain_id
        self.request_delay = request_delay

    def get_transactions(self, wallet: str, max_results: int = 200,
                         include_internal: bool = True) -> List[dict]:
        return self._fetch(wallet.lower(), max_results, include_internal)

    @lru_cache(maxsize=2048)
    def _fetch(self, wallet: str, max_results: int,
               include_internal: bool) -> List[dict]:
        time.sleep(self.request_delay)  # one rate-limit pause per wallet (both requests share it)
        # Step 1: normal external transactions
        params = {
            "chainid":    self.chain_id,
            "module":     "account",
            "action":     "txlist",
            "address":    wallet,
            "startblock": 0,
            "endblock":   99999999,
            "page":       1,
            "offset":     max_results,
            "sort":       "desc",
            "apikey":     self.api_key,
        }
        time.sleep(self.request_delay)
        try:
            resp = _request_with_retry("GET", ETHERSCAN_V2_URL, params=params, timeout=15)
            resp.raise_for_status()
        except BlockchainClientError:
            raise
        except requests.RequestException as e:
            raise BlockchainClientError(f"EVM request failed for {wallet}: {e}")

        data    = resp.json()
        status  = data.get("status")
        message = data.get("message", "")
        result  = data.get("result", "")

        if status == "1":
            txs = [self._normalize(tx) for tx in result]
        elif "No transactions found" in message or result == [] or result == "":
            txs = []
        else:
            raise BlockchainClientError(f"Etherscan error for {wallet}: {message} — {result}")

        # Step 2: also fetch internal (contract call) transactions
        if include_internal:
            params["action"] = "txlistinternal"
            try:
                resp2 = _request_with_retry(
                    "GET", ETHERSCAN_V2_URL, params=params, timeout=15
                )
                resp2.raise_for_status()
            except BlockchainClientError:
                raise
            except requests.RequestException as e:
                raise BlockchainClientError(
                    f"EVM internal tx request failed for {wallet}: {e}"
                )

            data2    = resp2.json()
            status2  = data2.get("status")
            message2 = data2.get("message", "")
            result2  = data2.get("result", "")

            if status2 == "1" and isinstance(result2, list):
                internal_txs = [self._normalize(tx) for tx in result2]
                # Merge and deduplicate by tx hash
                seen = {t["hash"] for t in txs}
                for itx in internal_txs:
                    if itx["hash"] not in seen:
                        txs.append(itx)
                        seen.add(itx["hash"])
                txs.sort(key=lambda t: t.get("timeStamp", "0"), reverse=True)

        return txs

    @staticmethod
    def _normalize(tx: dict) -> dict:
        return {
            "hash":      tx.get("hash", ""),
            "from":      tx.get("from", "").lower(),
            "to":        (tx.get("to") or "").lower(),
            "value":     tx.get("value", "0"),
            "timeStamp": tx.get("timeStamp", "0"),
            "chain":     "evm",
        }


# ---------------------------------------------------------------------------
# Tron Adapter (TronGrid REST API)
# ---------------------------------------------------------------------------

class TronAdapter:
    def __init__(self, api_key: str = "", request_delay: float = 0.20):
        self.api_key       = api_key
        self.request_delay = request_delay

    def get_transactions(self, wallet: str, max_results: int = 200) -> List[dict]:
        return self._fetch(wallet, min(max_results, 200))

    @lru_cache(maxsize=512)
    def _fetch(self, wallet: str, max_results: int) -> List[dict]:
        url     = f"{TRONGRID_URL}/v1/accounts/{wallet}/transactions"
        headers = {"TRON-PRO-API-KEY": self.api_key} if self.api_key else {}
        params  = {"limit": max_results, "order_by": "block_timestamp,desc"}
        time.sleep(self.request_delay)
        try:
            resp = _request_with_retry("GET", url, params=params, headers=headers, timeout=15)
            resp.raise_for_status()
        except BlockchainClientError:
            raise
        except requests.RequestException as e:
            raise BlockchainClientError(f"TronGrid request failed for {wallet}: {e}")

        data = resp.json()
        txs  = data.get("data", [])
        if not txs:
            return []
        return [self._normalize(tx, wallet) for tx in txs]

    @staticmethod
    def _normalize(tx: dict, queried_wallet: str) -> dict:
        """Normalize TronGrid transaction format."""
        raw_data = tx.get("raw_data", {})
        contract = (raw_data.get("contract") or [{}])[0]
        param    = contract.get("parameter", {}).get("value", {})
        from_addr = param.get("owner_address", "").lower()
        to_addr   = param.get("to_address", param.get("contract_address", "")).lower()
        amount    = str(param.get("amount", param.get("call_value", 0)))
        return {
            "hash":      tx.get("txID", ""),
            "from":      from_addr or queried_wallet.lower(),
            "to":        to_addr,
            "value":     amount,
            "timeStamp": str(tx.get("block_timestamp", 0) // 1000),
            "chain":     "tron",
        }


# ---------------------------------------------------------------------------
# Bitcoin Adapter (Blockstream.info — no API key required)
# ---------------------------------------------------------------------------

class BitcoinAdapter:
    def __init__(self, request_delay: float = 0.50):
        self.request_delay = request_delay

    def get_transactions(self, wallet: str, max_results: int = 200) -> List[dict]:
        return self._fetch(wallet, max_results)

    @lru_cache(maxsize=512)
    def _fetch(self, wallet: str, max_results: int) -> List[dict]:
        url = f"{BLOCKSTREAM_URL}/address/{wallet}/txs"
        time.sleep(self.request_delay)
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise BlockchainClientError(f"Blockstream request failed for {wallet}: {e}")

        raw_txs = resp.json()
        if not isinstance(raw_txs, list):
            return []
        return [self._normalize(tx, wallet) for tx in raw_txs[:max_results]]

    @staticmethod
    def _normalize(tx: dict, queried_wallet: str) -> dict:
        """Normalize Blockstream.info transaction format."""
        # Determine primary sender (first input address)
        inputs  = tx.get("vin", [])
        outputs = tx.get("vout", [])
        from_addr = ""
        if inputs:
            prevout = inputs[0].get("prevout", {})
            from_addr = prevout.get("scriptpubkey_address", "")

        # Determine primary recipient (first output that is NOT the sender)
        to_addr = ""
        total_value = 0
        for out in outputs:
            addr = out.get("scriptpubkey_address", "")
            if addr and addr != queried_wallet:
                to_addr = addr
                total_value += out.get("value", 0)
                break

        ts = tx.get("status", {}).get("block_time", 0)
        return {
            "hash":      tx.get("txid", ""),
            "from":      from_addr.lower() if from_addr else queried_wallet.lower(),
            "to":        to_addr.lower() if to_addr else "",
            "value":     str(total_value),   # satoshis
            "timeStamp": str(ts),
            "chain":     "bitcoin",
        }


# ---------------------------------------------------------------------------
# Multi-chain Client Router
# ---------------------------------------------------------------------------

class BlockchainClient:
    """
    Routes `get_transactions()` calls to the correct chain adapter.
    Chain-specific adapters are created lazily on first use.
    """

    def __init__(self, api_keys: Dict[str, str]):
        """
        api_keys: dict mapping chain key → API key string.
          Expected keys: "etherscan", "trongrid" (others optional/unused for free APIs)
        """
        self._etherscan_key = api_keys.get("etherscan", "")
        self._trongrid_key  = api_keys.get("trongrid",  "")
        self._adapters: Dict[str, object] = {}

    def _get_adapter(self, chain: str):
        if chain in self._adapters:
            return self._adapters[chain]

        meta = SUPPORTED_CHAINS.get(chain)
        if not meta:
            raise BlockchainClientError(f"Unsupported chain: {chain!r}")

        chain_type = meta["type"]
        if chain_type == "evm":
            adapter = EVMAdapter(api_key=self._etherscan_key, chain_id=meta["chain_id"])
        elif chain_type == "tron":
            adapter = TronAdapter(api_key=self._trongrid_key)
        elif chain_type == "bitcoin":
            adapter = BitcoinAdapter()
        else:
            raise BlockchainClientError(f"No adapter for chain type: {chain_type!r}")

        self._adapters[chain] = adapter
        return adapter

    def get_transactions(self, wallet: str, chain: str = "ethereum",
                         max_results: int = 200,
                         include_internal: bool = True) -> List[dict]:
        """
        Fetch and return normalized transactions for `wallet` on `chain`.

        For EVM chains, also fetches internal (contract call) transactions
        and merges them with normal transactions (deduplicated by tx hash).
        """
        adapter = self._get_adapter(chain)
        kwargs = {}
        meta = SUPPORTED_CHAINS.get(chain)
        if meta and meta.get("type") == "evm":
            kwargs["include_internal"] = include_internal
        return adapter.get_transactions(wallet, max_results, **kwargs)
