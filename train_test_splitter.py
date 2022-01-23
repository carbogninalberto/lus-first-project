'''
Splitting dataset in 70/30 train/test
-----------------------------------------
file             sentences  train   test
-----------------------------------------
AskUbuntuCorpus        162    113     49
ChatbotCorpus          206    144     62
WebApplicationsCorpus   89     62     27
-----------------------------------------
'''
import os
import json


files = ['AskUbuntuCorpus', 'ChatbotCorpus', 'WebApplicationsCorpus']

for file in files:
    os.system('mkdir -p dataset/NLU_Evaluation_Corpora/{}'.format(file))
    with open('dataset/NLU_Evaluation_Corpora/{}.json'.format(file), 'r') as original_file, \
            open('dataset/NLU_Evaluation_Corpora/{}/train.json'.format(file), 'w') as train_file, \
            open('dataset/NLU_Evaluation_Corpora/{}/test.json'.format(file), 'w') as test_file:
        
        data = json.load(original_file)['sentences']
        for sentence in data:
            txt = sentence['text']
            for entity in sentence['entities']:
                index = txt.find(entity['text'])
                entity['start'] = index
                entity['stop'] = index+len(entity['text'])
        train_n = int(len(data) * 0.7)
        test_n = len(data)-train_n
        print(file, len(data), len(data[:train_n]), len(data[train_n:]))

        json.dump({"sentences": data[:train_n]}, train_file, indent=2)
        json.dump({"sentences": data[train_n:]}, test_file, indent=2)

        