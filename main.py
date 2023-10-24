"""
Simple Deterministic Finite Automata(DFA) Simulator
Author: Kenyon Leblanc

This project is a personal implementation of a Deterministic Finite Automata(DFA) simulator.

Directions:
Make sure you are in the directory of "main.py". Start the program by typing "python main.py" or "python3 main.py".

At anytime, you may type "exit" to quit the program.

You will be prompted for a filename, please make sure to include the extension.
If not file is not found, you will be prompted to try again.

The file must be formatted in this specific format:
    Line 1: The first line of your file will be a single integer that indicates how many states the DFA contains.
    A note about states: States are represented by consecutive integers starting from zero. State zero is
    always the start state. All states of the DFA must be represented; this includes the dead state.

    Line 2: The second line of the file contains a space-separated list of integers that represent accepting
    states.

    Line 3: Alphabet: a space-separated list of characters in the DFA's alphabet.

    Lines 4 – end: Transitions: These will be represented in a table indexed by state number and character.
    The input file will have one line for each row of the table. Each row consists of integers that represent the
    states the machine will transition to on each of the alphabet characters. If the DFA has seven states and
    three characters, there will be seven lines containing three integers each. The first row corresponding to
    the transitions from state zero, the second from state one, etc. Note that all transitions must be
    represented; do not assume a missing transition for a character is to the dead state.

You will be prompted for a string to be inputted into the DFA.
If an invalid character is found, it will be displayed along with a list of valid characters.

If all input is valid, the process of iterating through the string will be shown.
{e} will be they symbol for the empty string.
At the end of the DFA computation will be an ACCEPTED or REJECTED.
ACCEPTED means that the processed string ended in an accepting state.
REJECTED means that the processed string ended in a dead state.

You will be continually asked for an input string until "exit" is entered.
"""

import os  # Check directory files

# Initialize global lists
state_table = []
accepting_states = []
alphabet = []


def check_valid_file(file_name):
    """
    Check if file provided by user input is valid.
    :param file_name: file name w/ extension
    :return: valid file name
    """
    # Current directory
    directory = os.getcwd()
    # List of files from cwd
    listed_directory = os.listdir(directory)
    # Continue loop until valid file name is given
    while file_name not in listed_directory:
        print("File not found, please try again.")
        file_name = input("Please enter file name with extension: ")
        check_exit_command(file_name)

    return file_name


def load_file(file_name):
    """
    Load data from file into global variables.
    :param file_name: Name of file
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Store line 2 into accepted states list
    accepting_states.extend(list(map(int, lines[1].split())))

    # Store line 3 into alphabet list
    alphabet.extend(lines[2].split())

    # Store remaining lines from 4 onward into state table
    for line in lines[3:]:
        values = list(map(int, line.split()))
        state_table.append(values)


def check_string_input(user_input):
    """
    Check all elements in string are in defined alphabet.
    :param user_input: String from user input
    :return: Returns a valid string
    """
    comma = ","
    list_alphabet = comma.join(alphabet)
    check = -1

    while check != 1:
        check = check + 1
        for char in user_input:
            if char not in alphabet:
                print(f"REJECTED")
                print(f"Found invalid character {char}")
                print(f"Valid characters are {list_alphabet}")
                user_input = input("Please enter a string to evaluate: ")
                check_exit_command(user_input)
                check = check - 1
                break
    return user_input


def automata_logic(string):
    """
    Replicate logic of inputting a string into a DFSM.
    :param string: String to be checked
    :return: Returns final state when entire string was checked
    """
    current_state = 0
    dummy_string = string

    # Iterate through all characters in string
    for element in string:
        print(f"{current_state},{dummy_string}", end=" -> ")
        # Loop used for column number for state_table
        for i, char in enumerate(alphabet):
            if char == element:
                column = i
                break
        # Move states
        current_state = state_table[current_state][column]
        # If element is last in string
        if len(dummy_string) == 1:
            # Represent empty string
            dummy_string = "e"
            print(f"{current_state},"+"{"+f"{dummy_string}"+"}")
            # Return final state
            return current_state
        # Pop leftmost character out of string
        dummy_string = dummy_string[1:]
        print(f"{current_state},{dummy_string}")


def check_state(state):
    """
    Check if state is an accepting state. Print result.
    :param state: Takes the state variable (integer)
    """
    if state in accepting_states:
        print("ACCEPTED")
    else:
        print("REJECTED")


def check_exit_command(string):
    """
    Check if string reads "exit". If so, exit gracefully.
    :param string:
    :return:
    """
    if string == "exit":
        print("Closing...")
        exit(0)


if __name__ == '__main__':
    arrow = " -> "

    print("Type exit at anytime to quit.")

    # Gather file names and load graph
    file_name = input("Please enter DFA file name with extension: ")
    check_exit_command(file_name)
    file_name = check_valid_file(file_name)
    print("Loading...")
    load_file("DFA.txt")

    # Infinite loop so that the user may input as many string inputs as they want.
    while 1:
        user_input = input("Please enter a string to evaluate: ")
        check_exit_command(user_input)
        user_input = check_string_input(user_input)

        print("Computing...")
        end_state = automata_logic(user_input)
        check_state(end_state)
