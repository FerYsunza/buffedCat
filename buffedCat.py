#
#  buffedCat.py
#
#  By Fer Ysunza, 12/01/24.
#

import os
import platform
import random

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_board(board, scores):
    clear_screen()
    print("BUFFED CAT!\n")
    print("Scores: Player - {}, Computer - {}, Draws - {}".format(scores["Player"], scores["Computer"], scores["Draw"]))
    print("\n   1   2   3")
    print("a  " + " | ".join(board[0]))
    print("  ---+---+---")
    print("b  " + " | ".join(board[1]))
    print("  ---+---+---")
    print("c  " + " | ".join(board[2]))
    print()

def player_move(board):
    while True:
        try:
            row_input = input("Enter row (a-c): ").lower()
            row_dict = {'a': 0, 'b': 1, 'c': 2}
            row = row_dict.get(row_input)
            col = int(input("Enter column (1-3): ")) - 1
            if row in row_dict.values() and 0 <= col <= 2 and board[row][col] == " ":
                board[row][col] = "X"
                break
            else:
                print("Invalid move, try again.")
        except ValueError:
            print("Please enter a valid number.")

def check_winner(board):
    for player in ["X", "O"]:
        if any(all(board[i][j] == player for j in range(3)) for i in range(3)) or \
           any(all(board[j][i] == player for j in range(3)) for i in range(3)) or \
           all(board[i][i] == player for i in range(3)) or \
           all(board[i][2 - i] == player for i in range(3)):
            return player
    return None

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner != None:
        return {"X": -10, "O": 10}[winner]
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

def computer_move(board):
    best_score = -float('inf')
    move = (0, 0)
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    move = (row, col)
    board[move[0]][move[1]] = "O"

def main():
    scores = {"Player": 0, "Computer": 0, "Draw": 0}
    play_again = 'y'

    while play_again.lower() == 'y':
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = "Player"

        while True:
            print_board(board, scores)
            if current_player == "Player":
                player_move(board)
                winner = check_winner(board)
                if winner == "X":
                    scores["Player"] += 1
                    print_board(board, scores)
                    print("Player wins!")
                    break
                elif winner == "O":
                    scores["Computer"] += 1
                    print_board(board, scores)
                    print("Computer wins!")
                    break

            else:
                print("Computer is making its move...")
                computer_move(board)
                winner = check_winner(board)
                if winner == "O":
                    scores["Computer"] += 1
                    print_board(board, scores)
                    print("Computer wins!")
                    break

            if check_draw(board):
                scores["Draw"] += 1
                print_board(board, scores)
                print("It's a draw!")
                break

            current_player = "Computer" if current_player == "Player" else "Player"

        play_again = input("\nWould you like to play another round? (y/n): ")

    print("Thanks for playing BUFFED CAT!")

if __name__ == "__main__":
    main()
