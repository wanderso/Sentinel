from traitlets import Integer, Unicode, Bool, List, validate, observe, TraitError
from ipywidgets import DOMWidget, register, Output
from IPython.core.display import Javascript, display

from Jupyter.RootClasses.Singleton import Singleton

@register
class SentinelTable(DOMWidget):
    _view_name = Unicode('SentinelTable').tag(sync=True)
    _view_module = Unicode('sentinel_table').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)

    # Attributes
    entry_list = List().tag(sync=True)
    entry_descriptions = List().tag(sync=True)
    class_list = List().tag(sync=True)
    table_header = Unicode("").tag(sync=True)
    selected_value_index = Integer(-1, help="The index of the selected value.").tag(sync=True)
    disabled = Bool(False, help="Enable or disable user changes.").tag(sync=True)
    reset_flag = Bool(False).tag(sync=True)

    def __init__(self, list_reference: List, class_list: List, table_header: str = "No title", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers = []
        self.entry_list = list_reference
        self.class_list = list(class_list)
        self.table_header = table_header
        self.js_handler = TableJavascriptHandler()
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


class TableJavascriptHandler(Output):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def activate_javascript(self):
        with self:
            carrie = Javascript(open("Jupyter\\UniversalDisplay\\CustomWidgets" +
                                     "\\SentinelTable\\sentinel_table.js", 'r').read())
            display(carrie)
