import pytest


@pytest.fixture(autouse=True)
def wait_for_first_block(web3, wait_for_block):
    wait_for_block(web3)


def test_uses_default_account_when_set(web3, extra_accounts,
                                       wait_for_transaction):
    web3.platon.default_account = extra_accounts[2]
    assert web3.platon.default_account == extra_accounts[2]

    txn_hash = web3.platon.send_transaction({
        "to": extra_accounts[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.platon.get_transaction(txn_hash)
    assert txn['from'] == extra_accounts[2]


def test_uses_defaultAccount_when_set_with_warning(web3, extra_accounts,
                                                   wait_for_transaction):
    with pytest.warns(DeprecationWarning):
        web3.platon.defaultAccount = extra_accounts[2]

    with pytest.warns(DeprecationWarning):
        assert web3.platon.defaultAccount == extra_accounts[2]

    txn_hash = web3.platon.send_transaction({
        "to": extra_accounts[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.platon.get_transaction(txn_hash)
    assert txn['from'] == extra_accounts[2]


def test_uses_given_from_address_when_provided(web3, extra_accounts,
                                               wait_for_transaction):
    web3.platon.default_account = extra_accounts[2]
    txn_hash = web3.platon.send_transaction({
        "from": extra_accounts[5],
        "to": extra_accounts[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.platon.get_transaction(txn_hash)
    assert txn['from'] == extra_accounts[5]


def test_uses_given_from_address_when_provided_with_warning(web3, extra_accounts,
                                                            wait_for_transaction):
    with pytest.warns(DeprecationWarning):
        web3.platon.defaultAccount = extra_accounts[2]

    with pytest.warns(DeprecationWarning):
        assert web3.platon.defaultAccount == extra_accounts[2]

    txn_hash = web3.platon.send_transaction({
        "from": extra_accounts[5],
        "to": extra_accounts[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.platon.get_transaction(txn_hash)
    assert txn['from'] == extra_accounts[5]
