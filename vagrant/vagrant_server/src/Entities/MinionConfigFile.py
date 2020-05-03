
class MinionConfigFile():

  def generateMinionConfigFile(self, conf_path, minion_id):
    buffer = ""
    ip_address = "192.168.50.10"

    file = open(conf_path / minion_id, "w")

    #Minion config file
    buffer += f"master: {ip_address}\n"
    buffer += f"id: {minion_id}\n"


    file.write(buffer)
    file.close()
    return buffer