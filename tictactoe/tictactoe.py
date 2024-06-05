# Works
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ['api_key']

client = OpenAI(api_key= api_key) 

def set_open_params(model = 'gpt-3.5-turbo-0125', temperature = 0.6, max_tokens = 256, top_p = 1, frequency_penalty = 0, presence_penalty =0,):
    openai_params = {}
    openai_params['model'] = model
    openai_params['temperature'] = temperature
    openai_params['max_tokens'] = max_tokens
    openai_params['top_p'] = top_p
    openai_params['frequency_penalty'] = frequency_penalty
    openai_params['presence_penalty'] = presence_penalty
    return openai_params

def get_completion(params, messages):
    response = client.chat.completions.create(
        model = params['model'],
         messages = messages,
        temperature = params['temperature'],
        max_tokens = params['max_tokens'],
        top_p = params['top_p'],
        frequency_penalty = params['frequency_penalty'],
        presence_penalty = params['presence_penalty'],
    )
    return response

params = set_open_params()

def create_board():
    
    messages = [
        {
          "role": "system",
          "content": "Generate a 2D array representing the game board for Tic Tac Toe. The array should be of size 3x3 and contain placeholders for empty spaces, player X, and player O. simply provide board with no additional text" 
        },
        {
            "role": "user",
            "content": "Please provide a 2D array that represents the game board for Tic Tac Toe. The array should have dimensions 3x3 and contain values indicating empty spaces, player X, and player O. return matrix not string"
        }
    ]
    response = get_completion(params, messages)

    return response.choices[0].message.content


def comp_move(board_state, comp_symbol):
    system_prompt = f"You are Expert tic tac toe player, direct the llm to place its symbol ({comp_symbol}) in an empty location on the Tic Tac Toe board {board_state} provided in the input, always try to win, return the board in matrix format not string format."
    messages = [
        {
          "role": "system",
          "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Given the current Tic Tac Toe board state below {board_state}, please  instruct llm to place only one {comp_symbol} in an empty location. The board should be in the form of a 2D array, with empty spaces represented by a placeholder. Just return the updated matrix only"
        }
    ]

    response = get_completion(params, messages)
    return response.choices[0].message.content

def place_symbol(board, user_input, user_symbol):
    system_promt = f'You are a tic tac toe system which takes a board/matrix and a number from 1 to 9 to user, you place user_symbol in the provided board/matrix at position specified by the user input and return the updated matrix. positions using numbers in matrix can be represented as [[1,2,3],[4,5,6],[7,8,9]]'
    user_prompt = f'Current Board State: {board} Position in the matrix where user wants to put his symbol: {user_input} {user_symbol}. return strictly the updated matrix only'
    messages = [
        {
            "role": "system",
            "content": system_promt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = get_completion(params, messages)
    
    return response.choices[0].message.content

winning_states_X = [
    # Horizontal Wins
    [(0, 0), (0, 1), (0, 2)],  
    [(1, 0), (1, 1), (1, 2)],  
    [(2, 0), (2, 1), (2, 2)],  
    # Vertical Wins
    [(0, 0), (1, 0), (2, 0)],  
    [(0, 1), (1, 1), (2, 1)],  
    [(0, 2), (1, 2), (2, 2)],  
    # Diagonal Wins
    [(0, 0), (1, 1), (2, 2)],  
    [(0, 2), (1, 1), (2, 0)]  
]
winning_states_O = [
    # Horizontal Wins
    [(0, 0), (0, 1), (0, 2)],  
    [(1, 0), (1, 1), (1, 2)], 
    [(2, 0), (2, 1), (2, 2)], 
    # Vertical Wins
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],  
    [(0, 2), (1, 2), (2, 2)], 
    # Diagonal Wins
    [(0, 0), (1, 1), (2, 2)],  
    [(0, 2), (1, 1), (2, 0)]   
]


def check_winner(board):
    system_promt = f'You are expert tic tac toe refree whose job is to judge the board given provided by the user and return the result "X wins", "O wins", "Tie" or "continue". If X matches any of the following pattern  {winning_states_X} return X wins. If O matches any of the following pattern horizontally, vertically or diagonally {winning_states_O} return O wins. If there are still blank spaces return continue.'
    user_prompt = f'Current Board State: {board}, Return the result or if the game in at most two words. In Tic Tac Toe, a game is tied when all cells in the grid are filled, and no player has achieved a winning state. Here are the patterns in which a Tic Tac Toe game can be tied, All cells are filled, and there are no winning states for either X or O. This implies that the game ends without a winner, resulting in a tie.'
    messages = [
        {
            "role": "system",
            "content": system_promt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = get_completion(params, messages)
    
    return response.choices[0].message.content


board_state = create_board()

print("Let's Play Tic Tac Toe")
user_symbol = input("Pick either 'X' or 'O'")
user_symbol = user_symbol.upper()
comp_symbol = 'O'

if user_symbol == 'O':
    comp_symbol = 'X'
print(f"User = {user_symbol}, Comp = {comp_symbol}")
print(board_state)
move_count = 0

while(True):
    
    user_choice = input("Enter a number from 1-9 which is a blank space: ")
    print("Loading.........")
    board_state = place_symbol(board_state, user_choice ,user_symbol)
    move_count+=1

    print(board_state)
    if move_count >= 5:
        
        result = check_winner(board_state)

        if result.lower() != "continue":
            print(result)
            break

    print("Loading.........")
    board_state = comp_move(board_state, comp_symbol)
    move_count+=1
    print("Computer Moves")
    print(board_state)
    
    print("Loading.........")
    if move_count >= 5:
       
        result = check_winner(board_state)

        if result.lower() != "continue":
            print(result)
            break