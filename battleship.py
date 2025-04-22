#!/usr/bin/env python3
"""
Battleship Game - Play against the computer in this classic naval combat game.
"""
import random
import os
import time

class Board:
    """Represents a game board for Battleship."""
    
    def __init__(self, size=10):
        """Initialize a board with the given size."""
        self.size = size
        self.board = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = {}  # Dictionary to track ships: {ship_name: [(row, col), ...]}
        self.hits = set()  # Set to track successful hits
        self.misses = set()  # Set to track misses
        
    def display(self, hide_ships=False):
        """Display the board with row and column labels."""
        # Print column headers (A-J)
        print('   ' + ' '.join(chr(65 + i) for i in range(self.size)))
        
        # Print rows with row numbers and board contents
        for i in range(self.size):
            row_display = []
            for j in range(self.size):
                cell = self.board[i][j]
                # If hide_ships is True, show only water, hits, and misses
                if hide_ships and cell == 'S':
                    row_display.append('~')
                else:
                    row_display.append(cell)
            print(f"{i:2d} {' '.join(row_display)}")
    
    def place_ship(self, ship_name, length, row, col, orientation):
        """
        Place a ship on the board.
        
        Args:
            ship_name: Name of the ship
            length: Length of the ship
            row, col: Starting position
            orientation: 'h' for horizontal, 'v' for vertical
            
        Returns:
            bool: True if placement was successful, False otherwise
        """
        # Check if placement is valid
        ship_positions = []
        
        if orientation.lower() == 'h':
            if col + length > self.size:
                return False  # Ship would go off the board
            
            # Check if any position is already occupied
            for j in range(col, col + length):
                if self.board[row][j] != '~':
                    return False
                ship_positions.append((row, j))
                
        elif orientation.lower() == 'v':
            if row + length > self.size:
                return False  # Ship would go off the board
            
            # Check if any position is already occupied
            for i in range(row, row + length):
                if self.board[i][col] != '~':
                    return False
                ship_positions.append((i, col))
        else:
            return False  # Invalid orientation
        
        # Place the ship
        for pos_row, pos_col in ship_positions:
            self.board[pos_row][pos_col] = 'S'
        
        # Store ship positions
        self.ships[ship_name] = ship_positions
        return True
    
    def place_ships_randomly(self, ships):
        """
        Place ships randomly on the board.
        
        Args:
            ships: Dictionary of {ship_name: length}
            
        Returns:
            bool: True if all ships were placed successfully
        """
        for ship_name, length in ships.items():
            placed = False
            attempts = 0
            max_attempts = 100  # Prevent infinite loop
            
            while not placed and attempts < max_attempts:
                # Random position and orientation
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                orientation = random.choice(['h', 'v'])
                
                placed = self.place_ship(ship_name, length, row, col, orientation)
                attempts += 1
            
            if not placed:
                # Reset board and start over if we couldn't place a ship
                self.__init__(self.size)
                return self.place_ships_randomly(ships)
                
        return True
    
    def receive_attack(self, row, col):
        """
        Process an attack at the given coordinates.
        
        Args:
            row, col: Attack coordinates
            
        Returns:
            str: 'hit', 'miss', or 'already_attacked'
        """
        if (row, col) in self.hits or (row, col) in self.misses:
            return 'already_attacked'
        
        if self.board[row][col] == 'S':
            self.board[row][col] = 'X'  # Mark as hit
            self.hits.add((row, col))
            
            # Check if this hit sank a ship
            for ship_name, positions in self.ships.items():
                if (row, col) in positions:
                    # Check if all positions of this ship are hit
                    if all((pos_row, pos_col) in self.hits for pos_row, pos_col in positions):
                        print(f"You sank the {ship_name}!")
            
            return 'hit'
        else:
            self.board[row][col] = 'O'  # Mark as miss
            self.misses.add((row, col))
            return 'miss'
    
    def all_ships_sunk(self):
        """Check if all ships have been sunk."""
        for positions in self.ships.values():
            if not all((row, col) in self.hits for row, col in positions):
                return False
        return True


