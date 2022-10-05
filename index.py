import datetime
import os
from brownie import *
import math
from dotenv import load_dotenv

""" This file implements some of the basic math used in v3. It prints a
wide variety of outputs to give you a glimpse of what is happening between 
ticks."""

load_dotenv()

WEB3_INFURA_PROJECT_ID = os.environ.get("WEB3_INFURA_PROJECT_ID")
ETHERSCAN_TOKEN = os.environ.get("ETHERSCAN_TOKEN")

os.environ["WEB3_INFURA_PROJECT_ID"] = WEB3_INFURA_PROJECT_ID
os.environ["ETHERSCAN_TOKEN"] = ETHERSCAN_TOKEN

network.connect('mainnet')

## Importing necessary contracts
factory = Contract.from_explorer('0x1F98431c8aD98523631AE4a59f267346ea31F984')
weth = Contract.from_explorer('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
usdc = Contract.from_explorer('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
lens = Contract.from_explorer('0xbfd8137f7d1516D3ea5cA83523914859ec47F573')
lp_3000 = Contract.from_explorer(factory.getPool(weth, usdc, 3000))
token0 = Contract.from_explorer(lp_3000.token0())
token1 = Contract.from_explorer(lp_3000.token1())

## Calculating current tick range
current_tick = lp_3000.slot0()[1]
lower_tick = math.floor(current_tick / 60) * 60
upper_tick = lower_tick + 60

## Calculating current price
price = 1.0001 ** (current_tick)
adjusted_price = price / (10 ** (token1.decimals() - token0.decimals()))

## Grabbing current liquidity in range
L = lp_3000.liquidity()

## Calculating Square Root Prices in the Current Tick Range
sa = 1.0001 ** (lower_tick // 2)
sb = 1.0001 ** (upper_tick // 2)
sp = price ** 0.5

## Calculating the Virtual Reserves in the Current Range
amount0 = L * (sb - sp) / (sp * sb)
amount1 = L * (sp - sa)

## Adjusting the Virtual Resevers to Human Readable Format
adj_amount0 = amount0 / (10 ** token0.decimals())
adj_amount1 = amount1 / (10 ** token1.decimals())
k = adj_amount0 * adj_amount1
rate = adj_amount0 / adj_amount1

## Calculating the Squared Price of token1 and token0
s0 = (L * sb) / (amount0 * sb + L)
s1 = (amount1 / L) + sa

## Adjusting the Squared Price to Human Readable Format
adj_s0 = (s0 ** 2) / (10 ** (token1.decimals() - token0.decimals()))
adj_s1 = (s1 ** 2) / (10 ** (token1.decimals() - token0.decimals()))

## Creating a Test Trade Amount within Current Tick
trade_amount = .5
t0 = (trade_amount * (10 ** token0.decimals())) ** 2

## Calculating new Squared Price of Token 0 after trade
st0 = (L * sb) / ((amount0 + t0) * sb + L)
new_tick = math.log(st0, 1.0001) * 2

## Adjusting new Square Price of Token 0 after trade
adj_st0 = (st0 ** 2) / (10 ** (token1.decimals() - token0.decimals()))

## Recalculating the Reserves of token 1 after trade
final_amount0 = L * (sb - st0) / (sp * sb)
final_amount1 = L * (st0 - sa)

## Adjusting the final reserve amounts
final_adj_amount0 = final_amount0 / (10 ** token0.decimals())
final_adj_amount1 = final_amount1 / (10 ** token1.decimals())
k1 = final_adj_amount0 * final_adj_amount1
rate1 = final_adj_amount0 / final_adj_amount1

## Taking difference in Amount 1 and Token 1 after Trade
amount1_out = amount1 - final_amount1
amount1_out_adj = amount1_out / (10 ** token1.decimals())

print(" ")
print(f"{datetime.datetime.now().strftime('[%I:%M:%S%p]')}")
print(" ")

print("######### TOKENS INCLUDED IN THE POOL ########")
print(f"Token 0 or Token x: {token0}")
print(f"Token 1 or Token y: {token1}")
print(f"Pool Address: {lp_3000.address}")
print(f"Current Exchange Rate: {adjusted_price}")

print(" ")

print("######### TICK RANGE AND PRICE RANGE DATA ########")
print(f"TICK RANGES (low, cur, up): {lower_tick, current_tick, upper_tick}")
print(f"PRICE RANGES (sa, sp, sb): {sa, sp, sb}")

print(" ")

print("######### RESERVE DATA INPUTS RANGE DATA ########")
print(f"Liquidity (L): {L}")
print(f"Square root Prices: {sa, sp, sb}")

print(" ")

print("######### CALCULATED RESERVE DATA ########")
print(f"Raw Reserve Data of x and y: {amount0, token0.symbol(), amount1, token1.symbol()}")
print(f"Adjusted Reserve Data: {adj_amount0, token0.symbol(), adj_amount1, token1.symbol()}")
print(f"Total Tick Liquidity K: {k}")

print(" ")

print("######### CALCULATED EXCHANGE RATE WITHIN TICK ########")
print(f"Exchange Rate: {rate}")
print(f"Inverted Rate: {1 / rate}")

print(" ")

print("######### CALCULATE PRICES FROM GIVEN RESERVES ########")
print(f"Square Price Token 0: {s0}")
print(f"Square Price Token 1: {s1}")
print(f"Adjusted Price Token 0: {adj_s0}")
print(f"Adjusted Price Token 1: {adj_s1}")

print(" ")

print("######### ATTEMPTED IN TICK TRADE OUTPUT ########")
print(f"New Square Price Token 0: {st0}")
print(f"Adjusted Price Token 0: {adj_st0}")

print(" ")

print("######### CALCULATED NEW RESERVE DATA ########")
print(f"Raw Reserve Data of x and y: {final_amount0, token0.symbol(), final_amount1, token1.symbol()}")
print(f"Adjusted Reserve Data: {final_adj_amount0, token0.symbol(), final_adj_amount1, token1.symbol()}")
print(f"Total Tick Liquidity K: {k1}")

print(" ")

print("######### CALCULATED EXCHANGE RATE WITHIN TICK ########")
print(f"Exchange Rate: {rate1}")
print(f"Inverted Rate: {1 / rate1}")

print(" ")

print("######### AFTER TRADE TOKEN 0 OUTPUT ########")
print(f"Squared Amount out of Token 1 from Trade: {amount1_out}")
print(f"Final Amount out of Token 1 from Trade: {amount1_out_adj}")
print(f"New tick after trade: {new_tick}")

print(" ")

## BROKEN CODE
""" ## This does not accurately change the price
t1 = (1 * (10 ** token1.decimals())) ** 2
st1 = ((amount1 + t1) / L) + sa
adj_st1 = (st1 ** 2) / (10 ** (token1.decimals() - token0.decimals())) """