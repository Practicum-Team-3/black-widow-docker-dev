#from Managers.VagrantManager import VagrantManager
import os

if __name__=="__main__":
    print(os.path.isfile('/home/vagrant/.ssh/id_rsa.pub'))
    #scenario_name = "Scenario_1"
    #vagrant_manager = VagrantManager()
    #vagrant_manager.runVagrantUp(scenario_name)