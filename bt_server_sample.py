import bt
import time

bt = bt.BT("basic")
print("waiting...")
time.sleep(2)
print("go")
bt.start()

while (1):
    addr, a = bt.receive()
    print("From " + str(addr) + " Received: " + str(a))

