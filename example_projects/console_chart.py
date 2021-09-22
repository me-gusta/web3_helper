import datetime
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple, Union

from core.blockchain.connections import connect_to_blockchain
from core.core_types.dex import load_dex, Dex
from core.core_types.network import load_network, Network
from core.core_types.tokens import ERC20Token
from core.printers import printable_float, PrintColor, cprint


@dataclass
class ConsoleChartConfig:
    network: Network
    dex: Dex
    token0: ERC20Token
    token1: ERC20Token
    delay: Union[int, float]


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


def console_chart(config: ConsoleChartConfig):
    w3 = connect_to_blockchain(network)

    config.dex.init_router(w3)
    prev_prices = (Decimal(0), Decimal(0))
    while True:
        prices = get_relative_prices(config.dex, config.token0, config.token1)
        if prices == prev_prices:
            continue

        percentage = calc_percentage(prev_prices, prices)
        print(datetime.datetime.now().strftime('%H:%M:%S'))
        print_token_info(config.token0, config.token1, prices[0], percentage[0])
        print_token_info(config.token1, config.token0, prices[1], percentage[1])
        print()

        prev_prices = prices
        time.sleep(config.delay)


if __name__ == '__main__':
    network = load_network('polygon')
    _config = ConsoleChartConfig(dex=load_dex('quickswap'),
                                 network=load_network('polygon'),
                                 token0=network.get_token_by_symbol('USDC'),
                                 token1=network.get_token_by_symbol('QUICK'),
                                 delay=1)
    console_chart(_config)
