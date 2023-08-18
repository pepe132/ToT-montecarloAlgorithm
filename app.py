import random
from tree_of_thoughts import OpenAILanguageModel
from tree_of_thoughts import MonteCarloTreeofThoughts

api_model= "gpt-3.5-turbo"
model = OpenAILanguageModel(api_key='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', api_model=api_model)
# Initialize the MonteCarloTreeofThoughts class with the model
tot = MonteCarloTreeofThoughts(model)
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def print_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]}")
            if i < 6:
                print("---------")

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def check_draw(self):
        return all(cell != ' ' for cell in self.board)

    def get_valid_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def make_move(self, position):
        self.board[position] = self.current_player
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def get_opponent(self):
        return 'O' if self.current_player == 'X' else 'X'

    def simulate_random_game(self):
        while not self.check_winner('X') and not self.check_winner('O') and not self.check_draw():
            valid_moves = self.get_valid_moves()
            move = random.choice(valid_moves)
            self.make_move(move)

        if self.check_winner('X'):
            return 'X'
        elif self.check_winner('O'):
            return 'O'
        else:
            return 'D'

    def monte_carlo_search(self, simulations):
        best_move = None
        best_score = float('-inf')
        for move in self.get_valid_moves():
            score_sum = 0
            for _ in range(simulations):
                cloned_game = TicTacToe()
                cloned_game.board = self.board.copy()
                cloned_game.current_player = self.current_player
                cloned_game.make_move(move)
                outcome = cloned_game.simulate_random_game()

                if outcome == 'X':
                    score_sum += 1
                elif outcome == 'D':
                    score_sum += 0.5

            # Calculate the win percentage for the current move
            win_percentage = (score_sum / simulations) * 100
            print(f"Move {move}: Win Percentage for X: {win_percentage:.2f}%")

            if score_sum > best_score:
                best_score = score_sum
                best_move = move

                num_thoughts = 1
                max_steps = 3
                max_states = 4
                pruning_threshold = 0.5
                solution = tot.solve(
                    initial_prompt='O',
                    num_thoughts=num_thoughts,
                    max_steps=max_steps,
                    max_states=max_states,
                    pruning_threshold=pruning_threshold,
                    # sleep_time=sleep_time
                )
                print(solution)

        return best_move

if __name__ == "__main__":
    game = TicTacToe()
    while not game.check_winner('X') and not game.check_winner('O') and not game.check_draw():
        game.print_board()
        if game.current_player == 'X':
            user_move = int(input("Enter your move (0-8): "))
            while user_move not in game.get_valid_moves():
                print("Invalid move. Try again.")
                user_move = int(input("Enter your move (0-8): "))
            game.make_move(user_move)
        else:
            simulations = 1000  # Increase this value for better performance, but it will take more time
            computer_move = game.monte_carlo_search(simulations)
            game.make_move(computer_move)

    game.print_board()

    if game.check_winner('X'):
        print("Congratulations! You win!")
    elif game.check_winner('O'):
        print("Computer wins!")
    else:
        print("It's a draw!")