from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'Zy13yR9hote9LqOb5od9xIscN'
consumer_secret = 'KpMArEaupk5YcMv51Ss8KUqKyRrqRpNz6YDPjStDm2cnsIUUUU'
access_token = '119684738-Y46Fy7IRkUCxHiEXuiLjAl2SqQA5Jq3Oeo3fJroa'
access_token_secret = 'LYd9TF3WjwX7NzBDEL5Zmu3fpvgGhjSTH2phvT3gigiQH'


fout = open('mivkkr.txt','a')
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        x = json.loads(data)
        tweet = x["text"]
        try:
            fout.write(tweet)
            fout.write("\n**END**\n")
        except:
            pass
        
    def on_error(self, status):
        print status
        if status==420:
            return False


def generate():
    teams = ['KKR','DD','MI','RPS','GL','RCB','KXIP','SRH']
    matches = list()
    for x in teams:
        for y in teams:
            if x!= y:
                match = x+'v'+y
                matches.append(match)

    return matches

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    x = generate()
    x.append('IPL')
    x.append('IPL2016')
    x.append('IPL9')    

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=x)
