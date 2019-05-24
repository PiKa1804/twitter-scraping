import tweepy
import pandas as pd
from datetime import datetime, timedelta
import time
start = time.time()

#change consumer_key, consumer_secret, access_token, access_token_secret

twitter = {"Link": [], "Name": [], "Text": [], "Date": [], "Hashtags":[]} 

words=[]
with open('words.txt') as f_in:
    words = list(line for line in (l.strip() for l in f_in) if line)
    
for i in range(0,len(words)):
    words[i]=words[i].split(":")[0]

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

print('Searching')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

time_last=(datetime.today()+timedelta(days=1)).date()
time_first=(datetime.today()-timedelta(days=2)).date()

alphabet=[]
char=['!','"','#','~','}','|','{','`','^',']','\'','[','@','?','>','=','<',';',':','/',',','+','*',')','(','\'','&','%','$']

for i in range(0, len(char)):
    alphabet.append(char[i])     

def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [idx for idx,item in enumerate(seq) if item in seen or seen_add(item)]

Date=[]
Name=[]
link=[]
Text=[]
hashtagi=[]

sum=0
letter=0


for i in range(0, len(words)):
    print(words[i])
    for tweet in tweepy.Cursor(api.search,q=words[i]+' -filter:retweets -filter',since=time_first,until=time_last, tweet_mode='extended', lang='pl', result_type='recent').items():

        if tweet.entities['urls']:
            for url in tweet.entities['urls']:
                if tweet.user.url != None:
                    for j in range(0,len(alphabet)):
                        if alphabet[j] in tweet.user.name:
                            letter=letter+1
                    
                    if letter==0:
                       print(tweet.user.name)
                       if tweet.entities['hashtags']:
                           hashtag=''
                           for url2 in tweet.entities['hashtags']:
                               hashtag=hashtag+(url2['text'])+','

                           Name.append(tweet.user.name)
                           Date.append(tweet.created_at.date())
                           link.append(str(url['expanded_url']))
                           Text.append(tweet.full_text)
                           hashtagi.append(hashtag)
                    letter=0
               
                break
        duplikat=list_duplicates(link)

        for i in range(0,len(duplikat)-1):
            del link[duplikat[i]]
            del Name[duplikat[i]]
            del Date[duplikat[i]]
            del Text[duplikat[i]]
            del hashtagi[duplikat[i]]
        sum=sum+1
                
    print(sum)


twitter['Link']=(link)
twitter['Text']=(Text)
twitter['Name']=(Name)
twitter['Date']=(Date)
twitter['Hashtags']=(hashtagi)


df = pd.DateFrame.from_dict(twitter,  orient='columns')

df = df[['Link','Text','Name','Date','Hashtags']]
writer = pd.ExcelWriter('Twitter.xlsx')
df.to_excel(writer, sheet_name='Sites',index=False)

workbook  = writer.book
worksheet = writer.sheets['Sites']
format2 = workbook.add_format({'text_wrap': True})

worksheet.set_column('A:A', 127, format2)
worksheet.set_column('B:B', 28, format2)
worksheet.set_column('C:C', 41, format2)

writer.save()

