from pypresence import Presence
from os import getenv as e
from time import time, sleep

ms = int(round(time() * 1000))

RPC = Presence(e('client_id'))
RPC.connect()
RPC.update(state="Running", details="Python Discord Bot",
           start=ms, large_image="amburp", large_text="ambu",
           small_image="foxrp", small_text="awoo")

while True:
    sleep(15)
