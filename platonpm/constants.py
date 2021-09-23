REGISTRY_URI_SCHEMES = ("erc1319", "platonpm")

PACKAGE_NAME_REGEX = "^[a-zA-Z][-_a-zA-Z0-9]{0,255}$"

DEFAULT_IPFS_BACKEND = "platonpm.backends.ipfs.InfuraIPFSBackend"

IPFS_GATEWAY_PREFIX = "https://ipfs.io/ipfs/"

INFURA_GATEWAY_MULTIADDR = "/dns4/ipfs.platon.io/tcp/5001/https/"

GITHUB_API_AUTHORITY = "api.github.com"

SUPPORTED_CHAIN_IDS = {
    1: "mainnet",
    3: "ropsten",
    4: "rinkeby",
    5: "goerli",
    42: "kovan",
}
