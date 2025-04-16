"""Utility functions for Aave action provider."""

from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Union

import web3
from web3 import Web3

from ...wallet_providers import EvmWalletProvider
from ..erc20.constants import ERC20_ABI
from .constants import (
    POOL_ABI, 
    POOL_ADDRESSES,
    UI_POOL_DATA_PROVIDER_ABI,
    UI_POOL_DATA_PROVIDER_ADDRESSES,
    PRICE_FEED_ABI
)


def get_token_decimals(wallet: EvmWalletProvider, token_address: str) -> int:
    """Get the number of decimals for a token.

    Args:
        wallet: The wallet provider for reading from contracts.
        token_address: The address of the token.

    Returns:
        int: The number of decimals for the token.

    """
    result = wallet.read_contract(
        contract_address=Web3.to_checksum_address(token_address),
        abi=ERC20_ABI,
        function_name="decimals",
        args=[]
    )
    return result


def get_token_symbol(wallet: EvmWalletProvider, token_address: str) -> str:
    """Get a token's symbol from its contract.

    Args:
        wallet: The wallet provider for reading from contracts.
        token_address: The address of the token contract.

    Returns:
        str: The token symbol.

    """
    return wallet.read_contract(
        contract_address=Web3.to_checksum_address(token_address),
        abi=ERC20_ABI,
        function_name="symbol",
        args=[]
    )


def get_token_balance(wallet: EvmWalletProvider, token_address: str) -> int:
    """Get the balance of a token for the wallet.

    Args:
        wallet: The wallet provider for reading from contracts.
        token_address: The address of the token.

    Returns:
        int: The balance in atomic units.

    """
    return wallet.read_contract(
        contract_address=Web3.to_checksum_address(token_address),
        abi=ERC20_ABI,
        function_name="balanceOf",
        args=[wallet.get_address()]
    )


def format_amount_with_decimals(amount: str, decimals: int) -> int:
    """Format a human-readable amount with the correct number of decimals.

    Args:
        amount: The amount as a string (e.g. "0.1").
        decimals: The number of decimals for the token.

    Returns:
        int: The amount in atomic units.

    """
    try:
        if amount == "max":
            return 2**256 - 1  # uint256 max for Aave's withdraw/repay all
        
        # Handle scientific notation
        if 'e' in amount.lower():
            amount_decimal = Decimal(amount)
            return int(amount_decimal * (10 ** decimals))
        
        # Handle regular decimal notation
        parts = amount.split('.')
        if len(parts) == 1:
            return int(parts[0]) * (10 ** decimals)
        
        whole, fraction = parts
        if len(fraction) > decimals:
            fraction = fraction[:decimals]
        else:
            fraction = fraction.ljust(decimals, '0')
        
        return int(whole) * (10 ** decimals) + int(fraction)
    except ValueError as e:
        raise ValueError(f"Invalid amount format: {amount}") from e


def format_amount_from_decimals(amount: int, decimals: int) -> str:
    """Format an atomic amount to a human-readable string.

    Args:
        amount: The amount in atomic units.
        decimals: The number of decimals for the token.

    Returns:
        str: The amount as a human-readable string.

    """
    if amount == 0:
        return "0"
    
    amount_decimal = Decimal(amount) / (10 ** decimals)
    # Format to remove trailing zeros and decimal point if whole number
    s = str(amount_decimal)
    return s.rstrip('0').rstrip('.') if '.' in s else s


def approve_token(wallet: EvmWalletProvider, token_address: str, spender_address: str, amount: int) -> str:
    """Approve a token for spending by Aave Pool contract.

    Args:
        wallet: The wallet provider for sending transactions.
        token_address: The address of the token to approve.
        spender_address: The address of the spender (Pool contract).
        amount: The amount to approve in atomic units.

    Returns:
        str: Transaction hash of the approval transaction.

    """
    token_contract = Web3().eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    encoded_data = token_contract.encode_abi(
        "approve", 
        args=[Web3.to_checksum_address(spender_address), amount]
    )
    
    params = {
        "to": Web3.to_checksum_address(token_address),
        "data": encoded_data,
    }
    
    tx_hash = wallet.send_transaction(params)
    wallet.wait_for_transaction_receipt(tx_hash)
    return tx_hash


