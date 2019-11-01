# Author
# William Lucca


words_dict = {}


def main():
    with open('input.txt', 'r') as f:
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
