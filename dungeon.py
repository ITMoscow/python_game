"""Правила подземелья: удар героя, бой, покупка, цены и карточки врагов.

Случайный выбор врага (random.choice) остался в game.py вместе с выбором,
урон врага берётся из карточки, поэтому random здесь не нужен.
"""

prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "ghoul": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}


class Hero:
    """Герой забега: имя, характеристики и текущее состояние."""

    def __init__(self, name, health, strength, agility, endurance):
        """Раскладывает характеристики по атрибутам и считает урон и запас сил."""
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        self.damage = 10 + strength * 1.5
        self.crit_damage = self.damage * 2
        self.stamina = health // 10 + endurance

    def __str__(self):
        """Формуляр героя одной строкой."""
        return f"{self.name}: health {self.health}, damage {self.damage:.1f}, stamina {self.stamina}"


def hero_hit(strike_n, damage, crit_damage):
    """Урон героя в удар номер strike_n.
    Возвращает пару (hit, crit): урон и признак критического удара.
    Урон и критический урон героя приходят параметрами.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0, damage=0, crit_damage=0):
    """Бой с enemy до гибели одного из двоих.
    bonus — надбавка к урону героя, по умолчанию 0: без эликсира
    бой идёт как прежде. Надбавка прибавляется после крита
    (к уже удвоенному урону), а не удваивается вместе с ним.
    Карточка врага берётся из enemy_stats по имени: нужны ключи
    hp, damage, loot. Печатает строки раундов.
    Возвращает (rounds, won, hero_health, loot): таблицу раундов,
    признак победы, здоровье после боя и трофеи в золоте.
    damage и crit_damage — урон героя, модуль глобалов game.py не видит.
    Глобальные переменные не меняет.
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy} emerges from the darkness!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n, damage, crit_damage)
        hit = hit + bonus
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
            blow = stats["damage"]
            hero_health -= blow
            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0
    return rounds, won, hero_health, loot


def buy(price, gold, quantity=1):
    """Покупает quantity штук товара ценой price за золото gold.
    quantity по умолчанию 1. Возвращает (gold_left, ok): остаток
    золота и признак успешной покупки. Ничего не печатает.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


if __name__ == "__main__":
    rounds, won, hp, loot = fight("skeleton", 100, 0, 20.5, 41.0)
    print(f"self-test: {len(rounds)} rounds, won={won}, loot={loot}")
