import pytest

from platon.exceptions import (
    BlockNotFound,
    ExtraDataLengthError,
)
from platon.middleware import (
    construct_fixture_middleware,
    gplaton_poa_middleware,
)


# In the spec, a block with extra data longer than 32 bytes is invalid
def test_long_extra_data(web3):
    return_block_with_long_extra_data = construct_fixture_middleware({
        'platon_getBlockByNumber': {'extraData': '0x' + 'ff' * 33},
    })
    web3.middleware_onion.inject(return_block_with_long_extra_data, layer=0)
    with pytest.raises(ExtraDataLengthError):
        web3.platon.get_block('latest')


def test_full_extra_data(web3):
    return_block_with_long_extra_data = construct_fixture_middleware({
        'platon_getBlockByNumber': {'extraData': '0x' + 'ff' * 32},
    })
    web3.middleware_onion.inject(return_block_with_long_extra_data, layer=0)
    block = web3.platon.get_block('latest')
    assert block.extraData == b'\xff' * 32


def test_node_proof_of_authority(web3):
    return_block_with_long_extra_data = construct_fixture_middleware({
        'platon_getBlockByNumber': {'extraData': '0x' + 'ff' * 33},
    })
    web3.middleware_onion.inject(gplaton_poa_middleware, layer=0)
    web3.middleware_onion.inject(return_block_with_long_extra_data, layer=0)
    block = web3.platon.get_block('latest')
    assert 'extraData' not in block
    assert block.proofOfAuthorityData == b'\xff' * 33


def test_returns_none_response(web3):
    return_none_response = construct_fixture_middleware({
        'platon_getBlockByNumber': None,
    })
    web3.middleware_onion.inject(gplaton_poa_middleware, layer=0)
    web3.middleware_onion.inject(return_none_response, layer=0)
    with pytest.raises(BlockNotFound):
        web3.platon.get_block(100000000000)
