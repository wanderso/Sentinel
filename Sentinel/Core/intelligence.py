class Faction:
    def __init__(self, context={}):
        self.members = []
        self.faction_name = ""
        self.goals = []
        self.facts = []

    def add_member(self, member):
        if member not in self.members:
            self.members.append(member)

    def set_name(self, name):
        self.faction_name = name

    def add_goal(self, goal):
        if goal not in self.goals:
            self.goals.append(goal)

    def process_AI(self):
        pass

class Mob:
    def __init__(self):
        self.factions = []
        self.name = []
        self.goals = []
        self.facts = []