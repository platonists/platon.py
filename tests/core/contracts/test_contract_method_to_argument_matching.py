import json
import pytest

from platon._utils.abi import (
    get_abi_input_types,
)
from platon._utils.function_identifiers import (
    FallbackFn,
    ReceiveFn,
)
from platon.exceptions import (
    ValidationError,
)

SINGLE_FN_NO_ARGS = json.loads('[{"constant":false,"inputs":[],"name":"a","outputs":[],"type":"function"}]')
SINGLE_FN_ONE_ARG = json.loads('[{"constant":false,"inputs":[{"name":"","type":"uint256"}],"name":"a","outputs":[],"type":"function"}]')
FALLBACK_FUNCTION = json.loads('[{"constant": false, "inputs": [], "name": "getData", "outputs": [{"name": "r", "type": "uint256"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"payable": false, "stateMutability": "nonpayable", "type": "fallback"}]')
RECEIVE_FUNCTION = json.loads('[{"constant": false, "inputs": [], "name": "getData", "outputs": [{"name": "r", "type": "uint256"}], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"payable": true, "stateMutability": "payable", "type": "receive"}]')
MULTIPLE_FUNCTIONS = json.loads('''
[
  {
    "constant": false,
    "inputs": [],
    "name": "a",
    "outputs": [],
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "name": "a",
    "outputs": [],
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "a",
    "outputs": [],
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "",
        "type": "uint8"
      }
    ],
    "name": "a",
    "outputs": [],
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "",
        "type": "int8"
      }
    ],
    "name": "a",
    "outputs": [],
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "",
        "type": "tuple[]",
        "components": [
          {"name": "", "type": "int256"},
          {"name": "", "type": "bool"}
        ]
      }
    ],
    "name": "a",
    "outputs": [],
    "type": "function"
  }
]
''')


def test_finds_single_function_without_args(web3):
    Contract = web3.platon.contract(abi=SINGLE_FN_NO_ARGS)

    abi = Contract._find_matching_fn_abi('a', [])
    assert abi['name'] == 'a'
    assert abi['inputs'] == []


def test_finds_single_function_with_args(web3):
    Contract = web3.platon.contract(abi=SINGLE_FN_ONE_ARG)

    abi = Contract._find_matching_fn_abi('a', [1234])
    assert abi['name'] == 'a'
    assert len(abi['inputs']) == 1
    assert abi['inputs'][0]['type'] == 'uint256'


def test_finds_fallback_function(web3):
    Contract = web3.platon.contract(abi=FALLBACK_FUNCTION)

    abi = Contract._find_matching_fn_abi(FallbackFn, [])
    assert abi['type'] == 'fallback'


def test_finds_receive_function(web3):
    Contract = web3.platon.contract(abi=RECEIVE_FUNCTION)

    abi = Contract._find_matching_fn_abi(ReceiveFn, [])
    assert abi['type'] == 'receive'


def test_error_when_no_function_name_match(web3):
    Contract = web3.platon.contract(abi=SINGLE_FN_NO_ARGS)

    with pytest.raises(ValidationError):
        Contract._find_matching_fn_abi('no_function_name', [1234])


@pytest.mark.parametrize(
    'arguments,expected_types',
    (
        ([], []),
        ([b'arst'], ['bytes32']),
        (['0xf00b47'], ['bytes32']),
        (['0x'], ['bytes32']),
        ([1234567890], ['uint256']),
        # ([255], ['uint8']),  # TODO: enable
        ([-1], ['int8']),
        ([[(-1, True), (2, False)]], ['(int256,bool)[]']),
    )
)
def test_finds_function_with_matching_args(web3, arguments, expected_types):
    Contract = web3.platon.contract(abi=MULTIPLE_FUNCTIONS)

    abi = Contract._find_matching_fn_abi('a', arguments)
    assert abi['name'] == 'a'
    assert len(abi['inputs']) == len(expected_types)
    assert set(get_abi_input_types(abi)) == set(expected_types)


def test_finds_function_with_matching_args_deprecation_warning(web3):
    Contract = web3.platon.contract(abi=MULTIPLE_FUNCTIONS)

    with pytest.warns(DeprecationWarning):
        abi = Contract._find_matching_fn_abi('a', [''])
        assert abi['name'] == 'a'
        assert len(abi['inputs']) == len(['bytes32'])
        assert set(get_abi_input_types(abi)) == set(['bytes32'])


def test_error_when_duplicate_match(web3):
    Contract = web3.platon.contract(abi=MULTIPLE_FUNCTIONS)

    with pytest.raises(ValidationError):
        Contract._find_matching_fn_abi('a', [100])


@pytest.mark.parametrize('arguments', (['0xf00b47'], [b''], [''], ['00' * 16]))
def test_strict_errors_if_type_is_wrong(w3_strict_abi, arguments):
    Contract = w3_strict_abi.platon.contract(abi=MULTIPLE_FUNCTIONS)

    with pytest.raises(ValidationError):
        Contract._find_matching_fn_abi('a', arguments)


@pytest.mark.parametrize(
    'arguments,expected_types',
    (
        ([], []),
        ([1234567890], ['uint256']),
        ([-1], ['int8']),
        ([[(-1, True), (2, False)]], ['(int256,bool)[]']),
    )
)
def test_strict_finds_function_with_matching_args(w3_strict_abi, arguments, expected_types):
    Contract = w3_strict_abi.platon.contract(abi=MULTIPLE_FUNCTIONS)

    abi = Contract._find_matching_fn_abi('a', arguments)
    assert abi['name'] == 'a'
    assert len(abi['inputs']) == len(expected_types)
    assert set(get_abi_input_types(abi)) == set(expected_types)
