from Sentinel.Core.dice import Dice
from Sentinel.Core.objective import Objective
from Sentinel.Core.character import Minion, Lieutenant
from Jupyter.UniversalDisplay.ComprehensiveTools.SentinelMultiTable.\
    SentinelTableInterface import SentinelTableEntry, SentinelTableContainer


class World:
    def __init__(self):
        self.environment_list = []
        self.scene_tracker = None
        self.entity_tracker = []
        self.active_entity = None
        self.challenge_list = []
        self.character_tracker = CharacterTracker()
        self._observers = []

    def add_observer(self, observ):
        self._observers.append(observ)

    def update_observers(self):
        for observ in self._observers:
            observ.observe_world()

    def add_entity(self, entity, ambush=False):
        new_tracker = TrackEntity(entity, ambush=ambush)
        self.entity_tracker.append(new_tracker)
        self.update_observers()

    def remove_entity(self, search_target):
        to_remove = self.find_entity(search_target)
        self.entity_tracker.remove(to_remove)
        self.update_observers()

    def add_objective(self, obj: Objective):
        self.challenge_list.append(obj)

    def get_objectives(self):
        primary_objectives = []
        secondary_objectives = []
        completed_objectives = []

        for objective in self.challenge_list:
            if objective:
                completed_objectives.append(objective)
            elif objective.is_main():
                primary_objectives.append(objective)
            else:
                secondary_objectives.append(objective)

        return primary_objectives, secondary_objectives, completed_objectives

    def set_scene_tracker(self, green, yellow, red):
        self.scene_tracker = SceneTracker(green, yellow, red)

    def get_scene_tracker(self):
        return self.scene_tracker

    def inc_scene_tracker(self):
        self.scene_tracker.advance_tracker()

    def set_character_tracker(self, ct):
        self.character_tracker = ct

    def get_character_tracker(self):
        return self.character_tracker

    def get_environment_list(self):
        return self.environment_list

    def set_environment(self, env):
        self.environment_list = [env]

    def add_environment(self, env):
        self.environment_list.append(env)


class CharacterTracker:
    def __init__(self):
        self.environment_list = []
        self.entity_tracker = []
        self.active_entity = None
        self._observers = []

    def add_observer(self, observ):
        self._observers.append(observ)

    def update_observers(self):
        for observ in self._observers:
            observ.observe_world()

    def create(self, input_data):
        if isinstance(input_data, str):
            (chara_type, die_val, name) = input_data.split(" ", 2)
            die = Dice(int(die_val.lstrip("d")))
            if chara_type == "Minion":
                new_chara = Minion(name, die)
                self.add_entity(new_chara)
            elif chara_type == "Lieutenant":
                new_chara = Lieutenant(name, die)
                self.add_entity(new_chara)

    def add_entity(self, entity, ambush=False):
        new_tracker = TrackEntity(entity, ambush=ambush)
        self.entity_tracker.append(new_tracker)
        self.update_observers()

    def remove_entity(self, search_target):
        to_remove = self.find_entity(search_target)
        self.entity_tracker.remove(to_remove)
        self.update_observers()

    def check_turn_over(self):
        for entity in self.entity_tracker:
            if not entity.check_acted():
                return False
        return True

    def reset_turn(self):
        for entity in self.entity_tracker:
            entity.set_acted(False)

    def hand_off(self, entity_hand):
        entity_now = self.find_entity(entity_hand)
        if self.active_entity == entity_now and len(self.entity_tracker) != 1:
            self.update_observers()
            return -1
        if self.active_entity is not None:
            self.active_entity.set_acted(True)
        if self.check_turn_over():
            self.reset_turn()
        elif entity_now.check_acted():
            self.active_entity.set_acted(False)
            self.update_observers()
            return -2
        self.active_entity = entity_now
        self.update_observers()
        return 1

    def find_entity(self, search_target):
        for entry in self.entity_tracker:
            if entry.get_entity() == search_target:
                return entry
        return None

    def get_active_entity(self):
        return self.active_entity

    def get_entity_status(self):
        has_moved = []
        is_moving = None
        not_moved = []
        for entry in self.entity_tracker:
            if entry == self.active_entity:
                is_moving = entry.get_entity()
            elif entry.check_acted():
                has_moved.append(entry.get_entity())
            else:
                not_moved.append(entry.get_entity())

        return not_moved, is_moving, has_moved

    def __str__(self):
        has_moved = []
        is_moving = None
        not_moved = []
        for entry in self.entity_tracker:
            if entry == self.active_entity:
                is_moving = entry
            elif entry.check_acted():
                has_moved.append(entry)
            else:
                not_moved.append(entry)

        retstr = str(self.get_scene_tracker()) + "\n\n"
        for entry in has_moved:
            retstr += str(entry.get_entity()) + " has already acted. \n"
        if is_moving:
            retstr += "\n" + str(is_moving.get_entity()) + " is the current actor. \n\n"
        elif len(has_moved) != 0 and len(not_moved) != 0:
            retstr += "\n"
        for entry in not_moved:
            retstr += str(entry.get_entity()) + " is ready to act. \n"

        return retstr


