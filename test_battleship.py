#!/usr/bin/env python3
"""
Unit tests for the Battleship game.
"""
import unittest
from battleship import Board, BattleshipGame

class TestBattleshipBoard(unittest.TestCase):
    """Test cases for the Board class."""
    
    def setUp(self):
        """Set up a test board."""
        self.board = Board(size=10)
    
    def test_board_initialization(self):
        """Test that the board is initialized correctly."""
        self.assertEqual(len(self.board.board), 10)
        self.assertEqual(len(self.board.board[0]), 10)
        self.assertEqual(self.board.board[0][0], '~')
        self.assertEqual(len(self.board.ships), 0)
        self.assertEqual(len(self.board.hits), 0)
        self.assertEqual(len(self.board.misses), 0)
    
    def test_place_ship_horizontal(self):
        """Test placing a ship horizontally."""
        # Place a ship of length 3 at position (0, 0) horizontally
        result = self.board.place_ship("Cruiser", 3, 0, 0, 'h')
        self.assertTrue(result)
        self.assertEqual(self.board.board[0][0], 'S')
        self.assertEqual(self.board.board[0][1], 'S')
        self.assertEqual(self.board.board[0][2], 'S')
        self.assertEqual(len(self.board.ships["Cruiser"]), 3)
    
    def test_place_ship_vertical(self):
        """Test placing a ship vertically."""
        # Place a ship of length 3 at position (0, 0) vertically
        result = self.board.place_ship("Cruiser", 3, 0, 0, 'v')
        self.assertTrue(result)
        self.assertEqual(self.board.board[0][0], 'S')
        self.assertEqual(self.board.board[1][0], 'S')
        self.assertEqual(self.board.board[2][0], 'S')
        self.assertEqual(len(self.board.ships["Cruiser"]), 3)
    
    def test_place_ship_out_of_bounds(self):
        """Test placing a ship that would go out of bounds."""
        # Try to place a ship of length 3 at position (8, 8) horizontally
        result = self.board.place_ship("Cruiser", 3, 8, 8, 'h')
        self.assertFalse(result)
        self.assertEqual(self.board.board[8][8], '~')
        self.assertNotIn("Cruiser", self.board.ships)
    
    def test_place_ship_overlap(self):
        """Test placing a ship that would overlap with another ship."""
        # Place first ship
        self.board.place_ship("Cruiser", 3, 0, 0, 'h')
        # Try to place second ship overlapping
        result = self.board.place_ship("Destroyer", 2, 0, 1, 'v')
        self.assertFalse(result)
        self.assertNotIn("Destroyer", self.board.ships)
    
    def test_receive_attack_hit(self):
        """Test receiving an attack that hits a ship."""
        self.board.place_ship("Cruiser", 3, 0, 0, 'h')
        result = self.board.receive_attack(0, 1)
        self.assertEqual(result, 'hit')
        self.assertEqual(self.board.board[0][1], 'X')
        self.assertIn((0, 1), self.board.hits)
    
    def test_receive_attack_miss(self):
        """Test receiving an attack that misses all ships."""
        self.board.place_ship("Cruiser", 3, 0, 0, 'h')
        result = self.board.receive_attack(1, 1)
        self.assertEqual(result, 'miss')
        self.assertEqual(self.board.board[1][1], 'O')
        self.assertIn((1, 1), self.board.misses)
    
    def test_receive_attack_already_attacked(self):
        """Test receiving an attack on a position that was already attacked."""
        self.board.place_ship("Cruiser", 3, 0, 0, 'h')
        self.board.receive_attack(0, 1)
        result = self.board.receive_attack(0, 1)
        self.assertEqual(result, 'already_attacked')
    
    def test_all_ships_sunk(self):
        """Test checking if all ships are sunk."""
        self.board.place_ship("Destroyer", 2, 0, 0, 'h')
        self.assertFalse(self.board.all_ships_sunk())
        
        # Sink the ship
        self.board.receive_attack(0, 0)
        self.assertFalse(self.board.all_ships_sunk())
        
        self.board.receive_attack(0, 1)
        self.assertTrue(self.board.all_ships_sunk())
    
    def test_place_ships_randomly(self):
        """Test placing ships randomly."""
        ships = {"Carrier": 5, "Battleship": 4}
        result = self.board.place_ships_randomly(ships)
        self.assertTrue(result)
        self.assertEqual(len(self.board.ships), 2)
        self.assertIn("Carrier", self.board.ships)
        self.assertIn("Battleship", self.board.ships)
        self.assertEqual(len(self.board.ships["Carrier"]), 5)
        self.assertEqual(len(self.board.ships["Battleship"]), 4)


if __name__ == "__main__":
    unittest.main()