#!/usr/bin/python3
from brownie import BeOurPest, config, network
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account
)

def deploy_be_our_pest():
    day_in_seconds = 24 * 60 * 60
    account = get_account()
    bop = BeOurPest.deploy(
        day_in_seconds, #high score reset interval
        60,             #retry submission interval
        60,             #retry collecting score interval
        {"from": account}
    )
    block_confirmations=6
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        block_confirmations=1
    bop.tx.wait(block_confirmations)
    print(f"BeOurGuest deployed to {bop.address}")
    # tx = fund_with_link(bop.address)
    # tx.wait(1)
    return bop


def main():
    deploy_be_our_pest()
