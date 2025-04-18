import random
import pickle
import classes as c


def forward(p, m):
    m.forward()


def right(p, m):
    m.right()


def left(p, m):
    m.left()


def backward(p, m):
    m.backward()


def save(p, m):
    x = str(input("Do you want to overwrite the current save state? (yes/no) ")).strip().lower()
    if x == "yes":
        print("Creating save state...")
        pickle.dump(p, open("save_player.dat", "wb"))
        pickle.dump(m, open("save_map.dat", "wb"))
    else:
        print("No save state was created!")


def quit_game(p, m):
    print("You leave this world")
    exit(0)


def print_help(p, m):
    keys = list(Commands.keys())
    print()
    print("Commands:")
    print(keys)


def pickup(p, m):
    loot = m.get_loot()
    looting = True
    while len(loot) > 0 and looting is True:
        print()
        print("What do you want to pickup? (Press 0 to stop Looting)")
        for i in range(len(loot)):         # Ausgabe des Loots
            print(f"{i+1}.{loot[i].name}")
        try:
            x = int(input(">")) - 1
            if x <= len(loot) and x > -1:
                if p.inventory.append(loot[x]):
                    print(f"You pickup {loot[x].name}")
                    loot.remove(loot[x])
                else:
                    looting = False
            elif x == -1:
                print("You stopped looting")
                looting = False
            else:
                print("Invalid Command")
        except ValueError:
            print("That was no valid number. Try again...")


def fight(p, m):
    enemies = m.get_enemies()
    loot = m.get_loot()
    total_xp = 0
    if len(enemies) > 0:
        while len(enemies) > 0:
            print()
            print("Who do you want to Attack? (Type the enemy's number.)")
            for i in range(len(enemies)):         # Ausgabe der Gegner
                print(f"{i+1}.{enemies[i].name}")
            try:
                x = int(input(">")) - 1
                print(f"You attack {enemies[x].name}")
                enemies[x].get_hit(p.ad)
                if enemies[x].is_dead():
                    total_xp += enemies[x].xp
                    loot.append(enemies[x].item)
                    enemies.remove(enemies[x])
            except (IndexError, ValueError):
                print("Oops! You missed.")
            for i in enemies:
                print(f"{i.name} attacks you.")
                p.get_hit(i.base_ad)
        print(f"You gain {total_xp} Xp")
        p.gain_xp(total_xp)
    else:
        print("There is no one to fight.")


def rest(p, m):
    enemies = m.get_enemies()
    rest = m.get_rest()
    if len(enemies) > 0:
        print("You can't rest. There are Enemies nearby.")
    elif rest is False:
        print("It is dangerous to rest here. Search a safe place.")
    else:
        p.rest()


def inventory(p, m):
    managing = True
    p.print_inventory()
    while managing is True:
        x = str(input("What do you want to do? (unequip/equip/eat/exit/toss) ")).lower().strip()
        if x == "exit":
            managing = False
        elif x == "equip":
            p.equip()
        elif x == "unequip":
            p.unequip()
        elif x == "eat":
            p.eat()
        elif x == "toss":
            p.toss()


def run(p, m):
    enemies = m.get_enemies()
    rand = random.randint(0, 3)
    if len(enemies) > 0:
        if rand == 0:
            enemies.clear()
            print("You escaped successfully!")
        else:
            print("You didn't manage to escape. The Monsters are attacking you!")
            fight(p, m)
    else:
        print("There is nothing to run from.")


def print_stats(p, m):
    p.print_stats(False)


def print_map(p, m):
    m.print_map()


Commands = {
    "help": print_help,
    "quit": quit_game,
    "pickup": pickup,
    "forward": forward,
    "right": right,
    "left": left,
    "backward": backward,
    "fight": fight,
    "save": save,
    "rest": rest,
    "inventory": inventory,
    "run": run,
    "stats": print_stats,
    "map": print_map,
    }

if __name__ == "__main__":
    x = str(input("Do you want to load an existing save state? (yes/no) ")).lower().strip()
    if x == "yes":
        player = pickle.load(open("save_player.dat", "rb"))
        map = pickle.load(open("save_map.dat", "rb"))
        print("Loading save state...")
        print(f"Welcome back {player.name}!")
    else:
        name = input("Enter your name: ")
        print()
        print(f"Hello {name}! Welcome to this World full of monsters, challenges, loot and new acquaintances.")
        print("Have Fun!")
        print()
        player = c.Player(500, 50, 0, name)
        map = c.Map(7, 7)
    print("(Type help to list the commands available)")
    map.print_state()
    while True:
        command = input(">").lower().strip()
        if command in Commands:
            Commands[command](player, map)
        else:
            print("Invalid Command!")
        map.print_state()
