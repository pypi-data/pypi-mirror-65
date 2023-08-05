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
            #missing histapd.conf adjustment
            hostapd_daemon_conf()
            os.system("systemctl unmask hostapd")
            os.system("systemctl enable hostapd")
            os.system("systemctl start hostapd")
            get_webiopi()


        atexit.register(_post_install)
        install.run(self)
        

setup(name='rocket-pi',
      version='0.1a4',
      description='Remote open control key enabling technology (Rocket)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gulliversoft/rocket',
      author='gulliversoft',
      author_email='fg7@gulliversoft.com',
      license='GPL3',
      packages=['rocket','rocketlauncher'],
      zip_safe=False,
      classifiers=["Intended Audience :: Education", "Operating System :: POSIX :: Linux"],
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
        os.system("./WebIOPi-0.7.1/setup.sh")
        
    

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
        
        
    filename = "/usr/sbin/dnsmasq1.conf"
    if(search(filename, "interface=wlan0") > 0):
        return
    else:
        body = "interface=wlan0\n%s\n" % (dhcprange)
        
        text_file = open(file, "w")
        text_file.write(body)
        text_file-close()
        

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
    file_object.write(interface)
    file_object.write(ip_leasetime)
    file_object.close()
    
    



def search(str, infile):
    if not os.path.isfile(filename):
        return -1
    with open(infile, 'r') as f:
        for line in f:
            if re.search(str, line):
                return line
    return -1

def configure_WiFi_wpa_supplicant():
    file = "/etc/wpa_supplicant/wpa_supplicant1.conf"
    if os.path.isfile(file):
        print("Your WiFi setup is already configured, exit now...")
        return
    else:
        ssid = input('SSID: ')
        psk = input('Password: ')
        country= input('Country code: DE, US, BG...: ')
        body = ("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n" +
        "update_config=1\n" +
        "country=%s\n\n" +
        "network={\n   SSID=\"%s\"\n   psk=\"%s\"\n}\n") % (country, ssid, psk)
        
        text_file = open(file, "w")
        text_file.write(body)
        text_file-close()
    
    
def setup_WiFi_network_interfaces():
    file = "/etc/network/interfaces1"
    if search("auto wlan0", infile) > 0:
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
        text_file-close()
        
        
def hostapd_daemon_conf():
    file = "/etc/default/hostapd1"
    content = "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\""
    if search(content, infile) > 0:
        print("Your hostapd daemon is configured, exit now...")
        return
    else:
        text_file = open(file, "w")
        text_file.write(content)
        text_file-close()
        
    
    
        
