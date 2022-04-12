import bt
import time

bt = bt.BT("basic")
bt.sync()
time.sleep(1)

while (1):
    bt.send(bt.server, "hello")
    time.sleep(1)
