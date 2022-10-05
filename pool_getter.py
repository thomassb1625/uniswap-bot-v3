import os
import datetime
from brownie import *
from dotenv import load_dotenv

load_dotenv()

WEB3_INFURA_PROJECT_ID = os.environ.get("WEB3_INFURA_PROJECT_ID")
ETHERSCAN_TOKEN = os.environ.get("ETHERSCAN_TOKEN")

os.environ["WEB3_INFURA_PROJECT_ID"] = WEB3_INFURA_PROJECT_ID
os.environ["ETHERSCAN_TOKEN"] = ETHERSCAN_TOKEN

network.connect('mainnet')

factory = Contract.from_explorer('0x1F98431c8aD98523631AE4a59f267346ea31F984')
quoterv1 = Contract.from_explorer('0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6')

print("========= START OF PULLING EVENT LOGS ===========")
print(f"{datetime.datetime.now().strftime('[%I:%M:%S%p]')}")
print(" ")

t0 = datetime.datetime.now()

pools = factory.events.PoolCreated.getLogs(None, 0, "latest",)
print(f"Found a total of {len(pools)} pools")
pool_list = [{
            "token0": i.args.token0,
            "token1": i.args.token1,
            "address": i.args.pool,
            "fee": i.args.fee,
            "tick_spacing": i.args.tickSpacing,
        } for i in pools]

t1 = datetime.datetime.now()

print(len(pool_list))

print("========= END OF GATHERING EVENTS ===========")
print(f"{datetime.datetime.now().strftime('[%I:%M:%S%p]')}")
print(" ")

print(f"The program took {t1 - t0}")
print(" ")