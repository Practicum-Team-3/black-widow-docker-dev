from Managers.DatabaseManager import DatabaseManager
from Managers.ScenarioManager import ScenarioManager

if __name__ == '__main__':
    db_manager = DatabaseManager()
    scenario_manager = ScenarioManager()
    scenario_name = 'Scenario_1'
    scenario_json = scenario_manager.getScenario(scenario_name)
    print(db_manager.insertScenario(scenario_json))
    #print(db_manager.getScenarios())
    #print(db_manager.getScenario(scenario_name))
    #scenario_json['scenario_id'] = 'Hi'
    #print(db_manager.editScenario(scenario_json))
    #print(db_manager.deleteScenario(scenario_name))