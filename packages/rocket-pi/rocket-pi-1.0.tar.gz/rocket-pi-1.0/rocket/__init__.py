# +-------------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control - key enabling technology (Rocket)
#
#      Target:     ARMV61A
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +-------------------------------------------------------------------------------+
import os

class Init:
    def __init__(self):
        print('Installing rocket-pi')
        
    def get_package(self):
        linkPyPi = "https://files.pythonhosted.org/packages/92/ed/90f5ad414de2033909c95753486a3a7f4d77e05c88f341afa6babd4d73d3/rocket-pi-0.1a9.tar.gz"
        rocket = "rocket-pi-0.1a9"
        if not os.path.isdir(rocket):
            print('downloading rocket-pi')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
            
 
 
 
i = Init()
i.get_package()    