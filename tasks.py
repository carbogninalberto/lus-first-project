import os

def terminal(command):
    os.system(command)

def baseline():
    # create baseline folder
    terminal("rm -r baseline")
    terminal("mkdir baseline")
    # copy dataset to folder
    terminal("cp ./dataset/NL2SparQL4NLU.train.conll.txt ./baseline/train.txt")
    terminal("cp ./dataset/NL2SparQL4NLU.test.conll.txt ./baseline/test.txt")
    terminal("cp ./dataset/NL2SparQL4NLU.test.utterances.txt ./baseline/utterances.txt")
    
    return 'baseline'

def atis():
    # create atis folder
    terminal("rm -r atis")
    terminal("mkdir atis")
    # copy dataset to folder
    terminal("cp ./dataset/ATIS/train.txt ./atis/train.txt")
    terminal("cp ./dataset/ATIS/test.txt ./atis/test.txt")
    terminal("cp ./dataset/ATIS/utterances.txt ./atis/utterances.txt")
    
    return 'atis'

def AskUbuntuCorpus():
    # create AskUbuntuCorpus folder
    terminal("rm -r AskUbuntuCorpus")
    terminal("mkdir AskUbuntuCorpus")
    # copy dataset to folder
    terminal("cp ./dataset/NLU_Evaluation_Corpora/AskUbuntuCorpus/train.txt ./AskUbuntuCorpus/train.txt")
    terminal("cp ./dataset/NLU_Evaluation_Corpora/AskUbuntuCorpus/test.txt ./AskUbuntuCorpus/test.txt")
    terminal("cp ./dataset/NLU_Evaluation_Corpora/AskUbuntuCorpus/utterances.txt ./AskUbuntuCorpus/utterances.txt")
    
    return 'AskUbuntuCorpus'

def ChatbotCorpus():
    # create ChatbotCorpus folder
    terminal("rm -r ChatbotCorpus")
    terminal("mkdir ChatbotCorpus")
    # copy dataset to folder
    terminal("cp ./dataset/NLU_Evaluation_Corpora/ChatbotCorpus/train.txt ./ChatbotCorpus/train.txt")
    terminal("cp ./dataset/NLU_Evaluation_Corpora/ChatbotCorpus/test.txt ./ChatbotCorpus/test.txt")
    terminal("cp ./dataset/NLU_Evaluation_Corpora/ChatbotCorpus/utterances.txt ./ChatbotCorpus/utterances.txt")
    
    return 'ChatbotCorpus'

def WebApplicationsCorpus():
    # create WebApplicationsCorpus folder
    terminal("rm -r WebApplicationsCorpus")
    terminal("mkdir WebApplicationsCorpus")
    # copy dataset to folder
    terminal("cp ./dataset/NLU_Evaluation_Corpora/WebApplicationsCorpus/train.txt ./WebApplicationsCorpus/train.txt")
    terminal("cp ./dataset/NLU_Evaluation_Corpora/WebApplicationsCorpus/test.txt ./WebApplicationsCorpus/test.txt")
    terminal("cp ./dataset/NLU_Evaluation_Corpora/WebApplicationsCorpus/utterances.txt ./WebApplicationsCorpus/utterances.txt")
    
    return 'WebApplicationsCorpus'