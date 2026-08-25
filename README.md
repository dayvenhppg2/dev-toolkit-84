# dev-toolkit-84

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

dev-toolkit-84 is a Python toolkit that assists developers in cryptocurrency projects by offering streamlined functions for wallet operations and blockchain queries. It supports multiple chains and helps with common development tasks like key generation and transaction preparation.

## Features
- HD wallet generation and key derivation for Bitcoin, Ethereum, and Solana
- Transaction building and signing with EIP-1559 fee estimation for EVM chains
- Unified queries for account balances, token holdings, and recent transactions
- Cryptographic helpers for message signing and address validation

## Installation

```bash
git clone https://github.com/Developer/dev-toolkit-84.git
cd dev-toolkit-84
pip install -e .
```

## Usage

```python
from dev_toolkit import generate_wallet, get_balance, estimate_gas

wallet = generate_wallet(chain="ethereum")
print(wallet.address)

balance = get_balance(wallet.address, chain="ethereum")
print(f"Balance: {balance}")

gas = estimate_gas(chain="ethereum", to="0x742d35Cc6634C0532925a3b844Bc454e4438f44e", value=0.05)
print(f"Estimated gas: {gas}")
```