class TrackEntity:
    def __init__(self, entity, ambush=False):
        self.entity = entity
        self.acted = not ambush

    def set_acted(self, acted):
        self.acted = acted

    def check_acted(self):
        return self.acted

    def get_entity(self):
        return self.entity


class SceneTracker:
    def __init__(self, green, yellow, red):
        assert (green >= 0) and (yellow >= 0) and (red >= 0)
        self.index = 0
        self.tracker = []
        for _ in range(0, green):
            self.tracker.append("Green")
        for _ in range(0, yellow):
            self.tracker.append("Yellow")
        for _ in range(0, red):
            self.tracker.append("Red")
        self.tracker.append("End of Scene")
        self._observers = []

    def get_tracker(self):
        return self.tracker[self.index]

    def get_tracker_list(self):
        return self.tracker

    def get_index(self):
        return self.index

    def get_entry_at_index(self, ind):
        return self.tracker[ind]

    def advance_tracker(self, advance=1):
        if len(self.tracker)-1 <= self.index:
            retstr = "End of Scene"
        else:
            self.index += advance
            retstr = self.tracker[self.index]
        for entry in self._observers:
            entry.observe_tracker()
        return retstr

    def add_observer(self, observ):
        self._observers.append(observ)

    def __str__(self):
        retstr = ""
        navigate_index = 0
        for entry in self.tracker[:-1]:
            if navigate_index < self.index:
                retstr += ">" + entry + "< "
            elif navigate_index == self.index:
                retstr += "(" + entry + ") "
            else:
                retstr += " " + entry + "  "
            navigate_index += 1

        return retstr


class Environment(SentinelTableContainer):
    def __init__(self, name):
        self.environment_name = name
        self.trait_list = []
        self.stored_boosts = []
        self.twists = []
        self._observers = []

    def add_trait(self, trait_name, die_size=6, context={}):
        self.trait_list.append(EnvironmentTrait(trait_name, die_size, context=context))
        for entry in self._observers:
            entry.observe_environment()

    def get_name(self):
        return self.environment_name

    def get_traits(self):
        return self.trait_list

    def add_observer(self, observ):
        self._observers.append(observ)

    def __str__(self):
        retstr = "Environment: " + self.environment_name + "\n"
        for entry in self.trait_list:
            retstr += str(entry) + "\n"
        return retstr


class EnvironmentTrait(SentinelTableEntry):
    die_sizes = [("Minimal", 4), ("Average", 6), ("Challenging", 8), ("Dangerous", 10), ("Catastrophic", 12)]

    def __init__(self, trait_name, die_size, context={}):
        self._observers = []
        self.name = trait_name
        self.die = Dice(die_size)
        self.context = context
        self.stored_boosts = []

    def __str__(self):
        return self.name + " " + str(self.die)

    def increase_die(self):
        pass

    def decrease_die(self):
        pass

    def change_die(self, new_die_value):
        self.die = Dice(new_die_value)
        self.update_observers()

    def get_name(self):
        return str(self)

    def get_description(self):
        if "description" in self.context:
            return self.context["description"]
        else:
            return ""

    def add_observer(self, observ):
        self._observers.append(observ)

    def update_observers(self):
        for observ in self._observers:
            observ.observe_event()


if __name__ == "__main__":

    new_environment = Environment("Michelle's Gymnasium")
    new_environment.add_trait("Please Keep Floors Clean", 6)
    new_environment.add_trait("Fights Happen Anywhere...", 6)
    new_environment.add_trait("...But Are Won Here", 6)
    new_environment.add_trait("Terror Is Non-Negotiable", 8)

    print(str(new_environment))

    new_world = World()
    new_world.set_scene_tracker(2, 4, 2)

    new_world.add_entity("Placeholder Minion")
    new_world.add_entity("Placeholder Lieutenant")
    new_world.add_entity("Placeholder Ambusher", ambush=True)
    new_world.add_entity("Placeholder Eraser")
    new_world.remove_entity("Placeholder Eraser")

    print(new_world)
    new_world.hand_off("Placeholder Ambusher")
    print(new_world)
    new_world.hand_off("Placeholder Minion")
    print(new_world)
    new_world.hand_off("Placeholder Lieutenant")
    print(new_world)
    new_world.hand_off("Placeholder Minion")
    print(new_world)


