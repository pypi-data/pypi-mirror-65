from typing import List
import requests

def get_words()->List[str]:
    dta = requests.get("https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt")
    return str(dta.content).split('\\n')


