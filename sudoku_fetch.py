import requests
from bs4 import BeautifulSoup
import sys
import re

from sudoku import Sudoku

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        nd, xh = sys.argv[1], sys.argv[2]
    else:
        nd, xh = 0, 1
    url = "http://www.sudokugame.org/archive/printsudoku.php"
    payload = {
        "nd": int(nd),
        "xh": int(xh),
    }
    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.text, "lxml")

    pattern = r"tmda='(\d+)'"
    match = re.search(pattern, soup.find("script").text)
    source = match.groups()[0][0:81]
    
    sudoku = Sudoku(source)
    sudoku.print()
    cleared = sudoku.run()
    if cleared:
        print("Cleared!")
    else:
        print("Not cleared...")
    sudoku.print()