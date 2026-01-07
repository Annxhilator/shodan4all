import argparse
def args():
    parser = argparse.ArgumentParser(description="A simple script using argparse to greet a user.")
    parser.add_argument("-s","--search" ,required=True ,type=str, help="The main search query.")
    parser.add_argument("-nd","--no-default" ,action="store_true", help="Dont use default search parameters, only additional.")
    parser.add_argument("-c","--cookies", required=True,type=str, help="Cookies to use to connect to shodan.")
    parser.add_argument("-no","--no-output", required=False, action="store_true", help="Dont allow creation of output file.")
    parser.add_argument("-ah","--allow_honeypot", required=False, action="store_true", help="Allow honeypots to be saved.")
    parser.add_argument("-ap","--aditional-parameters", required=False, type=str, help="Additional parameters for searching.")
    parser.add_argument("-sl","--sleep", required=False, type=int, default=5, help="Time between shodan requests. Used mainly to avoid 403/429.")
    parser.add_argument("-ss","--silent", required=False, action="store_true", help="Dont print output.")
    parser.add_argument("-dc","--dont-chain",required=False,action="store_true",help="Dont chain search parameters.")
    args = parser.parse_args()
    return args
args = args()


