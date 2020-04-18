from Managers.VagrantManager import VagrantManager

if __name__=="__main__":
    scenario_name = "Scenario_1"
    vagrant_manager = VagrantManager()
    vagrant_manager.runVagrantUp(scenario_name)