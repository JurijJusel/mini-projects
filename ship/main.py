from typing import Tuple, List, Set
from constants import MAX_SHIPS_BY_LENGTH, JSON_FILE_PATH, ROUNDS_PER_GAME
from statistic import print_statistics, calculate_statistics
from file import append_to_json_list


def convert_letter_number(letter: str, number: int) -> Tuple[int, int]:
    """
    Konvertuoja raidę ir skaičių į vidinę koordinatę (x, y)
    letter = 'A'-'J',
    number = 1-10
    """
    x = ord(letter.upper()) - ord("A")  # raidė nuo 0-9
    y = number - 1  # skaičius nuo 0-9
    return x, y


class Ship:
    """
    Klasė atstovauja vieną laivą „Laivų mūšio" žaidime.
    """
    def __init__(self, x: int, y: int, length: int, orientation: str):
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation.upper()
        self.hits: Set[Tuple[int, int]] = set()
        self.coordinates = self._generate_coordinates()

        if self.orientation not in ("H", "V"):
            print(
                f"Warning: '{orientation}' no valid Orientation"
                f" must be 'H' - horizontal or 'V' - vertical."
            )
            raise ValueError("Orientation must be 'H' - horizontal or 'V'- vertical.")

    def _generate_coordinates(self) -> List[Tuple[int, int]]:
        """
        Generuoja laivo koordinatės sąrašą pagal pradžios tašką, ilgį ir orientaciją.
        """
        if self.orientation == "H":  # horizontalus  einame į dešinę (keičiasi y)
            return [(self.x, self.y + i) for i in range(self.length)]
        else:  # verticalus einame žemyn (keičiasi x)
            return [(self.x + i, self.y) for i in range(self.length)]

    def register_hit(self, x: int, y: int) -> bool:
        if (x, y) in self.coordinates:
            self.hits.add((x, y))
            return True
        return False

    def is_sunk(self) -> bool:
        return len(self.hits) == len(self.coordinates)

    def __repr__(self):
        return f"Ship(length={self.length}, orientation='{self.orientation}', coords={self.coordinates})"


