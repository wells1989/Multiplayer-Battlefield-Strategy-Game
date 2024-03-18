# Multi-player Battlefield Strategy Game

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Project Notes](#project-notes)

## Description
This PyGame based project is a variable 2-4 player game, occuring on different map sizes. The game consists of taking over / attacking enemy cells / upgrading current cells to control the battlefield and eliminate other players.

**Project Areas: OOP and event-drive programming with Python, complex data types, abstraction and encapsulation, function decomposition**

## Installation

1. Clone the repository:

   ```bash
   gh repo clone wells1989/Multiplayer-Battlefield-Strategy-Game

2. Install dependencies:

   ```bash
   pip install -r requirements.txt 


## Usage
### Gameplay
- Players control their HQ cell to start the game, with random selection determining the first player.
- Each player has 3 turns in a round, which they can use to take over new cells, upgrade current cells or attack enemy cells.
- At the end of the round the player gains points based on the cells they control at that point.
- Certain Terrain cells will require extra upgrades to occupy them, but they also offer benefits when being used to attack other cells.
- When a cell is attacked:
  - The attacking and defending cells attributes are compare to determine the winner.
  - Comms allows you to attack with multiple cells simultaneously.
  - If the attacking player fails in the attack they also lose the remainder of their turn.
- The players can view the rules / restart the game at any point / reset the game (i.e. changing the number of players etc)

### Game GUI
- **Welcome screen / rules**

![Screenshot (596)](https://github.com/wells1989/Full-stack-blog/assets/122035759/dbbf9371-8fe1-4f50-8021-7c9e46ff2d4f)

- **Game start**

![Screenshot (597)](https://github.com/wells1989/Full-stack-blog/assets/122035759/1054a4be-7ad7-476c-aaeb-02e4bafcb837)

- **Mid Game**
![Screenshot (600)](https://github.com/wells1989/Full-stack-blog/assets/122035759/d82e35ae-f411-47cd-8314-04aa47ecd339)

- **Rules**
![Screenshot (599)](https://github.com/wells1989/Full-stack-blog/assets/122035759/09f73076-bd9b-4684-9934-ff44f5d95d85)

- **Game end**
![Screenshot (606)](https://github.com/wells1989/Full-stack-blog/assets/122035759/a4c2ea68-3aef-4f4c-9872-42d615b1ae4f)

### Project Notes:
- The goal of this project was to develop a more dynamic, variable game with more advanced functionality. I also refactored a lot of the code to incorporate modularity and abstraction throughout the process

#### Future-development:
- A future development would be to incprorate a different map style, for instance having a global map instead of the grid structure, also allowing player logins to track their win history.
