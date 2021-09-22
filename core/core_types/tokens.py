import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract

from core.constants import ABI
from core.misc import ma
from core.printers import cprint, PrintColor


@dataclass
class ERC20Token:
    address: Union[ChecksumAddress, str]
    symbol: str = None
    _decimals: int = None
    contract: Contract = None

    def __post_init__(self):
        self.address = ma(self.address)

    def __repr__(self):
        return f'<ERC20Token {self.symbol or self.address[:6]}>'

    @property
    def decimals(self) -> int:
        try:
            assert self._decimals is not None, f'Decimals is not initialized for {self}'
        except AssertionError:
            self._init_decimals()
            cprint(PrintColor.PINK, f'Decimals initiated for {self}')
        return self._decimals

    def _init_decimals(self):
        assert self.contract is not None, f'Contract is not initialized for {self}. Please use .init_contract(w3: Web3)'
        self._decimals = self.contract.functions.decimals().call()

    def init_contract(self, w3: Web3):
        self.contract = w3.eth.contract(address=ma(self.address), abi=ABI.ERC_20)

    def to_wei(self, amount: Union[Decimal, int]) -> int:
        """ Transforms human-readable amount to wei """
        return int((10 ** self.decimals) * amount)

    def from_wei(self, wei_amount: int):
        return Decimal(wei_amount) / (10 ** self.decimals)


class PlsDontUseItNeedsRefactoringERC20Token:
    is_test_token: bool = False
    _contract: Contract = None
    _name: str = None
    _symbol: str = None
    _decimals: Decimal = Decimal(-1)
    _total_supply: Decimal = Decimal(-1)

    def __init__(self, address_raw: str, initiate: list = None):
        """ initiate — list of functions that needs to be initiated"""
        self.address = ma(address_raw.lower())
        # self.contract(): Contract = w3.eth.contract(address=self.address, abi=ABI.ERC_20)
        if re.match(r'.*test.*', self.name(), re.IGNORECASE):
            self.is_test_token = True
            return
        if not initiate:
            return
        for key in initiate:
            self.__getattribute__(key)()

    def contract(self):
        if not self._contract:
            raise ValueError(f'Contract is not loaded for {self}')

    def name(self):
        if not self._name:
            self._name = self.contract().functions.name().call()
        return self._name

    def symbol(self):
        if not self._symbol:
            self._symbol = self.contract().functions.symbol().call()
        return self._symbol

    def decimals(self):
        if self._decimals == -1:
            self._decimals = Decimal(self.contract().functions.decimals().call())
        return self._decimals

    def holders(self):
        return Decimal(self.contract().functions.decimals().call())

    def total_supply(self):
        if self._total_supply <= 0:
            self._total_supply = Decimal(self.contract().functions.totalSupply().call())
        return self._total_supply

    def __repr__(self):
        return self.symbol()

    def calc_amount(self, amount: Union[Decimal, int]) -> Decimal:
        """ Transforms token amount to human-readable form """
        return amount / (10 ** self.decimals())

    def make_table(self, amount):
        return [self.name(), f'{round(self.calc_amount(amount), 4)} {self.symbol()}', self.address]

    # def find_holders(self, network: Type[Network]) -> int:
    #     return 0
    #     common_tokens = [PolygonTokens.USDC, PolygonTokens.WETH, PolygonTokens.DAI,
    #                      PolygonTokens.QUICK, PolygonTokens.USDT]
    #     if self.address.lower() in [x.lower() for x in common_tokens] or self.name == self.broken_field:
    #         return
    #
    #     html = r.get(url=network.get_token_url(self.address)).text
    #     soup = BeautifulSoup(html, parser='lxml', features='lxml')
    #     holders = soup.find('div', {'id': 'ContentPlaceHolder1_tr_tokenHolders'}).text.strip().split()
    #     self.holders = int(holders[1].replace(',', ''))
