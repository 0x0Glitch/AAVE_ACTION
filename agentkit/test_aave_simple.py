"""
Simple validation test for the Aave action provider structure.
"""

import os
import sys
import json

# Print the directory structure to understand what we're working with
print("Checking Aave action provider structure...")

aave_dir = "/Users/anshumanyadav/AAVE_CDP/agentkit/python/coinbase-agentkit/coinbase_agentkit/action_providers/aave"
print(f"Checking directory: {aave_dir}")

if os.path.exists(aave_dir):
    print("✅ Aave directory exists")
    files = os.listdir(aave_dir)
    print(f"Files in directory: {files}")
    
    # Check for essential files
    for file in ['__init__.py', 'aave_action_provider.py', 'constants.py', 'schemas.py', 'utils.py']:
        if file in files:
            print(f"✅ Found {file}")
            
            # Print the file size to verify it's not empty
            size = os.path.getsize(os.path.join(aave_dir, file))
            print(f"   Size: {size} bytes")
            
            # If it's aave_action_provider.py, check its content
            if file == 'aave_action_provider.py':
                with open(os.path.join(aave_dir, file), 'r') as f:
                    content = f.read()
                    actions = [
                        line for line in content.split('\n') 
                        if '@create_action' in line and 'name=' in line
                    ]
                    print(f"   Actions defined: {len(actions)}")
                    for action in actions:
                        print(f"   - {action.strip()}")
        else:
            print(f"❌ Missing {file}")
else:
    print("❌ Aave directory not found!")

print("\nAave action provider structure validation completed.")
print("\nInstructions for full integration:")
print("1. Make sure coinbase_agentkit package is installed in your Python environment")
print("2. Add this line to your import statements in your application:")
print("   from coinbase_agentkit import aave_action_provider")
print("3. Add aave_action_provider() to your action_providers list when creating AgentKit")
print("4. The Aave action provider will be available with the following actions:")
print("   - supply: Supply assets to Aave protocol")
print("   - withdraw: Withdraw supplied assets")
print("   - borrow: Borrow assets against collateral")
print("   - repay: Repay borrowed assets")
print("   - get_portfolio: Get portfolio details")
