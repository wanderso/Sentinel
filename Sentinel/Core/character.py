from Core.dice import Dice


class Character:
    def __init__(self, name, context={}):
        self.abilities = []
        self.timeline = None
        self.name = name
        self.world = None

    def set_timeline(self, timeline):
        self.timeline = timeline

    def get_timeline(self):
        return self.timeline

    def set_world(self, world):
        self.world = world

    def take_damage(self, damage):
        assert False

    def heal_damage(self, heal_count):
        assert False

    def perform_action(self):
        pass

    def remove(self):
        assert False

    def __str__(self):
        return str(self.name)


class Minion(Character):
    def __init__(self, name, die, context={}):
        super().__init__(name, context=context)
        self.name = name
        self.max_die = die
        self.value = None
        self.current_die = Dice(self.max_die.get_die_size(), context=self.max_die.get_context())

    def get_current_die(self):
        return self.current_die

    def roll_die(self):
        self.value = self.current_die.roll()
        return self.value

    def take_damage(self, damage):
        self.roll_die()
        damage_save = self.value
        if damage_save >= damage and self.current_die.get_die_size() != Dice.Minimum_Size:
            self.current_die.decrease_die_size()
        else:
            self.remove()

    def heal_damage(self, heal_count):
        for _ in range (0, heal_count):
            if self.current_die.get_die_size() < self.max_die.get_die_size():
                self.current_die.increase_die_size()

    def remove(self):
        print("Removing %s" % self.name)
        if self.world:
            self.world.remove_entity(self)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        if self.current_die.get_die_size() == self.max_die.get_die_size():
            repr_str = "%s (Minion d%d)" % (self.name, self.max_die.get_die_size())
        else:
            repr_str = "%s (Minion d%d [d%d])" % (self.name, self.max_die.get_die_size(), self.current_die.get_die_size())
        return repr_str


class Lieutenant(Character):
    def __init__(self, name, die, context={}):
        super().__init__(name, context=context)
        self.name = name
        self.max_die = die
        self.value = None
        self.current_die = Dice(self.max_die.get_die_size(), context=self.max_die.get_context())

    def get_current_die(self):
        return self.current_die

    def roll_die(self):
        self.value = self.current_die.roll()
        return self.value

    def take_damage(self, damage):
        self.roll_die()
        damage_save = self.value
        if damage_save < damage:
            if self.current_die.get_die_size() == 4:
                self.remove()
            else:
                self.current_die.decrease_die_size()

    def heal_damage(self, heal_count):
        for _ in range (0, heal_count):
            if self.current_die.get_die_size() < self.max_die.get_die_size():
                self.current_die.increase_die_size()

    def remove(self):
        print("Removing %s" % self.name)
        if self.world:
            self.world.remove_entity(self)


    def __str__(self):
        if self.current_die.get_die_size() == self.max_die.get_die_size():
            repr_str = "%s (Lieutenant d%d)" % (self.name, self.max_die.get_die_size())
        return repr_str




if __name__ == "__main__":
    d1 = Dice(6, context={'debug':True})
    d2 = Dice(8, context={'debug':True})
    m1 = Minion("Combat Network Teuer", d1)
    m2 = Minion("Silens Combat Drone", d2)

    m2.take_damage(m1.roll_die())
    m1.take_damage(m2.roll_die())

    print(repr(m1))
    print(repr(m2))


