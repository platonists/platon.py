import pytest

from platonpm.backends.http import (
    is_valid_api_github_uri,
)
from platonpm.backends.registry import (
    parse_registry_uri,
)
from platonpm.exceptions import (
    PlatonPMValidationError,
)
from platonpm.uri import (
    create_content_addressed_github_uri,
    is_valid_content_addressed_github_uri,
)


@pytest.mark.parametrize(
    "uri,expected",
    (
        ({}, False),
        (123, False),
        ("xxx", False),
        # invalid scheme
        ("api.github.com/repos/contents/path", False),
        ("http://api.github.com/repos/contents/path", False),
        # invalid authority
        ("http://raw.githubusercontent.com/repos/contents/path", False),
        ("https://github.com/repos/contents/path", False),
        # invalid path
        ("https://api.github.com", False),
        ("https://api.github.com/", False),
        ("https://api.github.com/contents/", False),
        ("https://api.github.com/repos/", False),
        # valid github urls
        ("https://api.github.com/repos/contents/path", True),
        (
            "https://api.github.com/repos/platonpm/platonpm-spec/contents/examples/owned/contracts/Owned.sol",
            True,
        ),
    ),
)
def test_is_valid_github_uri(uri, expected):
    actual = is_valid_api_github_uri(uri)
    assert actual is expected


@pytest.mark.parametrize(
    "uri,expected",
    (
        (
            "https://api.github.com/repos/platonpm/platonpm-spec/contents/examples/owned/contracts/Owned.sol",
            False,
        ),
        (
            "https://api.github.com/repos/platonpm/py-platonpm/git/blobs/a7232a93f1e9e75d606f6c1da18aa16037e03480",
            True,
        ),
    ),
)
def test_is_valid_content_addressed_github_uri(uri, expected):
    actual = is_valid_content_addressed_github_uri(uri)
    assert actual is expected


def test_create_github_uri():
    api_uri = "https://api.github.com/repos/platonpm/platonpm-spec/contents/examples/owned/1.0.0.json"
    expected_blob_uri = "https://api.github.com/repos/platonpm/platonpm-spec/git/blobs/8f9dc767d4c8b31fec4a08d9c0858d4f37b83180"
    actual_blob_uri = create_content_addressed_github_uri(api_uri)
    assert actual_blob_uri == expected_blob_uri


@pytest.mark.parametrize(
    "uri,expected",
    (
        (
            "erc1319://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", None, None, None, None],
        ),
        (
            "erc1319://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:3",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "3", None, None, None, None],
        ),
        (
            "erc1319://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:5/owned",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "5", "owned", None, None, None],
        ),
        (
            "erc1319://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/owned@1.0.0",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "owned", "1.0.0", None, None],
        ),
        (
            "erc1319://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/wallet@2.8.0/",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", None, None],
        ),
        # platonpm scheme
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/wallet@2.8.0",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", None, None],
        ),
        # w/o chain_id
        (
            "erc1319://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/owned",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "owned", None, None, None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@2.8.0",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", None, None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@8%400",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "8@0", None, None],
        ),
        # escaped chars
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/wallet@8%400",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "8@0", None, None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/wallet@%250",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "%0", None, None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/wallet@8%400/",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "8@0", None, None],
        ),
        # with namespaced manifest contents
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@2.8.0/deployments",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", "deployments", None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@2.8.0/deployments/",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", "deployments", None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@2.8.0/deployments/WalletContract",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", "deployments/WalletContract", None],
        ),
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@2.8.0/deployments/WalletContract/",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "2.8.0", "deployments/WalletContract", None],
        ),
        # unescaped chars & namespaced assets
        (
            "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@20%26/deployments/WalletContract/",
            ["0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729", "1", "wallet", "20&", "deployments/WalletContract", None],
        ),
    ),
)
def test_parse_registry_uri(uri, expected):
    address, chain_id, pkg_name, pkg_version, namespaced_asset, ens = parse_registry_uri(uri)
    assert address == expected[0]
    assert chain_id == expected[1]
    assert pkg_name == expected[2]
    assert pkg_version == expected[3]
    assert namespaced_asset == expected[4]


@pytest.mark.parametrize(
    "uri",
    (
        # invalid scheme
        "ethpx://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/owned@1.0.0",
        "erc1318://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/owned@1.0.0",
        "erc1318://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729:1/owned@1.0.0/",
        # missing package_name
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/@1.0.0",
        # unescaped chars in package_name
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/a!bc@1.0.0",
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/ab@@1.0.0",
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/!bc@1.0.0",
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/!bc@1.0.0/",
        # namespaced asset and missing version
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet/deployments/WalletContract",
        "platonpm://0x6b5DA3cA4286Baa7fBaf64EEEE1834C7d430B729/wallet@/deployments/WalletContract",
    )
)
def test_invalid_registry_uris(uri):
    with pytest.raises(PlatonPMValidationError):
        parse_registry_uri(uri)
