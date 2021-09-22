from dataclasses import dataclass
from typing import Union

from eth_typing import ChecksumAddress
from web3.contract import Contract

from core.constants import ABI, FILES_FOLDER
from core.core_types.tokens import ERC20Token
from core.misc import ma
from core.printers import cprint, PrintColor
from core.readers import safe_read_file, safe_load_json


@dataclass
class Dex:
    name: str

    swap_url: str
    factory_address: ChecksumAddress
    router_address: ChecksumAddress

    _factory: Contract = None
    _router: Contract = None

    @property
    def factory(self) -> Contract:
        assert self._factory is not None, 'Factory contract is not initialized'
        return self._factory

    @property
    def router(self) -> Contract:
        assert self._router is not None, 'Router contract is not initialized'
        return self._router

    def init_router(self, w3):
        if self._router:
            return
        self._router = w3.eth.contract(address=self.router_address, abi=ABI.UniswapV2Router02)

    def init_factory(self, w3):
        if self._factory:
            return
        self._factory = w3.eth.contract(address=self.factory_address, abi=ABI.UniswapV2Factory)

    def __repr__(self):
        return f'<{self.name.capitalize()} dex>'

    def make_swap_url(self, token: Union[ERC20Token, str]):
        address = get_token_address(token)
        return self.swap_url + address.lower()


def get_token_address(token: Union[ERC20Token, str]) -> str:
    if isinstance(token, ERC20Token):
        return token.address
    elif isinstance(token, str):
        return ma(token)
    raise ValueError(f'Unknown type {type(token)} for token {token}')


def load_dex(name: str) -> Dex:
    filename = 'dexes.json'
    raw = safe_read_file(FILES_FOLDER / filename)
    all_dexes = safe_load_json(raw, name=str, router_address=str, factory_address=str, swap_url=str)
    for obj in all_dexes:
        if obj['name'] == name:
            dex = Dex(obj['name'],
                      obj['swap_url'],
                      ma(obj['factory_address']),
                      ma(obj['router_address']))
            cprint(PrintColor.CYAN, f'Loaded {dex}')
            return dex
    raise ValueError(f'Dex with name `{name}` is not found. Check {filename}')
