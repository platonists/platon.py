import pytest

from platon_account import (
    Account,
)
from platon_account.signers.local import (
    LocalAccount,
)
import platon_keys
from platon_tester.exceptions import (
    ValidationError,
)
from platon_utils import (
    to_bytes,
    to_hex,
)
from platon_utils.toolz import (
    identity,
    merge,
    valfilter,
)
from hexbytes import (
    HexBytes,
)

from platon import Web3
from platon.exceptions import (
    InvalidAddress,
)
from platon.middleware import (
    construct_result_generator_middleware,
    construct_sign_and_send_raw_middleware,
)
from platon.middleware.signing import (
    gen_normalized_accounts,
)
from platon.providers import (
    BaseProvider,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)

PRIVATE_KEY_1 = to_bytes(
    hexstr='0x6a8b4de52b288e111c14e1c4b868bc125d325d40331d86d875a3467dd44bf829')

ADDRESS_1 = '0x634743b15C948820069a43f6B361D03EfbBBE5a8'

PRIVATE_KEY_2 = to_bytes(
    hexstr='0xbf963e13b164c2100795f53e5590010f76b7a91b5a78de8e2b97239c8cfca8e8')

ADDRESS_2 = '0x91eD14b5956DBcc1310E65DC4d7E82f02B95BA46'

KEY_FUNCS = (
    platon_keys.keys.PrivateKey,
    Account.from_key,
    HexBytes,
    to_hex,
    identity,
)


SAME_KEY_MIXED_TYPE = tuple(key_func(PRIVATE_KEY_1) for key_func in KEY_FUNCS)

MIXED_KEY_MIXED_TYPE = tuple(
    key_func(key) for key in [PRIVATE_KEY_1, PRIVATE_KEY_2] for key_func in KEY_FUNCS
)

SAME_KEY_SAME_TYPE = (
    platon_keys.keys.PrivateKey(PRIVATE_KEY_1),
    platon_keys.keys.PrivateKey(PRIVATE_KEY_1)
)

MIXED_KEY_SAME_TYPE = (
    platon_keys.keys.PrivateKey(PRIVATE_KEY_1), platon_keys.keys.PrivateKey(PRIVATE_KEY_2)
)


class DummyProvider(BaseProvider):
    def make_request(self, method, params):
        raise NotImplementedError("Cannot make request for {0}:{1}".format(
            method,
            params,
        ))


@pytest.fixture()
def result_generator_middleware():
    return construct_result_generator_middleware({
        'platon_sendRawTransaction': lambda *args: args,
        'net_version': lambda *_: 1,
        'platon_chainId': lambda *_: "0x02",
    })


@pytest.fixture()
def w3_base():
    return Web3(provider=DummyProvider(), middlewares=[])


@pytest.fixture()
def w3_dummy(w3_base, result_generator_middleware):
    w3_base.middleware_onion.add(result_generator_middleware)
    return w3_base


def hex_to_bytes(s):
    return to_bytes(hexstr=s)


@pytest.mark.parametrize(
    'method,key_object,from_,expected',
    (
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE, ADDRESS_2, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE, ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', MIXED_KEY_MIXED_TYPE, ADDRESS_2, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', MIXED_KEY_MIXED_TYPE, ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_SAME_TYPE, ADDRESS_2, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_SAME_TYPE, ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', MIXED_KEY_SAME_TYPE, ADDRESS_2, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', MIXED_KEY_SAME_TYPE, ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[0], ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[1], ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[2], ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[3], ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[4], ADDRESS_1, 'platon_sendRawTransaction'),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[0], ADDRESS_2, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[1], ADDRESS_2, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[2], ADDRESS_2, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[3], ADDRESS_2, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_MIXED_TYPE[4], ADDRESS_2, NotImplementedError),
        ('platon_call', MIXED_KEY_MIXED_TYPE, ADDRESS_1, NotImplementedError),
        ('platon_sendTransaction', SAME_KEY_SAME_TYPE, hex_to_bytes(ADDRESS_1),
         'platon_sendRawTransaction'),
    )
)
def test_sign_and_send_raw_middleware(
        w3_dummy,
        w3,
        method,
        from_,
        expected,
        key_object):
    w3_dummy.middleware_onion.add(
        construct_sign_and_send_raw_middleware(key_object))

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            w3_dummy.manager.request_blocking(
                method,
                [{
                    'to': '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf',
                    'from': from_,
                    'gas': 21000,
                    'gasPrice': 0,
                    'value': 1,
                    'nonce': 0
                }])
    else:
        actual = w3_dummy.manager.request_blocking(
            method,
            [{
                'to': '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf',
                'from': from_,
                'gas': 21000,
                'gasPrice': 0,
                'value': 1,
                'nonce': 0
            }])
        raw_txn = actual[1][0]
        actual_method = actual[0]
        assert actual_method == expected
        assert isinstance(raw_txn, bytes)


