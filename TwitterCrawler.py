import twint
# from textblob import TextBlob
# from textblob_de import TextBlobDE
from afinn import Afinn
from datetime import date, timedelta
import threading
import asyncio
from flask import Flask




class Team(threading.Thread):

    def __init__(self, handle, sinceDate, lang):
        threading.Thread.__init__(self)

        self.handle = handle
        self.sinceDate = date.today() - timedelta(sinceDate)
        self.lang = lang
        self.totalTweets = None
        self.sentimentScore = None


    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.afinn = Afinn(emoticons=True)

        self.twintConfig = twint.Config()
        self.configTwint()
        self.createLog()

        self.totalTweets = self.calculateTotalTweets()
        self.sentimentScore = self.calculateSentimentScore()

    def configTwint(self):
        self.twintConfig.To = self.handle
        self.twintConfig.Since = str(self.sinceDate)
        self.twintConfig.Format = "{date} - {tweet}"
        self.twintConfig.Store_csv = True
        self.twintConfig.Custom = ["tweet"]
        self.twintConfig.Output = "teams/" + self.handle + ".csv"

    def createLog(self):
        open("teams/" + self.handle + ".csv", 'w+').close() #leert den csv log des Teams
        twint.run.Search(self.twintConfig)

    def calculateTotalTweets(self):
        totalTweets = 0
        try:
            totalTweets = len( open("teams/" + self.handle + ".csv", "r", encoding='utf8').readlines() )
            open("teams/" + self.handle + ".csv", 'r').close() #schließt das File wieder
        except:
            print("Fehler in calculateTotalTweets")

        return totalTweets

    def calculateSentimentScore(self):
        score = 0
        file = open("teams/" + self.handle + ".csv", "r", encoding='utf8')
        tweet = file.readline()
        notNeutrals = 0.0001

        while tweet:
            tweetScore = self.afinn.score(tweet)

            if tweetScore != 0:
                notNeutrals+=1

            score += tweetScore
            tweet = file.readline()


        score = score/notNeutrals
        return score



t1 = Team("@Rangers", 1, 'en')
t1.start()

t2 = Team("@astros", 1, 'en')
t2.start()

while True:
    if not t1.isAlive() and not t2.isAlive():
        print("--------------------------TEAM 1-------------------------------")
        print("Analysiertes Team: " + str(t1.handle))
        print("Anzahl der analysierten Tweets: " + str(t1.totalTweets))
        print("Durchschnittlicher Sentiment Score: " + str(t1.sentimentScore))
        print("--------------------------------------------------------------")
        print("--------------------------TEAM 2-------------------------------")
        print("Analysiertes Team: " + str(t2.handle))
        print("Anzahl der analysierten Tweets: " + str(t2.totalTweets))
        print("Durchschnittlicher Sentiment Score: " + str(t2.sentimentScore))
        print("--------------------------------------------------------------")
        break

# app = Flask(__name__)
#
# @app.route("/")
# def index():
#     return "DAS IST EIN TEST"
#
# app.run(debug=True, host='127.0.0.1', port = '120')