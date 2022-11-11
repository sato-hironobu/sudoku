from problems import problems
import sys

def print_sudoku(sudoku):
	"""
	Print in sudoku style.
	"""
	print("-" * 17)
	for i in range(81):
		if i % 27 == 26:
			print(sudoku[i])
			print("-" * 17)
		elif i % 9 == 8:
			print(sudoku[i])
		elif i % 3 == 2:
			print(sudoku[i], end="|")
			
		else:
			print(sudoku[i], end=" ")

class Sudoku:
	
	def __init__(self, source):
		self.body = []
		for char in source:
			self.body.append(int(char))
		self.table = [ [1 for i in range(81)] for j in range(9)]
		self.update_table()
		
	def print(self):
		print_sudoku(self.body)

	def check_table(self):
		"""
		Print check table.
		"""
		for i in range(9):
			print(f"Table for {i+1}")
			print_sudoku(self.table[i])
	
	def get_block_of_position(self, position, type):
		"""
		Input
			position: a location of a sudoku cell
			type: a block type (row, column, square)
		
		Output
			a number of the block to which the cell location belongs
		"""
		if type == "row":
			block_number = position // 9
		elif type == "column":
			block_number = position % 9
		elif type == "square":
			block_number = position % 9 // 3 + position // 9 // 3 * 3
		return self.get_block_by_block_number(block_number, type)
		
	def get_block_by_block_number(self, block_number, type):
		"""
		Input
			block_number: a number of block
			type: a block type (row, column, square)
		
		Output:
			list of locations of cells which belong to the block
		"""
		if type == "row":
			return [block_number * 9 + i for i in range(9) ]
		elif type == "column":
			return [block_number + 9 * i for i in range(9)]
		elif type == "square":
			head = block_number // 3 * 27 + block_number % 3 * 3
			return [head + 9 * i + j for i in range(3) for j in range(3)]

	def search_block(self, num, type, block_number):
		"""
		Input
			num: a number to search for
			type: a type of block to search
			block_number: a number of block to search
		
		Output
			if a position of a number within certain block has been determined, return the position; otherwise return None
		"""
		block = self.get_block_by_block_number(block_number, type=type)
		cnt = 0
		for pos in block:
			if self.table[num][pos] == 1:
				position = pos
				cnt += 1
		if cnt == 1:
			return position
		return None

	def update_body(self):
		"""
		Investigate the check table and update the body.
		"""
		changed = False
		for num in range(9):
			for type in ("row", "column", "square"):
				for block_number in range(9):
					found = self.search_block(num, type, block_number)
					if found != None:
						if self.body[found] == 0:
							self.body[found] = num + 1
							changed = True
		return changed
	
	def update_table(self):
		"""
		Investigate the body and update the check table.
		"""
		for position in range(81):
			num = self.body[position]
			if num != 0:
				for i in range(9):
					if i != num - 1:
						self.table[i][position] = 0
				for type in ("row", "column", "square"):
					for j in self.get_block_of_position(position, type=type):
						if j != position:
							self.table[num-1][j] = 0
	
	def clear_check(self):
		"""
		Check if all cells are completed.
		"""
		cleared = True
		for num in self.body:
			if num == 0:
				cleared = False
		return cleared

	def run(self):
		while True:
			changed = self.update_body()
			self.update_table()
			if not changed: break
		return self.clear_check()

if __name__ == "__main__":
	if len(sys.argv) > 1:
		prob_num = int(sys.argv[1])
	else:
		prob_num = 1
	source = problems[prob_num - 1]
	sudoku = Sudoku(source)
	sudoku.print()
	cleared = sudoku.run()
	if cleared:
		print("Cleared!")
		sudoku.print()
	else:
		print("Not cleared...")
		sudoku.print()
		sudoku.check_table()