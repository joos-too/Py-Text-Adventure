import random


class Character:
    def __init__(self, hp, base_ad, armor, name):
        self.hp = hp
        self.base_ad = base_ad
        self.armor = armor
        self.name = name

    def get_hit(self, ad):
        if ad > self.armor:
            self.hp = self.hp - (ad - self.armor)
        elif ad <= self.armor:
            pass


class Enemies(Character):
    def __init__(self, hp, base_ad, armor, name, item, xp):
        Character.__init__(self, hp, base_ad, armor, name)
        self.item = item
        self.xp = xp

    def is_dead(self):
        if self.hp <= 0:
            print(f"{self.name} died.")
            return True
        elif self.hp > 0:
            print(f"{self.name} has {self.hp} HP left.")
            return False


class Goblin(Enemies):
    def __init__(self):
        Enemies.__init__(self, 100, 30, 0, "Goblin", Armor("Leather Armor", 5, 1, 10), 50)


class Ork(Enemies):
    def __init__(self):
        Enemies.__init__(self, 200, 50, 0, "Ork", Food("Orkmeat", 3, 2, 100), 100)


class GoblinWarrior(Enemies):
    def __init__(self):
        Enemies.__init__(self, 150, 50, 0, "Goblin Warrior", Weapon("Goblin Club", 4, 2, 20), 80)


