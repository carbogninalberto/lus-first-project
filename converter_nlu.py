import json
import sys

DATASET = sys.argv[1] if len(sys.argv) > 1 else "ATIS"
VALUE_KEY = "text" if len(sys.argv) > 1 else "value"
START_KEY = "start" if len(sys.argv) > 1 else "start"
END_KEY = "stop" if len(sys.argv) > 1 else "end"

with open('dataset/{}/train.json'.format(DATASET), 'r') as train, \
        open('dataset/{}/train.txt'.format(DATASET), 'w') as train_parsed:
    train_data = json.load(train)

    # getting common examples
    if DATASET == "ATIS":
        sentences = train_data['rasa_nlu_data']['common_examples']
    else:
        sentences = train_data['sentences']

    for sentence in sentences:
        entities = sentence['entities']
        txt = sentence['text'].replace('?', ' ?')
        txt_after = str(txt)
        for entity in entities:
            values = entity[VALUE_KEY].replace('?', ' ?').split(' ')
            txt_value = txt[entity[START_KEY]-1:entity[END_KEY]].strip()
            for i, v in enumerate(values):
                if i == 0:
                    values[i] = "[{}@B-{}]".format(v.replace(' ', '#'), entity['entity'])
                else:
                    values[i] = "[{}@I-{}]".format(v.replace(' ', '#'), entity['entity'])
            txt_values = ' '.join(values)
            txt_after = txt_after.replace(entity[VALUE_KEY], txt_values)

        # print(txt)
        # print(txt_after)
        lines = txt_after.split(' ')
        for line in lines:
            cleaned_line = line.replace('[', '').replace(']', '')
            if cleaned_line == line:
                train_parsed.write('{}\t{}\n'.format(line, 'O'))
            else:                
                cleaned_line = cleaned_line.split('@')
                train_parsed.write('{}\t{}\n'.format(cleaned_line[0].replace('#', ' '), cleaned_line[1]))
        train_parsed.write('\n')

with open('dataset/{}/test.json'.format(DATASET), 'r') as test, \
        open('dataset/{}/test.txt'.format(DATASET), 'w') as test_parsed, \
        open('dataset/{}/utterances.txt'.format(DATASET), 'w') as test_utterances:
    test_data = json.load(test)

    # getting common examples
    if DATASET == "ATIS":
        sentences = test_data['rasa_nlu_data']['common_examples']
    else:
        sentences = test_data['sentences']

    for sentence in sentences:
        test_utterances.write('{}\n'.format(sentence['text']))
        entities = sentence['entities']
        txt = sentence['text'].replace('?', ' ?')
        txt_after = str(txt)
        for entity in entities:
            values = entity[VALUE_KEY].replace('?', ' ?').split(' ')
            txt_value = txt[entity[START_KEY]-1:entity[END_KEY]].strip()
            for i, v in enumerate(values):
                if i == 0:
                    values[i] = "[{}@B-{}]".format(v.replace(' ', '#'), entity['entity'])
                else:
                    values[i] = "[{}@I-{}]".format(v.replace(' ', '#'), entity['entity'])
            txt_values = ' '.join(values)
            txt_after = txt_after.replace(entity[VALUE_KEY], txt_values)

        # print(txt)
        # print(txt_after)
        lines = txt_after.split(' ')
        for line in lines:
            cleaned_line = line.replace('[', '').replace(']', '')
            if cleaned_line == line:
                test_parsed.write('{}\t{}\n'.format(line, 'O'))
            else:                
                cleaned_line = cleaned_line.split('@')
                test_parsed.write('{}\t{}\n'.format(cleaned_line[0].replace('#', ' '), cleaned_line[1]))
        test_parsed.write('\n')