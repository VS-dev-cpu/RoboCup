echo "Installing Libs for Bluetooth - DON'T USE"

sudo apt-get update
sudo apt-get install bluetooth bluez libbluetooth-dev
sudo python3 -m pip install pybluez
