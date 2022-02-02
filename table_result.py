from glob import glob
import os


RESULTS_FOLDER = [
    "baseline/report",
    "atis/report",
    "AskUbuntuCorpus/report",
    "ChatbotCorpus/report",
    "WebApplicationsCorpus/report"
]


for result_path in RESULTS_FOLDER:
    results = list(glob(os.path.join(result_path, "*_evaluation.txt")))
    print(result_path.split('/report/')[0])
    for res in results:
        ngram = res.split('_')[0].split('/report/')[1]
        smooth = res.split('_')[1]
        with open(res, 'r') as f:
            lines = f.readlines()
            line = lines[1]
            metrics = line.split(';')
            # accuracy = metrics[0].replace('accuracy:', '').strip()
            precision = metrics[1].replace('precision:', '').strip()
            recall = metrics[2].replace('recall:', '').strip()
            FB1 = metrics[3].replace('FB1:', '').strip()
            print(ngram, "\t & ", smooth, "\t & ", precision, "\t & ", recall, "\t & ", FB1, ' \\\\')