class Board:
    """
    Klasė atstovauja žaidimo lentą 10x10 su laivais ir šūviais.

            1 2 3 4 5 6 7 8 9 10
        A |  . . . . . . . . . .
        B |  . . . . . . . . . .
        C |  . . . . . . . . . .
        D |  . . . . . . . . . .
        E |  . . . . . . . . . .
        F |  . . . . . . . . . .
        G |  . . . . . . . . . .
        H |  . . . . . . . . . .
        I |  . . . . . . . . . .
        J |  . . . . . . . . . .

            1     2      3     4     5     6     7     8     9     10
        A | (0,0) (0,1) (0,2) (0,3) (0,4) (0,5) (0,6) (0,7) (0,8) (0,9)
        B | (1,0) (1,1) (1,2) (1,3) (1,4) (1,5) (1,6) (1,7) (1,8) (1,9)
        C | (2,0) (2,1) (2,2) (2,3) (2,4) (2,5) (2,6) (2,7) (2,8) (2,9)
        D | (3,0) (3,1) (3,2) (3,3) (3,4) (3,5) (3,6) (3,7) (3,8) (3,9)
        E | (4,0) (4,1) (4,2) (4,3) (4,4) (4,5) (4,6) (4,7) (4,8) (4,9)
        F | (5,0) (5,1) (5,2) (5,3) (5,4) (5,5) (5,6) (5,7) (5,8) (5,9)
        G | (6,0) (6,1) (6,2) (6,3) (6,4) (6,5) (6,6) (6,7) (6,8) (6,9)
        H | (7,0) (7,1) (7,2) (7,3) (7,4) (7,5) (7,6) (7,7) (7,8) (7,9)
        I | (8,0) (8,1) (8,2) (8,3) (8,4) (8,5) (8,6) (8,7) (8,8) (8,9)
        J | (9,0) (9,1) (9,2) (9,3) (9,4) (9,5) (9,6) (9,7) (9,8) (9,9)
    """
    def __init__(self, size: int = 10):
        self.size = size
        self.ships: List[Ship] = []
        self.shots_taken: Set[Tuple[int, int]] = set()

    def is_space_free(self, ship: Ship) -> bool:
        for x, y in ship.coordinates:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        for existing in self.ships:
                            if (nx, ny) in existing.coordinates:
                                print(
                                    f"Laivas {ship} per arti esamo laivo: ({x},{y}) prie ({nx},{ny})"
                                )
                                return False
        return True

    def add_all_ships_together(self, ships: List[Ship]) -> bool:
        """
        Prideda visus laivus vienu metu jei visi teisingi.
        """
        # 1 Tikriname maksimalų kiekį
        for ship in ships:
            existing_count = sum(1 for s in self.ships if s.length == ship.length)
            new_count = sum(1 for s in ships if s.length == ship.length)
            if existing_count + new_count > MAX_SHIPS_BY_LENGTH.get(ship.length, 0):
                print(f"Per daug laivų ilgio {ship.length}")
                return False

        # 2 Tikriname ribas ir overlap
        for i, ship in enumerate(ships):
            for x, y in ship.coordinates:
                if not (0 <= x < self.size and 0 <= y < self.size):
                    print(f"Laivas {ship} išeina už ribų: ({x},{y})")
                    return False

                for other in ships[:i]:
                    if (x, y) in other.coordinates:
                        print(f"Laivai persidengia: ({x},{y})")
                        return False

        # 3 Tarpų tikrinimas
        for ship in ships:
            for x, y in ship.coordinates:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            for existing in self.ships:
                                if (nx, ny) in existing.coordinates:
                                    print(f"Per arti esamo laivo: ({x},{y}) prie ({nx},{ny})")
                                    return False

                            for other in ships:
                                if other is ship:
                                    continue
                                if (nx, ny) in other.coordinates:
                                    print(f"Nauji laivai per arti: ({x},{y}) prie ({nx},{ny})")
                                    return False

        # 4 Pridedame visus
        self.ships.extend(ships)
        return True

    def place_ship_by_letter_number(
        self, letter: str, number: int, length: int, orientation: str) -> Ship:
        """
        Sukuria laivą naudojant raidės ir skaičiaus koordinates.
        """
        x, y = convert_letter_number(letter, number)
        ship = Ship(x, y, length, orientation)
        return ship

    def all_ships_sunk(self) -> bool:
        """
        Patikrina ar visi laivai paskandinti.
        """
        remaining = sum(not ship.is_sunk() for ship in self.ships)
        #print(f"Likę laivai: {remaining}")
        if remaining == 0:
            #print("Visi laivai paskandinti!")
            return True
        return False

    def __repr__(self):
        return f"Board(size={self.size}, ships={self.ships})"