class Player(Character):
    def __init__(self, hp, base_ad, armor, name):
        Character.__init__(self, hp, base_ad, armor, name)
        self.inventory = Inventory()
        self.xp = 0
        self.max_hp = hp
        self.lvl = 1
        self.ad = base_ad

    def get_hit(self, ad):  # Version mit Output für Spieler
        if ad > self.armor:
            self.hp = self.hp - (ad - self.armor)
            if self.hp <= 0:
                self.die()
            print(f"You have {self.hp} HP left.")
        elif ad <= self.armor:
            print(f"Your armor protected you and you have {self.hp} HP left")

    @staticmethod
    def die():
        exit("You died. Try again.")

    def toss(self):
        print("What do you want to toss? (Armor/Weapon/Eatables/Items)")
        s = str(input(">")).lower().strip()
        if s == "armor":
            if len(self.inventory.armors) > 0:
                print("What do you want to toss?")
                self.inventory.print_armors()
                x = int(input(">")) - 1
                print(f"You tossed {self.inventory.armors[x].name}")
                self.inventory.remove(self.inventory.armors[x])
            else:
                print("You have no Armor to toss.")
        elif s == "weapon":
            if len(self.inventory.weapons) > 0:
                print("What do you want to toss?")
                self.inventory.print_weapons()
                x = int(input(">")) - 1
                print(f"You tossed {self.inventory.weapons[x].name}")
                self.inventory.remove(self.inventory.weapons[x])
            else:
                print("You have no items to toss.")
        elif s == "eatables":
            if len(self.inventory.eatables) > 0:
                print("What do you want to toss?")
                self.inventory.print_eatables()
                x = int(input(">")) - 1
                print(f"You tossed {self.inventory.eatables[x].name}")
                self.inventory.remove(self.inventory.eatables[x])
            else:
                print("You have no eatables to toss.")
        elif s == "items":
            if len(self.inventory.items) > 0:
                print("What do you want to toss?")
                self.inventory.print_items()
                x = int(input(">")) - 1
                print(f"You tossed {self.inventory.items[x].name}")
                self.inventory.remove(self.inventory.items[x])
            else:
                print("You have no items to toss.")
        else:
            print("Thats no valid category. Try again...")

    def eat(self):
        if len(self.inventory.eatables) > 0:
            if self.hp < self.max_hp:
                print("What do you want to eat?")
                self.inventory.print_eatables()
                x = int(input(">")) - 1
                self.hp += self.inventory.eatables[x].hp
                print(f"You regenerated {self.inventory.eatables[x].hp} Hp")
                self.inventory.remove(self.inventory.eatables[x])
            else:
                print("You have already full Hp")
        else:
            print("You have nothing to eat.")

    def equip(self):
        print("What do you want to equip? (Armor/Weapon/Exit)")
        s = str(input(">")).lower().strip()
        if s == "armor":
            if len(self.inventory.armors) > 0:
                if self.inventory.armor.name != "-":
                    print("You need to unequip the other armor first.")
                else:
                    print("Which armor do you want to equip?")
                    self.inventory.print_armors()
                    x = int(input(">")) - 1
                    self.armor = self.inventory.armors[x].ap
                    self.inventory.armor = self.inventory.armors[x]
                    print(f"You equiped {self.inventory.armor.name}. You now have {self.armor} Armor")
                    self.inventory.remove(self.inventory.armors[x])
            else:
                print("You have no armor to equip.")
        elif s == "weapon":
            if len(self.inventory.weapons) > 0:
                if self.inventory.weapon.name != "-":
                    print("You need to unequip the other weapon first.")
                else:
                    print("Which weapon do you want to equip?")
                    self.inventory.print_weapons()
                    x = int(input(">")) - 1
                    self.ad = self.inventory.weapons[x].attack_damage + self.base_ad
                    self.inventory.weapon = self.inventory.weapons[x]
                    print(f"You equiped {self.inventory.weapon.name}. You are now making {self.ad} Damage")
                    self.inventory.remove(self.inventory.weapons[x])
            else:
                print("You have no weapon to equip")
        else:
            print("You exited the Equipmenu.")

    def unequip(self):
        print("What do you want to unequip? (Armor/Weapon/Exit)")
        s = str(input(">")).lower().strip()
        if s == "armor":
            if self.inventory.armor.name != "-":
                if self.inventory.append(self.inventory.armor):
                    print(f"You unequiped {self.inventory.armor.name}")
                    self.inventory.armor = Armor("-", 0, 0, 0)
            else:
                print("You have no armor to unequip.")
        elif s == "weapon":
            if self.inventory.weapon.name != "-":
                if self.inventory.append(self.inventory.weapon):
                    print(f"You unequiped {self.inventory.weapon.name}")
                    self.inventory.weapon = Weapon("-", 0, 0, 0)
            else:
                print("You have no weapon to unequip")

    def rest(self):
        self.hp = self.max_hp
        print("You rested and feel energized again.")

    def gain_xp(self, total_xp):
        self.xp += total_xp
        self.lvl_up()

    def get_xp_border(self):
        return int(round(100 * (1.05**(self.lvl-1))))

    def lvl_up(self):
        while self.xp >= self.get_xp_border():
            self.xp = self.xp - self.get_xp_border()
            if self.lvl < 100:
                self.lvl += 1
                print(f"Level up! You reached Level {self.lvl}.")
                self.base_ad += 5
                self.max_hp += 20
                self.hp += 20
                self.print_stats(True)

    def print_inventory(self):
        self.inventory.print_inventory()

    def print_stats(self, is_lvl_up):
        if is_lvl_up is False:
            print(f"Player {self.name}")
            print(f"Level: {self.lvl} ({self.xp}/{self.get_xp_border()} Xp)")
            print(f"Health Points: {self.hp}/{self.max_hp}")
            print(f"Armor: {self.armor}")
            print(f"Attack Damage: {self.ad}")
        else:
            print(f"Player {self.name}")
            print(f"Level: {self.lvl} ({self.xp}/{self.get_xp_border()} Xp)")
            print(f"Health Points: {self.hp}/{self.max_hp} (+20)")
            print(f"Armor: {self.armor}")
            print(f"Attack Damage: {self.ad} (+5)")


class Item:
    def __init__(self, name, weight, worth):
        self.weight = weight
        self.worth = worth
        self.name = name


class Food(Item):
    def __init__(self, name, weight, worth, hp):
        Item.__init__(self, name, weight, worth)
        self.hp = hp


class Weapon(Item):
    def __init__(self, name, weight, worth, attack_damage):
        Item.__init__(self, name, weight, worth)
        self.attack_damage = attack_damage


class Sword(Weapon):
    def __init__(self, name, weight, worth, attack_damage):
        Weapon.__init__(self, name, weight, worth, attack_damage)


class Armor(Item):
    def __init__(self, name, weight, worth, ap):
        Item.__init__(self, name, weight, worth)
        self.ap = ap


