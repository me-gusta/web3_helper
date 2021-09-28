from dataclasses import dataclass
from typing import Union, List

from hexbytes import HexBytes

from core.constants import FILES_FOLDER
from core.core_types.tokens import ERC20Token
from core.misc import ma
from core.printers import cprint, PrintColor
from core.readers import safe_read_file, safe_load_json


@dataclass
class Network:
    name: str
    main_http: str
    main_ws: str
    testnet_http: str

    block_explorer: str
    tokens: List[ERC20Token] = None

    def __repr__(self):
        return f'<{self.name.capitalize()} network>'

    def add_tokens(self, tokens: List[dict]):
        self.tokens = []
        for token_info in tokens:
            self.tokens.append(ERC20Token(
                token_info['address'],
                token_info['symbol'],
                token_info['decimals']
            ))

    def get_token_by_symbol(self, symbol: str) -> ERC20Token:
        for x in self.tokens:
            if x.symbol == symbol:
                return x
        raise ValueError(f'Token with {symbol} not found in {self}')

    def get_token_by_address(self, address: str) -> ERC20Token:
        address = ma(address)
        for x in self.tokens:
            if x.address == address:
                return x
        raise ValueError(f'Token with {address} not found in {self}')

    def get_tx_url(self, tx_hash: Union[str, HexBytes]):
        if isinstance(tx_hash, HexBytes):
            tx_hash = tx_hash.hex()
        return self.block_explorer + f'tx/{tx_hash}'


def load_network(name: str) -> Network:
    filename = 'networks.json'
    raw = safe_read_file(FILES_FOLDER / filename)
    all_networks = safe_load_json(raw, name=str, main_http=str, main_ws=str,
                                  testnet_http=str, block_explorer=str, tokens=list)
    for obj in all_networks:
        if obj['name'] == name:
            network = Network(obj['name'],
                              obj['main_http'],
                              obj['main_ws'],
                              obj['testnet_http'],
                              obj['block_explorer'])
            network.add_tokens(obj['tokens'])
            cprint(PrintColor.CYAN, f'Loaded {network}')
            return network
    raise ValueError(f'Network with name `{name}` is not found. Check {filename}')