# Author
# William Lucca

FILES = [
    'input1.txt',
    'input2.txt'
]

word_dicts = {}

def construct_dicts():
    global word_dicts
    
    # Open each file to read line-by-line, word-by-word
    for file_name in FILES:
        with open(file_name, 'r') as f:
            for line in f:
                for word in line.split():
                    if word in word_dicts:
                        word_dicts[word] += 1
                    else:
                        word_dicts[word] = 1


def main():
    construct_dicts()
    
    for word in word_dicts:
        print(word, word_dicts[word])


if __name__ == '__main__':
    main()
