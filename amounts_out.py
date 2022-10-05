import os
import math
from brownie import *
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
lp = Contract.from_explorer(factory.getPool(weth, usdc, 3000))

print(" ")
print("========POOL========== ")
print(f"ADDRESS: {lp.address}")
print(f"TOKEN0: {lp.token0()}")
print(f"TOKEN1: {lp.token1()}")
print(" ")

""" Some data will be need to stored in the batching process and some
at the time that the function is called. I think we need to call the tick and the
liquidity each time but the decimals can be stored"""

""" DataStructure = [{
    "pool": contract object,
    "token0": contract object,
    "token1": contract object,
}] """

## tokenIn should be a contract object
## tokenOut should be a contract object
## pool should be a contract object
def swapExactInputSingle (tokenIn, tokenOut, pool, amountIn):
    current_tick = pool.slot0()[1]
    lower_tick = (current_tick // 60) * 60
    upper_tick = lower_tick + 60

    current_price = 1.0001 ** (current_tick / 2)
    lower_price = 1.0001 ** (lower_tick / 2)
    upper_price = 1.0001 ** (upper_tick / 2)
    
    L = pool.liquidity()
    
    if (tokenIn == pool.token1()):
        deltaY = amountIn
        delta_price = deltaY / L
        target_price = current_price + delta_price

        # Output printing
        """ print("========DELTA X INPUTS=======")
        print(f"Delta Y: {deltaY}")
        print(f"Delta Price: {delta_price}")
        print(f"Current Price: {current_price}")
        print(f"Delta Y Target: {target_price}")
        print(" ") """

        out = target_price > upper_price
        if (not out):
            dx = -((1 / target_price) - (1 / current_price)) * L
            return dx / (10 ** tokenOut.decimals())
        else:
            """ dy = (upper_price - current_price) * L
            dx = -((1 / upper_price) - (1 / current_price)) * L
            amount_remaining = deltaY - dy
            while amount_remaining > 0:
                delta_price = amount_remaining / L
                target_price = current_price + delta_price

                upper_price1 = upper_price + 60
                current_price = upper_price

                L_gross = pool.ticks(lower_tick)[0]
                L_net = pool.ticks(lower_tick)[1]
                L_next = L_gross + L_net
                
                dy = (target_price - current_price) * L_next
                dx = -((1 / target_price) - (1 / current_price)) * L_next
            
            return [dx / (10 ** tokenOut.decimals()), dy / (10 ** tokenIn.decimals()), amount_remaining / (10 ** tokenIn.decimals())] """
    else:
        deltaX = amountIn
        target_price = (current_price * L) / (deltaX * current_price + L)

        # Output printing
        """ print("========DELTA Y INPUTS=======")
        print(f"Delta X: {deltaX}")
        print(f"Current Price: {current_price}")
        print(f"Delta X Target: {target_price}")
        print(" ") """
        
        out = target_price < lower_price
        if (not out):
            dy = -((target_price) - (current_price)) * L
            return dy / (10 ** tokenOut.decimals())
        else:
            """ dy0 = -((1 / target_price) - (1 / upper_price)) * L

            L_gross = pool.ticks(lower_tick)[0]
            L_net = pool.ticks(lower_tick)[1]
            L_next = L_gross + L_net

            dy1 = -((1 / upper_price) - (1 / target_price)) * L_next
            dy = dy0 + dy1 """

            print("not implemented 2")

usdc_out = swapExactInputSingle(weth, usdc, lp, 1*10**weth.decimals())
weth_out = swapExactInputSingle(usdc, weth, lp, 1*10**usdc.decimals())
weth_out1 = swapExactInputSingle(usdc, weth, lp, usdc_out*10**usdc.decimals())

print("=======Final Outputs and Check=========")
print(f"Swapping 1 WETH for USDC: {usdc_out}")
print(f"Swapping 1 USDC for WETH: {weth_out}")
print(f"Other Swap: {weth_out1}")
print(round((1 / usdc_out), 5) == round(weth_out, 5))
print(" ")