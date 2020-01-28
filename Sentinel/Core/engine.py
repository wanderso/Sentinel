import Sentinel.Core.action as Action
import Sentinel.Core.character as Character
import Sentinel.Core.dice as Dice
import Sentinel.Core.objective as Objective
import Sentinel.Core.results as Results
import Sentinel.Core.timeline as Timeline
import Sentinel.Core.world as World


class Engine:
    def __init__(self):
        self.world = World.World()
        self.hand_off_required = False
        self.stack = []

    def add_character(self, chara, context={}):
        ambush = False
        if 'ambush' in context:
            ambush = context['ambush']
        timeline = Timeline.CharacterTimeline(chara)
        chara.set_timeline(timeline)
        self.world.add_entity(chara, ambush=ambush)

        chara.set_world(self.world)

    def start_scene(self, green, yellow, red):
        self.world.set_scene_tracker(green, yellow, red)
        self.world.reset_turn()

    def execute_turn(self, turn):
        pass

    def place_action_on_stack(self, action):
        self.stack.append(action)

    def resolve_action(self):
        action = self.stack.pop()
        action.execute()


if __name__ == "__main__":
    world_engine = Engine()

    d6 = Dice.Dice(6, context={'debug': True})
    d8 = Dice.Dice(8, context={'debug': True})

    m1 = Character.Minion("Combat Network Teuer", d6)
    m2 = Character.Minion("Silens Combat Drone", d8)
    m3 = Character.Minion("Silens Combat Drone", d8)
    m4 = Character.Minion("Combat Network Teuer", d6)

    world_engine.add_character(m1)
    world_engine.add_character(m2)
    world_engine.add_character(m3)
    world_engine.add_character(m4)

    world_engine.start_scene(2, 4, 2)

    action1 = Action.Attack(context={'target': m1, 'source': m2, 'damage types': ['Physical']})

    world_engine.place_action_on_stack(action1)
    world_engine.resolve_action()

    print(world_engine.world)
