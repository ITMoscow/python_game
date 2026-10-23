import random

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

def hero_hit(strike_n):
    """Урон героя в удар номер strike_n.
    Возвращает пару (hit, crit): урон и признак критического удара.
    Читает глобальные правила damage и crit_damage, не меняет ничего.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health):
    """Бой с enemy до гибели одного из двоих.
    Печатает строки раундов. Возвращает (rounds, won, hero_health):
    таблицу раундов, признак победы героя и здоровье после боя.
    Глобальные переменные не меняет: здоровье приходит параметром
    и возвращается новым значением.
    """
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy} emerges from the darkness!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        enemy_hp -= hit
        line = f"Round {round_n}: hero deals {hit:.1f}"
        if crit:
            line += " — critical!"
        else:
            line += "."
        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = random.randint(2, 6)
            hero_health -= blow
            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
    return rounds, enemy_hp <= 0, hero_health


menu_last = 8
running = True
actions = 0
outcome = "interrupt"
try:
    while running:
        print("What do you do?")
        print("1 - look around")
        print("2 - go forward")
        print("3 - rest")
        print("4 - listen")
        print("5 - light a torch")
        print("6 - train")
        print("7 - descend deeper")
        print("8 - leaderboard")
        print("0 - exit the dungeon")

        while True:
            choice = input()
            try:
                menu_number = int(choice)
            except ValueError:
                print("No such option. Enter an option number from the menu.")
                continue
            if 0 <= menu_number <= menu_last:
                break
            print("No such option. Enter an option number from the menu.")
        choice = str(menu_number)

        match choice:
            case "1":
                print("You look around. The room is empty, only dust on the floor.")

            case "2":
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("You go forward carefully. The floor creaks under your feet.")
                else:
                    health -= cost - stamina
                    stamina = 0
                    print("No strength left — you keep going on sheer stubbornness.")

            case "3":
                stamina = stamina + 3
                print("You sit on the floor and catch your breath. Strength returns.")

            case "4":
                print("You listen. Somewhere far away water is dripping.")

            case "5":
                stamina = stamina - 1
                print("You light a torch. Old inscriptions appear on the walls.")

            case "6":
                strikes = 5
                total_damage = 0
                crit_count = 0
                print("You walk up to the training dummy.")
                print("It has stood here since the last seeker came by.")
                print()
                print(f"You strike {strikes} times.")
                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i)
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

            case "7":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health = fight(enemy, health)
                    for r in rounds:
                        log.append(r)
                    if won:
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                    print(f"Battle: {len(rounds)} rounds.")

            case "8":
                if not log:
                    print("You haven't fought yet.")
                else:
                    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
                    print("Leaderboard (hero damage):")
                    for i in range(len(top)):
                        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")
                    worst = max(log, key=lambda r: r[2])
                    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")

            case "0":
                print("You climb back toward the light. The dungeon stays behind.")
                outcome = "exit"
                running = False

            case _:
                print("No such action.")

        if running:
            actions += 1
            print()
            print(f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)}")

        if health <= 0:
            print(f"{hero_name} falls. The dungeon claims another seeker.")
            outcome = "death"
            running = False
except KeyboardInterrupt:
    print()
    print("The player ended the session.")
finally:
    print(frame)
    if outcome == "death":
        print(f"You didn't make it, {hero_name}. Actions: {actions}.")
    elif outcome == "exit":
        print(f"Run over, {hero_name}. Actions: {actions}.")
    else:
        print(f"Session interrupted, {hero_name}. Actions: {actions}.")
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")
    print(frame)
