from dataclasses import dataclass

from web3.contract import Contract

from core.constants import FILES_FOLDER
from core.misc import ma
from core.printers import cprint, PrintColor
from core.readers import safe_read_file, safe_load_json
from core.core_types.tokens import ERC20Token


@dataclass
class Farm:
    name: str
    master_chef_address: str
    abi: dict
    token: ERC20Token

    master_chef: Contract = None

    def init_master_chef(self, w3):
        self.master_chef = w3.eth.contract(address=ma(self.master_chef_address.lower()), abi=self.abi)

    def __repr__(self):
        return f'<{self.name} farm>'


def load_farm(name: str) -> Farm:
    filename = 'farms.json'
    raw = safe_read_file(FILES_FOLDER / filename)
    all_farms = safe_load_json(raw, name=str, master_chef=str, token=dict, abi=list)
    for obj in all_farms:
        if obj['name'] == name:
            farm = Farm(obj['name'],
                        obj['master_chef'],
                        obj['abi'],
                        ERC20Token(obj['token']['address'], obj['token']['symbol']))
            cprint(PrintColor.CYAN, f'Loaded {farm}')
            return farm
    raise ValueError(f'Farm with name `{name}` is not found. Check {filename}')