def get_user_account_data(wallet: EvmWalletProvider, pool_address: str, account: Optional[str] = None) -> Dict[str, Union[Decimal, str]]:
    """Get user account data from Aave pool.

    Args:
        wallet: The wallet provider for reading from contracts.
        pool_address: The address of the Aave Pool contract.
        account: Optional account address. Defaults to wallet address.

    Returns:
        Dict[str, Union[Decimal, str]]: Dictionary containing account data.

    """
    if not account:
        account = wallet.get_address()

    # Get account data
    result = wallet.read_contract(
        contract_address=Web3.to_checksum_address(pool_address),
        abi=POOL_ABI,
        function_name="getUserAccountData",
        args=[account]
    )

    total_collateral_base, total_debt_base, available_borrows_base, current_liquidation_threshold, ltv, health_factor = result

    return {
        "totalCollateralBase": Decimal(total_collateral_base) / Decimal(10**18),
        "totalDebtBase": Decimal(total_debt_base) / Decimal(10**18),
        "availableBorrowsBase": Decimal(available_borrows_base) / Decimal(10**18),
        "currentLiquidationThreshold": Decimal(current_liquidation_threshold) / Decimal(10**4),
        "ltv": Decimal(ltv) / Decimal(10**4),
        "healthFactor": Decimal(health_factor) / Decimal(10**18) if health_factor > 0 else Decimal('inf'),
    }


def get_health_factor(wallet: EvmWalletProvider, pool_address: str, account: Optional[str] = None) -> Decimal:
    """Get the current health factor for a user.

    Args:
        wallet: The wallet provider for reading from contracts.
        pool_address: The address of the Aave Pool contract.
        account: Optional account address. Defaults to wallet address.

    Returns:
        Decimal: The current health factor.

    """
    account_data = get_user_account_data(wallet, Web3.to_checksum_address(pool_address), account)
    return account_data["healthFactor"]


def get_portfolio_details_markdown(wallet: EvmWalletProvider, network_id: str, account: Optional[str] = None) -> str:
    """Generate markdown formatted portfolio details for Aave.

    Args:
        wallet: The wallet provider for reading from contracts.
        network_id: The network ID to get portfolio details for.
        account: Optional account address. Defaults to wallet address.

    Returns:
        str: Markdown formatted portfolio details.

    """
    if account is None:
        account = wallet.get_address()
    
    pool_address = Web3.to_checksum_address(POOL_ADDRESSES[network_id])
    ui_data_provider_address = Web3.to_checksum_address(UI_POOL_DATA_PROVIDER_ADDRESSES[network_id])
    
    # Get user account data from Pool contract
    account_data = get_user_account_data(wallet, pool_address, account)
    
    # Format the account data into markdown
    markdown = f"# Aave Portfolio for {account[:6]}...{account[-4:]}\n\n"
    
    # Summary section
    markdown += "## Summary\n\n"
    markdown += f"**Total Collateral:** {account_data['totalCollateralBase']:.4f} ETH\n"
    markdown += f"**Total Debt:** {account_data['totalDebtBase']:.4f} ETH\n"
    markdown += f"**Available to Borrow:** {account_data['availableBorrowsBase']:.4f} ETH\n"
    markdown += f"**Liquidation Threshold:** {account_data['currentLiquidationThreshold']:.2%}\n"
    markdown += f"**Loan to Value:** {account_data['ltv']:.2%}\n"
    
    # Health factor with color indicators
    health_factor = account_data["healthFactor"]
    if health_factor == Decimal('inf'):
        markdown += "**Health Factor:** ∞ (No borrows)\n"
    elif health_factor >= 2:
        markdown += f"**Health Factor:** {health_factor:.2f} (Healthy)\n"
    elif health_factor >= 1.1:
        markdown += f"**Health Factor:** {health_factor:.2f} (Caution)\n"
    else:
        markdown += f"**Health Factor:** {health_factor:.2f} (Danger - Risk of Liquidation)\n"
    
    # Try to get detailed reserve data if UI Pool Data Provider is available
    try:
        # This is a placeholder for fetching reserve data from the UI Pool Data Provider
        # In a complete implementation, you would call getUserReservesData from UI Pool Data Provider
        markdown += "\n## Reserve Details\n\n"
        markdown += "*Detailed reserve information not available in this version*\n"
        
        # Advice section
        markdown += "\n## Recommendations\n\n"
        if health_factor < 1.1 and health_factor != Decimal('inf'):
            markdown += "- **WARNING**: Your position is at risk of liquidation. Consider repaying some debt or adding more collateral.\n"
        elif account_data['totalCollateralBase'] > 0 and account_data['totalDebtBase'] == 0:
            markdown += "- You have supplied collateral but have no borrows. You can borrow against your collateral or withdraw if needed.\n"
        elif account_data['availableBorrowsBase'] > 0:
            markdown += f"- You can safely borrow up to {account_data['availableBorrowsBase']:.4f} ETH more.\n"
            
    except Exception as e:
        # If there was an error fetching reserve data, just note it
        pass
    
    return markdown
