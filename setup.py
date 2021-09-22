from core.constants import FILES_FOLDER
import json


def create_wallets_file():
    dummy_wallets = [
        {
            "name": "main",
            "address": "0xAAAAAAAAAAAAAAAAAAAAA",
            "private_key": "ser_pls_paste_your_private_key_here"
        }]
    with open(FILES_FOLDER / 'wallets.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(dummy_wallets))


def create_networks_file():
    dummy_networks = [
        {
            "name": "polygon",
            "main_http": "https://rpc-mainnet.maticvigil.com",
            "main_ws": "",
            "testnet_http": "",
            "block_explorer": "https://polygonscan.com/",
            "tokens": [
                {
                    "symbol": "WETH",
                    "address": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
                    "decimals": 18
                },
                {
                    "symbol": "USDC",
                    "address": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                    "decimals": 6
                },
                {
                    "symbol": "USDT",
                    "address": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
                    "decimals": 6
                },
                {
                    "symbol": "DAI",
                    "address": "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063",
                    "decimals": 18
                },
                {
                    "symbol": "QUICK",
                    "address": "0x831753DD7087CaC61aB5644b308642cc1c33Dc13",
                    "decimals": 18
                }
            ]
        },
        {
            "name": "bsc",
            "main_http": "https://bsc-dataseed.binance.org/",
            "main_ws": "",
            "testnet_http": "",
            "block_explorer": "https://bscscan.com/",
            "tokens": [
                {
                    "symbol": "WETH",
                    "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
                    "decimals": 18
                },
                {
                    "symbol": "USDC",
                    "address": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
                    "decimals": 6
                },
                {
                    "symbol": "USDT",
                    "address": "0x55d398326f99059fF775485246999027B3197955",
                    "decimals": 6
                },
                {
                    "symbol": "DAI",
                    "address": "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3",
                    "decimals": 18
                }
            ]
        },

        {
            "name": "avax",
            "main_http": "https://api.avax.network/ext/bc/C/rpc",
            "main_ws": "",
            "testnet_http": "",
            "block_explorer": "https://cchain.explorer.avax.network/",
            "tokens": [
                {
                    "symbol": "WETH",
                    "address": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
                    "decimals": 18
                },
                {
                    "symbol": "USDC",
                    "address": "0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664",
                    "decimals": 6
                },
                {
                    "symbol": "USDT",
                    "address": "0xc7198437980c041c805A1EDcbA50c1Ce5db95118",
                    "decimals": 6
                },
                {
                    "symbol": "DAI",
                    "address": "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70",
                    "decimals": 18
                }
            ]
        }
    ]
    with open(FILES_FOLDER / 'networks.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(dummy_networks))


if __name__ == '__main__':
    create_wallets_file()
    create_networks_file()
