import json
import random
import dungeon

try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

title = "DUNGEON: THE SILENT WELL"
frame = "=" * 31

print(frame)
print(title)
print(frame)

print("What is the hero's name?")
hero_name = input()
print(f"Welcome, {hero_name}!")
print("You enter the dungeon. Dark and damp.")
print()

print("Hero setup.")
print("Health, strength, agility, endurance — one number per line:")
while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
    except ValueError:
        print("Oops: one of the lines is not a number. Enter all four again:")
        continue
    try:
        if health <= 0:
            raise ValueError(f"Health must be positive, but {health} was entered")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Characteristics cannot be negative")
        break
    except ValueError as e:
        print(f"{e}. Enter all four again:")

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // 10 + endurance
max_health = health
max_stamina = stamina

print("Hero characteristics:")
print(f"Health:    {health}")
print(f"Strength:  {strength}")
print(f"Agility:   {agility}")
print(f"Endurance: {endurance}")
print()
print(f"Hero damage: {damage:.1f}")
print(f"Critical damage: {crit_damage:.1f}")
print(f"Stamina reserve: {stamina}")
print()

enemies = ["ghoul", "skeleton", "spider", "bat"]
log = []
gold_total = 0
ability_bonus = 0
inventory = {}

MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]
hero_r, hero_c = 4, 2
visited = {(4, 2)}
LOOT = {(1, 1): "old coin", (2, 3): "dusty potion", (3, 3): "guard's gem"}
found_loot = set()
DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}

def print_leaderboard(log):
    """Печатает топ-3 раундов по урону героя и рекорд врага.
    Возвращает None: контракт функции — печать, а не данные.
    """
    if not log:
        print("You haven't fought yet.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")
    worst = max(log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")


def print_run_summary(log):
    """Печатает итог забега: суммарный и средний урон героя.
    Возвращает None. Безопасна на пустом журнале.
    """
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")


def scout(r, c, seen):
    """Рекурсивно считает комнаты, достижимые из клетки (r, c).
    seen — множество уже посчитанных клеток, общее на весь обход.
    Нижний ряд карты не закрыт стеной (там вход S), поэтому
    выход за границы проверяется так же, как стена.
    Возвращает число комнат, ничего не печатает.
    """
    if not (0 <= r < len(MAP) and 0 <= c < len(MAP[r])):
        return 0
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


def write_save():
    """Собирает состояние забега и пишет его в save.json.
    Кортежи и множества превращает в списки: JSON их не знает.
    Кроме образца сохраняет характеристики, потолки, надбавку,
    рюкзак и журнал — без них продолжение не восстановит урон и итог.
    Возвращает None.
    """
    save = {}
    save["hero"] = hero_name
    save["health"] = health
    save["stamina"] = stamina
    save["gold"] = gold_total
    save["actions"] = actions
    save["strength"] = strength
    save["agility"] = agility
    save["endurance"] = endurance
    save["max_health"] = max_health
    save["max_stamina"] = max_stamina
    save["bonus"] = ability_bonus
    save["inventory"] = inventory
    save["log"] = log
    save["enemies"] = enemies
    save["position"] = [hero_r, hero_c]
    save["visited"] = [list(p) for p in visited]
    save["loot"] = sorted(found_loot)
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)


num_to_verb = {"1": "look", "2": "go", "3": "rest", "4": "listen",
               "5": "torch", "6": "train", "7": "descend", "8": "leaders",
               "9": "shop", "10": "backpack", "11": "drink", "0": "exit"}

commands = ["look", "go", "rest", "listen", "torch", "train", "descend",
            "leaders", "shop", "backpack", "drink potion",
            "buy <item> [count]", "go <north|south|west|east>", "map", "scout", "exit"]
MENU = ["What do you do? (number or command; help for help)",
        "1 - look around (look)",
        "2 - go forward (go)",
        "3 - rest (rest)",
        "4 - listen (listen)",
        "5 - light a torch (torch)",
        "6 - train (train)",
        "7 - descend deeper (descend)",
        "8 - leaderboard (leaders)",
        "9 - shop (shop)",
        "10 - backpack (backpack)",
        "11 - drink potion (drink)",
        "map - dungeon map",
        "scout - count reachable rooms",
        "0 - exit the dungeon (exit)"]

