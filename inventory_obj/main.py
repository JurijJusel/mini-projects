from rich import print

class Hero():
    """Represents a hero character with inventory, armor, and skills."""

    def __init__(self, name):
        """Initialize a hero with name, empty inventory, and default stats."""
        self.name = name
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
        """
        Add an item to hero's inventory at specified slot.
        If item is armor, it increases defense and health stats.
        Args:
            item: Item object to add
            slot: Inventory slot number
        Returns:
            bool: True if item added successfully, False otherwise
        """
        for existing_item, existing_slot in self.inventory.items:
            if existing_slot == slot:
                print(f"❌ Slot {slot}, Item {item} is occupied!")
                return False

        if len(self.inventory.items) >= self.inventory.limit:
            print(f"❌ Inventory full!")
            return False

        if isinstance(item, Armor):
            self.armor.append(item)
            self.active_skills['defense'] += item.defense
            self.active_skills['health'] += item.defense

        return self.inventory.add(item, slot)

    def __repr__(self):
        return f"Hero(name={self.name}," \
                f"current_emotion={self.current_emotion}," \
                f"inventory={self.inventory}," \
                f"armor={self.armor}," \
                f"active_skills={self.active_skills})"


class Inventory:
    """Manages hero's inventory with item slots and capacity limit."""

    def __init__(self, limit=30):
        """
        Initialize inventory with maximum slot capacity.
        Args:
            limit: Maximum number of items allowed (default: 30)
        """
        self.items = []
        self.limit = limit

    def add(self, item, slot):
        """
        Add item to inventory at specified slot.
        Checks if slot is available and inventory is not full.
        Args:
            item: Item object to add
            slot: Inventory slot number
        Returns:
            bool: True if item added successfully, False otherwise
        """
        for existing_item, existing_slot in self.items:
            if existing_slot == slot:
                print(f"❌ Cannot add {item.name} to slot {slot}")
                return False

        if len(self.items) >= self.limit:
            print(f"❌ Inventory full! Cannot add {item.name}")
            return False

        self.items.append((item, slot))
        print(item.get_equip_message(slot))
        print(f"   Inventory: {len(self.items)}/{self.limit}")
        return True

    def remove(self, slot):
        """
        Remove item from specified slot.
        Args:
            slot: Inventory slot number to remove from
        """
        for i, (item, s) in enumerate(self.items):
            if s == slot:
                removed_item = self.items.pop(i)
                print(f"Removed {removed_item[0].name} from slot {slot}")
                return
        print(f"No item in slot {slot}")

    def __repr__(self):
        return f"Inventory(count={len(self.items)}/{self.limit})"


class Item:
    """Base class for all items in the game."""

    def __init__(self, name, item_type, **kwargs):
        """
        Initialize an item with name, type, and dynamic parameters.
        Args:
            name: Item name
            item_type: Category of item (key, document, currency, etc.)
            **kwargs: Additional item parameters (rare, weight, pages, etc.)
        """
        self.name = name
        self.item_type = item_type
        self.params = kwargs

    def get_equip_message(self, slot):
        """
        Get message displayed when item is added to inventory.
        Can be overridden by subclasses for custom messages.
        Args:
            slot: Inventory slot number
        Returns:
            str: Equip message
        """
        return f"📦 Item added: {self.name} to slot {slot}"

    def __repr__(self):
        params_str = ", ".join(f"{k}={v}" for k, v in self.params.items())
        return f"{self.__class__.__name__}(name={self.name}, type={self.item_type}, {params_str})"


class Armor(Item):
    """Armor item that provides defense bonus."""

    def __init__(self, name, defense, **kwargs):
        """
        Initialize armor with name and defense value.
        Args:
            name: Armor name
            defense: Defense value provided by this armor
            **kwargs: Additional armor parameters (durability, etc.)
        """
        super().__init__(name, "armor", defense=defense, **kwargs)
        self.defense = defense

    def get_equip_message(self, slot):
        return f"⚔️ ARMOR EQUIPPED! {self.name} is now protecting you! (Slot {slot}, Defense: +{self.defense})"


class Weapon(Item):
    """Weapon item that deals damage."""

    def __init__(self, name, damage, ammo=None, **kwargs):
        """
        Initialize weapon with name, damage, and optional ammo.
        Args:
            name: Weapon name
            damage: Damage value dealt by this weapon
            ammo: Ammunition count (optional)
            **kwargs: Additional weapon parameters (precision, fire_rate, etc.)
        """
        super().__init__(name, "weapon", damage=damage, ammo=ammo, **kwargs)
        self.damage = damage
        self.ammo = ammo

    def get_equip_message(self, slot):
        return f"🔫 WEAPON ACQUIRED! {self.name} added to slot {slot} (Damage: {self.damage}, Ammo: {self.ammo})"


class Pistol(Weapon):
    """Pistol weapon with default 15 ammo."""

    def __init__(self, name, damage, ammo=15, **kwargs):
        """
        Initialize pistol weapon.
        Args:
            name: Pistol name
            damage: Damage value
            ammo: Ammunition count (default: 15)
            **kwargs: Additional parameters
        """
        super().__init__(name, damage, ammo, **kwargs)


class AutomaticRifle(Weapon):
    """Automatic rifle weapon with default 30 ammo."""

    def __init__(self, name, damage, ammo=30, **kwargs):
        """
        Initialize automatic rifle weapon.

        Args:
            name: Rifle name
            damage: Damage value
            ammo: Ammunition count (default: 30)
            **kwargs: Additional parameters
        """
        super().__init__(name, damage, ammo, **kwargs)


class Drink(Item):
    """Consumable drink item that restores health."""

    def __init__(self, name, heal, **kwargs):
        """
        Initialize drink item.
        Args:
            name: Drink name
            heal: Health points restored when consumed
            **kwargs: Additional parameters
        """
        super().__init__(name, "drink", heal=heal, **kwargs)
        self.heal = heal

    def get_equip_message(self, slot):
        return f"🥤 POTION STORED! {self.name} added to slot {slot} (Heals: +{self.heal} HP)"


def main():

    batman = Hero("BATMAN APOLLO")
    print(batman)

    key = Item("Golden Key", "key", rare=True, weight=0.5)
    document = Item("Secret Document", "document", pages=50)
    armor = Armor("Kevlar Vest", defense=30, durability=100)
    pistol = Pistol("Glock", damage=15, precision=95)
    rifle = AutomaticRifle("AK-47", damage=25, fire_rate=800)
    head_rotection = Armor("Tactical Helmet", defense=40, durability=80)

    batman.buy_item(document, 2)
    batman.buy_item(armor, 3)
    batman.buy_item(key, 1)
    batman.buy_item(pistol, 4)
    batman.buy_item(rifle, 5)
    batman.buy_item(head_rotection, 6)

    print(batman)

    print("\n--- Inventory ---")
    for item, slot in batman.inventory.items:
        print(f"Slot {slot}: {item}")


if __name__ == "__main__":
    main()
