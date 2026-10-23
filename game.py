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

menu_last = 7
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
                    hit_damage = damage
                    if i % 3 == 0:
                        hit_damage = crit_damage
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
                    enemy_hp = 45
                    round_n = 0
                    print(f"You descend the stairs. A {enemy} emerges from the darkness!")
                    while enemy_hp > 0 and health > 0:
                        round_n += 1
                        if round_n % 3 == 0:
                            hit = crit_damage
                        else:
                            hit = damage
                        enemy_hp -= hit
                        line = f"Round {round_n}: hero deals {hit:.1f}"
                        if round_n % 3 == 0:
                            line += " — critical!"
                        else:
                            line += "."
                        if enemy_hp <= 0:
                            line += " Enemy falls."
                            log.append([round_n, hit, 0])
                        else:
                            blow = random.randint(2, 6)
                            health -= blow
                            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
                            log.append([round_n, hit, blow])
                        print(line)
                    if enemy_hp <= 0:
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                    print(f"Battle: {round_n} rounds.")

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
        print(f"You didn't make it, {hero_name}. Actions taken: {actions}.")
    elif outcome == "exit":
        print(f"The run is over, {hero_name}. Actions taken: {actions}.")
    else:
        print(f"Session interrupted, {hero_name}. Actions taken: {actions}.")
    print(frame)
