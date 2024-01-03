class PlayerCharacter():
    def __init__(self, player_name, character_name, speed, damage, defense, health):
        self.player_name = player_name
        self.character_name = character_name
        self.speed = speed
        self.damage = damage
        self.defense = defense
        self.health = health
        pass

    def __str__(self) -> str:
        return "player_name : {} character_name : {} speed : {} damage : {} defense : {} health : {}".format(self.player_name, self.character_name, self.speed, self.damage, self.defense, self.health)
    
    def __repr__(self) -> str:
        return "player_name : {} character_name : {} speed : {} damage : {} defense : {} health : {}".format(self.player_name, self.character_name, self.speed, self.damage, self.defense, self.health)

    async def attack(self, target):
        damage = (self.damage * 3) - (target.defense * 2)
        return damage