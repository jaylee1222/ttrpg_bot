class Monster:
    def __init__(self, modifier, name) -> None:
        self.modifier = modifier
        self.name = name
        self.attacks = None
        self.health = None
        pass

    def printMonster(self):
        return f"{self.modifier} {self.name}"