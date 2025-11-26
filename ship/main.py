from typing import List, Tuple, Set
from rich import print
from constants import MAX_SHIPS_BY_LENGTH


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
    Klasė atstovauja vieną laivą „Laivų mūšio“ žaidime.
    Vidinė koordinatė:
        x = eilutė (raidė A–J → 0–9)
        y = stulpelis (1–10 → 0–9)
    Parametrai:
        x (int): pradžios eilutė
        y (int): pradžios stulpelis
        length (int): laivo ilgis
        orientation (str): 'H' (horizontal), 'V' (vertical)
    Metodai:
        - register_hit(x, y)
        - is_sunk()
        - coordinates: visų laivo langelių sąrašas
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
        Grąžina sąrašą su (x, y) koordinatėmis.
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
        ships: List[Ship] - nauji laivai pridėjimui
        Grąžina True jei visi laivai pridėti sėkmingai,
        False jei bent vienas netinka.
        Patikrina ir prideda laivus tik jei visi teisingi.
        Jei bent vienas netinka – neprideda NIEKO.
        """
        # 1 Tikriname maksimalų kiekį (esami + nauji)
        for ship in ships:
            existing_count = sum(1 for s in self.ships if s.length == ship.length)
            new_count = sum(1 for s in ships if s.length == ship.length)
            if existing_count + new_count > MAX_SHIPS_BY_LENGTH.get(ship.length, 0):
                print(f"Per daug laivų ilgio {ship.length}")
                return False

        # 2 Tikriname ribas ir overlap naujų laivų tarpusavyje
        for i, ship in enumerate(ships):
            for x, y in ship.coordinates:

                # ribos
                if not (0 <= x < self.size and 0 <= y < self.size):
                    print(f"Laivas išeina už ribų: ({x},{y})")
                    return False

                # overlap su kitais naujais laivais
                for other in ships[:i]:
                    if (x, y) in other.coordinates:
                        print(f"Laivai persidengia: ({x},{y})")
                        return False

        # 3 Tarpų tikrinimas (nauji su naujais + nauji su esamais)
        for ship in ships:
            for x, y in ship.coordinates:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:

                            # tikrinam su esamais
                            for existing in self.ships:
                                if (nx, ny) in existing.coordinates:
                                    print(
                                        f"Per arti esamo laivo: ({x},{y}) prie ({nx},{ny})"
                                    )
                                    return False

                            # tikrinam su naujais
                            for other in ships:
                                if other is ship:
                                    continue
                                if (nx, ny) in other.coordinates:
                                    print(
                                        f"Nauji laivai per arti: ({x},{y}) prie ({nx},{ny})"
                                    )
                                    return False

        # 4 Jei viskas OK → pridedame VISUS VIENU METU
        self.ships.extend(ships)
        return True

    def place_ship_by_letter_number(
        self, letter: str, number: int, length: int, orientation: str
    ) -> Ship:
        """
        Prideda laivą į lentą naudojant raidės ir skaičiaus koordinates.
        letter = 'A'-'J',
        number = 1-10
        """
        x, y = convert_letter_number(letter, number)
        ship = Ship(x, y, length, orientation)
        return ship

    # Šūvis su skaitinėmis koordinatėmis
    def shoot(self, x: int, y: int) -> str:
        letter = chr(x + ord("A"))
        number = y + 1

        if (x, y) in self.shots_taken:
            return f"Already shot here ({letter},{number})"

        self.shots_taken.add((x, y))

        for ship in self.ships:
            if ship.register_hit(x, y):
                return (
                    f"Sunk({letter},{number})"
                    if ship.is_sunk()
                    else f"Hit({letter},{number})"
                )
        return f"Miss({letter},{number})"

    def shoot_by_letter_number(self, letter: str, number: int) -> str:
        """
        Shoot at the board using letter and number coordinates.
        letter = 'A'-'J',
        number = 1-10
        """
        x, y = convert_letter_number(letter, number)
        return self.shoot(x, y)

    def all_ships_sunk(self) -> bool:
        """
        Check if all ships are sunk.
        Returns True if all ships are sunk, False otherwise.
        remaining ships. (Likę laivai: 0)
        """
        remaining = sum(not ship.is_sunk() for ship in self.ships)
        print(f"Likę laivai: {remaining}")
        if remaining == 0:
            print("Visi laivai paskandinti!")
            return True
        else:
            return False

    def __repr__(self):
        return f"Board(size={self.size}, ships={self.ships})"


if __name__ == "__main__":
    board = Board()

    ship1 = board.place_ship_by_letter_number("A", 1, 5, "H")
    ship2 = board.place_ship_by_letter_number("c", 1, 2, "H")

    # Tikriname prieš pridėjimą
    if board.add_all_ships_together([ship1, ship2]):
        print("Visi laivai pridėti sekmingai i lentą")
    else:
        print("Bent vienas laivas blogai suformuotas, nieko nepridėdama i lenta")

    print(board)

    # Šauname
    print(board.shoot_by_letter_number("A", 1))
    print(board.shoot_by_letter_number("A", 1))
    print(board.shoot_by_letter_number("a", 2))
    print(board.shoot_by_letter_number("a", 3))
    print(board.shoot_by_letter_number("a", 4))
    print(board.shoot_by_letter_number("a", 6))
    print(board.shoot_by_letter_number("A", 5))

    print(board.shoot_by_letter_number("c", 1))
    print(board.shoot_by_letter_number("c", 2))

    print(board.all_ships_sunk())
