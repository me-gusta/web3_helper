from decimal import Decimal

from web3 import Web3

from core.blockchain.connections import connect_to_blockchain, send_transaction
from core.core_types.dex import load_dex
from core.core_types.network import load_network
from core.core_types.tokens import ERC20Token
from core.core_types.wallet import load_wallet
from core.printers import cprint, PrintColor

# Config
wallet = load_wallet('main')
dex = load_dex('avax_traderjoe')
network = load_network('avax')
amount = Decimal(0.83)
gas_price_gwei = 100

token_to_sell = network.get_token_by_symbol('WETH')
token_to_buy = ERC20Token('0x????????????????????????')

# Function
w3 = connect_to_blockchain(network)
dex.init_router(w3)


swap_tx = dex.router.functions.swapExactTokensForTokens(
        token_to_sell.to_wei(amount),
        1,
        [token_to_sell.address, token_to_buy.address],
        wallet.address,
        3249824084
    ).buildTransaction({'gasPrice': Web3.toWei(gas_price_gwei, 'gwei'),
                        'gas': 300000,
                        'nonce': w3.eth.get_transaction_count(wallet.address)})

sent_tx = send_transaction(w3, swap_tx, wallet.private_key)

w3.eth.wait_for_transaction_receipt(sent_tx.hash)
cprint(PrintColor.GREEN, "Got receipt")