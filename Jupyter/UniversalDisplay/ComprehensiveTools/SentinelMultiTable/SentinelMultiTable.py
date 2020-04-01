import ipywidgets
from typing import List
from Jupyter.UniversalDisplay.CustomWidgets.SentinelTable.SentinelTable import SentinelTable
from Jupyter.UniversalDisplay.ComprehensiveTools.SentinelMultiTable.\
    SentinelTableInterface import SentinelTableEntry, SentinelTableContainer


class SentinelMultiTable(ipywidgets.VBox):
    def __init__(self, contain_list: List[SentinelTableContainer], table_classes: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.selected_table = None

        self.single_displays = []

        self.table_list = contain_list

        for value in self.table_list:
            a1 = SingleSentinelDisplay(value, table_classes)
            self.single_displays.append(a1)
            a1.add_observer(self)

        self.children = tuple(self.single_displays)

    def receive_message(self, message_list):
        for entry in self.environment_list:
            entry.receive_message(message_list)

    def observe_display(self, single_display):
        if self.selected_table is not None and self.selected_table is not single_display:
            self.selected_table.clear_selected_trait()
        self.selected_table = single_display


class SingleSentinelDisplay(ipywidgets.VBox):
    def __init__(self, object_container: SentinelTableContainer, table_classes: List[str], *args, **kwargs):
        ipywidgets.VBox.__init__(self, *args, **kwargs)

        self._observers = []

        self.linked_objects: List[SentinelTableEntry] = list(object_container.get_traits())
        self.table_header = object_container.get_name()

        self.display_table = SentinelTable([], table_classes, self.table_header)

        self.display_table.add_observer(self)

        self.selected_trait = -1
        self.selected_table = False

        self.observe_environment()

        self.children = (self.display_table,)

    def add_observer(self, observ):
        self._observers.append(observ)

    def update_observers(self, selected_val_index):
        self.selected_trait = selected_val_index
        for observ in self._observers:
            if selected_val_index != -1:
                observ.observe_display(self)

    def update_table(self):
        name_list = []
        description_list = []
        for value in self.linked_objects:
            name_list.append(value.get_name())
            desc_value = value.get_description()
            if desc_value:
                description_list.append(desc_value)
            else:
                description_list.append("")

        self.display_table.set_entries(name_list, entry_descriptions=description_list)

    def observe_event(self):
        self.update_table()

    def clear_selected_trait(self):
        if self.selected_trait is not None and self.selected_trait != -1:
            self.environment_table.clear_selected()