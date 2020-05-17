import ipywidgets

from Sentinel.Core.world import World

from Jupyter.UniversalDisplay.ComprehensiveTools.SentinelMultiTable.SentinelMultiTable import SentinelMultiTable


class CharacterListDisplay(ipywidgets.VBox):
    def __init__(self, target_world: World, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_css_1 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/UniversalDisplay.css').read()))
        self.custom_css_2 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/Characters.css').read()))
        self.header = ipywidgets.HTML("<div class='component-header'>BRAID Sensor and Heartbeat Tracker - Characters</div>")
        self.single_displays = []

        self.target_tracker = target_world.get_character_tracker()
        self.target_tracker.add_observer(self)

        self.alt_display = SentinelMultiTable(self.target_tracker.get_tracker_list(), ['character-table'])
        extra_classes = ["ready", "active", "engaged"]

        self.alt_display.add_classes_list(extra_classes)

        self.refresh_cld()

    def observe_world(self):
        self.refresh_cld()

    def refresh_cld(self):
        self.children = (self.custom_css_1, self.custom_css_2, self.header, self.alt_display)


