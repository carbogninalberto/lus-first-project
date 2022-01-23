import tasks
import utils.functions as fn
import sys
import os
import subprocess
from subprocess import DEVNULL

# constants

NGRAMS = [2, 3, 4, 5]

SMOOTH = [  "absolute", 
            "katz", 
            "kneser_ney", 
            "presmoothed", 
            "unsmoothed", 
            "witten_bell"]


# main
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('''
HELP:

    python main.py <task> <ngrams> <smooth> <only_evaluate: default false>
        ''')
        sys.exit()

    only_evaluate = True if len(sys.argv) > 4 else False

    if sys.argv[1] == "baseline":
        
        print("Running <baseline>\n")
        path = tasks.baseline()
        
        fn.extract_sentences_tags("{}/train.txt".format(path), "{}/tags.txt".format(path))
        print("-> Extracted sentences tags!")

        pairs = fn.extract_sentence_map("{}/train.txt".format(path));
        print("-> Extracted pairs!")
        # print(pairs[:5])

        # creating lexicon
        tasks.terminal("ngramsymbols < {0}/train.txt > {0}/lex.txt".format(path))
        print("-> Created lexicon!")

        fn.define_transducer(pairs, export=os.path.join(path, 'fst.txt'))
        print("-> Defined WFST!")

        tasks.terminal("fstcompile --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/fst.txt > {0}/wfst.fst".format(path))
        print("-> complied WFST!\n")

        print("Running <baseline> params\n")

        tasks.terminal("mkdir -p {}/report".format(path))
        tasks.terminal("mkdir -p {}/tmp/test".format(path))

        print("-> REPORT")
        print("--------------------------------------")
        for n in NGRAMS:
            for s in SMOOTH:
                print("   NGRAM = {} SMOOTH = {}".format(n, s))
                out_pred_path = os.path.join(path, 'report', '{1}_{0}_pred.txt'.format(s, n))
                if os.path.exists(out_pred_path) and not only_evaluate:
                    os.system("rm -rf {}".format(out_pred_path))

                if not only_evaluate:
                    # create language model
                    tasks.terminal("farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' {0}/tags.txt > {0}/tags.far".format(path))
                    tasks.terminal("ngramcount --order={1}  --require_symbols=false {0}/tags.far > {0}/tags.cnts".format(path, n))
                    tasks.terminal("ngrammake --method={1} {0}/tags.cnts > {0}/tmp/{2}_{1}.lm".format(path, s, n))

                    # compile fsm
                    subprocess.call("cat {0}/utterances.txt | farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' --generate_keys=4 | \
                        farextract --filename_prefix={0}/tmp/test/ --filename_suffix='.fst'".format(path), shell=True, stdin=DEVNULL)
                    
                    # test
                    with open(os.path.join(path, 'test.txt')) as f:
                        test = f.read().strip('\n').split('\n\n')

                    filenames = next(os.walk(os.path.join('baseline', 'tmp/test')), (None, None, []))[2]
                    with open(out_pred_path, 'a') as pred_out:
                        for idx, filename in enumerate(filenames):
                            # print(filename)
                            output = subprocess.check_output("fstcompose {0}/tmp/test/{1} {0}/wfst.fst > {0}/comp.fst".format(
                                path, filename), shell=True)
                            # print(output.decode('utf-8'))
                            output = subprocess.check_output("fstcompose {0}/comp.fst {0}/tmp/{2}_{1}.lm > {0}/comp_t.fst".format(
                                path, s, n), shell=True)
                            os.system("fstrmepsilon {0}/comp_t.fst {0}/comp_no_epsilon.fst".format(path))
                            os.system("fstshortestpath {0}/comp_no_epsilon.fst {0}/comp_stspath.fst".format(path))
                            os.system("fsttopsort {0}/comp_stspath.fst {0}/comp_stspath_sorted.fst".format(path))
                            res = subprocess.check_output("fstprint --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/comp_stspath_sorted.fst".format(path), shell=True)
                            # print(res.decode('utf-8'))
                            res = res.decode('utf-8')
                            predict = []
                            for r in res.split('\n'):
                                t = r.split('\t')
                                if len(t) > 3:
                                    predict.append((t[2], t[3]))

                            for t in zip(test[idx].split('\n'), predict):
                                pred_out.write("{} {}\n".format(t[0].replace('\t', ' '), t[1][1]))
                            pred_out.write('\n')

                # EVALUATE
                os.system("perl utils/conlleval.pl <{1}> {0}/report/{3}_{2}_evaluation.txt".format(path, out_pred_path, s, n))
                # break
            # break
        print("--------------------------------------")

    elif sys.argv[1] == "atis":
        
        print("Running <atis>\n")
        path = tasks.atis()
        
        fn.extract_sentences_tags("{}/train.txt".format(path), "{}/tags.txt".format(path))
        print("-> Extracted sentences tags!")

        pairs = fn.extract_sentence_map("{}/train.txt".format(path));
        print("-> Extracted pairs!")
        # print(pairs[:5])

        # creating lexicon
        tasks.terminal("ngramsymbols < {0}/train.txt > {0}/lex.txt".format(path))
        print("-> Created lexicon!")

        fn.define_transducer(pairs, export=os.path.join(path, 'fst.txt'))
        print("-> Defined WFST!")

        tasks.terminal("fstcompile --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/fst.txt > {0}/wfst.fst".format(path))
        print("-> complied WFST!\n")

        print("Running <atis> params\n")

        tasks.terminal("mkdir -p {}/report".format(path))
        tasks.terminal("mkdir -p {}/tmp/test".format(path))

        print("-> REPORT")
        print("--------------------------------------")
        for n in NGRAMS:
            for s in SMOOTH:
                print("   NGRAM = {} SMOOTH = {}".format(n, s))
                out_pred_path = os.path.join(path, 'report', '{1}_{0}_pred.txt'.format(s, n))
                if os.path.exists(out_pred_path) and not only_evaluate:
                    os.system("rm -rf {}".format(out_pred_path))

                if not only_evaluate:
                    # create language model
                    tasks.terminal("farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' {0}/tags.txt > {0}/tags.far".format(path))
                    tasks.terminal("ngramcount --order={1}  --require_symbols=false {0}/tags.far > {0}/tags.cnts".format(path, n))
                    tasks.terminal("ngrammake --method={1} {0}/tags.cnts > {0}/tmp/{2}_{1}.lm".format(path, s, n))

                    # compile fsm
                    subprocess.call("cat {0}/utterances.txt | farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' --generate_keys=4 | \
                        farextract --filename_prefix={0}/tmp/test/ --filename_suffix='.fst'".format(path), shell=True, stdin=DEVNULL)
                    
                    # test
                    with open(os.path.join(path, 'test.txt')) as f:
                        test = f.read().strip('\n').split('\n\n')

                    filenames = next(os.walk(os.path.join('atis', 'tmp/test')), (None, None, []))[2]
                    with open(out_pred_path, 'a') as pred_out:
                        for idx, filename in enumerate(filenames):
                            # print(filename)
                            output = subprocess.check_output("fstcompose {0}/tmp/test/{1} {0}/wfst.fst > {0}/comp.fst".format(
                                path, filename), shell=True)
                            # print(output.decode('utf-8'))
                            output = subprocess.check_output("fstcompose {0}/comp.fst {0}/tmp/{2}_{1}.lm > {0}/comp_t.fst".format(
                                path, s, n), shell=True)
                            os.system("fstrmepsilon {0}/comp_t.fst {0}/comp_no_epsilon.fst".format(path))
                            os.system("fstshortestpath {0}/comp_no_epsilon.fst {0}/comp_stspath.fst".format(path))
                            os.system("fsttopsort {0}/comp_stspath.fst {0}/comp_stspath_sorted.fst".format(path))
                            res = subprocess.check_output("fstprint --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/comp_stspath_sorted.fst".format(path), shell=True)
                            # print(res.decode('utf-8'))
                            res = res.decode('utf-8')
                            predict = []
                            for r in res.split('\n'):
                                t = r.split('\t')
                                if len(t) > 3:
                                    predict.append((t[2], t[3]))

                            for t in zip(test[idx].split('\n'), predict):
                                pred_out.write("{} {}\n".format(t[0].replace('\t', ' '), t[1][1]))
                            pred_out.write('\n')

                # EVALUATE
                os.system("perl utils/conlleval.pl <{1}> {0}/report/{3}_{2}_evaluation.txt".format(path, out_pred_path, s, n))
                # break
            # break
        print("--------------------------------------")

    elif sys.argv[1] == "AskUbuntuCorpus":
        
        print("Running <AskUbuntuCorpus>\n")
        path = tasks.AskUbuntuCorpus()
        
        fn.extract_sentences_tags("{}/train.txt".format(path), "{}/tags.txt".format(path))
        print("-> Extracted sentences tags!")

        pairs = fn.extract_sentence_map("{}/train.txt".format(path));
        print("-> Extracted pairs!")
        # print(pairs[:5])

        # creating lexicon
        tasks.terminal("ngramsymbols < {0}/train.txt > {0}/lex.txt".format(path))
        print("-> Created lexicon!")

        fn.define_transducer(pairs, export=os.path.join(path, 'fst.txt'))
        print("-> Defined WFST!")

        tasks.terminal("fstcompile --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/fst.txt > {0}/wfst.fst".format(path))
        print("-> complied WFST!\n")

        print("Running <AskUbuntuCorpus> params\n")

        tasks.terminal("mkdir -p {}/report".format(path))
        tasks.terminal("mkdir -p {}/tmp/test".format(path))

        print("-> REPORT")
        print("--------------------------------------")
        for n in NGRAMS:
            for s in SMOOTH:
                print("   NGRAM = {} SMOOTH = {}".format(n, s))
                out_pred_path = os.path.join(path, 'report', '{1}_{0}_pred.txt'.format(s, n))
                if os.path.exists(out_pred_path) and not only_evaluate:
                    os.system("rm -rf {}".format(out_pred_path))

                if not only_evaluate:
                    # create language model
                    tasks.terminal("farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' {0}/tags.txt > {0}/tags.far".format(path))
                    tasks.terminal("ngramcount --order={1}  --require_symbols=false {0}/tags.far > {0}/tags.cnts".format(path, n))
                    tasks.terminal("ngrammake --method={1} {0}/tags.cnts > {0}/tmp/{2}_{1}.lm".format(path, s, n))

                    # compile fsm
                    subprocess.call("cat {0}/utterances.txt | farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' --generate_keys=4 | \
                        farextract --filename_prefix={0}/tmp/test/ --filename_suffix='.fst'".format(path), shell=True, stdin=DEVNULL)
                    
                    # test
                    with open(os.path.join(path, 'test.txt')) as f:
                        test = f.read().strip('\n').split('\n\n')

                    filenames = next(os.walk(os.path.join('AskUbuntuCorpus', 'tmp/test')), (None, None, []))[2]
                    with open(out_pred_path, 'a') as pred_out:
                        for idx, filename in enumerate(filenames):
                            # print(filename)
                            output = subprocess.check_output("fstcompose {0}/tmp/test/{1} {0}/wfst.fst > {0}/comp.fst".format(
                                path, filename), shell=True)
                            # print(output.decode('utf-8'))
                            output = subprocess.check_output("fstcompose {0}/comp.fst {0}/tmp/{2}_{1}.lm > {0}/comp_t.fst".format(
                                path, s, n), shell=True)
                            os.system("fstrmepsilon {0}/comp_t.fst {0}/comp_no_epsilon.fst".format(path))
                            os.system("fstshortestpath {0}/comp_no_epsilon.fst {0}/comp_stspath.fst".format(path))
                            os.system("fsttopsort {0}/comp_stspath.fst {0}/comp_stspath_sorted.fst".format(path))
                            res = subprocess.check_output("fstprint --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/comp_stspath_sorted.fst".format(path), shell=True)
                            # print(res.decode('utf-8'))
                            res = res.decode('utf-8')
                            predict = []
                            for r in res.split('\n'):
                                t = r.split('\t')
                                if len(t) > 3:
                                    predict.append((t[2], t[3]))

                            for t in zip(test[idx].split('\n'), predict):
                                pred_out.write("{} {}\n".format(t[0].replace('\t', ' '), t[1][1]))
                            pred_out.write('\n')

                # EVALUATE
                os.system("perl utils/conlleval.pl <{1}> {0}/report/{3}_{2}_evaluation.txt".format(path, out_pred_path, s, n))
                # break
            # break
        print("--------------------------------------")

    elif sys.argv[1] == "ChatbotCorpus":
        
        print("Running <ChatbotCorpus>\n")
        path = tasks.ChatbotCorpus()
        
        fn.extract_sentences_tags("{}/train.txt".format(path), "{}/tags.txt".format(path))
        print("-> Extracted sentences tags!")

        pairs = fn.extract_sentence_map("{}/train.txt".format(path));
        print("-> Extracted pairs!")
        # print(pairs[:5])

        # creating lexicon
        tasks.terminal("ngramsymbols < {0}/train.txt > {0}/lex.txt".format(path))
        print("-> Created lexicon!")

        fn.define_transducer(pairs, export=os.path.join(path, 'fst.txt'))
        print("-> Defined WFST!")

        tasks.terminal("fstcompile --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/fst.txt > {0}/wfst.fst".format(path))
        print("-> complied WFST!\n")

        print("Running <ChatbotCorpus> params\n")

        tasks.terminal("mkdir -p {}/report".format(path))
        tasks.terminal("mkdir -p {}/tmp/test".format(path))

        print("-> REPORT")
        print("--------------------------------------")
        for n in NGRAMS:
            for s in SMOOTH:
                print("   NGRAM = {} SMOOTH = {}".format(n, s))
                out_pred_path = os.path.join(path, 'report', '{1}_{0}_pred.txt'.format(s, n))
                if os.path.exists(out_pred_path) and not only_evaluate:
                    os.system("rm -rf {}".format(out_pred_path))

                if not only_evaluate:
                    # create language model
                    tasks.terminal("farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' {0}/tags.txt > {0}/tags.far".format(path))
                    tasks.terminal("ngramcount --order={1}  --require_symbols=false {0}/tags.far > {0}/tags.cnts".format(path, n))
                    tasks.terminal("ngrammake --method={1} {0}/tags.cnts > {0}/tmp/{2}_{1}.lm".format(path, s, n))

                    # compile fsm
                    subprocess.call("cat {0}/utterances.txt | farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' --generate_keys=4 | \
                        farextract --filename_prefix={0}/tmp/test/ --filename_suffix='.fst'".format(path), shell=True, stdin=DEVNULL)
                    
                    # test
                    with open(os.path.join(path, 'test.txt')) as f:
                        test = f.read().strip('\n').split('\n\n')

                    filenames = next(os.walk(os.path.join('ChatbotCorpus', 'tmp/test')), (None, None, []))[2]
                    with open(out_pred_path, 'a') as pred_out:
                        for idx, filename in enumerate(filenames):
                            # print(filename)
                            output = subprocess.check_output("fstcompose {0}/tmp/test/{1} {0}/wfst.fst > {0}/comp.fst".format(
                                path, filename), shell=True)
                            # print(output.decode('utf-8'))
                            output = subprocess.check_output("fstcompose {0}/comp.fst {0}/tmp/{2}_{1}.lm > {0}/comp_t.fst".format(
                                path, s, n), shell=True)
                            os.system("fstrmepsilon {0}/comp_t.fst {0}/comp_no_epsilon.fst".format(path))
                            os.system("fstshortestpath {0}/comp_no_epsilon.fst {0}/comp_stspath.fst".format(path))
                            os.system("fsttopsort {0}/comp_stspath.fst {0}/comp_stspath_sorted.fst".format(path))
                            res = subprocess.check_output("fstprint --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/comp_stspath_sorted.fst".format(path), shell=True)
                            # print(res.decode('utf-8'))
                            res = res.decode('utf-8')
                            predict = []
                            for r in res.split('\n'):
                                t = r.split('\t')
                                if len(t) > 3:
                                    predict.append((t[2], t[3]))

                            for t in zip(test[idx].split('\n'), predict):
                                pred_out.write("{} {}\n".format(t[0].replace('\t', ' '), t[1][1]))
                            pred_out.write('\n')

                # EVALUATE
                os.system("perl utils/conlleval.pl <{1}> {0}/report/{3}_{2}_evaluation.txt".format(path, out_pred_path, s, n))
                # break
            # break
        print("--------------------------------------")

    elif sys.argv[1] == "WebApplicationsCorpus":
        
        print("Running <WebApplicationsCorpus>\n")
        path = tasks.WebApplicationsCorpus()
        
        fn.extract_sentences_tags("{}/train.txt".format(path), "{}/tags.txt".format(path))
        print("-> Extracted sentences tags!")

        pairs = fn.extract_sentence_map("{}/train.txt".format(path));
        print("-> Extracted pairs!")
        # print(pairs[:5])

        # creating lexicon
        tasks.terminal("ngramsymbols < {0}/train.txt > {0}/lex.txt".format(path))
        print("-> Created lexicon!")

        fn.define_transducer(pairs, export=os.path.join(path, 'fst.txt'))
        print("-> Defined WFST!")

        tasks.terminal("fstcompile --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/fst.txt > {0}/wfst.fst".format(path))
        print("-> complied WFST!\n")

        print("Running <WebApplicationsCorpus> params\n")

        tasks.terminal("mkdir -p {}/report".format(path))
        tasks.terminal("mkdir -p {}/tmp/test".format(path))

        print("-> REPORT")
        print("--------------------------------------")
        for n in NGRAMS:
            for s in SMOOTH:
                print("   NGRAM = {} SMOOTH = {}".format(n, s))
                out_pred_path = os.path.join(path, 'report', '{1}_{0}_pred.txt'.format(s, n))
                if os.path.exists(out_pred_path) and not only_evaluate:
                    os.system("rm -rf {}".format(out_pred_path))

                if not only_evaluate:
                    # create language model
                    tasks.terminal("farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' {0}/tags.txt > {0}/tags.far".format(path))
                    tasks.terminal("ngramcount --order={1}  --require_symbols=false {0}/tags.far > {0}/tags.cnts".format(path, n))
                    tasks.terminal("ngrammake --method={1} {0}/tags.cnts > {0}/tmp/{2}_{1}.lm".format(path, s, n))

                    # compile fsm
                    subprocess.call("cat {0}/utterances.txt | farcompilestrings --symbols={0}/lex.txt --unknown_symbol='<UNK>' --generate_keys=4 | \
                        farextract --filename_prefix={0}/tmp/test/ --filename_suffix='.fst'".format(path), shell=True, stdin=DEVNULL)
                    
                    # test
                    with open(os.path.join(path, 'test.txt')) as f:
                        test = f.read().strip('\n').split('\n\n')

                    filenames = next(os.walk(os.path.join('WebApplicationsCorpus', 'tmp/test')), (None, None, []))[2]
                    with open(out_pred_path, 'a') as pred_out:
                        for idx, filename in enumerate(filenames):
                            # print(filename)
                            output = subprocess.check_output("fstcompose {0}/tmp/test/{1} {0}/wfst.fst > {0}/comp.fst".format(
                                path, filename), shell=True)
                            # print(output.decode('utf-8'))
                            output = subprocess.check_output("fstcompose {0}/comp.fst {0}/tmp/{2}_{1}.lm > {0}/comp_t.fst".format(
                                path, s, n), shell=True)
                            os.system("fstrmepsilon {0}/comp_t.fst {0}/comp_no_epsilon.fst".format(path))
                            os.system("fstshortestpath {0}/comp_no_epsilon.fst {0}/comp_stspath.fst".format(path))
                            os.system("fsttopsort {0}/comp_stspath.fst {0}/comp_stspath_sorted.fst".format(path))
                            res = subprocess.check_output("fstprint --isymbols={0}/lex.txt --osymbols={0}/lex.txt {0}/comp_stspath_sorted.fst".format(path), shell=True)
                            # print(res.decode('utf-8'))
                            res = res.decode('utf-8')
                            predict = []
                            for r in res.split('\n'):
                                t = r.split('\t')
                                if len(t) > 3:
                                    predict.append((t[2], t[3]))

                            for t in zip(test[idx].split('\n'), predict):
                                pred_out.write("{} {}\n".format(t[0].replace('\t', ' '), t[1][1]))
                            pred_out.write('\n')

                # EVALUATE
                os.system("perl utils/conlleval.pl <{1}> {0}/report/{3}_{2}_evaluation.txt".format(path, out_pred_path, s, n))
                # break
            # break
        print("--------------------------------------")