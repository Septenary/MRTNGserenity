import dataclasses
from .players import GameClass, Player, Spec
from . import errorlog

@dataclasses.dataclass
class Raid:
    players: list[Player] = dataclasses.field(default_factory=list)

    def add_player(self, Player):
        self.players.append(Player)

    def getplayers(self, gameclass: GameClass, spec: Spec = None) -> list[Player]:
        if isinstance(gameclass, GameClass):
            gc = gameclass
        if isinstance(gameclass, str):
            gc = GameClass(gameclass.upper())
        
        if spec:
            if isinstance(spec, Spec):
                sp = spec
            if isinstance(spec, str):
                sp = Spec(spec.upper())
            return [x for x in self.players if x.gameclass == gc and x.spec == sp]
        else:
            return [x for x in self.players if x.gameclass == gc]

    def getplayers_by_classspec(self, gameclass: GameClass, spec: Spec = None) -> Player:
        try:
            return self.getplayers(gameclass=gameclass, spec=spec)
        except:
            errorlog.add(f"No match found for gameclass: {gameclass}, spec: {spec}")

    def getplayers_by_flag(self, flag: str, value: any) -> list[Player]:
        ret = [x for x in self.players if x.role.__dict__[flag] == value]
        if ret == []:
            errorlog.add(f"No matches found for a player with flag '{self.flag}'.")
        return ret

    def getplayer_by_name(self, name: str, errors: bool = True) -> Player:
        for player in self.players:
            if player.name.upper() == name.upper():
                return player
        if errors:
            errorlog.add(f"No player with name '{name}' is in the raid. Either correct the raid assignments, or correct raid composition.")

def load_raid(json_str: str) -> Raid:
    new_raid = Raid()

    for player in json_str["raidDrop"]:
        print(player)
