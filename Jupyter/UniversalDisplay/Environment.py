import ipywidgets
from Sentinel.Core.world import World
from Jupyter.UniversalDisplay.ComprehensiveTools.SentinelMultiTable.SentinelMultiTable import SentinelMultiTable


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

        self.alt_display = SentinelMultiTable(self.environment_list, ["environment-table"])

        self.children = (self.custom_css_1, self.custom_css_2, self.header, self.alt_display, self.debug_readout)

    def observe_display(self, single_display):
        if self.selected_table is not None and self.selected_table is not single_display:
            self.selected_table.clear_selected_trait()
        self.selected_table = single_display

    def get_selected_trait(self):
        return self.alt_display.get_selected_entry()