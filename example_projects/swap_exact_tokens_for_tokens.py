from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from web3 import Web3

from core.blockchain.connections import connect_to_blockchain, send_transaction
from core.core_types.dex import load_dex, Dex
from core.core_types.network import load_network, Network
from core.core_types.tokens import ERC20Token
from core.core_types.wallet import load_wallet, Wallet
from core.printers import cprint, PrintColor


@dataclass
class SwapConfig:
    wallet: Wallet
    dex: Dex
    network: Network
    amount: Union[int, float]
    gas_price_gwei: Union[int, float]

    token_to_sell: ERC20Token
    token_to_buy: ERC20Token


def swap_exact_tokens_for_tokens(config: SwapConfig):
    w3 = connect_to_blockchain(config.network)
    config.dex.init_router(w3)

    swap_tx = config.dex.router.functions.swapExactTokensForTokens(
        config.token_to_sell.to_wei(config.amount),
        1,
        [config.token_to_sell.address, config.token_to_buy.address],
        config.wallet.address,
        3249824084
    ).buildTransaction({'gasPrice': Web3.toWei(config.gas_price_gwei, 'gwei'),
                        'gas': 300000,
                        'nonce': w3.eth.get_transaction_count(config.wallet.address)})

    sent_tx = send_transaction(w3, swap_tx, config.wallet.private_key)

    w3.eth.wait_for_transaction_receipt(sent_tx.hash)
    cprint(PrintColor.GREEN, "Got receipt")


if __name__ == '__main__':
    avax_network = load_network('avax')
    _config = SwapConfig(
        wallet=load_wallet('main'),
        dex=load_dex('avax.pangolin'),
        network=avax_network,

        amount=80,
        gas_price_gwei=30,

        token_to_sell=avax_network.get_token_by_symbol('USDC'),
        token_to_buy=ERC20Token('????????????'),
    )
