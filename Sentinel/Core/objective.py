from Jupyter.UniversalDisplay.ComprehensiveTools.SentinelMultiTable.\
    SentinelTableInterface import SentinelTableEntry


class Objective(SentinelTableEntry):
    def __init__(self, obj_description, chal_list, is_main=False):
        self.name = obj_description
        self.main_objective = is_main
        self.challenge_list = chal_list
        self.expanded = False
        self._observers = set()

        for entry in chal_list:
            if isinstance(entry, Challenge):
                entry.add_observer(self)

    def __bool__(self):
        for challenge in self.challenge_list:
            if not challenge:
                return False
        return True

    def __add__(self, other):
        if type(other) == int:
            for challenge in self.challenge_list:
                if not challenge:
                    challenge += other

    def get_name(self):
        return self.name

    def add_observer(self, observ):
        self._observers.add(observ)

    def observe_challenge(self):
        for observ in self._observers:
            observ.observe_objective()

    def get_description(self):
        chal_list = self.get_challenges()
        ret_str = ""
        for entry in chal_list:
            ret_str += str(entry) + "\n"
        return ret_str

    def get_challenges(self):
        list_ret = []
        for entry in self.challenge_list:
            list_ret.append(str(entry))
        return list_ret

    def is_main(self):
        return self.main_objective


class Challenge:
    def __init__(self, task_count, cha_description):
        self.count = task_count
        self.complete = 0
        self.description = cha_description
        self._observers = set()

    def __bool__(self):
        return self.count <= self.complete

    def __add__(self, other):
        if isinstance(other, int):
            self.complete += other
            for observ in self._observers:
                observ.observe_challenge()
        return self

    def __str__(self):
        return ("☑"*self.complete) + ("☐"*(self.count-self.complete)) + " " + self.description

    def add_observer(self, observ):
        self._observers.add(observ)


if __name__ == "__main__":
    new_cha = Challenge(2, "Defuse the bombs!")
    new_cha+1
    print(new_cha)
