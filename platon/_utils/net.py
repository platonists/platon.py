from typing import (
    Callable,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
    default_root_munger,
)

listening: Method[Callable[[], bool]] = Method(
    RPC.net_listening,
    mungers=[default_root_munger],
)

peer_count: Method[Callable[[], int]] = Method(
    RPC.net_peerCount,
    mungers=[default_root_munger],
)

version: Method[Callable[[], str]] = Method(
    RPC.net_version,
    mungers=[default_root_munger],
)

