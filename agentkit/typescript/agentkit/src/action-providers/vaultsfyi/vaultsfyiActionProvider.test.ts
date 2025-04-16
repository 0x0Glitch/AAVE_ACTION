import { VaultsfyiActionProvider } from "./vaultsfyiActionProvider";
import { Network } from "../../network";
import { EvmWalletProvider } from "../../wallet-providers";
import { VAULTSFYI_SUPPORTED_CHAINS } from "./constants";

const mockFetchResult = (status: number, data: object) => {
  return {
    json: async () => data,
    status,
    ok: status >= 200 && status < 300,
  };
};

const mockVault = (num: number) => ({
  apiResult: {
    address: `0x${num.toString(16).padStart(40, "0")}`,
    network: `network-${num}`,
    name: `vault-${num}`,
    protocol: `protocol-${num}`,
    token: {
      name: `token-${num}`,
      assetAddress: `0x${num.toString(16).padStart(40, "0")}`,
      symbol: `T${num}`,
      decimals: 18,
    },
    tvlDetails: {
      tvlUsd: num.toString(),
    },
    apy: {
      base: {
        "7day": num * 100,
      },
      rewards: {
        "7day": num * 100,
      },
      total: {
        "7day": num * 100,
      },
    },
    isTransactional: true,
  },
  transformedResult: {
    name: `vault-${num}`,
    address: `0x${num.toString(16).padStart(40, "0")}`,
    network: `network-${num}`,
    protocol: `protocol-${num}`,
    tvlInUsd: num,
    token: {
      name: `token-${num}`,
      address: `0x${num.toString(16).padStart(40, "0")}`,
      symbol: `T${num}`,
    },
    apy: {
      base: num,
      rewards: num,
      total: num,
    },
    link: `https://app.vaults.fyi/opportunity/network-${num}/0x${num.toString(16).padStart(40, "0")}`,
  },
});

const MOCK_TX_HASH = "0xmock-hash";