@pytest.fixture()
def w3():
    return Web3(PlatonTesterProvider())


@pytest.mark.parametrize(
    'key_object',
    (
        (SAME_KEY_MIXED_TYPE),
        (MIXED_KEY_MIXED_TYPE),
        (SAME_KEY_SAME_TYPE),
        (MIXED_KEY_SAME_TYPE),
        (SAME_KEY_MIXED_TYPE[0]),
        (SAME_KEY_MIXED_TYPE[1]),
        (SAME_KEY_MIXED_TYPE[2]),
        (SAME_KEY_MIXED_TYPE[3]),
        (SAME_KEY_MIXED_TYPE[4]),
    )
)
def test_gen_normalized_accounts(key_object):
    accounts = gen_normalized_accounts(key_object)
    assert all(isinstance(account, LocalAccount) for account in accounts.values())


def test_gen_normalized_accounts_type_error(w3):
    with pytest.raises(TypeError):
        gen_normalized_accounts(1234567890)


@pytest.fixture()
def fund_account(w3):
    # fund local account
    tx_value = w3.toVon(10, 'ether')
    for address in (ADDRESS_1, ADDRESS_2):
        w3.platon.send_transaction({
            'to': address,
            'from': w3.platon.accounts[0],
            'gas': 21000,
            'value': tx_value})
        assert w3.platon.get_balance(address) == tx_value


@pytest.mark.parametrize(
    'transaction,expected,key_object,from_',
    (
        (
            #  Transaction with set gas
            {
                'gas': 21000,
                'gasPrice': 0,
                'value': 1
            },
            -1,
            MIXED_KEY_MIXED_TYPE,
            ADDRESS_1,
        ),
        (
            #  Transaction with no set gas
            {
                'value': 1
            },
            -1,
            MIXED_KEY_MIXED_TYPE,
            ADDRESS_1,
        ),
        (
            # Transaction with mismatched sender
            # expect a validation error with send_transaction + unmanaged account
            {
                'gas': 21000,
                'value': 10
            },
            ValidationError,
            SAME_KEY_MIXED_TYPE,
            ADDRESS_2,
        ),
        (
            #  Transaction with invalid sender
            {
                'gas': 21000,
                'value': 10
            },
            InvalidAddress,
            SAME_KEY_MIXED_TYPE,
            '0x0000',
        )
    )
)
def test_signed_transaction(
        w3,
        fund_account,
        transaction,
        expected,
        key_object,
        from_):
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(key_object))

    # Drop any falsy addresses
    to_from = valfilter(bool, {'to': w3.platon.accounts[0], 'from': from_})

    _transaction = merge(transaction, to_from)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            start_balance = w3.platon.get_balance(_transaction.get('from', w3.platon.accounts[0]))
            w3.platon.send_transaction(_transaction)
    else:
        start_balance = w3.platon.get_balance(_transaction.get('from', w3.platon.accounts[0]))
        w3.platon.send_transaction(_transaction)
        assert w3.platon.get_balance(_transaction.get('from')) <= start_balance + expected


@pytest.mark.parametrize(
    'from_converter,to_converter',
    (
        (identity, identity),
        (hex_to_bytes, identity),
        (identity, hex_to_bytes),
        (hex_to_bytes, hex_to_bytes),
    )
)
def test_sign_and_send_raw_middleware_with_byte_addresses(
        w3_dummy,
        from_converter,
        to_converter):
    private_key = PRIVATE_KEY_1
    from_ = from_converter(ADDRESS_1)
    to_ = to_converter(ADDRESS_2)

    w3_dummy.middleware_onion.add(
        construct_sign_and_send_raw_middleware(private_key))

    actual = w3_dummy.manager.request_blocking(
        'platon_sendTransaction',
        [{
            'to': to_,
            'from': from_,
            'gas': 21000,
            'gasPrice': 0,
            'value': 1,
            'nonce': 0
        }])
    raw_txn = actual[1][0]
    actual_method = actual[0]
    assert actual_method == 'platon_sendRawTransaction'
    assert isinstance(raw_txn, bytes)
