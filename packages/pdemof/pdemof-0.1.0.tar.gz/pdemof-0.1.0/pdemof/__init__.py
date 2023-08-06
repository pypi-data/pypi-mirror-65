import requests


class Pdemof:
    def __init__(self):
        print('initialized')
    def req(self):
        url='https://google.com/humans.txt'
        r=requests.get(url)
        print(r.text) 

    def cout(self):
        print('made by MUHAMMAD FAHIM')
