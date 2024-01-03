from dice import dungeon_dice_roll
class Monster:
    def __init__(self, modifier, name, speed, attacks, health, defense, damage) -> None:
        self.modifier = modifier
        self.name = modifier + " " + name
        self.speed = speed
        self.attacks = attacks
        self.health = health
        self.defense = defense
        self.damage = damage
        pass

    def __str__(self) -> str:
        return "modifier : {} name : {} speed : {} attacks : {} health : {} defense : {} damage : {}".format(self.modifier, self.name, self.speed, self.attacks, self.health, self.defense, self.damage)
    
    def __repr__(self) -> str:
        return "modifier : {} name : {} speed : {} attacks : {} health : {} defense : {} damage : {}".format(self.modifier, self.name, self.speed, self.attacks, self.health, self.defense, self.damage)
        
    # def __repr__(self) -> str:
    #     return {"modifier":self.modifier, "name":self.name, "speed":self.speed, "attacks":self.attacks, "health":self.health, "defense":self.defense, "damage":self.damage}
    
    async def attack(self, target):
        # index = adungeon_dice_roll(1, len(self.attacks) - 1)
        # attack = self.attacks[index]
        damage = (self.damage * 3) - (target.defense * 2)
        return damage

    def printMonster(self):
        return f"{self.modifier} {self.name}"