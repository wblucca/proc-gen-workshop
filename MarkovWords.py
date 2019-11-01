# Author
# William Lucca

import random

FILES = [
    'input1.txt',
    'input2.txt'
]

# Markov chain data
starting_words = []
word_dicts = {}


def add_pair_to_dict(first, second):
    """Mark the word pair in the dictionary as an existing/more common relationship
    
    :param first: The preceding word, as it appears in the training data
    :param second: The following word, as it appears in the training data
    """
    
    global starting_words, word_dicts
    
    # If first is an empty or terminal string, add second as a starting word
    if first is '' or is_terminal(first):
        if second not in starting_words:
            starting_words.append(second)
        return
    
    # Add/increment the pair
    if first in word_dicts:
        if second in word_dicts[first]:
            # If this pair already exists, increment
            word_dicts[first][second] += 1
        else:
            # If this latter half of the pair doesn't exist, start it at 1
            word_dicts[first][second] = 1
    else:
        # If neither part of this word pair exists, start it at 1
        word_dicts[first] = {second: 1}


def construct_dicts():
    """Read through input files to train the program on word relationships"""
    
    global word_dicts
    
    # Open each file to read line-by-line, word-by-word
    for file_name in FILES:
        with open(file_name, 'r') as f:
            # Previous word (in this file)
            last_word = ''
            for line in f:
                for word in line.split():
                    add_pair_to_dict(last_word, word)
                    last_word = word


def get_next_word(last_word):
    """Using weightings in dictionaries, randomly select the next word
    
    :param last_word: The prior word to use to when selecting the next word
    :return: The next word
    :raises Exception: If something goes wrong when computing probabilities of
    the next word, raise an exception
    """
    
    # Count up the number of possible words, including repeats
    num_choices = 0
    if last_word in word_dicts:
        for word in word_dicts[last_word]:
            num_choices += word_dicts[last_word][word]
    
    # Return empty string if no valid choice
    if num_choices == 0:
        return ''
    
    # Pick a random value for the word
    rand = random.random()
    cumulative_prob = 0
    
    # Add up the cumulative probability (from 0 to 1) and return the current
    # when reaching the random value in the cumulative probability
    for word in word_dicts[last_word]:
        cumulative_prob += word_dicts[last_word][word] / num_choices
        if rand < cumulative_prob:
            return word
    
    # Probabilities didn't accumulate to one
    raise Exception('Probabilities for next word did not accumulate to 1.')


def string_from_dicts():
    """Returns a string created from the Markov chain input data
    
    The string is terminated when it reaches a terminal case i.e.
    is_terminal(string)).
    
    :return: The generated string after meeting some termination case
    """
    
    # Get random starting word and begin string with it
    starting_word_id = random.randint(0, len(starting_words) - 1)
    last_word = starting_words[starting_word_id]
    string = last_word.capitalize()
    
    while not is_terminal(string) and last_word is not '':
        next_word = get_next_word(last_word)
        string += next_word
        last_word = next_word
    
    return string


def is_terminal(string):
    """Defines the rules for when to terminate the generated string
    
    :param string: The string to check for termination
    :return: True if satisfying termination conditions, False otherwise
    """
    
    # Don't terminate if empty
    if len(string) == 0:
        return False
    
    # Terminate on period
    if string[-1] is '.':
        return True
    
    return False


def main():
    """Train the Markov chain and produce output from it"""
    
    construct_dicts()
    
    for word in word_dicts:
        print(word, word_dicts[word])
    
    print(string_from_dicts())


if __name__ == '__main__':
    main()
