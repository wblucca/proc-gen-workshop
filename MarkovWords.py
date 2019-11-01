# Author
# William Lucca

FILES = [
    'input1.txt',
    'input2.txt'
]

words_dict = {}


def main():
    
    # Open each file to read line-by-line, word-by-word
    for file_name in FILES:
        with open(file_name, 'r') as f:
            for line in f:
                for word in line.split():
                    if word in words_dict:
                        words_dict[word] += 1
                    else:
                        words_dict[word] = 1
    
    for word in words_dict:
        print(word, words_dict[word])


if __name__ == '__main__':
    main()
