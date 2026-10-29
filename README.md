[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# dev-toolkit-84

`dev-toolkit-84` is an asynchronous Python library engineered for rapid blockchain data extraction, smart contract interaction, and gas-efficient transaction management. Built for Web3 developers and quantitative traders, it streamlines multi-RPC endpoint failover and real-time EVM event monitoring into a single unified interface.

## Features

- **Multi-RPC Load Balancing:** Automatically routes JSON-RPC requests across primary and fallback nodes to ensure zero-downtime block fetching.
- **Dynamic Gas Strategy Engine:** Calculates optimal EIP-1559 priority fees in real time using mempool density and block base fee histograms.
- **EVM Event Streaming:** Listens to raw contract log streams over WebSockets with automatic reconnection and chain-reorg handling.
- **ABI Auto-Resolution:** Automatically fetches, decodes, and caches verified smart contract ABIs directly from Etherscan-compatible APIs.

## Installation

Install `dev-toolkit-84` via `pip`:

```bash
pip install dev-toolkit-84
```

For WebSocket and high-performance JSON parsing support, install with optional dependencies:

```bash
pip install dev-toolkit-84[fast]
```

## Quick Start

The following example demonstrates initializing an RPC connection and retrieving optimized gas parameters for an Ethereum transaction:

```python
import asyncio
from dev_toolkit_84 import CryptoClient, GasEstimator

async def main():
    # Initialize high-availability provider client
    client = CryptoClient(
        rpc_urls=[
            "https://eth-mainnet.g.alchemy.com/v2/your-api-key",
            "https://rpc.ankr.com/eth"
        ]
    )
    
    # Calculate optimal EIP-1559 gas fees
    estimator = GasEstimator(client)
    gas_params = await estimator.get_eip1559_fees(priority="fast")

    print(f"Base Fee: {gas_params.base_fee_gwei:.2f} Gwei")
    print(f"Max Priority Fee: {gas_params.max_priority_fee_gwei:.2f} Gwei")

if __name__ == "__main__":
    asyncio.run(main())
```

## License

Distributed under the MIT License. See `LICENSE` for more information.