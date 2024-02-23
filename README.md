# friendly-octo-waddle

### Things we need to decide on as a group:

1. What the project is going to be about

   - Connect-4 with an AI trained using Reinforcement Learning (RL).
   - Want to support HvH AIvH & AIvAI

3. What programming language we're gonna use

    - Python, probably a simple command-line interface to start

4. Plan out the initial tasks

    - Crash course in Python!
    - Develop logic for the game, inc HvH mode
      + User interface
      + Logic to determine rules (valid moves, winning conditions, stalemate/end-game, positioning tokens)
      + Design the game "model" (the implementation of the game state)
    - Introduce the ideas behind simple RL, including state-action spaces (Q-tables) & Q-Learning
    - Implement agent using Q-Learning
      + TODO: define steps

5. Structure

   - Need an interface to customize the game
   - Print the game board
   - Players need to play the game
   - allow for different player types
   - different game modes (e.g. player vs machine, player vs player)
   - Get input from the players
   - Place the piece in the board
   - check if the move was valid.
   - Decide what happens when the move is invalid.
   - check if the player wins
   - 