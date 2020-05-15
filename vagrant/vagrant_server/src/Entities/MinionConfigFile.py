
class MinionConfigFile():

  def generateMinionConfigFile(self, conf_path, minion_id):
    """
    Generates the minion config file.
    :param conf_path: Path where the minion config file is saved
    :param minion_id: Minion id string
    :return: String containing the minion config file
    """
    buffer = ""
    ip_address = "192.168.50.1"

    file = open(conf_path / minion_id, "w")

    #Minion config file
    buffer += f"master: {ip_address}\n"
    buffer += f"id: {minion_id}\n"


    file.write(buffer)
    file.close()
    return buffer