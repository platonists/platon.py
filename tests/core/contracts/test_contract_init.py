import pytest

from platon._utils.ens import (
    contract_ens_addresses,
    ens_addresses,
)
from platon.exceptions import (
    BadFunctionCallOutput,
    NameNotFound,
)


@pytest.fixture()
def math_addr(MathContract, address_conversion_func):
    web3 = MathContract.web3
    deploy_txn = MathContract.constructor().transact({'from': web3.platon.coinbase})
    deploy_receipt = web3.platon.wait_for_transaction_receipt(deploy_txn)
    assert deploy_receipt is not None
    return address_conversion_func(deploy_receipt['contractAddress'])


def test_contract_with_unset_address(MathContract):
    with contract_ens_addresses(MathContract, []):
        with pytest.raises(NameNotFound):
            MathContract(address='unsetname.platon')


def test_contract_with_name_address(MathContract, math_addr):
    with contract_ens_addresses(MathContract, [('thedao.platon', math_addr)]):
        mc = MathContract(address='thedao.platon')
        caller = mc.web3.platon.coinbase
        assert mc.address == 'thedao.platon'
        assert mc.functions.return13().call({'from': caller}) == 13


def test_contract_with_name_address_from_platon_contract(
    web3,
    MATH_ABI,
    MATH_CODE,
    MATH_RUNTIME,
    math_addr,
):
    with ens_addresses(web3, [('thedao.platon', math_addr)]):
        mc = web3.platon.contract(
            address='thedao.platon',
            abi=MATH_ABI,
            bytecode=MATH_CODE,
            bytecode_runtime=MATH_RUNTIME,
        )

        caller = mc.web3.platon.coinbase
        assert mc.address == 'thedao.platon'
        assert mc.functions.return13().call({'from': caller}) == 13


def test_contract_with_name_address_changing(MathContract, math_addr):
    # Contract address is validated once on creation
    with contract_ens_addresses(MathContract, [('thedao.platon', math_addr)]):
        mc = MathContract(address='thedao.platon')

    caller = mc.web3.platon.coinbase
    assert mc.address == 'thedao.platon'

    # what happens when name returns no address at all
    with contract_ens_addresses(mc, []):
        with pytest.raises(NameNotFound):
            mc.functions.return13().call({'from': caller})

    # what happens when name returns address to different contract
    with contract_ens_addresses(mc, [('thedao.platon', '0x' + '11' * 20)]):
        with pytest.raises(BadFunctionCallOutput):
            mc.functions.return13().call({'from': caller})

    # contract works again when name resolves correctly
    with contract_ens_addresses(mc, [('thedao.platon', math_addr)]):
        assert mc.functions.return13().call({'from': caller}) == 13
