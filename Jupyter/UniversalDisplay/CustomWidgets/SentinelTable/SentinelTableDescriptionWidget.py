from traitlets import Integer, Unicode, Bool, List, validate, observe, TraitError
from ipywidgets import DOMWidget, register, Output
from IPython.core.display import Javascript, display


@register
class SentinelTableDescriptionWidget(DOMWidget):
    _view_name = Unicode('SentinelTableDescriptionWidget').tag(sync=True)
    _view_module = Unicode('sentinel_table_description_widget').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)

    # Attributes
    entry_list = List().tag(sync=True)
    entry_descriptions = List().tag(sync=True)
    entry_descriptions_metadata = List().tag(sync=True)
    class_list = List().tag(sync=True)
    table_header = Unicode("").tag(sync=True)
    selected_value_index = Integer(-1, help="The index of the selected value.").tag(sync=True)
    disabled = Bool(False, help="Enable or disable user changes.").tag(sync=True)
    reset_flag = Bool(False).tag(sync=True)
    expandable = Bool(False).tag(sync=True)

    def __init__(self, list_reference: List, class_list: List, table_header: str = "No title",
                 expandable: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers = []
        self.entry_list = list_reference
        self.class_list = class_list
        self.table_header = table_header
        self.expandable = expandable
        self.js_handler = TableDescriptionWidgetJavascriptHandler()
        self.js_handler.activate_javascript()

    def add_observer(self, observ):
        self._observers.append(observ)

    @observe('selected_value_index')
    def on_selection_change(self, change):
        for observ in self._observers:
            observ.update_observers(self.selected_value_index)

    def set_entries(self, list_data, entry_descriptions=None):
        self.entry_list = list_data
        if not entry_descriptions:
            self.entry_descriptions = [""] * len(self.entry_list)
        else:
            self.entry_descriptions = entry_descriptions

    @validate('selected')
    def _valid_value(self, proposal):
        if proposal['value'] not in self.entry_list:
            raise TraitError('Selected entry not found in dictionary')
        return proposal['value']

    def get_selected_value(self):
        if self.selected_value_index >= 0:
            return self.entry_list[self.selected_value_index]
        else:
            return None

    def clear_selected(self):
        self.reset_flag = not self.reset_flag

    def append_class(self, class_name):
        new_list = list(self.class_list)
        new_list.append(class_name)
        self.class_list = new_list

    def erase_class(self, class_name):
        new_list = list(self.class_list)
        new_list.remove(class_name)
        self.class_list = new_list

    def is_full(self):
        if "empty" in self.class_list:
            self.erase_class("empty")

    def is_empty(self):
        if "empty" not in self.class_list:
            self.append_class("empty")


class TableDescriptionWidgetJavascriptHandler(Output):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def activate_javascript(self):
        with self:
            carrie = Javascript(open("Jupyter\\UniversalDisplay\\CustomWidgets" +
                                     "\\SentinelTable\\sentinel_table_description_widget.js", 'r').read())
            display(carrie)
