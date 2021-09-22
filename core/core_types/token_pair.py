from dataclasses import dataclass

from web3 import Web3
from web3.contract import Contract

from core.constants import ABI
from core.core_types.dex import Dex
from core.core_types.tokens import ERC20Token
from core.printers import cprint, PrintColor


@dataclass
class TokenPair:
    token0: ERC20Token
    token1: ERC20Token
    contract: Contract


def get_token_pair(w3: Web3,
                   token0: ERC20Token,
                   token1: ERC20Token,
                   dex: Dex) -> TokenPair:
    dex.init_factory(w3)
    pair_address = dex.factory.functions.getPair(token0.address, token1.address).call()
    pair = w3.eth.contract(address=pair_address, abi=ABI.UniswapV2Pair)

    cprint(PrintColor.BLUE, f'Got {token0}-{token1} token pair. Address: {pair.address}')
    return TokenPair(token0, token1, pair)


def get_pair_prices(pair: TokenPair):
    reserves = pair.contract.functions.getReserves().call()
    token0_reserves = pair.token0.from_wei(reserves[0])
    token1_reserves = pair.token1.from_wei(reserves[1])
    print(token0_reserves, token1_reserves, token0_reserves / token1_reserves)