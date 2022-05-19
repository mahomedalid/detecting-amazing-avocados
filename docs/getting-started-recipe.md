# Getting started recipe

This is a condensed set of instructions to setup the Raspberry Pi with the Adafruit Arduino Brainhat and the avocado models. All these instructions are detailed in the links from the [README](/README.md), this is only a cheatsheet quick reference guide for impatient contributors.

## Initial setup of the BrainHAT

```
cd ~
sudo apt update
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
# REBOOT Y
```

## More Adafruit stuff including the display

```
pip3 install --upgrade adafruit-circuitpython-dotstar adafruit-circuitpython-motor adafruit-circuitpython-bmp280
sudo apt-get install -y vim git
cd ~
sudo pip3 install --upgrade adafruit-python-shell click
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo python3 adafruit-pitft.py --display=st7789_240x240 --rotation=0 --install-type=fbcp
# REBOOT Y
```

## Testing the camera + display

```
# Enable legacy camera 
sudo raspi-config
```

```
# Test camera
pip3 install picamera
raspistill -t 0
```

## Installing grafana and sqlite plugin

```
sudo apt-get install sqlite3
curl https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana-archive-keyrings.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/grafana-archive-keyrings.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

grafana-cli plugins install frser-sqlite-datasource

# Grafana will be accessible at http://<IPADDRESS>:3000, you can check your ip address with hostname -I, user: admin pass: admin
```

## Downloading the model and prediction code

```
pip install numpy --upgrade
cd ~
wget https://raw.githubusercontent.com/lobe/lobe-python/master/scripts/lobe-rpi-install.sh
sudo bash lobe-rpi-install.sh
```

```
cd ~
git clone https://github.com/mahomedalid/detecting-amazing-avocados/
```

## Running the prediction

```
cd ~
cd detecting-amazing-avocados/src
sudo python3 main.py
```