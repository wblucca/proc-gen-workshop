# Author
# William Lucca

FILES = [
    'input1.txt',
    'input2.txt'
]

word_dicts = {}


def add_word_pair(first, second):
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
                    add_word_pair(last_word, word)
                    last_word = word


def main():
    construct_dicts()
    
    for word in word_dicts:
        print(word, word_dicts[word])


if __name__ == '__main__':
    main()
