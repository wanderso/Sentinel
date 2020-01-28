import ipywidgets

from Sentinel.Core.world import Environment, EnvironmentTrait


class EnvironmentDisplay(ipywidgets.VBox):
    def __init__(self, environment_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_css = ipywidgets.HTML("<style>{0}</style>".format(open('Jupyter/UniversalDisplay/UniversalDisplay.css').read()))
        self.header = ipywidgets.HTML("<div class='component-header'>Commlink Situational Awareness Scanner - Environments</div>")
        self.single_displays = []

        for value in environment_list:
            self.single_displays.append(SingleEnvironmentDisplay(value))

        self.children = (self.custom_css, self.header,) + tuple(self.single_displays)


class SingleEnvironmentDisplay(ipywidgets.VBox):
    def __init__(self, env: Environment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.associated_environment = env

        env_name = self.associated_environment.get_name()
        trl = self.associated_environment.get_traits()

        table_text = "<table class='environment-table'>\n" \
                     "<tr class='environment-table'><th class='environment-table'>{0}</th></tr>\n".format(env_name)

        for value in trl:
            table_text += "<tr class='environment-table'><td class='environment-table'>{0}<td></tr>\n".format(str(value))

        table_text += "</table>"

        self.environment_table = ipywidgets.HTML(table_text)
        self.children = (self.environment_table,)