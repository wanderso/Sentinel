import ipywidgets

from Sentinel.Core.world import World

from Jupyter.UniversalDisplay.ComprehensiveTools.SentinelMultiTable.SentinelMultiTable import SentinelMultiTable


class ObjectiveDisplay(ipywidgets.VBox):
    def __init__(self, target_world: World, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_css_1 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/UniversalDisplay.css').read()))
        self.custom_css_2 = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/Objectives.css').read()))
        self.header = ipywidgets.HTML("<div class='component-header'>Mission Focus and Targeting Computer - Objectives</div>")

        self.target_world = target_world
        self.target_objectives = target_world.get_objective_tracker()

        self.alt_display = SentinelMultiTable(self.target_objectives.get_tracker_list(), ['objective-table'], expandable=True)
        extra_classes = ["primary", "secondary", "completed"]
        self.alt_display.add_classes_list(extra_classes)

        self.primary_table = None
        self.secondary_table = None
        self.completed_table = None

        self.observe_objective()

    def observe_world(self):
        self.refresh_cld()

    def refresh_cld(self):
        self.children = (self.custom_css_1, self.custom_css_2, self.header, self.alt_display)

    def observe_objective(self):
        primary_table_text = "<table class='objective-table primary'>\n" \
                             "<tr class='objective-table primary'><th class='objective-table primary'>" \
                             "{0}</th></tr>\n".format("Primary Objectives")

        secondary_table_text = "<table class='objective-table secondary'>\n" \
                               "<tr class='objective-table secondary'><th class='objective-table secondary'>" \
                               "{0}</th></tr>\n".format("Secondary Objectives")

        completed_table_text = "<table class='objective-table complete'>\n" \
                               "<tr class='objective-table complete'><th class='objective-table complete'>" \
                               "{0}</th></tr>\n".format("Completed Objectives")

        (primary, secondary, completed) = self.target_world.get_objectives()

        for entry in primary:
            entry.add_observer(self)
            list_of_challenges = entry.get_challenges()

            add_text = "<tr class='objective-table'><td class='objective-table'>" \
                       "<table class='individual-objective-table'><tr><th>{0}</th></tr>".format(entry.get_description())

            for chal in list_of_challenges:
                add_text += "<tr><td class='individual-objective-table'>{0}</td></tr>".format(chal)

            add_text += "</table></tr>\n"

            primary_table_text += add_text

        for entry in secondary:
            entry.add_observer(self)
            list_of_challenges = entry.get_challenges()

            add_text = "<tr class='objective-table'><td class='objective-table'>" \
                       "<table class='individual-objective-table'><tr><th>{0}</th></tr>".format(entry.get_description())

            for chal in list_of_challenges:
                add_text += "<tr><td class='individual-objective-table'>{0}</td></tr>".format(chal)

            add_text += "</table></tr>\n"

            secondary_table_text += add_text

        for entry in completed:
            entry.add_observer(self)
            list_of_challenges = entry.get_challenges()

            add_text = "<tr class='objective-table'><td class='objective-table'>" \
                       "<table class='individual-objective-table'><tr><th>{0}</th></tr>".format(entry.get_description())

            for chal in list_of_challenges:
                add_text += "<tr><td class='individual-objective-table'>{0}</td></tr>".format(chal)

            add_text += "</table></tr>\n"

            completed_table_text += add_text

        primary_table_text += "</table>"
        secondary_table_text += "</table>"
        completed_table_text += "</table>"

        self.primary_table = ipywidgets.HTML(primary_table_text)
        self.secondary_table = ipywidgets.HTML(secondary_table_text)
        self.completed_table = ipywidgets.HTML(completed_table_text)

        self.children = (self.custom_css_1, self.custom_css_2, self.header,
                         self.primary_table, self.secondary_table, self.completed_table, self.alt_display)
