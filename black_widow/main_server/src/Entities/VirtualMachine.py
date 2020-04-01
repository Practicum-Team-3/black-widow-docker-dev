from Entities.NetworkSettings import NetworkSettings
from Entities.Provision import Provision
from Entities.Entity import Entity


class VirtualMachine(Entity):
  def __init__(self, name="", os="", is_attacker=False):
    self.name = name
    self.os = os
    self.is_attacker = is_attacker
    self.shared_folders = tuple()  # tuples of (hostPath, guestPath)
    self.network_settings = NetworkSettings()
    self.provision = Provision("pingVictim")
    self.gui = False

  def setOS(self, os):
    """
    Sets the OS for this virtual machine
    :param os: String with the virtual machine OS
    """
    self.os = os

  def setName(self, name):
    """
    Sets the name for this virtual machine
    :param name: String with the virtual machine name
    """
    self.name = name

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

  def setProvision(self, provision):
    """
    Sets the provision for this virtual machine
    :param provision: Object which carries the provision data
    """
    self.provision = provision

  def dictionary(self):
    """
    Generates a dictionary for the Virtual Machine object
    :return: A dictionary with Virtual Machine data
    """
    dicti = dict()
    dicti["os"] = self.os
    dicti["name"] = self.name
    dicti["is_attacker"] = self.is_attacker
    dicti["shared_folders"] = self.shared_folders
    dicti["network_settings"] = self.network_settings.dictionary()
    dicti["provisions"] = self.provision.dictionary()
    dicti["gui"] = self.gui
    return dicti

  def objectFromDictionary(self, dict):
    self.os = dict["os"]
    self.name = dict["name"]
    self.is_attacker = dict["is_attacker"]
    self.shared_folders = dict["shared_folders"]
    self.network_settings = NetworkSettings().objectFromDictionary(dict["network_settings"])
    self.provision = Provision().objectFromDictionary(dict["provisions"])
    self.gui = dict["gui"]
    return self