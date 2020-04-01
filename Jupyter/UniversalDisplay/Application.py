import ipywidgets as widgets

from Jupyter.UniversalDisplay.SceneTracker import SceneTrackerDisplay
from Jupyter.UniversalDisplay.Environment import EnvironmentDisplay
from Jupyter.UniversalDisplay.Characters import CharacterListDisplay
from Jupyter.UniversalDisplay.Objectives import ObjectiveDisplay

from Jupyter.RootClasses.Singleton import Singleton


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                **kwargs)
        return cls._instances[cls]

    @classmethod
    def __instancecheck__(mcs, instance):
        if instance.__class__ is mcs:
            return True
        else:
            return isinstance(instance.__class__, mcs)


class SentinelApplication(metaclass=Singleton):
    def __init__(self, world):
        self.app_window = ApplicationWindow(world)

    def receive_message(self, message):
        self.app_window.receive_message(message)

    def return_display(self):
        return self.app_window


class ApplicationWindow(widgets.VBox):
    def __init__(self, world, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.target_world = world

        self.st = SceneTrackerDisplay(self.target_world)
        self.sed = EnvironmentDisplay(self.target_world)
        self.cld = CharacterListDisplay(self.target_world)
        self.od = ObjectiveDisplay(self.target_world)

        self.children = (self.st, self.sed, self.cld, self.od)

    def receive_message(self, message):
        split_msg = message.split(" ", 2)
        if split_msg[0] == "environment":
            self.sed.recieve_message()
