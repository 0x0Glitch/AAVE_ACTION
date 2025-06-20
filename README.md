# Aave V3 Action Provider for Coinbase AgentKit

## Description

This module introduces an **Aave V3 action provider** for AgentKit, enabling comprehensive interactions with the Aave protocol on **Base mainnet**. The implementation supports lending, borrowing, and asset management functionalities consistent with existing Compound and Morpho providers.

*Note*: Testnet features are currently unavailable due to limited data (contract addresses, etc.). Efforts are ongoing to extend functionality to **Base Sepolia**.

## Key Features Implemented

* **Supply assets** to the Aave V3 pool
* **Withdraw supplied assets**
* **Borrow assets** with variable interest rates
* **Repay borrowed assets**
* **View portfolio details**, including health factor
* **Enable/disable assets as collateral**

aave/
├── aave_action_provider.py   
├── constants.py             
├── schemas.py               
├── utils.py               
├── __init__.py              
              
tests/action_providers/aave/
├── conftest.py              
├── test_aave_provider.py    
├── test_aave_supply.py      
└── test_aave_schemas.py     

## Example Interactions

### 1. Checking Portfolio

**Prompt:**

```
Check my Aave portfolio
```

**Wallet Details:**

* Provider: `cdp_wallet_provider`
* Address: `0xfe7fAF4FF695087dF4C997dE8771F8187d871Af4`
* Network:

  * Protocol Family: `evm`
  * Network ID: `base-mainnet`
  * Chain ID: `8453`
  * Native Balance: `1073835519462478`

**Portfolio Summary:**

| Metric                | USD     | Base Units |
| --------------------- | ------- | ---------- |
| Total Collateral      | \$0.046 | 4,620,524  |
| Total Debt            | \$0.000 | 20,099     |
| Available to Borrow   | \$0.037 | 3,676,320  |
| Liquidation Threshold | 83.00%  | -          |
| Loan to Value         | 80.00%  | -          |
| Health Factor         | 190.81  | Healthy    |

**Recommendations:**
Your borrowed amount is minimal and your position is healthy. You may borrow additional assets or repay existing debts as necessary.

---

### 2. Supplying WETH to Aave

**Prompt:**

```
Supply 0.00001 WETH to Aave
```

**Result:**

```
Successfully supplied 0.00001 WETH to Aave.
Transaction Hash: 0x7317d1543a680440b3f55093184d1a9bb5c02763388f17e6dbc7ed664788e818
Health Factor improved: 190.81 → 256.60
```

---

### 3. Borrowing Against Collateral

**Prompt:**

```
Borrow 0.01 USDC from Aave
```

**Result:**

```
Successfully borrowed 0.01 USDC (Variable Interest Rate).
Transaction Hash: 0xe5884d7a1467202b5e8c44ff6d4b6e74b4ad73fab62c267d692e72c51c45594b
Health Factor changed: 256.60 → 5.06
```

---

### 4. Repaying Borrowed Assets

**Prompt:**

```
Repay 0.001 USDC of 0xA8dd4312126816755Ba2a90e80a8E135866209a7
```

**Result:**

```
Successfully repaid 0.001 USDC (Variable Interest Rate).
Transaction Hash: 0xf0367f1bfb1a777ee3ba7c24f4f585ab3be56f3416bdb5c1201cc5909e50e9b3
Health Factor remains stable at 5.05
```

---

### 5. Withdrawing Assets

**Prompt:**

```
Withdraw 0.00001 WETH from Aave
```

**Result:**

```
Successfully withdrew 0.00001 WETH.
Transaction Hash: 0x60d2858ae0ea47202bcdfa9c28fe1e05b46bf858b5530ee4913799c05bfd9b7f
Health Factor changed: 5.05 → 3.76
```

---

### 6. Setting Collateral

**Prompt:**

```
Set WETH as collateral
```

**Result:**

```
Successfully enabled WETH as collateral.
Transaction Hash: 0xba533b957fa474d3f906b640c6413baeecf0e9a8d30db47c5ce1a8bd68b0d729
Total collateral remains at 0 ETH (0 Wei)
Health Factor unchanged at 3.76
```

---

These structured examples illustrate clear, interactive scenarios demonstrating the capabilities of the Aave V3 Action Provider integrated with AgentKit.
