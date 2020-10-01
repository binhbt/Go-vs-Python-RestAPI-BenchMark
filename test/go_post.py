import uuid
from datetime import datetime
from locust import HttpLocust, TaskSet, task, between
from locust import ResponseError
# from locust.contrib.fasthttp import FastHttpLocust

from random import randint
import random


class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4())

    @task(1)
    def testpost(self):

        words = [["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "ThirdTeen", "FourTeen", "FiveTeen", "SixTeen", "SevenTeen", "EightTeen", "NineTeen", "TwenTy", "TwentyOne", "TwenTySecond", "TwentyThree", "TwentyFour", "TwentyFive", "TwentySix", "TwentySeven", "TwentyEight", "TwentyNine", "Thirdty"],
                 ["red", "yellow", "green", "AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue", "BlueViolet", "Brown", "BurlyWood",
                  "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue", "Cornsilk", "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkViolet", "DimGray", "Gainsboro"],
                 ["cats", "dogs", "zebras", "lion", "tiger", "elephant", "Aves", "Bovinae", "Canidae", "Equidae", "Felidae", "Suidae", "Procyonidae", "Viverridae", "Mustelidae",
                  "Leporidae", "Osteichthyes", "Aardvark", "Albatross", "Alligator", "Alpaca", "Bee", "Camel", "Deer", "Emu", "Fly", "Giraffe", "Hare", "Jellyfish", "Kangaroo"],
                 ["jumped.", "danced.", "wrote poetry.", "assessed", "evaluated", "transmitted", "commissioned", "researched", "guaranteed", "sanctioned", "assigned", "administered", "budgeted", "ameliorated", "processed", "approximated", "brainstormed", "rejuvenated", "transformed", "deciphered", "enlarged", "arbitrated", "collaborated", "drafted", "envisioned", "balanced", "mobilized", "instructed", "orchestrated", "streamlined"]]

        random_json = {}
        random_json['Title'] =  'Python and MongoDB'
        random_json['Body'] = 'PyMongo is fun, you guys'

        self.client.post('/tasks/', json=random_json)


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
    wait_time = between(0.1, 0.1)
