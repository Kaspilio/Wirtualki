import gi
import os
from abc import ABC, abstractmethod
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class VMInterface(ABC):
    """
    Abstract base class for handling virtual machines.
    Provides an interface for finding, starting, and stopping VMs.
    """

    @abstractmethod
    def find_vms(self, directory: str):
        pass

    @abstractmethod
    def start_vm(self, vm_name: str):
        pass

    @abstractmethod
    def stop_vm(self, vm_name: str):
        pass


class VMwareHandler(VMInterface):
    """
    Class for handling VMware virtual machines.
    Implements methods to find, start, and stop VMs.
    """

    def find_vms(self, directory: str):
        vms = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.vmx'):
                    vms.append(os.path.join(root, file))
        return vms

    def start_vm(self, vm_name: str):
        try:
            print(f"Starting VMware VM: {vm_name}")
            return True
        except Exception as e:
            print(f"Failed to start VM: {e}")
            return False

    def stop_vm(self, vm_name: str):
        try:
            print(f"Stopping VMware VM: {vm_name}")
            return True
        except Exception as e:
            print(f"Failed to stop VM: {e}")
            return False


class VirtualBoxHandler(VMInterface):
    """
    Class for handling VirtualBox virtual machines.
    Implements methods to find, start, and stop VMs.
    """

    def find_vms(self, directory: str):
        vms = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.vbox'):
                    vms.append(os.path.join(root, file))
        return vms

    def start_vm(self, vm_name: str):
        try:
            print(f"Starting VirtualBox VM: {vm_name}")
            return True
        except Exception as e:
            print(f"Failed to start VM: {e}")
            return False

    def stop_vm(self, vm_name: str):
        try:
            print(f"Stopping VirtualBox VM: {vm_name}")
            return True
        except Exception as e:
            print(f"Failed to stop VM: {e}")
            return False


class VMManagerApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="VM Manager")
        self.set_default_size(600, 400)

        self.vmware_handler = VMwareHandler()
        self.virtualbox_handler = VirtualBoxHandler()

        self.create_ui()

    def create_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Directory input
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, False, False, 0)

        label = Gtk.Label(label="VM Directory:")
        hbox.pack_start(label, False, False, 0)

        self.directory_entry = Gtk.Entry()
        hbox.pack_start(self.directory_entry, True, True, 0)

        find_button = Gtk.Button(label="Find VMs")
        find_button.connect("clicked", self.on_find_vms)
        hbox.pack_start(find_button, False, False, 0)

        # VM List
        self.vm_list_store = Gtk.ListStore(str, str)  # Name, Path
        self.vm_list = Gtk.TreeView(model=self.vm_list_store)

        for i, column_title in enumerate(["VM Name", "VM Path"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.vm_list.append_column(column)

        vm_list_scrolled = Gtk.ScrolledWindow()
        vm_list_scrolled.add(self.vm_list)
        vbox.pack_start(vm_list_scrolled, True, True, 0)

        # Start/Stop buttons
        button_box = Gtk.Box(spacing=6)
        vbox.pack_start(button_box, False, False, 0)

        self.start_button = Gtk.Button(label="Start VM")
        self.start_button.connect("clicked", self.on_start_vm)
        button_box.pack_start(self.start_button, True, True, 0)

        self.stop_button = Gtk.Button(label="Stop VM")
        self.stop_button.connect("clicked", self.on_stop_vm)
        button_box.pack_start(self.stop_button, True, True, 0)

    def on_find_vms(self, widget):
        directory = self.directory_entry.get_text()
        vm_paths = self.vmware_handler.find_vms(directory) + self.virtualbox_handler.find_vms(directory)
        self.vm_list_store.clear()
        for vm_path in vm_paths:
            vm_name = os.path.basename(vm_path)
            self.vm_list_store.append([vm_name, vm_path])

    def on_start_vm(self, widget):
        model, treeiter = self.vm_list.get_selection().get_selected()
        if treeiter is not None:
            vm_name = model[treeiter][0]
            vm_path = model[treeiter][1]
            if vm_path.endswith('.vmx'):
                self.vmware_handler.start_vm(vm_path)
            elif vm_path.endswith('.vbox'):
                self.virtualbox_handler.start_vm(vm_path)

    def on_stop_vm(self, widget):
        model, treeiter = self.vm_list.get_selection().get_selected()
        if treeiter is not None:
            vm_name = model[treeiter][0]
            vm_path = model[treeiter][1]
            if vm_path.endswith('.vmx'):
                self.vmware_handler.stop_vm(vm_path)
            elif vm_path.endswith('.vbox'):
                self.virtualbox_handler.stop_vm(vm_path)


def main():
    app = VMManagerApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