class Inventory:
    def __init__(self):
        self.items = []
        self.eatables = []
        self.armors = []
        self.weapons = []
        self.storage = 0
        self.max_storage = 10
        self.weapon = Weapon("-", 0, 0, 0)
        self.armor = Armor("-", 0, 0, 0)

    def print_inventory(self):
        print(f"Inventory ({self.storage}/{self.max_storage} kg):")
        print()
        print(f"Weapon: {self.weapon.name} ({self.weapon.attack_damage} Extra Damage)")
        print(f"Armor: {self.armor.name} ({self.armor.ap} Armor)")
        print()
        print("Items:")
        for i in self.items:
            print(f"{i.name}, {i.weight} kg")
        print("Eatables:")
        for i in self.eatables:
            print(f"{i.name}, {i.weight} kg, heals {i.hp} Hp")
        print("Armor:")
        for i in self.armors:
            print(f"{i.name}, {i.weight} kg, {i.ap} Armor")
        print("Weapons:")
        for i in self.weapons:
            print(f"{i.name}, {i.weight} kg, {i.attack_damage} Damage")

    def print_eatables(self):
        for i in range(len(self.eatables)):
            print(f"{i+1}.{self.eatables[i].name}")

    def print_armors(self):
        for i in range(len(self.armors)):
            print(f"{i+1}.{self.armors[i].name}")

    def print_weapons(self):
        for i in range(len(self.weapons)):
            print(f"{i+1}.{self.weapons[i].name}")

    def print_items(self):
        for i in range(len(self.items)):
            print(f"{i+1}.{self.items[i].name}")

    def append(self, item):
        if (self.storage + item.weight) > self.max_storage:
            print("Your bag is full and you need to make space.")
            return False
        else:
            if isinstance(item, Armor):
                self.armors.append(item)
            elif isinstance(item, Weapon):
                self.weapons.append(item)
            elif isinstance(item, Food):
                self.eatables.append(item)
            else:
                self.items.append(item)
            self.storage += item.weight
            return True

    def remove(self, item):
        if isinstance(item, Armor):
            self.armors.remove(item)
        elif isinstance(item, Weapon):
            self.weapons.remove(item)
        elif isinstance(item, Food):
            self.eatables.remove(item)
        else:
            self.items.remove(item)
        self.storage -= item.weight


class Field:
    def __init__(self, enemies, safe_place):
        self.enemies = enemies  # List of enemies
        self.loot = []  # List of items
        self.safe_place = safe_place

    @staticmethod
    def gen_random():
        rand = random.randint(0, 3)
        if rand == 0:
            return Field([], True)
        if rand == 1:
            return Field([Ork(), Goblin()], False)
        if rand == 2:
            return Field([Goblin()], False)
        if rand == 3:
            return Field([Goblin(), GoblinWarrior()], False)

    def print_state(self):
        print()
        print("You look around and see:")
        for i in self.enemies:
            print(i.name)
        for i in self.loot:
            print(i.name)
        if len(self.enemies) == 0 and len(self.loot) == 0 and self.safe_place is False:
            print("Nothing special.")
        if self.safe_place is True:
            print("A place to rest.")


class Map:
    def __init__(self, width, height):
        self.state = []
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        for i in range(width):
            fields = []
            for j in range(height):
                fields.append(Field.gen_random())
            self.state.append(fields)

    def print_state(self):
        self.state[self.x][self.y].print_state()

    def print_map(self):
        print("Map (Your position x):")
        for i in range(self.height-1, -1, -1):
            for j in range(self.width):
                if i == self.y and j == self.x:
                    print("x", end=" ")
                else:
                    print("-", end=" ")
            print("")

    def right(self):
        if self.x == len(self.state)-1:
            print("You see huge mountains, which you can't pass.")
        elif len(self.state[self.x][self.y].enemies) == 0:
            self.x += 1
        else:
            print("The Enemies are blocking your way!")

    def left(self):
        if self.x == 0:
            print("You see a wild river, which you can't cross safely.")
        elif len(self.state[self.x][self.y].enemies) == 0:
            self.x -= 1
        else:
            print("The Enemies are blocking your way!")

    def forward(self):
        if self.y == len(self.state[self.x])-1:
            print("You see cliffs, but you can't jump safely")
        elif len(self.state[self.x][self.y].enemies) == 0:
            self.y += 1
        else:
            print("The Enemies are blocking your way!")

    def backward(self):
        if self.y == 0:
            print("You see a giant lake and you can spot large glowing eyes under the surface.")
        elif len(self.state[self.x][self.y].enemies) == 0:
            self.y -= 1
        else:
            print("The Enemies are blocking your way!")

    def get_enemies(self):
        return self.state[self.x][self.y].enemies

    def get_loot(self):
        return self.state[self.x][self.y].loot

    def get_rest(self):
        return self.state[self.x][self.y].safe_place