class Shooter:
    """
    Klasė atsakinga už šaudymą į Board.
    """
    def __init__(self, board):
        self.board = board
        self.current_position = 0  # Tikra pozicija lentoje (0-99)
        self.shots_sequence = []

    def shoot(self, x: int, y: int) -> str:
        """
        Atlieka šūvį į lentą.
        """
        letter = chr(x + ord("A"))
        number = y + 1

        if (x, y) in self.board.shots_taken:
            return f"Already shot here ({letter},{number})"

        self.board.shots_taken.add((x, y))

        for ship in self.board.ships:
            if ship.register_hit(x, y):
                return (
                    f"Sunk({letter},{number})"
                    if ship.is_sunk()
                    else f"Hit({letter},{number})"
                )
        return f"Miss({letter},{number})"

    def shoot_by_letter_number(self, letter: str, number: int) -> str:
        """
        Atlieka šūvį naudodamas raidę ir skaičių.
        """
        x, y = convert_letter_number(letter, number)
        return self.shoot(x, y)

    def _position_to_coords(self, pos: int) -> Tuple[int, int]:
        """
        Konvertuoja vienmačią poziciją (0-99) į koordinates (x, y).
        pos 0 → (0,0), pos 5 → (0,5), pos 10 → (1,0)
        """
        x = pos // self.board.size
        y = pos % self.board.size
        return x, y

    def auto_shoot_next(self) -> str:
        """
        Atlieka VIENĄ automatinį šūvį pagal pagerinta logiką:

        Pradeda nuo pozicijos, kuri dalijasi iš 5 (0, 5, 10, 15...).
        Kai pataiko arba jau šautas:
        - +1 pozicija (dinamiškai šoka)
        - Tada vėl kas 5 (+5 nuo naujos pozicijos)

        Pavyzdys:
        - Šauna pos 0 (A1) → Hit → +1
        - Šauna pos 1 (A2) → tada kas 5 → +5
        - Šauna pos 6 (A7) → Miss → +5
        - Šauna pos 11 (B2)

        Jei paskandytas laivas ilgio 1 → +2 pozicijos.

        Returns:
            str: šūvio rezultatas arba "No more shots"
        """
        max_position = self.board.size * self.board.size

        # Jei viršijom ribą
        if self.current_position >= max_position:
            return "No more shots"

        # Konvertuojame poziciją į koordinates
        x, y = self._position_to_coords(self.current_position)

        # Jei jau šovėme į šią poziciją, praleidžiame +1
        while (x, y) in self.board.shots_taken:
            self.current_position += 1
            if self.current_position >= max_position:
                return "No more shots"
            x, y = self._position_to_coords(self.current_position)

        # Atliekame šūvį
        result = self.shoot(x, y)
        self.shots_sequence.append(result)

        # Logika priklausomai nuo rezultato
        if "Sunk" in result:
            # Patikrinkime laivo ilgį
            for ship in self.board.ships:
                if (x, y) in ship.coordinates and ship.is_sunk():
                    if ship.length == 1:
                        # Laivas ilgio 1 → praleidžiame +2
                        self.current_position += 2
                    else:
                        # Ilgesnis laivas → +1
                        self.current_position += 1
                    break
        elif "Hit" in result:
            self.current_position += 1
        elif "Already" in result:
            self.current_position += 1
        else:
            self.current_position += 5

        return result

    def auto_shoot_all(self, max_rounds: int = ROUNDS_PER_GAME) -> List[str]:
        """
        Atlieka VISUS automatinius šūvius RATAIS iki visi laivai paskandinti.
        Kai pasiekia pabaigą (pos 100), grįžta į pradžią (pos 0).
        Args:
            max_rounds (int): maksimalus ratų skaičius (default: None - be limito)
                             Jei None, šaudo be limito (iki laivai paskandinti)
        Returns:
            List[str]: visų šūvių rezultatų sąrašas
        """
        results = []
        rounds = 0

        while not self.board.all_ships_sunk():
            # Tikriname ar pasiektas limitas
            if max_rounds is not None and rounds >= max_rounds:
                print(f"Pasiektas maksimalus ratų skaičius ({max_rounds})")
                break

            result = self.auto_shoot_next()

            if result == "No more shots":
                self.current_position = 0
                rounds += 1
                print(f"--- Ratas {rounds} baigtas, pradedame iš naujo ---")
                continue

            results.append(result)

        if self.board.all_ships_sunk():
            print(f"Visi laivai paskandinti per {rounds + 1} ratus!")

        return results


if __name__ == "__main__":
    print("\n" + "="*50)
    print("=== Testuojame auto_shoot_all() ===")
    print("="*50 + "\n")

    board = Board()

    ship5 = board.place_ship_by_letter_number("I", 1, 5, "H")
    ship4 = board.place_ship_by_letter_number("C", 6, 4, "H")
    ship3 = board.place_ship_by_letter_number("C", 1, 3, "H")
    ship3_1 = board.place_ship_by_letter_number("A", 7, 3, "H")
    ship2_1 = board.place_ship_by_letter_number("E", 3, 2, "H")
    ship2_2 = board.place_ship_by_letter_number("E", 6, 2, "H")
    ship2_3 = board.place_ship_by_letter_number("I", 9, 2, "V")
    ship1_1 = board.place_ship_by_letter_number("G", 1, 1, "H")
    ship1_2 = board.place_ship_by_letter_number("G", 3, 1, "H")
    ship1_3 = board.place_ship_by_letter_number("G", 5, 1, "H")
    ship1_4 = board.place_ship_by_letter_number("G", 8, 1, "H")
    ship1_5 = board.place_ship_by_letter_number("J", 7, 1, "H")

    ships = [
        ship5, ship4, ship3, ship3_1,
        ship2_1, ship2_2, ship2_3,
        ship1_1, ship1_2, ship1_3, ship1_4,ship1_5
    ]

    print(board.add_all_ships_together(ships))

    shooter = Shooter(board)
    results = shooter.auto_shoot_all()

    print(f"\n=== REZULTATAI ===")
    print(results)
    print(board.all_ships_sunk())
    print_statistics(results)

    print("Write data to json file ...")
    get_statistic = calculate_statistics(results)
    print(get_statistic)
    append_to_json_list(get_statistic, JSON_FILE_PATH)
    print("Write data to json Done!!!.")
