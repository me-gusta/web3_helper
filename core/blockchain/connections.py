from eth_account.datastructures import SignedTransaction
from web3 import Web3
from web3.middleware import geth_poa_middleware

from core.core_types.network import Network
from core.printers import PrintColor, cprint


def connect_to_blockchain(network: Network, use_ws: bool= False) -> Web3:
    if use_ws:
        w3 = Web3(Web3.WebsocketProvider(network.main_ws)) #, websocket_kwargs={'max_size': 1_000_000_000}))
    else:
        w3 = Web3(Web3.HTTPProvider(network.main_http))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    if w3.isConnected():
        cprint(PrintColor.CYAN, f'Connected to {network}. Block number: {w3.eth.block_number}')
    else:
        cprint(PrintColor.RED, f'Not connected to {network}')
        return exit()
    return w3


def send_transaction(w3: Web3, txn: dict, private_key: str) -> SignedTransaction:
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    cprint(PrintColor.GREEN, f'Sending transaction: {signed_txn.hash.hex()}')
    return signed_txn
