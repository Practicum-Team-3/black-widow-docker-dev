from Managers.VagrantManager import VagrantManager

if __name__=="__main__":
    vagrant_manager = VagrantManager()
    vagrant_manager.runVagrantUp('Test_Scenario')