import time
from time import sleep
import random

from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from loguru import logger

from settings import *
from modules.swap import swap_cake
from modules.binance_withdraw import binance_withdraw

def generate_wallets(wallets):
    if isinstance(wallets, int):
        with open(f'new_aptos_private_keys{time.time()}.txt', 'a+') as f:
            for i in range(wallets):
                f.write(str(Account.generate().private_key) + '\n')

    else:
        with open(f'aptos_addresses{time.time()}.txt', 'a+') as f:
            for key in wallets:
                f.write(str(Account.load_key(key=key).address()) + '\n')

if __name__ == '__main__':
    print(f'----------------------------------------------------'
          f'\nsubscribe to us : https://t.me/my_utils\n'
          f'----------------------------------------------------')

    MODULE = int(input('''
    MODULE:
    0.  generate_aptos_wallets
    1.  binance_withdraw
    2.  aptos_swap
    3.  aptos_bridge(only in full version)
    4.  add_liquidity(only in full version)
    5.  create_nft_and_listing(only in full version)
    Выберите модуль (0 - 2) : '''))

    with open('private_keys.txt', 'r', encoding='utf-8-sig') as file:
            private_keys = [row.strip() for row in file]

    class ClientConfig:
        """Common configuration for clients, particularly for submitting transactions"""

        expiration_ttl: int = 600
        gas_unit_price: int = GAS_PRICE
        max_gas_amount: int = GAS_LIMIT
        transaction_wait_in_seconds: int = 20


    REST_CLIENT = RestClient(NODE_URL, client_config=ClientConfig)

    if MODULE == 0:
        if MODE:
            generate_wallets(int(N))
        else:
            generate_wallets(private_keys)
        exit()

    if MODULE == 2:
        logger.info(f'Успешно загружено {len(private_keys)} wallet\'s')
        random.shuffle(private_keys)
        for n in range(ITERATIONS):
            for key in private_keys:
                    if RANDOM_SWAP:
                        amount = random.uniform(SWAP_AMOUNT_FROM, SWAP_AMOUNT_TO)
                    else:
                        amount = SWAP_AMOUNT_FROM
                    swap_cake(REST_CLIENT, key, random.choice(DEX), amount, SLIPPAGE, random.choice(TOKEN_FROM),
                              random.choice(TOKEN_TO))

    if MODULE == 1:
        with open('withdraw_addresses', 'r', encoding='utf-8-sig') as f:
            addresses = [row.strip() for row in f]
        logger.info(f'Успешно загружено {len(addresses)} wallet\'s')
        random.shuffle(addresses)
        for address in addresses:
            if RANDOM_WITHDRAW:
                amount = round(random.uniform(WITHDRAW_AMOUNT_FROM, WITHDRAW_AMOUNT_TO), 5)
            else:
                amount = WITHDRAW_AMOUNT_FROM
            binance_withdraw(address, amount, symbolWithdraw, network)
            time.sleep(random.randint(WAIT_FROM, WAIT_TO))
