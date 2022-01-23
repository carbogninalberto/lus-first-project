import math
from collections import defaultdict

def extract_sentences_tags(file_path, output_path):
    lines = []

    with open(file_path, 'r') as file:
        sentences = file.readlines()
        current_sentence = ""
        for sentence in sentences:
            # print(sentence)
            if sentence.strip('\n') != '':
                current_sentence += sentence.strip('\n').split('\t')[1] + " "
            else:
                lines.append(current_sentence + "\n")
                current_sentence = ""

    with open(output_path, 'w+') as file:
        file.writelines(lines)


def extract_sentence_map(file_path):
    pairs = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip('\n') != '':
                pairs.append(
                    (line.strip('\n').split('\t')[0], line.strip('\n').split('\t')[1])
                )
    return pairs


def define_transducer(pairs, export='baseline/fst.txt'):
    tags = defaultdict(int)
    words_tags = defaultdict(int)
    for pair in pairs:
        # tuple (word, tag)
        word = "{}\t{}".format(pair[0], pair[1])
        tag = pair[1]

        # word counting
        words_tags[word] += 1
        # tag counting
        tags[tag] += 1
    
    # probability
    prob_wt = defaultdict(float)
    for word in words_tags:
        t = word.split('\t')[1]
        # print(t, word)
        prob_wt[word] = -math.log(words_tags[word]/tags[t])

    n_tags = len(tags)
    for t in tags:
        # print(t, 1/n_tags)
        prob_wt['<UNK>\t{}'.format(t)] = -math.log(1/n_tags)

    with open(export, 'w+') as fst_file:
        for wt in prob_wt:
            line = "0\t0\t{}\t{}\t{}\n".format(wt.split('\t')[0], 
                                                wt.split('\t')[1], 
                                                prob_wt[wt]
                                            )
            fst_file.write(line)
        fst_file.write('0')
    

