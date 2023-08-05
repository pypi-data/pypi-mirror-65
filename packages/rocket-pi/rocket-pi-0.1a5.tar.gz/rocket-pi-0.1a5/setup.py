# +---------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control key enabling technology (Rocket)
#
#      Target:     ARMV61A
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +---------------------------------------------------------------------------+

import atexit
import os
import sys
from setuptools import setup
from setuptools.command.install import install
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

def logo():
    print()
    print("                                          ")
    print("######                                    ")
    print("#     #  ####   ####  #    # ###### ##### ")
    print("#     # #    # #    # #   #  #        #   ")
    print("######  #    # #      ####   #####    #   ")
    print("#   #   #    # #      #  #   #        #   ")
    print("#    #  #    # #    # #   #  #        #   ")
    print("#     #  ####   ####  #    # ######   #   ")
    print("                                          ")


class CustomInstall(install):
    def run(self):
        def _post_install():

            # Add your post install code here
            logo()
            import rocket
            print(rocket.joke())
            import rocketlauncher
            print(rocketlauncher.joke())
            # Get hostapd or dnsmasq if needed
            get_hostapd()
            get_config_dnsmasq("dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h")
            os.system("systemctl reload dnsmasq")
            setup_WiFi_network_interfaces()
            os.system("systemctl stop dnsmasq")
            os.system("systemctl stop hostapd")
            configure_WiFi_wpa_supplicant()
            adjust_staticIP_dhcpcd("interface wlan0", "static ip_address=192.168.4.1/24")
            adjust_staticIP_dhcpcd("interface eth0", "static ip_address=192.168.1.10/24")
            configure_hostapd()
            hostapd_daemon_conf()
            os.system("systemctl unmask hostapd")
            os.system("systemctl enable hostapd")
            os.system("systemctl start hostapd")
            get_webiopi()
            rev, board, memory = revToModel()
            print ("Revision: %s, Board: %s, Memory: %s" % (rev,board,memory))
            if(board == 'PiZero'):
               get_BCM2835_patch()


        atexit.register(_post_install)
        install.run(self)


setup(name='rocket-pi',
      version='0.1a5',
      description='Remote open control key enabling technology (Rocket)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gulliversoft/rocket',
      author='gulliversoft',
      author_email='fg7@gulliversoft.com',
      license='GPL3',
      packages=['rocket','rocketlauncher'],
      zip_safe=False,
      classifiers=["Intended Audience :: Education",
               'Development Status :: 3 - Alpha',
               'Programming Language :: Python :: 3', 
               "Operating System :: POSIX :: Linux",
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware'],
      cmdclass={'install': CustomInstall})
      #install_requires[''])

def get_webiopi():
    """
    Try to install webiopi on host machine if not present

    :return: None
    :rtype: None
    """
    os.system("ls")
    if not os.path.isfile("/WebIOPi-0.7.1/setup.sh"):
        print("WebIOPi not found, installing now...")
        os.system("tar xvzf ./rocket/WebIOPi-0.7.1.bin")
        os.chdir("WebIOPi-0.7.1")
        os.system("./setup.sh")


def get_config_dnsmasq(dhcprange):
    """
    Try to install dnsmasq (dhcp server) on host machine if not present
    in second step adjusts the address range

    :return: None
    :rtype: None
    """
    filename = "/usr/sbin/dnsmasq"

    if not os.path.isfile(filename):
        print("dhcp server (dnsmasq) not found, installing now...")
        os.system("apt-get install dnsmasq")

    if not os.path.isfile(filename):
        sys.exit(("\nUnable to install the \'dnsmasq\' package!\n" + 
                  "This process requires a persistent internet connection!\n" +
                  "Run apt-get update for changes to take effect.\n" +
                  "Rerun the script to install dnsmasq.\n" +
                  "Closing"))

    filename = "/usr/sbin/dnsmasq.conf"
    if(search(filename, "interface=wlan0") > 0):
        return
    else:
        body = "interface=wlan0\n%s\n" % (dhcprange)
        text_file = open(filename, "w")
        text_file.write(body)
        text_file.close()


def get_hostapd():
    """
    Try to install hostapd on host system if not present

    :return: None
    :rtype: None
    """
    filename = "/usr/sbin/hostapd"

    if not os.path.isfile(filename):
        print(filename + " not found, installing now...")
        os.system("apt-get install hostapd")

    if not os.path.isfile(filename):
        sys.exit(("\nUnable to install the \'hostapd\' package!\n" + 
        "This process requires a persistent internet connection!\n" +
        "Run apt-get update for changes to take effect.\n" +
        "Rerun the script to install hostapd.\n" +
        "Closing"))

def adjust_staticIP_dhcpcd(interface, ip_leasetime):
    """
    configure static IP for the given interface

    :return: None
    :rtype: ip_range
    """
    filename = "/etc/dhcpcd.conf"

    if not os.path.isfile(filename):
        sys.exit((filename + " not found, break"))


    if(search(filename, interface) > 0 and search(filename, ip_leasetime) > 0):
        print("Static " + ip_leasetime + " for " + interface + " was already set")
        return

    file_object = open(filename, 'a')

    # Append at the end of file
    file_object.write(interface + "\n")
    file_object.write(ip_leasetime+ "\n")
    file_object.close()


def search(str, filename):
    if not os.path.isfile(filename):
        return -1
    n = 0
    with open(filename, 'r') as f:
        for line in f:
            if re.search(str, line):
                return n
            n += 1
    return -1

def configure_WiFi_wpa_supplicant():
    file = "/etc/wpa_supplicant/wpa_supplicant.conf"
    if os.path.isfile(file):
        print("Your WiFi setup is already configured, exit now...")
        return
    else:
        ssid = input('Router SSID: ')
        psk = input('Router Password: ')
        country= input('Country code: DE, US, BG...: ')
        body = ("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n" +
        "update_config=1\n" +
        "country=%s\n\n" +
        "network={\n   SSID=\"%s\"\n   psk=\"%s\"\n}\n") % (country, ssid, psk)
        text_file = open(file, "w")
        text_file.write(body)
        text_file.close()

def setup_WiFi_network_interfaces():
    file = "/etc/network/interfaces1"
    if search("auto wlan0", file) > 0:
        print("Your WiFi setup keeps auto wlan0, exit now...")
        return
    else:
        body = ("#interfaces(5) file used by ifup(8) and ifdown(8)\n" +
        "auto wlan0\n" +
        "allow-hotplug wlan0\n" +
        "iface wlan0 inet dhcp\n" +
        "wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n" +
        "iface default inet dhcp")

        text_file = open(file, "w")
        text_file.write(body)
        text_file.close()

def hostapd_daemon_conf():
    file = "/etc/default/hostapd"
    content = "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\""
    if search(content, file) > 0:
        print("Your hostapd daemon is configured, exit now...")
        return
    else:
        text_file = open(file, "w")
        text_file.write(content)
        text_file.close()

def get_BCM2835_patch():
    """
    Reason: different starting address of the GPIO's between the BCM's
    0x3f000000 instead of 0x20000000
    :return: None
    :rtype: None
    """

    file = "webiopi-pi2bplus.patch"
    os.system("ls")
    if os.path.isfile(file):
       print("patch is already here, exit now...")
       return

    os.system("wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch")
    os.system("patch -p1 -i webiopi-pi2bplus.patch")

    file = "/python/native/gpio.c"
    if os.path.isfile(file):
       print("Wrong start up folder for patch validation, exit now...")
       return

    if(search(file, "#define BCM2708_PERI_BASE 0x3f000000") > 0):
       print("BCM2835 patch done...")
       return

    print("BCM2835 patch not successful...")


def getRevision():
  # Extract revision from cpuinfo file
  revision = "ERROR"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:8]=='Revision':
        revision = line[11:15]
        full_revision = line[11:17]
