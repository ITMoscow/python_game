title = "ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ"
frame = "=" * 31

print(frame)
print(title)
print(frame)

print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")
while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
    except ValueError:
        print("Ой: одна из строк не число. Введите все четыре снова:")
        continue
    try:
        if health <= 0:
            raise ValueError(f"Здоровье должно быть положительным, а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Характеристики не могут быть отрицательными")
        break
    except ValueError as e:
        print(f"{e}. Введите все четыре снова:")

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // 10 + endurance

print("Характеристики героя:")
print(f"Здоровье:     {health}")
print(f"Сила:         {strength}")
print(f"Ловкость:     {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас сил: {stamina}")
print()

running = True
actions = 0
while running:
    print("Что делаешь?")
    print("1 - осмотреться")
    print("2 - идти вперёд")
    print("3 - отдохнуть")
    print("4 - прислушаться")
    print("5 - зажечь факел")
    print("6 - тренировка")
    print("0 - выйти из подземелья")

    valid = ("0", "1", "2", "3", "4", "5", "6")
    choice = input()
    while choice not in valid:
        print("Такого пункта нет. Введи номер пункта из меню.")
        choice = input()
    match choice:
        case "1":
            print("Вы осмотрелись. Комната пуста, только пыль на полу.")

        case "2":
            cost = 2
            if stamina >= cost:
                stamina -= cost
                print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
            else:
                health -= cost - stamina
                stamina = 0
                print("Сил больше нет — вы идёте на одном упорстве.")

        case "3":
            stamina = stamina + 3
            print("Вы садитесь на пол и переводите дух. Силы возвращаются.")

        case "4":
            print("Вы прислушиваетесь. Где-то далеко капает вода.")

        case "5":
            stamina = stamina - 1
            print("Вы зажигаете факел. На стенах проступают старые надписи.")

        case "6":
            strikes = 5
            total_damage = 0
            crit_count = 0
            print("Вы подходите к тренировочному чучелу.")
            print("Оно стоит здесь с тех пор, как сюда приходил последний искатель.")
            print()
            print(f"Наносите {strikes} ударов.")
            for i in range(1, strikes + 1):
                hit_damage = damage
                if i % 3 == 0:
                    hit_damage = crit_damage
                    crit_count += 1
                    print(f"Удар {i}: {hit_damage:.1f} — критический!")
                else:
                    print(f"Удар {i}: {hit_damage:.1f}")
                total_damage += hit_damage
            stamina = stamina - 1
            print()
            print(f"Итог: {strikes} ударов, {crit_count} критический.")
            print(f"Общий урон: {total_damage:.1f}")
            print(f"Средний урон: {total_damage / strikes:.1f}")

        case "0":
            print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
            running = False

        case _:
            print("Такого действия нет.")

    if running:
        actions += 1
        print()
        print(f"Здоровье: {health} Запас сил: {stamina}")

    if health <= 0:
        print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
        running = False

print(frame)
if health <= 0:
    print(f"Ты не дошёл, {hero_name}. Действий совершено: {actions}.")
else:
    print(f"Забег окончен, {hero_name}. Действий совершено: {actions}.")
print(frame)
