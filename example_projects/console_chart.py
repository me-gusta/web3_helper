import datetime
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple, Union

from core.blockchain.connections import connect_to_blockchain
from core.core_types.dex import load_dex, Dex
from core.core_types.network import load_network, Network
from core.core_types.tokens import ERC20Token
from core.core_types.wallet import Wallet, load_wallet
from core.printers import printable_float, PrintColor, cprint


@dataclass
class ConsoleChartConfig:
    network: Network
    dex: Dex
    token0: ERC20Token
    token1: ERC20Token
    delay: Union[int, float]
    wallet: Wallet = None


def get_relative_prices(dex: Dex,
                        token0: ERC20Token,
                        token1: ERC20Token) -> Tuple[Decimal, Decimal]:
    """Returns x, y.
        x: X token1 per 1 token0
        y: Y token0 per 1 token1"""
    token0_price = dex.router.functions.getAmountsOut(
        token0.to_wei(1),
        [token0.address, token1.address]).call()
    token1_price = dex.router.functions.getAmountsOut(
        token1.to_wei(1),
        [token1.address, token0.address]).call()
    return token1.from_wei(token0_price[1]), token0.from_wei(token1_price[1])


def calc_percentage(previous: Tuple[Decimal, Decimal], current: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    try:
        percent0 = 100 - ((100 * current[0]) / previous[0])
        percent1 = 100 - ((100 * current[1]) / previous[1])
    except ZeroDivisionError:
        return Decimal(0), Decimal(0)
    return percent0, percent1


def print_token_info(token0: ERC20Token,
                     token1: ERC20Token,
                     price: Decimal,
                     percent: Decimal):
    if percent > 0:
        color = PrintColor.RED
        prefix = "-"
    elif percent < 0:
        color = PrintColor.GREEN
        percent = abs(percent)
        prefix = "+"
    else:
        color = PrintColor.ENDC
        prefix = ""

    cprint(color, f'{printable_float(price)} {token1.symbol} = 1 {token0.symbol} {prefix}{printable_float(percent)}')


def print_wallet_tokens(token0: ERC20Token,
                        token1: ERC20Token,
                        price0: Decimal,
                        price1: Decimal,
                        wallet: Wallet):
    # NOTE: This function is inaccurate since it doesn't take into account slippage.
    # Use only for reference.
    # For precise price calculation use getAmountsOut
    balance0 = token0.from_wei(
        token0.contract.functions.balanceOf(wallet.address).call()
    )
    balance1 = token0.from_wei(
        token1.contract.functions.balanceOf(wallet.address).call()
    )
    cprint(PrintColor.PINK, f'    {balance0} {token0.symbol} = {balance0 * price0} {token1.symbol}')
    cprint(PrintColor.PINK, f'    {balance1} {token1.symbol} = {balance1 * price1} {token0.symbol}')


def console_chart(config: ConsoleChartConfig):
    w3 = connect_to_blockchain(config.network)

    config.dex.init_router(w3)
    prev_prices = (Decimal(0), Decimal(0))
    config.token0.init_contract(w3)
    config.token1.init_contract(w3)
    while True:
        prices = get_relative_prices(config.dex, config.token0, config.token1)
        if prices == prev_prices:
            continue

        percentage = calc_percentage(prev_prices, prices)
        print(datetime.datetime.now().strftime('%H:%M:%S'))
        print_token_info(config.token0, config.token1, prices[0], percentage[0])
        print_token_info(config.token1, config.token0, prices[1], percentage[1])
        if config.wallet:
            print_wallet_tokens(config.token0, config.token1,
                                prices[0], prices[1],
                                config.wallet)
        print()
        prev_prices = prices
        time.sleep(config.delay)


if __name__ == '__main__':
    avax_network = load_network('avax')
    avax_config = ConsoleChartConfig(dex=load_dex('avax.pangolin'),
                                     network=avax_network,
                                     token0=avax_network.get_token_by_symbol('USDC'),
                                     token1=ERC20Token('????????????????????'),
                                     delay=5,
                                     wallet=load_wallet('main'))
    console_chart(avax_config)
