import os
import bluetooth

class BT():
    def __init__(self, hostname):
        os.system("bluetoothctl discoverable on")
        
        mac_rpi0_samu = "B8:27:EB:48:52:95"    #RPI0
        mac_rpi3_samu = "B8:27:EB:10:0D:19"    #RPI1
        mac_rpi4_samu = "DC:A6:32:6B:3A:AB"    #RPI2
        
        mac_rpi4_zeti = "DC:A6:32:78:BC:C7"    #RPI3
        mac_rpi4_mate = "DC:A6:32:25:D2:CC"    #RPI4
        
        self.server = mac_rpi4_samu
        self.rpi0 = mac_rpi0_samu    #ROOSTER
        self.rpi1 = mac_rpi3_samu    #PIG 1
        self.rpi2 = mac_rpi4_zeti    #PIG 2
        self.rpi3 = mac_rpi4_mate    #PIG 3
      
        if (hostname == "server"):
            
            on_rpi0 = 0
            on_rpi1 = 0
            on_rpi2 = 0
            on_rpi3 = 0
            
            while (on_rpi0 == 0 or on_rpi1 == 0 or on_rpi2 == 0 or on_rpi3 == 0):
                addr, data = self.receive()
                if (addr == self.rpi0):
                    on_rpi0 = 1
                if (addr == self.rpi1):
                    on_rpi1 = 1
                if (addr == self.rpi2):
                    on_rpi2 = 1
                if (addr == self.rpi3):
                    on_rpi3 = 1
                
        elif (hostname == "basic"):
            pass
        else:
            self.send(self.server, "asd")
    
    def receive(self):
        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
          
        port = 1
        server_sock.bind(("",port))
        server_sock.listen(1)
          
        client_sock,address = server_sock.accept()
          
        data = client_sock.recv(1024)
          
        client_sock.close()
        server_sock.close()
          
        return address[0], data;
      
    def send(self, targetBluetoothMacAddress, message):
        try:
            sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            sock.connect((targetBluetoothMacAddress, 1))
            sock.send(message)
            sock.close()
        except:
            print("FAILED TO SEND MESSAGE '" + str(message) + "' TO " + str(targetBluetoothMacAddress))
        
    def sync(self):
        addr, data = self.receive()

    def start(self):
        if (self.rpi0 != ""):
            self.send(self.rpi0, "start")
            
        if (self.rpi1 != ""):
            self.send(self.rpi1, "start")
        
        if (self.rpi2 != ""):
            self.send(self.rpi2, "start")
            
        if (self.rpi3 != ""):
            self.send(self.rpi3, "start")