#        print (full_revision)
    f.close()
  except:
    revision = "ERROR"
  if revision[0] == "a" or revision[0] == "9":
    revision = full_revision

  return revision

def revToModel():
  rev = getRevision()
#  print (rev)
  model = [
    "0002", ["Model B Rev 1.0", "256MB"],
    "0003", ["Model B Rev 1.0 (no fuses,D14)", "256MB"],
    "0004", ["Model B Rev 2.0 (mounting holes,Sony)", "256MB"],
    "0005", ["Model B Rev 2.0 (mounting holes,Qisda)", "256MB"],
    "0006", ["Model B Rev 2.0 (mounting holes,Egoman)", "256MB"],
    "0007", ["Model A (Egoman)", "256MB"],
    "0008", ["Model A (Sony)", "256MB"],
    "0009", ["Model A (Qisda)", "256MB"],
    "000d", ["Model B Rev 2.0 (mounting holes,Egoman)", "512MB"],
    "000e", ["Model B Rev 2.0 (mounting holes,Sony)", "512MB"],
    "000f", ["Model B Rev 2.0 (mounting holes,Qisda)", "512MB"],
    "0010", ["Model B+", "512MB"],
    "0011", ["Compute Module", "512MB"],
    "0012", ["Model A+", "256MB"],
    "0014", ["Compute Module", "512MB"],
    "900092", ["PiZero", "512MB"],
    "a01041", ["Model 2B (Sony)", "1GB"],
    "a21041", ["Model 2B (Embest)", "1GB"]
  ]
  ix = model.index(rev)
  board, memory = model[ix+1]
  return (rev, board, memory)

def configure_hostapd():
  filename = "/ets/hostapd/hostapd.conf"
  ssid = input('Access point SSID: ')
  psk = input('Password: ')
  body = ("interface=wlan0\n" +
        "driver=n180211\n" +
        "ssid=%s\n" +
        "hw_mode=g\n" +
        "channel=7\n" +
        "wmm_enabled=0\n" +
        "macaddr_acl=0\n" +
        "auth_algs=1\n" +
        "ignore_broadcast_ssid=0\n" +
        "wpa=2\n" +
        "wpa_passphrase=%s\n" +
        "wpa_key_mgmt=WPA-PSK\n" +
        "wpa_pairwise=TKIP\n" +
        "rsn_pairwise=CCMP\n") % (ssid, psk)
  text_file = open(file, "w")
  text_file.write(body)
  text_file.close()
    