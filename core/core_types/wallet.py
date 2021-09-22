from dataclasses import dataclass

from eth_typing import ChecksumAddress

from core.constants import FILES_FOLDER
from core.misc import ma
from core.printers import cprint, PrintColor
from core.readers import safe_read_file, safe_load_json


@dataclass
class Wallet:
    name: str
    address: ChecksumAddress
    private_key: str

    def __repr__(self):
        return f'<{self.name.capitalize()} {self.address[:6]} wallet>'


def load_wallet(name: str) -> Wallet:
    filename = 'wallets.json'
    raw = safe_read_file(FILES_FOLDER / filename)
    all_wallets = safe_load_json(raw, name=str, address=str, private_key=str)
    for obj in all_wallets:
        if obj['name'] == name:
            wallet = Wallet(obj['name'],
                            ma(obj['address'].lower()),
                            obj['private_key'])
            cprint(PrintColor.CYAN, f'Loaded {wallet}')
            return wallet
    raise ValueError(f'Wallet with name `{name}` is not found. Check {filename}')
