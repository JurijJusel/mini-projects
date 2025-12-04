# 🚢 Battleship Game

A Python implementation of the classic Battleship game with an intelligent
auto-shooting algorithm.

## 📋 Features

- **10x10 Game Board** with coordinate system (A-J, 1-10)
- **Ship Placement** with automatic collision detection
- **Manual Shooting** by coordinates
- **Auto-Shooting Algorithm** with smart targeting:
  - Shoots every 5th position initially
  - Dynamically adjusts when hitting ships
  - Skips known empty spaces after sinking 1-length ships
  - Multi-round capability until all ships are destroyed
- **Statistics Tracking**:
  - First hit detection
  - Hit/Miss percentages
  - Total shots and accuracy metrics

## 🎮 Game Rules

### Ship Configuration
- **1x Ship (Length 5)**: Carrier
- **1x Ship (Length 4)**: Battleship
- **2x Ships (Length 3)**: Cruiser
- **3x Ships (Length 2)**: Destroyer
- **4x Ships (Length 1)**: Submarine

### Placement Rules
- Ships must be placed horizontally ('H') or vertically ('V')
- Ships cannot overlap
- Ships must have at least 1 empty cell between them (including diagonals)
- Ships must stay within the 10x10 board

## 🚀 Quick Start

### Basic Usage

```python
from battleship import Board, Ship, Shooter, print_statistics

# Create board
board = Board()

# Create ships
ships = [
    Ship(8, 0, 5, "H"),  # I1 - Carrier (length 5)
    Ship(2, 5, 4, "H"),  # C6 - Battleship (length 4)
    Ship(2, 0, 3, "H"),  # C1 - Cruiser (length 3)
    Ship(0, 6, 3, "H"),  # A7 - Cruiser (length 3)
    Ship(4, 2, 2, "H"),  # E3 - Destroyer (length 2)
    Ship(4, 5, 2, "H"),  # E6 - Destroyer (length 2)
    Ship(4, 8, 2, "H"),  # E9 - Destroyer (length 2)
    Ship(6, 0, 1, "H"),  # G1 - Submarine (length 1)
    Ship(6, 3, 1, "H"),  # G4 - Submarine (length 1)
    Ship(6, 5, 1, "H"),  # G6 - Submarine (length 1)
    Ship(6, 7, 1, "H"),  # G8 - Submarine (length 1)
]

# Add all ships to board
board.add_all_ships_together(ships)

# Create shooter
shooter = Shooter(board)

# Auto-shoot until all ships are sunk
results = shooter.auto_shoot_all()

# Display statistics
print_statistics(results)
```

### Alternative: Place Ships by Letter-Number Coordinates

```python
# Create ships using letter-number notation
ship5 = board.place_ship_by_letter_number("I", 1, 5, "H")  # I1
ship4 = board.place_ship_by_letter_number("C", 6, 4, "H")  # C6
ship3 = board.place_ship_by_letter_number("C", 1, 3, "H")  # C1

# Add to board
board.add_all_ships_together([ship5, ship4, ship3, ...])
```

### Manual Shooting

```python
# Shoot by coordinates (x, y)
result = shooter.shoot(0, 0)  # Shoot at A1
print(result)  # "Hit(A,1)" or "Miss(A,1)" or "Sunk(A,1)"

# Or shoot by letter-number
result = shooter.shoot_by_letter_number("B", 5)  # Shoot at B5
```

### Auto-Shooting with Round Limit

```python
# Limit to 10 rounds
results = shooter.auto_shoot_all(max_rounds=10)

# Unlimited rounds (default)
results = shooter.auto_shoot_all()
```

## 📊 Statistics

The game tracks comprehensive statistics:

```python
from battleship import calculate_statistics, print_statistics

# Get statistics as dictionary
stats = calculate_statistics(results)
print(f"First hit at shot: {stats['first_hit_shot']}")
print(f"Hit percentage: {stats['hit_percentage']}%")

# Or print formatted statistics
print_statistics(results)
```

### Statistics Output Example

```
==================================================
📊 SHOOTING STATISTICS
==================================================
🎯 First hit: 3 shot
📍 Total shots: 87
✅ Hits (Hit + Sunk): 15
💥 Ships sunk: 4
❌ Misses: 72
🔁 Already shot: 0
📈 Hit percentage: 17.24%
📉 Miss percentage: 82.76%
==================================================
```

## 🎯 Auto-Shooting Algorithm

The intelligent shooting algorithm works as follows:

1. **Initial Pattern**: Shoots every 5th position (0, 5, 10, 15, 20...)
   - Position 0 → (0,0) = A1
   - Position 5 → (0,5) = A6
   - Position 10 → (1,0) = B1
   - etc.

2. **On Hit**: Shifts +1 position and continues
   - Example: Hit at A1 → Next shot at A2

3. **On Miss**: Jumps +5 positions (back to pattern)
   - Example: Miss at A2 → Next shot at A7

4. **On Sunk (Length 1)**: Skips +2 positions
   - Reason: Next cell is guaranteed empty (game rules)
   - Example: Sunk at A1 → Skip A2, shoot at A3

5. **On Already Shot**: Shifts +1 position
   - Avoids duplicate shots

6. **Multi-Round**: When reaching position 100, resets to 0 and continues until all ships are destroyed

## 🏗️ Class Structure

### `Ship`
Represents a single ship on the board.

```python
ship = Ship(x, y, length, orientation)
# x, y: starting coordinates (0-9)
# length: ship length (1-5)
# orientation: 'H' (horizontal) or 'V' (vertical)
```

### `Board`
Manages the game board, ships, and shot tracking.

```python
board = Board(size=10)
board.add_all_ships_together(ships)  # Add multiple ships
board.all_ships_sunk()  # Check if game is over
```

### `Shooter`
Handles shooting mechanics and auto-shooting algorithm.

```python
shooter = Shooter(board)
shooter.shoot(x, y)  # Manual shot
shooter.auto_shoot_next()  # Single auto-shot
shooter.auto_shoot_all()  # Auto-shoot until all ships sunk
```

## 📐 Coordinate System

```
     1     2     3     4     5     6     7     8     9    10
A | (0,0) (0,1) (0,2) (0,3) (0,4) (0,5) (0,6) (0,7) (0,8) (0,9)
B | (1,0) (1,1) (1,2) (1,3) (1,4) (1,5) (1,6) (1,7) (1,8) (1,9)
C | (2,0) (2,1) (2,2) (2,3) (2,4) (2,5) (2,6) (2,7) (2,8) (2,9)
...
J | (9,0) (9,1) (9,2) (9,3) (9,4) (9,5) (9,6) (9,7) (9,8) (9,9)
```

## 🧪 Run the script
To run the Battleship game with an auto-shooting algorithm, execute the following command:

```bash
python3 main.py
```

This will:
1. Create a board with sample ships
2. Run auto-shooting algorithm
3. Display shot-by-shot results
4. Show final statistics

## 📝 Shot Results

- `"Miss(A,1)"` - Shot missed
- `"Hit(A,1)"` - Shot hit a ship
- `"Sunk(A,1)"` - Shot sunk a ship completely
- `"Already shot here (A,1)"` - Position already targeted

## 🎓 Example Game Flow

```python
# Setup
board = Board()
ships = [
    Ship(0, 0, 1, "H"),  # A1
    Ship(2, 2, 2, "H"),  # C3-C4
    Ship(5, 5, 3, "V"),  # F6-H6
]
board.add_all_ships_together(ships)

# Play
shooter = Shooter(board)
results = shooter.auto_shoot_all()

# Results
print_statistics(results)
```
