import os
import pytest

from tests.integration.common import (
    MiscWebsocketTest,
)
from tests.utils import (
    get_open_port,
    wait_for_ws,
)
from platon import Web3
from platon._utils.module_testing import (
    NetModuleTest,
    VersionModuleTest,
)

from .common import (
    ParityPlatonModuleTest,
    ParityModuleTest,
    ParityPersonalModuleTest,
    ParitySetModuleTest,
    ParityTraceModuleTest,
    ParityWeb3ModuleTest,
)


@pytest.fixture(scope="module")
def ws_port():
    return get_open_port()


@pytest.fixture(scope="module")
def endpoint_uri(ws_port):
    return 'ws://localhost:{0}'.format(ws_port)


@pytest.fixture(scope="module")
def parity_command_arguments(
    parity_import_blocks_process,
    parity_binary,
    datadir,
    passwordfile,
    author,
    ws_port
):
    return (
        parity_binary,
        '--chain', os.path.join(datadir, 'chain_config.json'),
        '--base-path', datadir,
        '--unlock', author,
        '--password', passwordfile,
        '--ws-port', ws_port,
        '--ws-origins', '*',
        '--ws-apis', 'all',
        '--jsonrpc-experimental',
        '--no-ipc',
        '--no-jsonrpc',
    )


@pytest.fixture(scope="module")
def parity_import_blocks_command(parity_binary, ws_port, datadir, passwordfile):
    return (
        parity_binary,
        'import', os.path.join(datadir, 'blocks_export.rlp'),
        '--chain', os.path.join(datadir, 'chain_config.json'),
        '--base-path', datadir,
        '--password', passwordfile,
        '--ws-port', str(ws_port),
        '--ws-origins', '*',
        '--ws-apis', 'all',
        '--jsonrpc-experimental',
        '--no-ipc',
        '--no-jsonrpc',
        '--tracing', 'on',
    )


@pytest.fixture(scope="module")
def web3(parity_process, endpoint_uri, event_loop):
    event_loop.run_until_complete(wait_for_ws(endpoint_uri, event_loop))
    _web3 = Web3(Web3.WebsocketProvider(endpoint_uri))
    return _web3


class TestParityWeb3ModuleTest(ParityWeb3ModuleTest):
    pass


class TestParityPlatonModuleTest(ParityPlatonModuleTest):
    pass


class TestParityVersionModule(VersionModuleTest):
    pass


class TestParityNetModule(NetModuleTest):
    pass


class TestParityPersonalModuleTest(ParityPersonalModuleTest):
    pass


class TestParityTraceModuleTest(ParityTraceModuleTest):
    pass


class TestParityModuleTest(ParityModuleTest):
    pass


class TestParitySetModuleTest(ParitySetModuleTest):
    pass


class TestMiscWebsocketTest(MiscWebsocketTest):
    pass
