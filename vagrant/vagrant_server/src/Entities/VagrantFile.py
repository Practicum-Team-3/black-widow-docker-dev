
class VagrantFile():
  def vagrantFilePerMachine(self , machine , machine_path):
    """
    Creates a vagrant file for this machine
    :param machine: Object which carries the virtual machine data
    :param machine_path: Folder path to this machine
    :return: String used to write the vagrant file
    """
    buffer = ""
    machine_vagrant_file_path = machine_path / "Vagrantfile"
    file = open(machine_vagrant_file_path, "w")
    #Opening
    buffer = f"Vagrant.configure(\"2\") do |config|\n"
    #Machines
    buffer += f'\tconfig.vm.define "{machine["name"]}" do |{machine["name"]}|\n'
    #This will help identify the vm inside the vagrant environment
    buffer += f'\t\t{machine["name"]}.vm.hostname = "{machine["name"]}"\n'
    buffer += f'\t\t{machine["name"]}.vm.box = "{machine["os"]}"\n'

    #setup static ip
    if machine["network_settings"]["ip_address"]:
        network_settings = machine["network_settings"]
        buffer += f'\t\t{machine["name"]}.vm.network \"private_network\", ip: \"{network_settings["ip_address"]}\", virtualbox__intnet: true\n'

    #setup synced folders
    '''
    if machine["shared_folders"] != None:
      host = machine["shared_folders"][0]
      guest = machine["shared_folders"][1]
      buffer += f'\t\t{machine["name"]}.vm.synced_folder \"{host}\", \"{guest}\"\n'
    '''
    buffer += f'\t\t{machine["name"]}.vm.synced_folder "./host_shared_folder", "/guest_shared_folder" \n'
    #set provision
    if "provisions" in machine:
        provisions = machine["provisions"]
        for provision in provisions:
            buffer += f'\t\t{machine["name"]}.vm.provision \"{provision["provision_type"]}\", inline: <<-SHELL\n'
            for command in provision["commands"]:
                buffer += f'\t\t\t{command}\n'
            buffer += f'\t\tSHELL\n'
    buffer += f'\tend\n'
    #GUI
    buffer += f"\tconfig.vm.provider \"virtualbox\" do |vb|\n"
    #Added to show machine name in virtualbox
    buffer += f'\t\tvb.name = \"{machine["name"]}\"\n'
    buffer += f"\t\tvb.gui = "
    if machine["gui"]:
        buffer += "true\n"
    else:
        buffer += "false\n"
    buffer += f'\t\tvb.memory = \"{machine["base_memory"]}\"\n'
    buffer += f'\t\tvb.cpus = \"{machine["processors"]}\"\n'
    buffer += f"\tend\n"
    buffer += f"end\n"

    file.write(buffer)
    file.close()
    return buffer