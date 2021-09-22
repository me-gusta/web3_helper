from dataclasses import dataclass

from eth_typing import ChecksumAddress
from web3 import Web3

from core.blockchain.connections import connect_to_blockchain, send_transaction
from core.constants import MAX_INT256
from core.core_types.dex import load_dex
from core.core_types.network import load_network, Network
from core.core_types.tokens import ERC20Token
from core.core_types.wallet import load_wallet, Wallet
from core.printers import cprint, PrintColor


@dataclass
class ApproveConfig:
    spender_address: ChecksumAddress
    token_address: str
    wallet: Wallet
    network: Network
    gas_price_gwei: int


def approve_erc20_token(config):

    token = ERC20Token(config.token_address)
    w3 = connect_to_blockchain(config.network)
    token.init_contract(w3)

    approve_tx = token.contract.functions.approve(
        config.spender_address, MAX_INT256
    ).buildTransaction({'gasPrice': Web3.toWei(config.gas_price_gwei, 'gwei'),
                        'gas': 300000,
                        'nonce': w3.eth.get_transaction_count(config.wallet.address)})
    sent_tx = send_transaction(w3, approve_tx, config.wallet.private_key)

    w3.eth.wait_for_transaction_receipt(sent_tx.hash)
    cprint(PrintColor.GREEN, "Got receipt")


if __name__ == '__main__':
    _config = ApproveConfig(
        spender_address=load_dex('avax_traderjoe').router_address,
        token_address='0x?????????????????????????????????',
        wallet=load_wallet('main'),
        network=load_network('avax'),
        gas_price_gwei=90,
    )
    approve_erc20_token(_config)
