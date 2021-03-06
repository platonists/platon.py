import pytest

from platon import Web3
from platon.exceptions import (
    InvalidAddress,
)
from platon.middleware import (
    construct_fixture_middleware,
    name_to_address_middleware,
)
from platon.providers.base import (
    BaseProvider,
)

NAME = "dump.platon"
ADDRESS = "0x0000000000000000000000000000000000000000"
BALANCE = 0


class TempENS():
    def __init__(self, name_addr_pairs):
        self.registry = dict(name_addr_pairs)

    def address(self, name):
        return self.registry.get(name, None)


@pytest.fixture
def w3():
    w3 = Web3(provider=BaseProvider(), middlewares=[])
    w3.ens = TempENS({NAME: ADDRESS})
    w3.middleware_onion.add(name_to_address_middleware(w3))
    return w3


def test_pass_name_resolver(w3):
    return_chain_on_mainnet = construct_fixture_middleware({
        'net_version': '1',
    })
    return_balance = construct_fixture_middleware({
        'platon_getBalance': BALANCE
    })
    w3.middleware_onion.inject(return_chain_on_mainnet, layer=0)
    w3.middleware_onion.inject(return_balance, layer=0)
    assert w3.platon.get_balance(NAME) == BALANCE


def test_fail_name_resolver(w3):
    return_chain_on_mainnet = construct_fixture_middleware({
        'net_version': '2',
    })
    w3.middleware_onion.inject(return_chain_on_mainnet, layer=0)
    with pytest.raises(InvalidAddress, match=r'.*platon\.platon.*'):
        w3.platon.get_balance("platon.platon")
