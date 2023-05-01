# Market Analysis Tool for Solana
This system allows for the gathering and calculations regarding market data for NFT collections on Magic Eden.

## Folder Structure
./saves -> Folder where save data will be stored <br/>
./src/common -> Common files and functions <br/>
./src/files -> System to save and load files <br/>
./src/jobs -> System and MapReduce jobs <br/>
./src/market -> System to gather market data <br/>
./src/terminal -> System that allows for user interaction with the tool <br/>

## Set Up
### Requirements:
1. Python 3 installed on local machine
2. A venv (optional) to run the python script
### Set Up Steps:
1. (optional) set up venv
2. run the following bach commands
```shell
pip install -r requirements.txt
```

## Running the Tool
To run the tool use the following bash command:
```shell
python main.py
```

## Optional Arguments
When launching the tool from the shell, you may give the following arguments:
- "-e" (default) -> Show Log and Error loggers
- "-d" -> Shows Log and Debug loggers
- "-ed" -> Shows all three type of loggers
- "-n" -> No loggers are shown