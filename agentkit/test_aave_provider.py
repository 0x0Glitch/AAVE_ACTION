"""
Test script for the Aave action provider.
"""

import sys
# Add the path to agentkit
sys.path.append("/Users/anshumanyadav/AAVE_CDP/agentkit/python")

from coinbase_agentkit.action_providers.aave.aave_action_provider import AaveActionProvider
from coinbase_agentkit.action_providers.aave.schemas import AavePortfolioSchema
from coinbase_agentkit.network import Network

def test_aave_provider():
    """Test the Aave action provider functionality."""
    print("Creating Aave action provider...")
    provider = AaveActionProvider()
    
    print("\nTesting supported networks...")
    # Test with supported network
    base_sepolia = Network(protocol_family="evm", network_id="base-sepolia", chain_id=84532)
    supported = provider.supports_network(base_sepolia)
    print(f"base-sepolia supported: {supported}")
    
    # Test with unsupported network
    eth_mainnet = Network(protocol_family="evm", network_id="ethereum", chain_id=1)
    supported = provider.supports_network(eth_mainnet)
    print(f"ethereum supported: {supported}")
    
    # Print schema information
    print("\nSchema info for portfolio action:")
    schema = AavePortfolioSchema.schema()
    print(f"Properties: {schema.get('properties', {})}")
    
    print("\nAave action provider initialization successful!")
    print("Available actions:")
    print("- supply: Supply assets to Aave protocol")
    print("- withdraw: Withdraw supplied assets")
    print("- borrow: Borrow assets against collateral")
    print("- repay: Repay borrowed assets")
    print("- get_portfolio: Get portfolio details")

if __name__ == "__main__":
    test_aave_provider()
