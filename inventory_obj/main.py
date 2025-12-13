from rich import print


class Hero():
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.inventory = Inventory()
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

    def buy_item(self, item, slot):
        self.inventory.add(item, slot)


    def buy_armor(self, armor):
        self.armor.append(armor)
        print(f"{self.name} buy {armor}")

    def __repr__(self):
        return f"Hero(name={self.name}," \
                f"current_emotion={self.current_emotion}," \
                f"inventory={self.inventory}," \
                f"armor={self.armor}," \
                f"active_skills={self.active_skills})"


class Inventory:
    def __init__(self, limit=30):
        self.items = []
        self.limit = limit

    def add(self, item, slot):
        if len(self.items) < self.limit:
            self.items.append((item, slot))
            item_name = getattr(item, 'item_name', getattr(item, 'name', 'Unknown Item'))
            print(f"Added {item_name} to slot {slot}. Inventory: {len(self.items)}/{self.limit}")
        else:
            item_name = getattr(item, 'item_name', getattr(item, 'name', 'Unknown Item'))
            print(f"Inventory full! Cannot add {item_name}")

    def remove(self, slot):
        for i, (item, s) in enumerate(self.items):
            if s == slot:
                removed_item = self.items.pop(i)
                item_name = getattr(removed_item[0], 'item_name', getattr(removed_item[0], 'name', 'Unknown Item'))
                print(f"Removed {item_name} from slot {slot}")
                return
        print(f"No item in slot {slot}")

    def __repr__(self):
        return f"Inventory(count={len(self.items)}/{self.limit})"


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
    batman = Hero("BATMAN APOLLO")
    print(batman)

    key = Item("Golden Key", "key")
    document = Item("Secret Document", "document")
    coin = Item("Gold Coin", "currency")
    pistol = Pistol("Glock", damage=15)
    rifle = AutomaticRifle("AK-47", damage=25)
    armor = Armor("Kevlar Vest", defense=20)

    batman.buy_item(key, 1)
    batman.buy_item(document, 2)
    batman.buy_item(coin, 3)
    batman.buy_item(pistol, 4)
    batman.buy_item(rifle, 5)
    batman.buy_armor(armor)

    print(batman.inventory)
    print(batman)


if __name__ == "__main__":
    main()