describe("VaultsfyiActionProvider", () => {
  const provider = new VaultsfyiActionProvider({ apiKey: "test-api-key" });
  let mockWalletProvider: jest.Mocked<EvmWalletProvider>;
  let mockedFetch: jest.Mock;
  const originalFetch = global.fetch;

  beforeAll(() => {
    global.fetch = mockedFetch = jest.fn();
  });

  afterAll(() => {
    global.fetch = originalFetch;
  });

  beforeEach(() => {
    mockWalletProvider = {
      getAddress: jest.fn(),
      getBalance: jest.fn(),
      getName: jest.fn(),
      getNetwork: jest.fn().mockReturnValue({
        protocolFamily: "evm",
        networkId: "test-network",
      }),
      nativeTransfer: jest.fn(),
      readContract: jest.fn(() => Promise.resolve(18)), // token decimals
      sendTransaction: jest.fn(() => Promise.resolve(MOCK_TX_HASH)),
      waitForTransactionReceipt: jest.fn(),
    } as unknown as jest.Mocked<EvmWalletProvider>;
  });

  describe("network support", () => {
    it("should support all vaultsfyi networks", () => {
      Object.keys(VAULTSFYI_SUPPORTED_CHAINS).forEach(network => {
        expect(
          provider.supportsNetwork({
            protocolFamily: "evm",
            chainId: network,
          }),
        ).toBe(true);
      });
    });

    it("should not support other protocol families", () => {
      expect(
        provider.supportsNetwork({
          protocolFamily: "evm",
          chainId: "some-other-chain",
        }),
      ).toBe(false);
    });

    it("should handle invalid network objects", () => {
      expect(provider.supportsNetwork({} as Network)).toBe(false);
    });
  });

  describe("vaults action", () => {
    it("should return a transformed vault", async () => {
      const mockedVault = mockVault(1);
      mockedFetch.mockResolvedValue(mockFetchResult(200, { data: [mockedVault.apiResult] }));
      const args = {};
      const result = await provider.vaults(mockWalletProvider, args);
      expect(JSON.parse(result)).toStrictEqual({
        totalResults: 1,
        nextPage: false,
        results: [mockedVault.transformedResult],
      });
    });

    it("should filter by protocol", async () => {
      const mockedVaults = [mockVault(1), mockVault(2)];
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, { data: mockedVaults.map(v => v.apiResult) }),
      );
      const args = { protocol: "protocol-1" };
      const result = await provider.vaults(mockWalletProvider, args);
      expect(JSON.parse(result)).toStrictEqual({
        totalResults: 1,
        nextPage: false,
        results: [mockedVaults[0].transformedResult],
      });
    });

    it("should take a limit", async () => {
      const mockedVaults = [mockVault(1), mockVault(2)];
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, { data: mockedVaults.map(v => v.apiResult) }),
      );
      const args = { take: 1 };
      const result = await provider.vaults(mockWalletProvider, args);
      expect(JSON.parse(result)).toStrictEqual({
        totalResults: 2,
        nextPage: true,
        results: [mockedVaults[0].transformedResult],
      });
    });

    describe("sorting", () => {
      it("should sort by TVL", async () => {
        const mockedVaults = [mockVault(2), mockVault(1)];
        mockedFetch.mockResolvedValue(
          mockFetchResult(200, { data: mockedVaults.map(v => v.apiResult) }),
        );
        const args = { sort: { field: "tvl", direction: "asc" } } as const;
        const result = await provider.vaults(mockWalletProvider, args);
        expect(JSON.parse(result)).toStrictEqual({
          totalResults: 2,
          nextPage: false,
          results: [mockedVaults[1].transformedResult, mockedVaults[0].transformedResult],
        });
      });

      it("should sort by APY", async () => {
        const mockedVaults = [mockVault(2), mockVault(1)];
        mockedFetch.mockResolvedValue(
          mockFetchResult(200, { data: mockedVaults.map(v => v.apiResult) }),
        );
        const args = { sort: { field: "apy", direction: "asc" } } as const;
        const result = await provider.vaults(mockWalletProvider, args);
        expect(JSON.parse(result)).toStrictEqual({
          totalResults: 2,
          nextPage: false,
          results: [mockedVaults[1].transformedResult, mockedVaults[0].transformedResult],
        });
      });

      it("should sort by name by default", async () => {
        const mockedVaults = [mockVault(2), mockVault(1)];
        mockedFetch.mockResolvedValue(
          mockFetchResult(200, { data: mockedVaults.map(v => v.apiResult) }),
        );
        const args = {};
        const result = await provider.vaults(mockWalletProvider, args);
        expect(JSON.parse(result)).toStrictEqual({
          totalResults: 2,
          nextPage: false,
          results: [mockedVaults[1].transformedResult, mockedVaults[0].transformedResult],
        });
      });
    });

    it("should return an error if the API request fails", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(500, { error: "Internal Server Error", message: "some more info" }),
      );
      const args = {};
      expect(await provider.vaults(mockWalletProvider, args)).toBe(
        "Failed to fetch vaults: Internal Server Error, some more info",
      );
    });
  });

  describe("deposit action", () => {
    it("should execute deposit", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, {
          currentActionIndex: 0,
          actions: [
            {
              tx: {
                to: "0x123",
                data: "0x456",
                value: "1",
                chainId: 1,
              },
              description: "Deposit to vault",
            },
          ],
        }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      const response = await provider.deposit(mockWalletProvider, args);
      expect(response).toBe("Deposit successful");
      expect(mockWalletProvider.sendTransaction).toHaveBeenCalledWith({
        to: "0x123",
        data: "0x456",
        value: 1n,
        chainId: 1,
      });
      expect(mockWalletProvider.waitForTransactionReceipt).toHaveBeenCalledWith(MOCK_TX_HASH);
    });

    it("should execute multiple transactions", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, {
          currentActionIndex: 0,
          actions: [
            {
              tx: {
                to: "0x123",
                data: "0x456",
                value: "1",
                chainId: 1,
              },
              description: "Deposit to vault",
            },
            {
              tx: {
                to: "0x789",
                data: "0xabc",
                value: "2",
                chainId: 1,
              },
              description: "Deposit to vault",
            },
          ],
        }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      const response = await provider.deposit(mockWalletProvider, args);
      expect(response).toBe("Deposit successful");
      expect(mockWalletProvider.sendTransaction).toHaveBeenCalledWith({
        to: "0x123",
        data: "0x456",
        value: 1n,
        chainId: 1,
      });
      expect(mockWalletProvider.sendTransaction).toHaveBeenCalledWith({
        to: "0x789",
        data: "0xabc",
        value: 2n,
        chainId: 1,
      });
      expect(mockWalletProvider.waitForTransactionReceipt).toHaveBeenCalledWith(MOCK_TX_HASH);
    });

    it("should return an error if the API request fails", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(500, { error: "Internal Server Error", message: "some more info" }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      expect(await provider.deposit(mockWalletProvider, args)).toBe(
        "Failed to fetch deposit transactions: Internal Server Error, some more info",
      );
    });
  });

  describe("redeem action", () => {
    it("should execute redeem", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, {
          currentActionIndex: 0,
          actions: [
            {
              tx: {
                to: "0x123",
                data: "0x456",
                value: "1",
                chainId: 1,
              },
              description: "Redeem from vault",
            },
          ],
        }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      const response = await provider.redeem(mockWalletProvider, args);
      expect(response).toBe("Redeem successful");
      expect(mockWalletProvider.sendTransaction).toHaveBeenCalledWith({
        to: "0x123",
        data: "0x456",
        value: 1n,
        chainId: 1,
      });
      expect(mockWalletProvider.waitForTransactionReceipt).toHaveBeenCalledWith(MOCK_TX_HASH);
    });

    it("should return an error if the API request fails", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(500, { error: "Internal Server Error", message: "some more info" }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      expect(await provider.redeem(mockWalletProvider, args)).toBe(
        "Failed to fetch redeem transactions: Internal Server Error, some more info",
      );
    });
  });

  describe("claim rewards action", () => {
    it("should execute claim rewards", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, {
          currentActionIndex: 0,
          actions: [
            {
              tx: {
                to: "0x123",
                data: "0x456",
                value: "1",
                chainId: 1,
              },
              description: "Claim rewards from vault",
            },
          ],
        }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      const response = await provider.claim(mockWalletProvider, args);
      expect(response).toBe("Claim successful");
      expect(mockWalletProvider.sendTransaction).toHaveBeenCalledWith({
        to: "0x123",
        data: "0x456",
        value: 1n,
        chainId: 1,
      });
      expect(mockWalletProvider.waitForTransactionReceipt).toHaveBeenCalledWith(MOCK_TX_HASH);
    });

    it("should return an error if the API request fails", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(500, { error: "Internal Server Error", message: "some more info" }),
      );
      const args = {
        vaultAddress: "0x123",
        assetAddress: "0x456",
        network: "mainnet",
        amount: 1,
      } as const;
      expect(await provider.claim(mockWalletProvider, args)).toBe(
        "Failed to fetch claim transactions: Internal Server Error, some more info",
      );
    });
  });

  describe("wallet balances action", () => {
    it("should strip and transform balances correctly", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, {
          mainnet: [
            {
              address: "0x123",
              name: "token-1",
              symbol: "T1",
              balance: (10 ** 18).toString(),
              decimals: 18,
              somethingElse: "should be stripped",
            },
          ],
        }),
      );
      const response = await provider.balances(mockWalletProvider);
      expect(JSON.parse(response)).toStrictEqual({
        mainnet: [
          {
            address: "0x123",
            name: "token-1",
            symbol: "T1",
            balance: 1,
          },
        ],
      });
    });

    it("should return an error if the API request fails", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(500, { error: "Internal Server Error", message: "some more info" }),
      );
      expect(await provider.balances(mockWalletProvider)).toBe(
        "Failed to fetch wallet balances: Internal Server Error, some more info",
      );
    });
  });

  describe("wallet positions action", () => {
    it("should strip and transform positions correctly", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(200, {
          mainnet: [
            {
              vaultName: "vault-1",
              vaultAddress: "0x123",
              asset: {
                assetAddress: "0x456",
                name: "token-1",
                symbol: "T1",
                decimals: 18,
              },
              balanceNative: (10 ** 18).toString(),
              balanceLp: (10 ** 18).toString(),
              unclaimedUsd: "100",
              apy: {
                base: 100,
                rewards: 100,
                total: 100,
              },
            },
          ],
        }),
      );
      const response = await provider.positions(mockWalletProvider);
      expect(JSON.parse(response)).toStrictEqual({
        mainnet: [
          {
            name: "vault-1",
            vaultAddress: "0x123",
            asset: {
              address: "0x456",
              name: "token-1",
              symbol: "T1",
            },
            underlyingTokenBalance: 1,
            lpTokenBalance: 1,
            unclaimedRewards: true,
            apy: {
              base: 1,
              rewards: 1,
              total: 1,
            },
          },
        ],
      });
    });

    it("should return an error if the API request fails", async () => {
      mockedFetch.mockResolvedValue(
        mockFetchResult(500, { error: "Internal Server Error", message: "some more info" }),
      );
      expect(await provider.positions(mockWalletProvider)).toBe(
        "Failed to fetch positions: Internal Server Error, some more info",
      );
    });
  });
});
