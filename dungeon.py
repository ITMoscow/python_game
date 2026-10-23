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

    def strike(self, n):
        """Урон в удар номер n; возвращает пару (hit, crit)."""
        if n % 3 == 0:
            return self.crit_damage, True
        return self.damage, False

    def spend_stamina(self, cost):
        """Тратит cost сил. Если сил не хватает, недостающее берётся из здоровья.
        Возвращает True, если шли на упорстве и здоровье списано.
        """
        if self.stamina >= cost:
            self.stamina -= cost
            return False
        self.health -= cost - self.stamina
        self.stamina = 0
        return True

    def heal(self, amount, cap):
        """Лечит на amount, но не выше потолка cap."""
        self.health = min(self.health + amount, cap)

    def __str__(self):
        """Формуляр героя одной строкой."""
        return f"{self.name}: health {self.health}, damage {self.damage:.1f}, stamina {self.stamina}"


class Enemy:
    """Враг на один бой: рабочая копия карточки из enemy_stats."""

    def __init__(self, name, stats):
        """Берёт здоровье, урон и трофеи из карточки stats."""
        self.name = name
        self.hp = stats["hp"]
        self.damage = stats["damage"]
        self.loot = stats["loot"]


def fight(enemy, hero, bonus=0):
    """Бой объекта enemy с объектом hero до гибели одного из двоих.
    bonus — надбавка к урону героя, по умолчанию 0; прибавляется после
    крита. Здоровье героя и врага меняется на месте, в объектах.
    Печатает строки раундов. Возвращает (rounds, won, loot).
    """
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy.name} emerges from the darkness!")
    while enemy.hp > 0 and hero.health > 0:
        round_n += 1
        hit, crit = hero.strike(round_n)
        hit = hit + bonus
        enemy.hp -= hit
        line = f"Round {round_n}: hero deals {hit:.1f}"
        if crit:
            line += " — critical!"
        else:
            line += "."
        if enemy.hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            hero.health -= enemy.damage
            line += f" {enemy.name.capitalize()} health: {enemy.hp:.1f}. {enemy.name.capitalize()} hits for {enemy.damage}."
            rounds.append([round_n, hit, enemy.damage])
        print(line)
    won = enemy.hp <= 0
    loot = enemy.loot if won else 0
    return rounds, won, loot


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
    test_hero = Hero("test", 100, 7, 5, 4)
    test_enemy = Enemy("skeleton", enemy_stats["skeleton"])
    rounds, won, loot = fight(test_enemy, test_hero, 0)
    print(f"self-test: {len(rounds)} rounds, won={won}, loot={loot}")
