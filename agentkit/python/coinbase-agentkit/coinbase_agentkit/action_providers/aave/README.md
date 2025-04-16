# Aave Action Provider

This module provides actions to interact with the Aave V3 protocol on Base mainnet and Base Sepolia testnet for lending and borrowing operations.

## Overview

The Aave Action Provider enables AI agents to interact with the Aave V3 protocol on the Base network, allowing for operations such as:

- Supply assets as collateral
- Withdraw supplied assets
- Borrow assets against collateral
- Repay borrowed assets
- Retrieve portfolio details

## Supported Networks

- Base Mainnet
- Base Sepolia (testnet)

## Supported Assets

**Base Mainnet:**
- WETH (wrapped ETH)
- USDC
- cbETH (Coinbase ETH)
- wstETH (wrapped staked ETH)

**Base Sepolia:**
- WETH
- USDC

## Actions

### supply

Supply assets to Aave as collateral for borrowing or earning interest.

**Parameters:**
- `asset_id`: The asset to supply (e.g., `weth`, `usdc`, `cbeth`, `wsteth`)
- `amount`: The amount of tokens to supply in human-readable format (e.g., `0.1`)
- `on_behalf_of`: (Optional) The address to supply on behalf of
- `referral_code`: (Optional) Referral code, default is 0

### withdraw

Withdraw previously supplied assets from Aave.

**Parameters:**
- `asset_id`: The asset to withdraw (e.g., `weth`, `usdc`, `cbeth`, `wsteth`)
- `amount`: The amount to withdraw or `max` to withdraw all
- `to`: (Optional) The address to withdraw to

### borrow

Borrow assets from Aave against your supplied collateral.

**Parameters:**
- `asset_id`: The asset to borrow (e.g., `weth`, `usdc`, `cbeth`, `wsteth`)
- `amount`: The amount to borrow
- `interest_rate_mode`: (Optional) Interest rate mode: 1 for stable, 2 for variable (default)
- `on_behalf_of`: (Optional) The address to borrow on behalf of
- `referral_code`: (Optional) Referral code

### repay

Repay borrowed assets to Aave.

**Parameters:**
- `asset_id`: The asset to repay (e.g., `weth`, `usdc`, `cbeth`, `wsteth`)
- `amount`: The amount to repay or `max` to repay all
- `interest_rate_mode`: (Optional) Interest rate mode: 1 for stable, 2 for variable (default)
- `on_behalf_of`: (Optional) The address to repay debt for

### get_portfolio

Retrieve portfolio details from Aave including supplied collateral, borrowed assets, and health factor.

**Parameters:**
- `account`: (Optional) The address to get portfolio details for

## Example Usage

```python
from coinbase_agentkit.wallet_providers import EvmWalletProvider
from coinbase_agentkit.action_providers.aave import aave_action_provider

# Initialize wallet provider
wallet = EvmWalletProvider(...)

# Initialize Aave action provider
provider = aave_action_provider()

# Supply 0.1 WETH
result = provider.supply(wallet, {
    "asset_id": "weth",
    "amount": "0.1"
})
print(result)

# Borrow 50 USDC
result = provider.borrow(wallet, {
    "asset_id": "usdc",
    "amount": "50",
    "interest_rate_mode": 2  # Variable rate
})
print(result)

# Get portfolio details
result = provider.get_portfolio(wallet, {})
print(result)
```

## Implementation Details

- The provider interacts with Aave V3 contracts directly using Web3.py.
- Token approvals are handled automatically before supply and repay actions.
- Health factor checks ensure borrowing and withdrawal operations maintain a safe position.
- Portfolio details include total collateral, total debt, available borrowing capacity, and health factor.

## Network Support

The provider supports networks where Aave V3 is deployed, with address mappings for Base mainnet and Base Sepolia.

## Error Handling

The provider implements robust error checking for:
- Insufficient token balances
- Insufficient collateral for borrowing
- Risk of liquidation when withdrawing collateral
- Invalid input parameters

## Notes

- Health factor should be maintained above 1.0 to avoid liquidation.
- Variable interest rates (mode 2) are recommended for most users.
- Some assets may only support variable rate borrowing.
