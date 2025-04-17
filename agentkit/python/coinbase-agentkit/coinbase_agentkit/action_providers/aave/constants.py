"""Constants for Aave action provider."""

SUPPORTED_NETWORKS = ["base-mainnet", "base-sepolia"]

ASSET_ADDRESSES = {
    "base-mainnet": {
        "weth": "0x4200000000000000000000000000000000000006",
        "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "cbeth": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
        "wsteth": "0xc1CBa3fCea344f92D9239c08C0568f6F2F0ee452",
    },
    "base-sepolia": {
        "weth": "0x4200000000000000000000000000000000000006",
        "usdc": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    },
}

POOL_ADDRESSES = {
    "base-mainnet": "0xa238dd80c259a72e81d7e4664a9801593f98d1c5",
    "base-sepolia": "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
}

# Pool Addresses Provider - used to get addresses of other Aave contracts
POOL_ADDRESSES_PROVIDER = {
    "base-mainnet": "0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D",
    "base-sepolia": "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951",
}

# Addresses for UI Pool Data Provider - used for getting portfolio information
UI_POOL_DATA_PROVIDER_ADDRESSES = {
    "base-mainnet": "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5",
    "base-sepolia": "0xF8AEBE0f34E563E56C6F5f3bF44D31f2576a2Dfa",  # not sure about this
}

# ABI for Aave V3 Pool contract - essential functions
POOL_ABI = [
    # supply function
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "address", "name": "onBehalfOf", "type": "address"},
            {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
        ],
        "name": "supply",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # withdraw function
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "address", "name": "to", "type": "address"},
        ],
        "name": "withdraw",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # borrow function
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "interestRateMode", "type": "uint256"},
            {"internalType": "uint16", "name": "referralCode", "type": "uint16"},
            {"internalType": "address", "name": "onBehalfOf", "type": "address"},
        ],
        "name": "borrow",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # repay function
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "interestRateMode", "type": "uint256"},
            {"internalType": "address", "name": "onBehalfOf", "type": "address"},
        ],
        "name": "repay",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # getUserAccountData function
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {"internalType": "uint256", "name": "totalCollateralBase", "type": "uint256"},
            {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"},
            {"internalType": "uint256", "name": "availableBorrowsBase", "type": "uint256"},
            {"internalType": "uint256", "name": "currentLiquidationThreshold", "type": "uint256"},
            {"internalType": "uint256", "name": "ltv", "type": "uint256"},
            {"internalType": "uint256", "name": "healthFactor", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    # setUserUseReserveAsCollateral function
    {
        "inputs": [
            {"internalType": "address", "name": "asset", "type": "address"},
            {"internalType": "bool", "name": "useAsCollateral", "type": "bool"},
        ],
        "name": "setUserUseReserveAsCollateral",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

# ABI for UI Pool Data Provider
UI_POOL_DATA_PROVIDER_ABI = [
    {
        "inputs": [
            {
                "internalType": "contract IPoolAddressesProvider",
                "name": "provider",
                "type": "address",
            },
            {"internalType": "address", "name": "user", "type": "address"},
        ],
        "name": "getUserReservesData",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "underlyingAsset", "type": "address"},
                    {"internalType": "uint256", "name": "scaledATokenBalance", "type": "uint256"},
                    {
                        "internalType": "bool",
                        "name": "usageAsCollateralEnabledOnUser",
                        "type": "bool",
                    },
                    {"internalType": "uint256", "name": "stableBorrowRate", "type": "uint256"},
                    {"internalType": "uint256", "name": "scaledVariableDebt", "type": "uint256"},
                    {"internalType": "uint256", "name": "principalStableDebt", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "stableBorrowLastUpdateTimestamp",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct IUiPoolDataProviderV3.UserReserveData[]",
                "name": "",
                "type": "tuple[]",
            },
            {"internalType": "uint8", "name": "", "type": "uint8"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "contract IPoolAddressesProvider",
                "name": "provider",
                "type": "address",
            }
        ],
        "name": "getReservesData",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "underlyingAsset", "type": "address"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                    {"internalType": "uint256", "name": "decimals", "type": "uint256"},
                    {"internalType": "uint256", "name": "baseLTVasCollateral", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "reserveLiquidationThreshold",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "reserveLiquidationBonus",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "reserveFactor", "type": "uint256"},
                    {"internalType": "bool", "name": "usageAsCollateralEnabled", "type": "bool"},
                    {"internalType": "bool", "name": "borrowingEnabled", "type": "bool"},
                    {"internalType": "bool", "name": "stableBorrowRateEnabled", "type": "bool"},
                    {"internalType": "bool", "name": "isActive", "type": "bool"},
                    {"internalType": "bool", "name": "isFrozen", "type": "bool"},
                    {"internalType": "bool", "name": "isPaused", "type": "bool"},
                    {"internalType": "uint128", "name": "liquidityIndex", "type": "uint128"},
                    {"internalType": "uint128", "name": "variableBorrowIndex", "type": "uint128"},
                    {"internalType": "uint128", "name": "liquidityRate", "type": "uint128"},
                    {"internalType": "uint128", "name": "variableBorrowRate", "type": "uint128"},
                    {"internalType": "uint128", "name": "stableBorrowRate", "type": "uint128"},
                    {"internalType": "uint40", "name": "lastUpdateTimestamp", "type": "uint40"},
                    {"internalType": "address", "name": "aTokenAddress", "type": "address"},
                    {
                        "internalType": "address",
                        "name": "stableDebtTokenAddress",
                        "type": "address",
                    },
                    {
                        "internalType": "address",
                        "name": "variableDebtTokenAddress",
                        "type": "address",
                    },
                    {
                        "internalType": "address",
                        "name": "interestRateStrategyAddress",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "availableLiquidity", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "totalPrincipalStableDebt",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "averageStableRate", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "stableDebtLastUpdateTimestamp",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "totalScaledVariableDebt",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "priceInMarketReferenceCurrency",
                        "type": "uint256",
                    },
                    {"internalType": "address", "name": "priceOracle", "type": "address"},
                    {"internalType": "uint256", "name": "variableRateSlope1", "type": "uint256"},
                    {"internalType": "uint256", "name": "variableRateSlope2", "type": "uint256"},
                    {"internalType": "uint256", "name": "stableRateSlope1", "type": "uint256"},
                    {"internalType": "uint256", "name": "stableRateSlope2", "type": "uint256"},
                    {"internalType": "uint8", "name": "baseStableBorrowRate", "type": "uint8"},
                    {"internalType": "uint8", "name": "baseVariableBorrowRate", "type": "uint8"},
                    {"internalType": "uint8", "name": "optimalUsageRatio", "type": "uint8"},
                    {"internalType": "bool", "name": "isPaused", "type": "bool"},
                ],
                "internalType": "struct IUiPoolDataProviderV3.AggregatedReserveData[]",
                "name": "",
                "type": "tuple[]",
            },
            {"internalType": "uint8", "name": "", "type": "uint8"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# ABI for Pool Addresses Provider
POOL_ADDRESSES_PROVIDER_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "id", "type": "bytes32"}],
        "name": "getAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# Price feed ABI for getting asset prices from Chainlink oracles
