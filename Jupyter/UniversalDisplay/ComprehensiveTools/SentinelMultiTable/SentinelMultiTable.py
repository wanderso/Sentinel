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
            a1 = SingleSentinelDisplay(value, table_classes, *args, **kwargs)
            self.single_displays.append(a1)
            a1.add_observer(self)

        self.children = tuple(self.single_displays)

    def observe_display(self, single_display):
        if self.selected_table is not None and self.selected_table is not single_display:
            self.selected_table.clear_selected_trait()
        self.selected_table = single_display

    def get_selected_entry(self):
        if self.selected_table is None:
            return None
        return self.selected_table.get_selected_entry()

    def add_classes_list(self, list_of_classes):
        for i in range(len(list_of_classes)):
            self.single_displays[i].append_class(list_of_classes[i])

    def remove_classes_list(self, list_of_classes):
        for i in range(len(list_of_classes)):
            self.single_displays[i].remove_class(list_of_classes[i])


class SingleSentinelDisplay(ipywidgets.VBox):
    def __init__(self, object_container: SentinelTableContainer, table_classes: List[str], *args, **kwargs):
        ipywidgets.VBox.__init__(self, *args, **kwargs)

        self._observers = []

        self.linked_objects: List[SentinelTableEntry] = object_container.get_traits()
        self.table_header = object_container.get_name()

        self.table_classes = list(table_classes)

        self.display_table = SentinelTable([], self.table_classes, self.table_header, *args, **kwargs)

        object_container.add_observer(self)
        self.display_table.add_observer(self)

        self.selected_trait = -1
        self.selected_table = False

        self.observe_event()

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
        if len(self.linked_objects) == 0:
            self.display_table.is_empty()
        else:
            self.display_table.is_full()
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
            self.display_table.clear_selected()

    def get_selected_entry(self):
        if self.selected_trait == -1:
            return None
        return self.linked_objects[self.selected_trait]

    def append_class(self, class_name):
        self.display_table.append_class(class_name)

    def remove_class(self, class_name):
        self.display_table.remove_class(class_name)
