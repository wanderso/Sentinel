class Scene:
    def __init__(self):
        self.start_of_scene = []
        self.end_of_scene = []


class Turn:
    def __init__(self):
        self.start_of_turn = []
        self.actions_on_turn = []
        self.end_of_turn = []

        self.actions_taken = []

        self.character = None

    def insert_action_location(self, action, index=-1, WHICH_FLAG=0):
        target_array = None
        if WHICH_FLAG == 0:
            target_array = self.actions_on_turn
        elif WHICH_FLAG < 0:
            target_array = self.start_of_turn
        else:
            target_array = self.end_of_turn
        target_array.insert(index, action)

    def insert_start_action(self, action, index=-1):
        self.insert_action_location(action, index=index, WHICH_FLAG=-1)

    def insert_end_action(self, action, index=-1):
        self.insert_action_location(action, index=index, WHICH_FLAG=1)

    def insert_action(self, action, index=-1):
        self.insert_action_location(action, index=index, WHICH_FLAG=0)

    def __str__(self):
        retstr = ""
        if self.start_of_turn:
            start_string = ""
            for entry in self.start_of_turn:
                if start_string != "":
                    start_string += " " + entry
                else:
                    start_string += entry
            if retstr != "":
                retstr += "\n"
            retstr += "At the start of this turn, {}.".format(start_string)
        if self.actions_on_turn:
            action_string = ""
            for entry in self.actions_on_turn:
                if action_string != "":
                    action_string += " " + entry
                else:
                    action_string += entry
            if retstr != "":
                retstr += "\n"
            retstr += "{}.".format(action_string)
        if self.end_of_turn:
            end_string = ""
            for entry in self.end_of_turn:
                if end_string != "":
                    end_string += " " + entry
                else:
                    end_string += entry
            if retstr != "":
                retstr += "\n"
            retstr += "At the end of this turn, {}.".format(end_string)
        return retstr


class CharacterTimeline:
    def __init__(self, character, scene=None):
        self.scene = scene
        self.character = character
        self.turns = [Turn()]
        self.turn_index = 0

    def __getitem__(self, i):
        return self.access_turn(distance_from_index=i)

    def access_turn(self, distance_from_index=0):
        length_of_turns = len(self.turns)
        if length_of_turns <= self.turn_index + distance_from_index:
            if (distance_from_index + self.turn_index) >= 0:
                for _ in range(distance_from_index + self.turn_index - length_of_turns + 1):
                    new_turn = Turn()
                    self.turns.append(new_turn)
        elif self.turn_index + distance_from_index < 0:
            for _ in range(-(distance_from_index + self.turn_index)):
                new_turn = Turn()
                self.turns.insert(0,new_turn)
                self.turn_index += 1
            return self.turns[0]
        return self.turns[self.turn_index + distance_from_index]


class FullTimeline:
    def __init__(self):
        self.turns = []

    def add_turn(self, turn):
        self.turns.append(turn)

if __name__ == "__main__":
    timeline = CharacterTimeline("Details")
    two_before_now = timeline.access_turn(-2)
    two_before_now.insert_start_action("draw a card")
    two_before_now.insert_end_action("discard a card")
    two_after_now = timeline.access_turn(2)
    two_after_now.insert_action("draw two cards")
    for entry in timeline.turns:
        print("{" + str(entry) + "}")