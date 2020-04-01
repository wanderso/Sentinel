import ipywidgets

from Sentinel.Core.character import Character, Lieutenant
from Sentinel.Core.world import World


class CharacterListDisplay(ipywidgets.VBox):
    def __init__(self, target_world : World, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_css_1 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/UniversalDisplay.css').read()))
        self.custom_css_2 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/Characters.css').read()))
        self.header = ipywidgets.HTML("<div class='component-header'>BRAID Sensor and Heartbeat Tracker - Characters</div>")
        self.single_displays = []

        self.target_tracker = target_world.get_character_tracker()
        self.target_tracker.add_observer(self)

        self.yet_to_act = []
        self.active = []
        self.acted = []

        self.ready_table = None
        self.active_character = None
        self.engaged_table = None

        self.selected_table = None

        self.refresh_cld()

    def observe_world(self):
        self.refresh_cld()

    def refresh_cld(self):
        self.yet_to_act, self.active, self.acted = self.target_tracker.get_entity_status()

        ready_table_text = "<table class='character-table ready'>\n" \
                           "<tr class='character-table ready'><th class='character-table ready'>"\
                           "{0}</th></tr>\n".format("Ready Characters")

        engaged_table_text = "<table class='character-table acted'>\n" \
                           "<tr class='character-table acted'><th class='character-table engaged'>" \
                           "{0}</th></tr>\n".format("Engaged Characters")

        for value in self.yet_to_act:
            csd = CharacterSingleDisplay(value)
            self.single_displays.append(csd)
            ready_table_text += str(csd)

        for value in self.acted:
            csd = CharacterSingleDisplay(value)
            self.single_displays.append(csd)
            engaged_table_text += str(csd)

        engaged_table_text += "</table>"

        ready_table_text += "</table>"

        if self.active is not None:
            active_display_text = "<div class='character-table active-character-header'>{0}</div>" \
                                  "<div class='character-table active-character-display'>{1}</div>"\
                                  .format("Active Character", str(self.active))

        else:
            active_display_text = ""

        self.ready_table = ipywidgets.HTML(ready_table_text)
        self.active_character = ipywidgets.HTML(active_display_text)
        self.engaged_table = ipywidgets.HTML(engaged_table_text)

        self.children = (self.custom_css_1, self.custom_css_2, self.header,
                         self.ready_table, self.active_character, self.engaged_table)


class CharacterSingleDisplay:
    def __init__(self, character_selected: Character, *args, **kwargs):
        self.associated_character = character_selected

    def __str__(self):
        character_short = str(self.associated_character)
        character_long = repr(self.associated_character)
        return "<tr class='character-table'><td class='character-table'>{0}" \
               "<div class='character-table-description hide-display' >{1}" \
               "</div></td></tr>\n".format(character_short, character_long)


