
# Hero Inventory System

A Python-based inventory management system for RPG heroes with equipment,
items, and character stats.

## Features

- **Hero Management**: Create heroes with customizable names and stats
- **Inventory System**: Manage items with slot-based storage (default limit: 30 slots)
- **Armor Equipment**: Equip armor to increase defense and health stats
- **Weapon System**: Store weapons with damage and ammo tracking
- **Item Types**: Support for multiple item categories (weapons, armor, potions, keys, documents, etc.)
- **Dynamic Parameters**: Add custom parameters to any item
- **Rich Output**: Colored console output for better readability

## Installation

### Requirements
- Python 3.12+
- `rich` library for colored output

### Setup
```bash
pip install rich
```

## Usage

### Basic Example

```python
from hero_inventory import Hero, Armor, Pistol, Item

# Create a hero
batman = Hero("BATMAN APOLLO")

# Create items
armor = Armor("Kevlar Vest", defense=30, durability=100)
pistol = Pistol("Glock", damage=15, precision=95)
key = Item("Golden Key", "key", rare=True, weight=0.5)

# Add items to inventory
batman.buy_item(armor, slot=1)
batman.buy_item(pistol, slot=2)
batman.buy_item(key, slot=3)

# Display hero stats
print(batman)
```

## Classes

### Hero
Main character class representing the player.

**Attributes:**
- `name` (str): Hero's name
- `inventory` (Inventory): Hero's inventory
- `armor` (list): Equipped armor pieces
- `emotions` (list): Available emotions
- `current_emotion` (str): Current emotion state
- `active_skills` (dict): Hero's stats and abilities

**Methods:**
- `buy_item(item, slot)`: Add item to inventory

### Inventory
Manages item storage with slot-based system.

**Attributes:**
- `items` (list): List of (item, slot) tuples
- `limit` (int): Maximum inventory capacity

**Methods:**
- `add(item, slot)`: Add item to specific slot
- `remove(slot)`: Remove item from slot

### Item
Base class for all items.

**Attributes:**
- `name` (str): Item name
- `item_type` (str): Item category
- `params` (dict): Dynamic item parameters

**Methods:**
- `get_equip_message(slot)`: Return equip message

### Armor
Equipment that provides defense bonus.

**Attributes:**
- `defense` (int): Defense value

**Example:**
```python
armor = Armor("Steel Plate", defense=25, durability=150)
```

### Weapon
Base weapon class with damage and ammunition.

**Attributes:**
- `damage` (int): Damage value
- `ammo` (int): Ammunition count

### Pistol
Handgun weapon with default 15 ammo.

**Example:**
```python
pistol = Pistol("Desert Eagle", damage=20)
```

### AutomaticRifle
Rifle weapon with default 30 ammo.

**Example:**
```python
rifle = AutomaticRifle("M16", damage=25)
```

### Drink
Consumable item that restores health.

**Attributes:**
- `heal` (int): Health points restored

**Example:**
```python
potion = Drink("Health Potion", heal=50)
```

## Game Mechanics

### Adding Armor
When armor is equipped:
- Defense stat increases by armor's defense value
- Health increases by armor's defense value
- Hero's armor list is updated

```python
armor = Armor("Kevlar Vest", defense=30)
batman.buy_item(armor, slot=1)
# Defense: +30
# Health: +30
```

### Inventory Slots
- Each item occupies exactly one slot
- Slots are numbered and cannot be shared
- Maximum 30 items (default, configurable)

### Dynamic Item Parameters
Add custom attributes to any item:

```python
# Weapon with custom parameters
rifle = AutomaticRifle("AK-47", damage=25, fire_rate=800, accuracy=85)

# General item with custom parameters
document = Item("Secret Document", "document", pages=50, encrypted=True)

# Armor with custom parameters
helmet = Armor("Tactical Helmet", defense=40, weight=2.5, material="Carbon")
```

## Output Examples

### Armor Equipped
```
⚔️ ARMOR EQUIPPED! Kevlar Vest is now protecting you! (Slot 1, Defense: +30)
   Inventory: 1/30
```

### Weapon Acquired
```
🔫 WEAPON ACQUIRED! Glock added to slot 2 (Damage: 15, Ammo: 15)
   Inventory: 2/30
```

### Potion Stored
```
🥤 POTION STORED! Health Potion added to slot 3 (Heals: +50 HP)
   Inventory: 3/30
```

### Error Messages
```
❌ Slot 1 is already occupied!
❌ Inventory full! Cannot add item
```

## Stats System

Default hero stats:
```python
{
    'strength': 10,
    'precision': 10,
    'intellect': 10,
    'vitality': 10,
    'damage': 10,
    'defense': 10,
    'health': 100,
    'mana': 10
}
```

Stats can be modified by:
- Equipping armor (increases defense and health)
- Other game mechanics (future implementation)

## File Structure

```
project/
├── hero_inventory.py    # Main game code
└── README.md           # This file
```

## Running the Project

```bash
python hero_inventory.py
```

This will run the `main()` function which demonstrates:
1. Creating a hero
2. Adding various items to inventory
3. Displaying hero stats
4. Listing all inventory items

## Future Enhancements

- [ ] Remove items from inventory with stat reduction
- [ ] Weapon usage and ammo management
- [ ] Potion consumption system
- [ ] Quest system
- [ ] NPC interactions
- [ ] Save/Load game state
- [ ] Multiple hero management
- [ ] Trading system

## Author

Created as a Python learning project focusing on OOP concepts:
- Class inheritance
- Polymorphism
- Encapsulation
- Method overriding

## License

Free to use and modify for learning purposes.