PRICE_FEED_ABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"internalType": "uint80", "name": "roundId", "type": "uint80"},
            {"internalType": "int256", "name": "answer", "type": "int256"},
            {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
            {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

# Aave Price Oracle addresses
PRICE_ORACLE_ADDRESSES = {
    "base-mainnet": "0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156",
    "base-sepolia": "0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156",  # Same as mainnet for now, update if different
}

# Aave Price Oracle ABI
PRICE_ORACLE_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
        "name": "getAssetPrice",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address[]", "name": "assets", "type": "address[]"}],
        "name": "getAssetsPrices",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "BASE_CURRENCY",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "BASE_CURRENCY_UNIT",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# ABI for Aave Data Provider, used to get reserve configuration and user data
AAVE_DATA_PROVIDER_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
        "name": "getReserveConfigurationData",
        "outputs": [
            {"internalType": "uint256", "name": "decimals", "type": "uint256"},
            {"internalType": "uint256", "name": "ltv", "type": "uint256"},
            {"internalType": "uint256", "name": "liquidationThreshold", "type": "uint256"},
            {"internalType": "uint256", "name": "liquidationBonus", "type": "uint256"},
            {"internalType": "uint256", "name": "reserveFactor", "type": "uint256"},
            {"internalType": "bool", "name": "usageAsCollateralEnabled", "type": "bool"},
            {"internalType": "bool", "name": "borrowingEnabled", "type": "bool"},
            {"internalType": "bool", "name": "stableBorrowRateEnabled", "type": "bool"},
            {"internalType": "bool", "name": "isActive", "type": "bool"},
            {"internalType": "bool", "name": "isFrozen", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
        "name": "getReserveData",
        "outputs": [
            {"internalType": "uint256", "name": "availableLiquidity", "type": "uint256"},
            {"internalType": "uint256", "name": "totalStableDebt", "type": "uint256"},
            {"internalType": "uint256", "name": "totalVariableDebt", "type": "uint256"},
            {"internalType": "uint256", "name": "liquidityRate", "type": "uint256"},
            {"internalType": "uint256", "name": "variableBorrowRate", "type": "uint256"},
            {"internalType": "uint256", "name": "stableBorrowRate", "type": "uint256"},
            {"internalType": "uint256", "name": "averageStableBorrowRate", "type": "uint256"},
            {"internalType": "uint256", "name": "liquidityIndex", "type": "uint256"},
            {"internalType": "uint256", "name": "variableBorrowIndex", "type": "uint256"},
            {"internalType": "uint40", "name": "lastUpdateTimestamp", "type": "uint40"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# Addresses for Aave Data Provider
DATA_PROVIDER_ADDRESSES = {
    "base-mainnet": "0xC4Fcf9893072d61Cc2899C0054877Cb752587981",  # Base mainnet data provider
    "base-sepolia": "0x9445F13Be4F7Af90B42c8936B69ba604CB240F34",  # Base Sepolia data provider (placeholder)
}