class BattleshipGame:
    """Main game class for Battleship."""
    
    def __init__(self, board_size=10):
        """Initialize the game with player and computer boards."""
        self.board_size = board_size
        self.player_board = Board(board_size)
        self.computer_board = Board(board_size)
        
        # Standard Battleship ships
        self.ships = {
            'Carrier': 5,
            'Battleship': 4,
            'Cruiser': 3,
            'Submarine': 3,
            'Destroyer': 2
        }
        
        # Computer's possible moves
        self.computer_moves = [(i, j) for i in range(board_size) for j in range(board_size)]
        random.shuffle(self.computer_moves)
        
        # Track computer's successful hits for smarter targeting
        self.computer_hits = []
        
    def setup_game(self):
        """Set up the game by placing ships."""
        self.clear_screen()
        print("==== BATTLESHIP GAME ====")
        print("\nSetting up the game...")
        
        # Place computer's ships randomly
        self.computer_board.place_ships_randomly(self.ships)
        
        # Let player place ships
        print("\nPlace your ships on the board:")
        print("S = Ship, ~ = Water")
        
        choice = input("\nDo you want to place ships manually or randomly? (m/r): ").lower()
        
        if choice == 'm':
            self.place_ships_manually()
        else:
            self.player_board.place_ships_randomly(self.ships)
            print("\nYour ships have been placed randomly:")
            self.player_board.display()
            input("\nPress Enter to continue...")
    
    def place_ships_manually(self):
        """Let the player place ships manually."""
        for ship_name, length in self.ships.items():
            placed = False
            
            while not placed:
                self.clear_screen()
                print(f"\nPlacing {ship_name} (length: {length})")
                self.player_board.display()
                
                try:
                    position = input("\nEnter starting position (e.g., A0): ")
                    col = ord(position[0].upper()) - 65  # Convert A-J to 0-9
                    row = int(position[1:])
                    
                    orientation = input("Enter orientation (h for horizontal, v for vertical): ").lower()
                    
                    if self.player_board.place_ship(ship_name, length, row, col, orientation):
                        placed = True
                    else:
                        print("\nInvalid placement. Ship would go off the board or overlap another ship.")
                        input("Press Enter to try again...")
                except (ValueError, IndexError):
                    print("\nInvalid input. Please use format like 'A0'.")
                    input("Press Enter to try again...")
        
        print("\nAll ships placed successfully!")
        self.player_board.display()
        input("\nPress Enter to start the game...")
    
    def player_turn(self):
        """Handle the player's turn."""
        self.clear_screen()
        print("\n==== YOUR TURN ====")
        print("\nYour board:")
        self.player_board.display()
        print("\nComputer's board:")
        self.computer_board.display(hide_ships=True)
        
        valid_move = False
        while not valid_move:
            try:
                position = input("\nEnter position to attack (e.g., A0): ")
                col = ord(position[0].upper()) - 65  # Convert A-J to 0-9
                row = int(position[1:])
                
                if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                    print("Position out of bounds. Try again.")
                    continue
                
                result = self.computer_board.receive_attack(row, col)
                
                if result == 'already_attacked':
                    print("You've already attacked this position. Try again.")
                else:
                    valid_move = True
                    if result == 'hit':
                        print("HIT! You hit a ship!")
                    else:
                        print("MISS! You missed.")
            except (ValueError, IndexError):
                print("Invalid input. Please use format like 'A0'.")
        
        input("\nPress Enter to continue...")
    
    def computer_turn(self):
        """Handle the computer's turn."""
        self.clear_screen()
        print("\n==== COMPUTER'S TURN ====")
        
        # Smart targeting: If there are hits, target adjacent cells
        if self.computer_hits:
            # Get the last hit
            last_hit_row, last_hit_col = self.computer_hits[-1]
            
            # Try adjacent cells (up, right, down, left)
            adjacent_cells = [
                (last_hit_row - 1, last_hit_col),
                (last_hit_row, last_hit_col + 1),
                (last_hit_row + 1, last_hit_col),
                (last_hit_row, last_hit_col - 1)
            ]
            
            # Filter valid moves that haven't been tried
            valid_adjacent = [
                (r, c) for r, c in adjacent_cells
                if 0 <= r < self.board_size and 0 <= c < self.board_size
                and (r, c) not in self.player_board.hits
                and (r, c) not in self.player_board.misses
            ]
            
            if valid_adjacent:
                row, col = random.choice(valid_adjacent)
            else:
                # If no valid adjacent cells, remove the hit from tracking
                # and choose randomly
                self.computer_hits.pop()
                if self.computer_moves:
                    row, col = self.computer_moves.pop()
                else:
                    # Fallback if we somehow run out of moves
                    row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
        else:
            # Random targeting
            if self.computer_moves:
                row, col = self.computer_moves.pop()
            else:
                # Fallback if we somehow run out of moves
                row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
        
        print(f"Computer attacks position {chr(65 + col)}{row}")
        time.sleep(1)  # Add a small delay for better UX
        
        result = self.player_board.receive_attack(row, col)
        
        if result == 'hit':
            print("HIT! The computer hit your ship!")
            self.computer_hits.append((row, col))
        else:
            print("MISS! The computer missed.")
        
        print("\nYour board:")
        self.player_board.display()
        
        input("\nPress Enter to continue...")
    
    def play(self):
        """Main game loop."""
        self.setup_game()
        
        while True:
            # Player's turn
            self.player_turn()
            if self.computer_board.all_ships_sunk():
                self.clear_screen()
                print("\n🎉 CONGRATULATIONS! You won! 🎉")
                print("\nYou sank all of the computer's ships!")
                break
            
            # Computer's turn
            self.computer_turn()
            if self.player_board.all_ships_sunk():
                self.clear_screen()
                print("\n😢 GAME OVER! You lost! 😢")
                print("\nThe computer sank all of your ships!")
                break
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    # Start the game
    game = BattleshipGame()
    game.play()