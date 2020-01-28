from Sentinel.Core.dice import Dice, DicePool
from Sentinel.Core.character import Minion, Lieutenant


class Action:
    def __init__(self, context={}):
        self.dice_pool = None
        self.context = context
        self.on_stack = []
        self.before_dice_roll = []
        self.after_dice_roll = []
        self.after_resolution = []
        self.process_context()

    def process_context(self):
        pass

    def execute(self):
        for fxn in self.before_dice_roll:
            fxn(self.context)
        self.roll_dice()
        for fxn in self.after_dice_roll:
            fxn(self.context)
        self.execute_internals()
        for fxn in self.after_resolution:
            fxn(self.context)

    def execute_internals(self):
        # virtual method
        assert False

    def roll_dice(self):
        if self.dice_pool is None:
            return None
        elif type(self.dice_pool) == Dice:
            self.dice_pool.roll()
            pass
        elif type(self.dice_pool) == DicePool:
            self.dice_pool.roll()
            pass
        else:
            pass


class Attack(Action):
    def __init__(self, context={}):
        super().__init__(context=context)

    def process_context(self):
        self.action_type = "Attack"
        if 'target' in self.context:
            self.target = self.context['target']
        if 'source' in self.context:
            self.source = self.context['source']
        if 'dice_pool' in self.context:
            self.dice_pool = self.context['dice pool']
        else:
            source_type = type(self.source)
            if source_type == Minion or source_type == Lieutenant:
                self.dice_pool = self.source.get_current_die()
        if 'damage types' in self.context:
            self.types = self.context['damage types']
        else:
            self.types = ['Physical', 'Energy']


    def execute_internals(self):
        dam_val = 0
        if self.dice_pool is None:
            return None
        elif type(self.dice_pool) == Dice:
            dam_val = self.dice_pool.get_num()
        elif type(self.dice_pool) == DicePool:
            dam_val = self.dice_pool.get_mid()
        else:
            dam_val = self.dice_pool
        self.target.take_damage(dam_val)

    def __str__(self):
        return "Attack {}.".format(self.target)

if __name__ == "__main__":
    d1 = Dice(6, context={'debug': True})
    d2 = Dice(8, context={'debug': True})

    m1 = Minion("Combat Network Teuer", d1)
    m2 = Minion("Silens Combat Drone", d2)

    action1 = Attack(context={'target': m1, 'source': m2, 'damage types': ['Physical']})
    print(action1)
    action1.execute()

    print(m1.current_die.die)
