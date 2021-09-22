from typing import Any, Dict

from eth_typing import ChecksumAddress
from web3 import Web3


def ma(address: str) -> ChecksumAddress:
    """ Make Address. A wrapper for this long name function """
    return Web3.toChecksumAddress(address.lower())


def iter_obj(obj: Any, no_underscores=True, show_types=False) -> Dict[str, Any]:
    args = obj.__dir__()
    if no_underscores:
        args = [x for x in args if not x.startswith('_')]
    out = {}
    for arg in args:
        value = obj.__getattribute__(arg)
        if show_types:
            value = (type(value), value)
        out[arg] = value

    return out
