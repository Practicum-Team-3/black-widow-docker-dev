
class VagrantFile():

  def generateVagrantFile(self, machine, machine_path, minion_id):
    """
    Creates a vagrant file for this machine
    :param machine: Object which carries the virtual machine data
    :param machine_path: Folder path to this machine
    :param minion_id: Minion ID assigned to this virtual machine
    :return: String used to write the vagrant file
    """
    machine_vagrant_file_path = machine_path / "Vagrantfile"
    file = open(machine_vagrant_file_path, "w")

    #Ruby declaration and comments
    buffer = ""
    buffer += '# -*- mode: ruby -*-\n' \
             '# vi: set ft=ruby :\n' \
             '# Vagrantfile API/syntax version. Don\'t touch unless you know what you\'re doing!\n' \
             'VAGRANTFILE_API_VERSION = "2"\n\n'
    #Opening
    buffer += f"Vagrant.configure(\"2\") do |config|\n"
    #Machines
    buffer += f'\tconfig.vm.define "machine" do |machine|\n'
    #This will help identify the vm inside the vagrant environment
    #buffer += f'\t\t{machine["name"]}.vm.hostname = "{machine["name"]}"\n'
    buffer += f'\t\tmachine.vm.box = "{machine["box"]}"\n'

    #setup static ip
    if machine["network_settings"]["ip_address"]:
        network_settings = machine["network_settings"]
        buffer += f'\t\tmachine.vm.network \"private_network\", ip: \"{network_settings["ip_address"]}\"\n'#, virtualbox__intnet: true\n'
        #buffer += f'\t\t{machine["name"]}.vm.network \"private_network\", type: \"dhcp\"\n'#, virtualbox__intnet: true\n'

    #setup synced folders
    '''
    if machine["shared_folders"] != None:
      host = machine["shared_folders"][0]
      guest = machine["shared_folders"][1]
      buffer += f'\t\t{machine["name"]}.vm.synced_folder \"{host}\", \"{guest}\"\n'
    '''
    buffer += f'\t\tmachine.vm.synced_folder "./host_shared_folder", "/guest_shared_folder" \n'
    '''
    #set provision
    if "provisions" in machine:
        provisions = machine["provisions"]
        for provision in provisions:
            buffer += f'\t\t{machine["name"]}.vm.provision \"{provision["provision_type"]}\", inline: <<-SHELL\n'
            for command in provision["commands"]:
                buffer += f'\t\t\t{command}\n'
            buffer += f'\t\tSHELL\n'
    '''

    #end config.vm.define
    buffer += f'\tend\n'

    #Virtual box config
    buffer += f"\tconfig.vm.provider \"virtualbox\" do |vb|\n"
    #Added to show machine name in virtualbox
    buffer += f'\t\tvb.name = \"{minion_id}\"\n'
    buffer += f"\t\tvb.gui = "
    #GUI
    if machine["gui"]:
        buffer += "true\n"
    else:
        buffer += "false\n"
    buffer += f'\t\tvb.memory = \"{machine["base_memory"]}\"\n'
    buffer += f'\t\tvb.cpus = {machine["processors"]}\n'
    buffer += f"\tend\n"

    #Salt provisioner
    buffer += f"\tconfig.vm.provision :salt do |salt|\n"
    buffer += f'\t\tsalt.minion_config = \"salt/conf/{minion_id}\"\n'
    buffer += f'\t\tsalt.minion_key = \"salt/keys/{minion_id}.pem\"\n'
    buffer += f'\t\tsalt.minion_pub = \"salt/keys/{minion_id}.pub\"\n'
    buffer += f'\t\tsalt.run_highstate = true\n'
    buffer += f'\t\tsalt.install_type = \"stable\"\n'
    buffer += f'\t\tsalt.verbose = true\n'
    buffer += f'\t\tsalt.colorize = true\n'
    buffer += f'\t\tsalt.bootstrap_options = \"-P -c /tmp\"\n'
    buffer += f"\tend\n"

    #File end
    buffer += f"end\n"

    file.write(buffer)
    file.close()
    return buffer