running = True
actions = 0
outcome = "interrupt"
try:
    while running:
        print("\n".join(MENU))
        print()

        line = input()
        cmd = line.strip().lower()
        while cmd == "":
            print("Empty command. Type a command or number.")
            line = input()
            cmd = line.strip().lower()
        words = cmd.split()
        verb = words[0]
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]

        match verb:
            case "look":
                print("You look around. The room is empty, only dust on the floor.")

            case "go":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"You found {item}! Unique loot: {len(found_loot)}.")
                        print(f"You step {words[1]}. Room ({hero_r}, {hero_c}).")
                    else:
                        print(f"Cannot go {words[1]}: wall or edge.")
                else:
                    cost = 2
                    if stamina >= cost:
                        stamina -= cost
                        print("You go forward carefully. The floor creaks under your feet.")
                    else:
                        health -= cost - stamina
                        stamina = 0
                        print("No strength left — you keep going on sheer stubbornness.")

            case "rest":
                stamina = stamina + 3
                print("You sit on the floor and catch your breath. Strength returns.")

            case "listen":
                print("You listen. Somewhere far away water is dripping.")

            case "torch":
                stamina = stamina - 1
                print("You light a torch. Old inscriptions appear on the walls.")

            case "train":
                strikes = 5
                total_damage = 0
                crit_count = 0
                print("You walk up to the training dummy.")
                print("It has stood here since the last seeker came by.")
                print()
                print(f"You strike {strikes} times.")
                for i in range(1, strikes + 1):
                    hit_damage, crit = dungeon.hero_hit(i, damage, crit_damage)
                    if crit:
                        crit_count += 1
                        print(f"Strike {i}: {hit_damage:.1f} — critical!")
                    else:
                        print(f"Strike {i}: {hit_damage:.1f}")
                    total_damage += hit_damage
                stamina = stamina - 1
                print()
                print(f"Total: {strikes} strikes, {crit_count} critical.")
                print(f"Total damage: {total_damage:.1f}")
                print(f"Average damage: {total_damage / strikes:.1f}")

            case "descend":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health, loot = dungeon.fight(enemy, health, ability_bonus, damage, crit_damage)
                    for r in rounds:
                        log.append(r)
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        win_line = f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon. Loot: {loot} gold."
                        if COLOR:
                            print(Fore.YELLOW + win_line + Style.RESET_ALL)
                        else:
                            print(win_line)
                    print(f"Battle: {len(rounds)} rounds.")

            case "leaders":
                print_leaderboard(log)

            case "shop":
                print("Shop:")
                for name, price in dungeon.prices.items():
                    print(f"{name}: {price} gold")

            case "buy":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])
                if item == "":
                    print("Buy what? Type: buy <item>.")
                    continue
                if item not in dungeon.prices:
                    print("No such item in the shop.")
                    continue
                if qty <= 0:
                    print("Quantity must be a positive number.")
                    continue
                gold_total, ok = dungeon.buy(dungeon.prices[item], gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    print(f"Bought {qty} {item} for {dungeon.prices[item] * qty} gold. Gold left: {gold_total}.")
                else:
                    print(f"Not enough gold: need {dungeon.prices[item] * qty}, have {gold_total}.")

            case "backpack":
                if not inventory:
                    print("Backpack is empty.")
                else:
                    print("Backpack:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} pcs")

            case "drink":
                item = " ".join(words[1:]) or "potion"
                if inventory.get(item, 0) == 0:
                    print(f"No {item} in the backpack.")
                else:
                    health = min(health + 10, max_health)
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    print(f"You drink a {item}. Health: {health}. Potions left: {inventory.get(item, 0)}.")

            case "map":
                print("Map:")
                for i in range(len(MAP)):
                    cells = []
                    for j in range(len(MAP[i])):
                        cell = "@" if (i, j) == (hero_r, hero_c) else MAP[i][j]
                        cells.append(cell)
                    print(" ".join(cells))

            case "scout":
                seen = set()
                print(f"Scout: {scout(hero_r, hero_c, seen)} rooms reachable.")

            case "help":
                print("Commands: " + ", ".join(commands) + ".")
                print("Numbers 0-11 work as before.")

            case "exit":
                print("You climb back toward the light. The dungeon stays behind.")
                write_save()
                print("Progress saved.")
                outcome = "exit"
                running = False

            case _:
                print(f"Don't understand command: '{line.strip()}'. Type 'help'.")
                continue

        if running:
            actions += 1
            print()
            state = f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)} Gold: {gold_total}"
            if COLOR:
                print(Fore.GREEN + state + Style.RESET_ALL)
            else:
                print(state)

        if health <= 0:
            print(f"{hero_name} falls. The dungeon claims another seeker.")
            outcome = "death"
            running = False
except KeyboardInterrupt:
    print()
    print("The player ended the session.")
finally:
    if inventory:
        print("Left behind in the backpack:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} pcs")
    else:
        print("Left behind in the backpack: nothing.")
    print(frame)
    if outcome == "death":
        print(f"You didn't make it, {hero_name}. Actions: {actions}.")
    elif outcome == "exit":
        print(f"Run over, {hero_name}. Actions: {actions}.")
    else:
        print(f"Session interrupted, {hero_name}. Actions: {actions}.")
    print_run_summary(log)
    print(frame)
