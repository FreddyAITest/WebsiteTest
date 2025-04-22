# Battleship Game

A Python implementation of the classic Battleship game where you can play against the computer.

## Game Description

Battleship is a strategy type guessing game for two players. It is played on ruled grids on which each player's fleet of ships are marked. The locations of the fleets are concealed from the other player. Players alternate turns calling "shots" at the other player's ships, and the objective of the game is to destroy the opposing player's fleet.

## How to Play

1. Run the game using Python:
   ```
   python battleship.py
   ```

2. When the game starts, you'll be asked if you want to place your ships manually or randomly:
   - Choose 'm' for manual placement
   - Choose 'r' for random placement

3. If you choose manual placement, for each ship:
   - Enter the starting position (e.g., A0, B3, etc.)
   - Enter the orientation ('h' for horizontal, 'v' for vertical)

4. During gameplay:
   - Take turns with the computer attacking each other's boards
   - Enter coordinates (e.g., A0, B3) to attack the computer's board
   - The game will show hits (X) and misses (O)
   - The first player to sink all of the opponent's ships wins

## Game Features

- 10x10 game board
- 5 ships of different sizes:
  - Carrier (5 spaces)
  - Battleship (4 spaces)
  - Cruiser (3 spaces)
  - Submarine (3 spaces)
  - Destroyer (2 spaces)
- Smart computer AI that targets adjacent cells after a hit
- Visual representation of the game boards
- Ship placement validation to prevent overlapping or out-of-bounds ships

## Board Legend

- `~`: Water (empty space)
- `S`: Ship (only visible on your board)
- `X`: Hit
- `O`: Miss

## Requirements

- Python 3.x
- No external libraries required

## Future Improvements

- Graphical user interface
- Difficulty levels for the computer AI
- Network play against other human players
- Save/load game functionality