import ipywidgets
from IPython.core.display import Javascript, display
from Sentinel.Core.world import Environment, EnvironmentTrait, World
from Jupyter.UniversalDisplay.CustomWidgets.SentinelTable.SentinelTable import SentinelTable


class EnvironmentDisplay(ipywidgets.VBox):
    def __init__(self, target_world: World, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_css_1 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/UniversalDisplay.css').read()))
        self.custom_css_2 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/Environment.css').read()))
        self.header = ipywidgets.HTML("<div class='component-header'>Commlink Situational Awareness Scanner - Environments</div>")

        self.debug_readout = ipywidgets.Output()

        self.selected_table = None
        self.single_displays = []

        self.environment_list = target_world.get_environment_list()

        for value in self.environment_list:
            a1 = SingleEnvironmentDisplay(value)
            self.single_displays.append(a1)
            a1.add_observer(self)

        self.children = (self.custom_css_1, self.custom_css_2, self.header) + tuple(self.single_displays) + \
                        (self.debug_readout,)

    def observe_display(self, single_display):
        if self.selected_table is not None and self.selected_table is not single_display:
            self.selected_table.clear_selected_trait()
        self.selected_table = single_display


class SingleEnvironmentDisplay(ipywidgets.VBox):
    def __init__(self, env: Environment, *args, **kwargs):
        ipywidgets.VBox.__init__(self, *args, **kwargs)

        self.associated_environment = env
        self.associated_environment.add_observer(self)

        self._observers = []

        self.environment_table = SentinelTable([], ["environment-table"],
                                               self.associated_environment.get_name())

        self.environment_table.add_observer(self)

        self.selected_trait = -1
        self.selected_table = False

        self.observe_environment()

        self.children = (self.environment_table,)

    def add_observer(self, observ):
        self._observers.append(observ)

    def update_observers(self, selected_val_index):
        self.selected_trait = selected_val_index
        for observ in self._observers:
            if selected_val_index != -1:
                observ.observe_display(self)

    def update_table(self):
        trl = self.associated_environment.get_traits()
        new_list = []
        value_list = []
        for value in trl:
            new_list.append(str(value))
            desc_value = value.get_description()
            if desc_value:
                value_list.append(desc_value)
            else:
                value_list.append("")

        self.environment_table.set_entries(new_list, entry_descriptions=value_list)

    def observe_environment(self):
        self.update_table()

    def clear_selected_trait(self):
        if self.selected_trait is not None and self.selected_trait != -1:
            self.environment_table.clear_selected()
