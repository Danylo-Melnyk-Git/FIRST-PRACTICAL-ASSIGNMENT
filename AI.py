from tkinter import *
from tkinter import StringVar
from tkinter import messagebox
from ttkbootstrap import Style, Label, Radiobutton, Button, Scale
from ttkbootstrap.constants import *
import random
import time

# all global variables
global selected_pair, root, Game, selected_algorithm, game_starter, selected_string_length, Get_Started
total_ai_move_time = 0
ai_move_count = 0
nodes_visited = 0
numbers = []
game_scores = [0, 0]
current_turn = 0
selected_index = []


# Game window function
def Game_Window():
    global Get_Started, numbers, selected_index, selected_pair, Game, Turn_Label
    # checks if every attribute of the game is selected
    if selected_algorithm is None or game_starter is None or selected_string_length is None:
        messagebox.showerror("Error",
                             "Please make sure to select the game starter, algorithm, and string length before starting the game!")
    else:
        # Hide the current window
        Get_Started.withdraw()

        # Create a Game_Window
        Game = Toplevel()
        Game.title("Numerical String Game")
        Game.state('zoomed')  # Maximize the new window

        # Window Title
        Label(Game, text="The Generated String is: ", font=("Helvetica", 18)).pack(pady=20)

        # Function to Generate the string
        def generate_str(string_length):
            return [random.randint(1, 9) for _ in range(string_length)]

        numbers = generate_str(selected_string_length)
        Label(Game, text=numbers, font=("Helvetica", 18), bootstyle="default,inverse").pack(pady=10)

        # Label to display the selected pair
        Label(Game, text="Please select any two adjacent numbers", font=("Helvetica", 14)).pack(
            pady=10)

        # Function to handle selection of numbers
        selected_index = [None]  # Using a list to store selected index

        def select_number(index):
            global selected_index, selected_pair
            if selected_index[0] is None:
                selected_index[0] = index
            elif abs(selected_index[0] - index) == 1:  # Check if the selected index is adjacent
                # Store the selected pair globally
                selected_pair = (numbers[selected_index[0]], numbers[index])
                selected_pair_label.config(text=f"The selected pair is: {selected_pair}")
                # Clear selection
                buttons[selected_index[0]].config()
            else:
                print("Number is not selected")

        # Creating a frame to hold the buttons horizontally
        button_frame = Frame(Game)
        button_frame.pack(pady=10)

        # Determining button width based on the length of the generated string
        button_width = max(2, 3)

        # Creating buttons for each number in the string
        buttons = []
        for i, number in enumerate(numbers):
            button = Button(button_frame, text=number, width=button_width, command=lambda idx=i: select_number(idx),
                            bootstyle="warning-outline")
            button.pack(side=LEFT, padx=5, pady=10)
            buttons.append(button)

            # Label to display selected pair
        selected_pair_label = Label(Game, text="The selected pair is: ", font=("Helvetica", 14))
        selected_pair_label.pack(pady=10)

        # Function to create the buttons to select a pair
        def update_buttons():
            for i, button in enumerate(buttons):
                if i < len(numbers):
                    button.config(text=numbers[i], state=NORMAL)
                else:
                    button.pack_forget()  # This hides the button if it's beyond the current numbers list

        def update_scores():
            # Assuming player 0 is human, player 1 is AI
            AI_Score.config(text=str(game_scores[1]))
            Your_Score.config(text=str(game_scores[0]))

        def update_turn():
            global current_turn
            # Toggle between 0 and 1 to switch turns
            current_turn = (current_turn + 1) % 2
            # Update the UI element that indicates whose turn it is
            Turn_Label.config(text="Your turn!" if current_turn == 0 else "AI's turn...")

        def check_game_end():
            global game_scores
            if len(numbers) <= 1:
                player_score, ai_score = game_scores
                if player_score > ai_score:
                    result_text = "Congratualtions! You win."
                elif player_score < ai_score:
                    result_text = "Good Luck! AI wins."
                else:
                    result_text = "It's a draw!"

                messagebox.showinfo("Game Over", f"{result_text}")
                response = messagebox.askyesno("Game Over", "The game has ended. Do you want to play again?")
                if response:
                    Back_To_Get_Started()  # Starting a new game
                else:
                    Game.destroy()  # Closing the game window

        # Replacing the numbers according to the taks
        def replace_pair():
            global numbers, game_scores, current_turn, selected_index, selected_pair

            pair_sum = sum(selected_pair)

            replacement_value = 0
            if pair_sum > 7:
                replacement_value = 1
                game_scores[current_turn] += 1
            elif pair_sum < 7:
                replacement_value = 3
                game_scores[(current_turn + 1) % 2] -= 1
            else:  # pair_sum == 7
                replacement_value = 2
                game_scores[0] += 1
                game_scores[1] += 1

            # Update the numbers list with the replacement value
            numbers[selected_index[0]] = replacement_value
            del numbers[selected_index[0] + 1]  # deleting the second number of the pair

            # Update UI elements
            update_buttons()
            update_scores()
            update_turn()
            reset_pairs()
            check_game_end()

        def minimax(state, depth, max_player):
            global nodes_visited
            nodes_visited += 1
            if depth == 0 or len(state) <= 1:
                return evaluate_state(state), None

            if max_player:
                max_eval = float('-inf')
                best_action = None
                for i in range(len(state) - 1):
                    new_state = state[:i] + [state[i] + state[i + 1]] + state[i + 2:]
                    eval, _ = minimax(new_state, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_action = i
                return max_eval, best_action
            else:
                min_eval = float('inf')
                best_action = None
                for i in range(len(state) - 1):
                    new_state = state[:i] + [state[i] + state[i + 1]] + state[i + 2:]
                    eval, _ = minimax(new_state, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_action = i
                return min_eval, best_action

        def alpha_beta(state, depth, alpha, beta, max_player):
            global nodes_visited
            nodes_visited += 1
            if depth == 0 or len(state) <= 1:
                return evaluate_state(state), None

            if max_player:
                max_eval = float('-inf')
                best_action = None
                for Element in range(len(state) - 1):
                    new_state = state[:Element] + [state[Element] + state[Element + 1]] + state[Element + 2:]
                    evaluate_1, _ = alpha_beta(new_state, depth - 1, alpha, beta, False)
                    if evaluate_1 > max_eval:
                        max_eval = evaluate_1
                        best_action = Element
                    alpha = max(alpha, evaluate_1)
                    if beta <= alpha:
                        break
                return max_eval, best_action
            else:
                min_eval = float('inf')
                best_action = None
                for Element in range(len(state) - 1):
                    new_state = state[:Element] + [state[Element] + state[Element + 1]] + state[Element + 2:]
                    evaluate_1, _ = alpha_beta(new_state, depth - 1, alpha, beta, True)
                    if evaluate_1 < min_eval:
                        min_eval = evaluate_1
                        best_action = Element
                    beta = min(beta, evaluate_1)
                    if beta <= alpha:
                        break
                return min_eval, best_action

        def evaluate_state(state):
            # Simple evaluation function - return the sum of all numbers in the state
            return sum(state)

        # Integrate with AI's turn
        def AI_turn():
            global numbers, game_scores, current_turn, selected_algorithm, selected_index, selected_pair, nodes_visited, total_ai_move_time, ai_move_count
            start_time = time.perf_counter()
            if selected_algorithm == "Minimax":
                best_action = minimax(numbers, 1, 3)[1]
            else:  # Alpha-Beta pruning
                best_action = alpha_beta(numbers, 1, float('-inf'), float('inf'), 3)[1]

            end_time = time.perf_counter()
            move_time = end_time - start_time
            total_ai_move_time += move_time
            ai_move_count += 1
            average_time = total_ai_move_time / ai_move_count  # algorithm time usage computation

            if best_action is not None:
                selected_index[0] = best_action
                Play_button.config(state=NORMAL)
                Reset_button.config(state=NORMAL)
                # Set the selected_pair variable based on the selected_index
                selected_pair = (numbers[selected_index[0]], numbers[selected_index[0] + 1])
                replace_pair()
                print("Completed move by AI")
                print(f"Avarage time taken for the move: {average_time} seconds")
                print(f"Total nodes visited for this move: {nodes_visited}")

        def Player_turn():
            global numbers, game_scores, current_turn

            replace_pair()

            if current_turn == 1:
                Play_button.config(state=DISABLED)
                Game.after(1500, AI_turn)

        def Start_game():
            global current_turn
            # Set initial turn based on game starter
            if game_starter == "User":
                current_turn = 0  # User's turn
                Turn_Label.config(text="Your turn!")
                Start_button.config(state=DISABLED)
                Play_button.config(state=NORMAL)
                Reset_button.config(state=NORMAL)
            else:
                current_turn = 1  # Computer's turn
                Turn_Label.config(text="AI's turn...")
                Start_button.config(state=DISABLED)
                Play_button.config(state=NORMAL)
                # Start with AI's turn if computer starts
                Game.after(1500, AI_turn)

        Play_frame = Frame(Game)
        Play_frame.pack(pady=10)

        Play_button = Button(Play_frame, text="Play", command=Player_turn, bootstyle="success",
                             width=10)  # Set width to 10
        Play_button.pack(padx=100, pady=10)
        Play_button.config(state=DISABLED)

        def reset_pairs():
            # Clear both indices in selected_index list
            selected_index[0] = None
            selected_pair_label.config(text="The selected pair is: ")

        Start_button = Button(Play_frame, text="Start", command=Start_game, bootstyle="success",
                              width=10)  # Set width to 10
        Start_button.pack(padx=100, pady=10)

        Reset_button = Button(Play_frame, text="Reset", bootstyle="danger", command=reset_pairs,
                              width=10)  # Set width to 10
        Reset_button.pack(padx=100, pady=10)
        Reset_button.config(state=DISABLED)

        Score_Title_frame = Frame(Game)
        Score_Title_frame.pack(pady=10)

        Label(Score_Title_frame, text="AI SCORE ", font=("Helvetica", 14)).pack(side=LEFT, padx=200,
                                                                                pady=10)

        Label(Score_Title_frame, text="YOUR SCORE ", font=("Helvetica", 14)).pack(side=LEFT,
                                                                                  padx=200, pady=10)

        Score_frame = Frame(Game)
        Score_frame.pack(pady=10)

        AI_Score = Label(Score_frame, text="0", font=("Helvetica", 14))
        AI_Score.pack(side=LEFT, padx=250, pady=10)
        Your_Score = Label(Score_frame, text="0", font=("Helvetica", 14))
        Your_Score.pack(side=LEFT, padx=250, pady=10)

        Turn_Label = Label(Game, text=" ", font=("Helvetica", 14))
        Turn_Label.pack(pady=10)

        def Back_To_Get_Started():
            global game_scores
            game_scores = [0, 0]
            # Destroy the Game_Window
            Game.destroy()
            # Restore the visibility of the root window
            root.deiconify()
            Get_Started_Window()

        Back_button = Button(Game, text="Back", bootstyle="danger", command=Back_To_Get_Started,
                             width=10)  # Set width to 10
        Back_button.pack(side=LEFT, padx=20, pady=10)


# Get Started Window
def Get_Started_Window():
    global selected_algorithm, game_starter, selected_string_length, Get_Started

    # Hiding the current window
    root.withdraw()

    # Creating a Get_Started_Window
    Get_Started = Toplevel()
    Get_Started.title("Numerical String Game")
    Get_Started.state('zoomed')  # Maximize the new window

    # Window Title
    Label(Get_Started, text="Game Setup", font=("Helvetica", 28)).pack(pady=40)

    # Who starts the game?     
    Label(Get_Started, text="Who starts the game?", font=("Helvetica", 14)).pack(pady=10)

    # Funtion for displaying who starts the game
    def Starter_selc():
        global game_starter
        game_starter = "User" if Game_Starter.get() == "User" else "Computer"
        Starter_Label.config(text="The game will be started with the " + f'{game_starter}')

    frame_2 = Frame(Get_Started)
    frame_2.pack(pady=30, side=TOP)

    Game_Starters = ["User", "Computer"]
    Game_Starter = StringVar()

    for Who_Start in Game_Starters:
        Radiobutton(frame_2, bootstyle="success", variable=Game_Starter, text=Who_Start, value=Who_Start,
                    command=Starter_selc).pack(side=LEFT, padx=10)

    Starter_Label = Label(Get_Started, text="The game will be started with the ", font=("Helvetica", 9))
    Starter_Label.pack(pady=10)

    # Choosing the algorithm!     
    Label(Get_Started, text="Choose the algorithm!", font=("Helvetica", 14)).pack(pady=10)

    def Algorithm_selc():
        global selected_algorithm
        selected_algorithm = My_Algorithm.get()
        Algorithm_Label.config(text="The chosen algorithm is " + f'{selected_algorithm}')

    frame_2 = Frame(Get_Started)
    frame_2.pack(pady=30, side=TOP)

    Algorithms = ["Minimax", "AlphaBeta"]
    My_Algorithm = StringVar()

    for Algorithm in Algorithms:
        Radiobutton(frame_2, bootstyle="success", variable=My_Algorithm, text=Algorithm, value=Algorithm,
                    command=Algorithm_selc).pack(side=LEFT, padx=10)

    Algorithm_Label = Label(Get_Started, text="The chosen algorithm is ", font=("Helvetica", 9))
    Algorithm_Label.pack(pady=10)

    # String length     
    Label(Get_Started, text="Select the string length!", font=("Helvetica", 14)).pack(pady=10)

    def scaler(e):
        global selected_string_length
        selected_string_length = int(my_scale.get())
        Scale_Label.config(text="The selected length is " + f'{selected_string_length}')

    my_scale = Scale(Get_Started, bootstyle="success", from_=15, to=25, command=scaler)
    my_scale.pack(pady=30)

    Scale_Label = Label(Get_Started, text="The selected length is ", font=("Helvetica", 9))
    Scale_Label.pack(pady=10)

    # Let's Play Button           
    Style().configure('success.TButton', font=("Helvetica", 18))
    button_2 = Button(Get_Started, command=Game_Window, text="Let's play!", style='success.TButton')
    button_2.pack(pady=20)


# Main Window
def Main_Window():
    global root
    root = Style(theme='superhero').master
    root.title("Numerical String Game")
    root.state('zoomed')  # Maximize the current window
    # Title
    Label(text="Welcome to the Numerical String Game!", font=("Helvetica", 28)).pack(pady=50)
    # Subtitle
    Label(root, text="Game description:", font=("Helvetica", 18), bootstyle="default,inverse").pack(pady=30)
    # Description
    label_3 = Label(
        text="Before starting the game, the player should choose the length of the numerical string which is should be between 15 and 25. Then, the game software randomly generates a numerical string containing the numbers 1 to 9. At the beginning of the game, Each player has 0 points and the players perform the moves sequentially. The player chooses any pair of two adjacent numbers and replaces it with a single number based on the following conditions:",
        font=("Helvetica", 14))
    label_3.pack()
    label_3.configure(wraplength=1200)

    label_4 = Label(
        text="1. If the sum of the numbers > 7, then the pair of numbers is replaced by 1 and one point is added to the player's score.",
        font=("Helvetica", 14))
    label_4.pack()
    label_4.configure(wraplength=1000)

    label_5 = Label(
        text="2. If the sum of the numbers < 7, then it is replaced by 3 and 1 point is deducted from the opponent's score.",
        font=("Helvetica", 14))
    label_5.pack()
    label_5.configure(wraplength=1000)

    label_6 = Label(
        text="3. if the sum of the numbers = 7, then it is replaced by 2 and 1 point is added to both the player's score and the opponent's score.",
        font=("Helvetica", 14))
    label_6.pack()
    label_6.configure(wraplength=1000)

    label_7 = Label(
        text="Finally, The game ends when there are no more pairs of numbers to replace. If the players have the same number of points, the result is a draw. Otherwise, the player with the higher number of points wins. ",
        font=("Helvetica", 14))
    label_7.pack(pady=10)
    label_7.configure(wraplength=1200)
    # Get Started button
    Style().configure('success.TButton', font=("Helvetica", 18))
    button_1 = Button(text="Get Started!", command=Get_Started_Window, style='success.TButton')
    button_1.pack(pady=80)

    root.mainloop()


Main_Window()
