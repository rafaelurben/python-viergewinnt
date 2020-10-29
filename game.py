# 2020 - Cyril Gremaud / Rafael Urben
### Imports

from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.console import Console, RenderGroup
from rich import pretty
pretty.install()

### Helper functions

console = Console()
clearconsole = console.clear
print = console.print

### Constants

COLORS = [
    (0, 0, 0),
    (217,95, 73),
    (73, 118, 167),
]

COLORNAMES = [
    "Leer",
    "Rot",
    "Blau",
]

### Classes

class VierGewinnt():
    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height

        self.__game = [[0 for w in range(self.width)] for h in range(self.height)]

        self.current_player = 1

    # Print

    def print(self):
        clearconsole()

        gtb = Table(title="Spielfeld", show_lines=True)
        for i in range(self.width):
            gtb.add_column(str(i+1).zfill(2), justify="center")
        for r in self.__game:
            gtb.add_row(
                *[Text("  ", style=Style(bgcolor="rgb"+str(COLORS[p]))) for p in r]
            )

        ctb = Table("N", "CO", "FARBE", title="Spieler", show_lines=True)
        for i in range(len(COLORS)):
            ctb.add_row(
                Text(str(i), style=Style(
                    underline=self.current_player == i)), 
                Text("  ", style=Style(
                    bgcolor="rgb"+str(COLORS[i]))), 
                Text(str(COLORNAMES[i])),
            )

        tb = Table.grid(padding=2, pad_edge=True)
        tb.title = "Vier Gewinnt"
        tb.add_row(gtb, ctb)

        print("\n", tb, justify="center")

    # Get

    @property
    def rows(self):
        return self.__game

    def row(self, n: int):
        return self.rows(n)

    @property
    def cols(self):
        return [[self.rows[h][w] for h in range(self.height)] for w in range(self.width)]

    def col(self, n:int):
        return self.cols(n)

    @property
    def dias(self):
        dias = []
        w = 0 
        h = self.height-1
        while w < self.width:
            dia = []
            _w, _h = w, h

            while _w < self.width and _h < self.height:
                dia.append(self.rows[_h][_w])
                _w += 1
                _h += 1

            dias.append(dia)
            if h > 0:
                h -= 1
            else:
                w += 1
        w = 0
        h = 0
        while w < self.width:
            dia = []
            _w, _h = w, h

            while _w < self.width and _h >= 0:
                dia.append(self.rows[_h][_w])
                _w += 1
                _h -= 1

            dias.append(dia)
            if h < self.height-1:
                h += 1
            else:
                w += 1
        return dias


    # Set

    def _next_player(self):
        self.current_player = (self.current_player+1 if self.current_player < len(COLORS)-1 else 1)

    def _can_add_to_column(self, n: int):
        if n >= self.width:
            return None
        return not self.rows[0][n]

    def _add_to_column(self, n:int):
        if self._can_add_to_column(n):
            for h in range(self.height-1, -1, -1):
                if not self.__game[h][n]:
                    self.rows[h][n] = self.current_player
                    self._next_player()
                    return True
            return False
        else:
            return None

    # Checks

    def _is_full(self):
        return not 0 in self.rows[0]

    def _get_winner(self):
        for ls in [self.rows, self.cols, self.dias]:
            for l in ls:
                for i in range(len(l)-3):
                    if (not l[i] == 0) and (l[i] == l[i+1]) and (l[i+1] == l[i+2]) and (l[i+2] == l[i+3]):
                        return l[i]
        return 0

    # Game

    def main(self):
        self.print()
        while True:
            try:
                n = int(input("Enter column: "))
                success = self._add_to_column(n-1)
                self.print()

                if not success:
                    print("Diese Spalte existiert nicht oder ist bereits voll!")
                
                if self._is_full():
                    print("Das Spielfeld ist voll!")
                    break
                else:
                    winner = self._get_winner()
                    if winner:
                        print(COLORNAMES[winner], "hat das Spiel gewonnen!")
                        break
            except ValueError:
                self.print()
                print("Dies ist keine Zahl!")

### Main

if __name__ == "__main__":
    try:
        g = VierGewinnt()
        g.main()
    except KeyboardInterrupt:
        pass
