# Author
# William Lucca
import random

FILES = [
    'input1.txt',
    'input2.txt'
]

word_dicts = {}


def add_pair_to_dict(first, second):
    global word_dicts
    
    # If either is an empty string, don't modify dictionary
    if first is '' or second is '':
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
    num_choices = 0
    for word in word_dicts[last_word]:
        num_choices += word_dicts[last_word][word]
    
    rand = random.random()
    cumulative_prob = 0
    
    for word in word_dicts[last_word]:
        cumulative_prob += word_dicts[last_word][word] / num_choices
        if rand < cumulative_prob:
            return word
    
    # Probabilities didn't accumulate to one
    raise Exception('Probabilities for next word did not accumulate to 1.')


def string_from_dicts():
    string = ''
    last_word = 'a'
    
    while not should_terminate(string):
        next_word = get_next_word(last_word)
        string += next_word
        last_word = next_word
    
    return string


def should_terminate(string):
    # Don't terminate if empty
    if len(string) == 0:
        return False
    
    # Terminate on period
    if string[-1] is '.':
        return True
    
    return False


def main():
    construct_dicts()
    
    for word in word_dicts:
        print(word, word_dicts[word])
    
    print(string_from_dicts())


if __name__ == '__main__':
    main()
