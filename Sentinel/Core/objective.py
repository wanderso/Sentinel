class Objective:
    def __init__(self, obj_description, chal_list, is_main=False):
        self.description = obj_description
        self.main_objective = is_main
        self.challenge_list = chal_list

    def __bool__(self):
        for challenge in self.challenge_list:
            if not challenge:
                return False
        return True

    def __add__(self,other):
        if type(other) == int:
            for challenge in self.challenge_list:
                if not challenge:
                    challenge += other


class Challenge:
    def __init__(self, task_count, cha_description):
        self.count = task_count
        self.complete = 0
        self.description = cha_description

    def __bool__(self):
        return self.count <= self.complete

    def __add__(self, other):
        if type(other) == int:
            self.complete += other
        return self

    def __str__(self):
        return ("[X]"*self.complete) + ("[ ]"*(self.count-self.complete)) + " " + self.description

if __name__ == "__main__":
    new_cha = Challenge(2, "Defuse the bombs!")
    new_cha+1
    print(new_cha)