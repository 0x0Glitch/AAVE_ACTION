# Aave Action Provider for Coinbase AgentKit

## Overview

This repository contains an implementation of an Aave Action Provider for the Coinbase AgentKit framework. The Aave Action Provider enables AI agents to interact with the Aave V3 protocol on Base mainnet, providing functionality for lending, borrowing, and managing positions.

## Features

The Aave Action Provider supports the following actions:

- **Supply**: Deposit assets to Aave as collateral
- **Withdraw**: Withdraw supplied assets from Aave
- **Borrow**: Borrow assets against supplied collateral
- **Repay**: Repay borrowed assets
- **Get Portfolio**: Retrieve user portfolio details from Aave

## File Structure

```
python/coinbase-agentkit/coinbase_agentkit/action_providers/aave/
├── __init__.py              # Package initialization
├── aave_action_provider.py  # Main action provider implementation
├── constants.py             # Contract addresses and ABIs
├── schemas.py               # Input validation schemas
└── utils.py                 # Utility functions for Aave interactions
```

## Implementation Details

### Action Provider

The `AaveActionProvider` class in `aave_action_provider.py` implements the core functionality for interacting with the Aave protocol. It inherits from the base `ActionProvider` class and leverages the `create_action` decorator to define actions.

### Schemas

Input validation is handled through Pydantic schemas defined in `schemas.py`, ensuring that all inputs to actions are properly validated before execution:

- `AaveSupplySchema` - For supply actions
- `AaveWithdrawSchema` - For withdraw actions
- `AaveBorrowSchema` - For borrow actions
- `AaveRepaySchema` - For repay actions
- `AavePortfolioSchema` - For portfolio retrieval

### Constants

The `constants.py` file contains essential contract addresses and ABIs required for interacting with Aave, including:

- `POOL_ADDRESSES` - Addresses of the Aave Pool contract across networks
- `ASSET_ADDRESSES` - Addresses of supported assets (WETH, USDC, etc.)
- `POOL_ABI` - ABI for the Aave Pool contract
- `PRICE_FEED_ABI` - ABI for Chainlink price feeds
- `UI_POOL_DATA_PROVIDER_ABI` - ABI for retrieving user data

### Utilities

The `utils.py` file contains helper functions for:

- Token decimals and symbol retrieval
- Balance checking
- Amount formatting
- Token approvals
- Health factor calculations
- Portfolio data formatting

## Key Considerations

### Security

- All addresses are converted to checksum format using `Web3.to_checksum_address()` to ensure secure interactions with Ethereum contracts
- Token approvals are implemented before supply/repay operations
- Health factor calculations help prevent liquidation risks

### Integration with Chatbot

The action provider is integrated into the langchain-cdp-chatbot example by adding it to the action providers list in `chatbot.py`:

```python
from coinbase_agentkit.action_providers import (
    aave_action_provider,
    # other providers
)

# In the generate_agent function
action_providers = [
    aave_action_provider(),
    # other providers
]
```

## Usage Examples

### Supply Assets

```
Supply 0.1 WETH to Aave
```

### View Portfolio

```
Show my Aave portfolio
```

### Borrow Assets

```
Borrow 100 USDC from Aave at a variable interest rate
```

### Withdraw Assets

```
Withdraw 0.05 WETH from Aave
```

### Repay Debt

```
Repay 50 USDC to Aave
```

## Environment Setup

1. Ensure all required environment variables are set in `.env.local`:
   - `CDP_API_KEY_NAME`
   - `CDP_API_KEY_PRIVATE_KEY`
   - `OPENAI_API_KEY`
   - `NETWORK_ID` (set to `base-mainnet` for this implementation)

2. Install dependencies:
   ```bash
   make install
   ```

3. Run the chatbot:
   ```bash
   make run
   ```

## Troubleshooting

If you encounter issues with address format errors, ensure that all addresses are properly checksummed using `Web3.to_checksum_address()` before passing them to Web3.py functions.

## Future Improvements

- Add support for more assets and networks
- Implement debt switching functionality
- Add support for eMode and efficiency mode
- Implement isolation mode support
- Add liquidation risk warnings

## License

This project is licensed under the terms of the Apache License 2.0.
<!--  -->