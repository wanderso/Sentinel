import ipywidgets

from Jupyter.Widgets.ImageWidgets import create_image_from_file, change_image_from_file

from Sentinel.Core.world import World, SceneTracker


class SceneTrackerDisplay(ipywidgets.VBox):
    def __init__(self, target_world: World, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tracker = target_world.get_scene_tracker()

        self.tray = SceneTrackerTray(self.tracker)
        self.custom_css = ipywidgets.HTML(
            "<style>{0}</style>".format(open('Jupyter/UniversalDisplay/UniversalDisplay.css').read()))

        self.title_label = ipywidgets.HTML("<div class='component-header'>Divinatio Tensiometer Universal Testing Machine - Scene Tracker</div>")

        self.children = (self.custom_css, self.title_label, self.tray)


class SceneTrackerTray(ipywidgets.HBox):
    def __init__(self, scene_tracker, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.green_box_cross = create_image_from_file("Jupyter/Images/SceneTracker/Green_Cross.png")
        self.yellow_box_cross = create_image_from_file("Jupyter/Images/SceneTracker/Yellow_Cross.png")
        self.red_box_cross = create_image_from_file("Jupyter/Images/SceneTracker/Red_Cross.png")
        self.green_box = create_image_from_file("Jupyter/Images/SceneTracker/Green_No_Cross.png")
        self.yellow_box = create_image_from_file("Jupyter/Images/SceneTracker/Yellow_No_Cross.png")
        self.red_box = create_image_from_file("Jupyter/Images/SceneTracker/Red_No_Cross.png")

        self.scene_tracker = self.set_scene_tracker(scene_tracker)
        self.scene_tracker.add_observer(self)

        self.index = 0
        self.tracker_list = []

        self.set_tracker_list()

    def set_scene_tracker(self, st: SceneTracker) -> SceneTracker:
        self.scene_tracker = st
        return st

    def set_tracker_list(self):
        tl = self.scene_tracker.get_tracker_list()
        self.index = self.scene_tracker.get_index()
        self.tracker_list = []
        tl_ex = []
        index2 = 0
        for entry in tl:
            if entry == "Green":
                if self.index > index2:
                    tl_ex.append("Jupyter/Images/SceneTracker/Green_Cross.png")
                else:
                    tl_ex.append("Jupyter/Images/SceneTracker/Green_No_Cross.png")
            elif entry == "Yellow":
                if self.index > index2:
                    tl_ex.append("Jupyter/Images/SceneTracker/Yellow_Cross.png")
                else:
                    tl_ex.append("Jupyter/Images/SceneTracker/Yellow_No_Cross.png")
            elif entry == "Red":
                if self.index > index2:
                    tl_ex.append("Jupyter/Images/SceneTracker/Red_Cross.png")
                else:
                    tl_ex.append("Jupyter/Images/SceneTracker/Red_No_Cross.png")
            index2 += 1

        children_to_add = tuple()

        for entry in tl_ex:
            new_widget = create_image_from_file(entry)
            children_to_add += (new_widget,)
            self.tracker_list.append(new_widget)

        self.children = children_to_add

    def observe_tracker(self):
        tl = self.scene_tracker.get_tracker_list()
        if len(tl)-1 != len(self.tracker_list):
            self.set_tracker_list()
            print("Setting tracker list - len(t1) {0}, len(self.tracker_list) {1}".format(len(tl), len(self.tracker_list)))
            return
        i1 = self.scene_tracker.get_index()
        while i1 > self.index:
            color = tl[self.index]
            if color == "Green":
                color = "Jupyter/Images/SceneTracker/Green_Cross.png"
            elif color == "Yellow":
                color = "Jupyter/Images/SceneTracker/Yellow_Cross.png"
            elif color == "Red":
                color = "Jupyter/Images/SceneTracker/Red_Cross.png"
            change_image_from_file(color, self.tracker_list[self.index])
            print("Changing file once")
            self.index += 1
