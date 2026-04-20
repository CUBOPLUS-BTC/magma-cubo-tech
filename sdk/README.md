# magma-sdk

Synchronous Python client for the Magma / SatScore Bitcoin API.

Stdlib-only (no `requests` dependency). Typed dataclass responses, a single
`MagmaClient` facade, automatic retries on transient failures, and a
structured exception hierarchy so callers can react to specific HTTP status
codes without string matching.

## Install

```bash
pip install -e ./sdk
```

## Quick start

```python
from magma_sdk import MagmaClient

client = MagmaClient("https://api.magma.example")

# Public endpoints
projection = client.savings.project(monthly_usd=100, years=10)
print(projection.scenarios[0].projected_value)

comparison = client.remittance.compare(amount_usd=500, frequency="monthly")
print(comparison.best_channel, comparison.annual_savings)

price = client.price.get()
print(price.price_usd, price.sources_count)

# Authenticated endpoints — Nostr (NIP-07) flow
challenge = client.auth.create_challenge(pubkey="a" * 64)
# ...have the wallet sign an event with `challenge`...
session = client.auth.verify(signed_event=signed, challenge=challenge.challenge)
# The token is stored automatically after verify().

progress = client.savings.progress()
print(progress.streak_months, progress.total_invested_usd)
```

## LNURL-auth flow

```python
ln = client.auth.create_lnurl()
print("Scan:", ln.lnurl)

while True:
    status = client.auth.lnurl_status(ln.k1)
    if status.authenticated:
        print("Logged in as", status.pubkey)
        break
```

## Error handling

```python
from magma_sdk import (
    APIError, AuthenticationError, RateLimitError, TransportError,
)

try:
    client.savings.progress()
except AuthenticationError:
    ...  # token expired — re-auth
except RateLimitError as e:
    ...  # back off; e.detail may explain why
except TransportError:
    ...  # network or DNS problem
except APIError as e:
    print(e.status, e.detail)
```

## Configuration

```python
client = MagmaClient(
    "https://api.magma.example",
    token="optional_initial_bearer",
    timeout=10.0,       # per-request seconds
    max_retries=2,      # transient failures (5xx, 429, network)
    backoff=0.25,       # exponential base, doubles each retry
    user_agent="my-app/1.0",
)
```

## Status

`v0.1`: stable covering public endpoints and session management. Pagination,
async support, and auto-refresh for expired tokens are tracked for a future
release.
