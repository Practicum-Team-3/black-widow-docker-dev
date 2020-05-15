from Entities.NetworkSettings import NetworkSettings
from Entities.Provision import Provision
from Entities.Program import Program
from Entities.Entity import Entity


class VirtualMachine(Entity):
  def __init__(self, name="", box="generic/alpine37", os="", base_memory = "1024", processors = "2", is_attacker=False, shared_folders = ('./vmfiles', '/sharedfolder'), uuid = ""):
    self.name = name
    self.box = box
    self.os = os
    self.is_attacker = is_attacker
    self.base_memory = base_memory
    self.processors = processors
    self.shared_folders =  shared_folders     # tuples of (hostPath, guestPath)
    self.network_settings = NetworkSettings()
    self.provision = [Provision("pingVictim")]
    self.gui = False
    self.programs = [Program()]
    self.uuid = uuid

  def setName(self, name):
    """
    Sets the name for this virtual machine
    :param name: String with the virtual machine name
    """
    self.name = name

  def setOS(self, os):
    """
    Sets the OS for this virtual machine
    :param os: String with the virtual machine OS
    """
    self.os = os

  def setBaseMemory(self, base_memory):
    self.base_memory = base_memory

  def addSharedFolder(self, hostPath, guestPath):
    """
    Adds the shared folder between the host and the guest
    :param hostPath: String with the host path
    :param guestPath: String with the guest path
    """
    self.shared_folders = (hostPath, guestPath)

  def setNetworkSettings(self, network_settings):
    """
    Sets the network settings for this virtual machine
    :param network_settings: Object which carries the network settings data
    """
    self.network_settings = network_settings

  def enableGUI(self, isVisible):
    """
    Enables the GUI for this virtual machine
    :param isVisible: Boolean to enable or disable the GUI in a virtual machine
    """
    self.gui = isVisible

  def setProvision(self, i, provision):
    """
    Sets the provision for this virtual machine
    :param provision: Object which carries the provision data
    """
    if i < len(self.provision):
      self.provision[i] = provision

  def dictionary(self):
    """
    Generates a dictionary for the Virtual Machine object
    :return: A dictionary with Virtual Machine data
    """
    dicti = dict()
    dicti["name"] = self.name
    dicti["box"] = self.box
    dicti["os"] = self.os
    dicti["base_memory"] = self.base_memory
    dicti["processors"] = self.processors
    dicti["is_attacker"] = self.is_attacker
    dicti["shared_folders"] = self.shared_folders
    dicti["network_settings"] = self.network_settings.dictionary()
    dicti["provisions"] = [prov.dictionary() for prov in self.provision]
    dicti["programs"] = [prog.dictionary() for prog in self.programs]
    dicti["gui"] = self.gui
    dicti["uuid"] = self.uuid
    return dicti

  def objectFromDictionary(self, dict):
    """
    Creates a VirtualMachine object from a dictionary.
    :param dict: A dictionary containing the VirtualMachine's data
    :return: A VirtualMachine object
    """
    self.name = dict["name"]
    self.box = dict["box"]
    self.os = dict["os"]
    self.base_memory = dict["base_memory"]
    self.processors = dict["processors"]
    self.is_attacker = dict["is_attacker"]
    self.shared_folders = dict["shared_folders"]
    self.network_settings = NetworkSettings().objectFromDictionary(dict["network_settings"])
    self.provision = [Provision().objectFromDictionary(prov) for prov in dict["provisions"]]
    self.programs = [Program().objectFromDictionary(prog) for prog in dict["programs"]]
    self.gui = dict["gui"]
    self.uuid = dict["uuid"]
    return self