from rich import print


class Hero():
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.armor = []
        self.emotions = ['happy', 'angry', 'surprised', 'sad', 'calm']
        self.current_emotion = 'calm'
        self.active_skills = {
            'strength': 10,
            'precision': 10,
            'intellect': 10,
            'vitality': 10,
            'damage': 10,
            'defense': 10,
            'health': 100,
            'mana': 10
        }

    def buy_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} buy {item}")

    def buy_armor(self, armor):
        self.armor.append(armor)
        print(f"{self.name} buy {armor}")

    def __repr__(self):
        return f"Hero(name={self.name}," \
                f"current_emotion={self.current_emotion}," \
                f"inventory={self.inventory}," \
                f"armor={self.armor}," \
                f"active_skills={self.active_skills})"


class Weapon:
    def __init__(self, name, damage, ammo):
        self.name = name
        self.damage = damage
        self.ammo = ammo

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, damage={self.damage}, ammo={self.ammo})"


class Pistol(Weapon):
    def __init__(self, name, damage, ammo=15):
        super().__init__(name, damage, ammo)


class AutomaticRifle(Weapon):
    def __init__(self, name, damage, ammo=30):
        super().__init__(name, damage, ammo)


class Drink:
    def __init__(self, name, heal):
        self.name = name
        self.heal = heal

    def __repr__(self):
        return f"Drink(name={self.name}, heal={self.heal})"


class Item:
    def __init__(self, item_name, item_type):
        self.item_name = item_name
        self.item_type = item_type

    def __repr__(self):
        return f"Item(name={self.item_name}, type={self.item_type})"


class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

    def __repr__(self):
        return f"Armor(name={self.name}, defense={self.defense})"


def main():
    batman_apollo = Hero("BATMAN APOLLO")
    print(batman_apollo)


if __name__ == "__main__":
    main()
