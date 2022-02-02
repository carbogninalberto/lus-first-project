# lus-first-project

This repo contains the code for the first mid-term project of the course 2021 Language Understanding System.

### **Student:** Alberto Carbognin
### **Mat:** 211420

## configure
You may want to setup a virtual environment or use conda.
For instance we can run:

```
python3 -m venv venv
```
then we activate the virtual environment with

```
source venv/bin/activate
```

This step is not required because the scripts are only using the core python3 libraries.

We then need to install by compiling from source the following libraries:
- openfst
- opengrm

More information can be found [here](https://www.openfst.org/).

You also need to have perl installed, because I used the original script to perform the evaluation.

## Running

To run the script on the already parsed dataset you can launch the following terminal (assuming that you already source the virtual enviroment, if you are using it):

```bash
python main.py <task> <ngrams> <smooth> <only_evaluate: default false>
```

Specify the parameter `task` with the name of the dataset you want to perform the run. It could be a value of:
- baseline
- atis
- AskUbuntuCorpus
- ChatbotCorpus
- WebApplicationsCorpus

Other parameters can be specify to perform a specify evaluation with a certain configuration.