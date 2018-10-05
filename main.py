import re,os,json
from requests_html import HTMLSession, HTML
from datetime import datetime
import time
import urllib

def save_json(idd, title, time,duration,link):
    obj = {'data': []}
    obj['data'].append({'id': idd})
    obj['data'].append({'title': title})
    obj['data'].append({'time': time.strftime("%Y-%m-%d %H:%M:%S")})
    obj['data'].append({'duration': duration})
    obj['data'].append({'url':link })
    #print(obj)
    with open(str(idd) + '.json', 'w') as outfile:
      json.dump(obj, outfile)
    os.rename(str(idd) + '.json', paths+"/"+ str(idd) + '.json')
    print("{} Saved".format(idd))

def save_thumbnail(idd,screenshot):
  if not os.path.exists(paths+"/"+str(idd) + '.jpg'):
    urllib.request.urlretrieve(screenshot, str(idd) + ".jpg")
    os.rename(str(idd) + ".jpg", paths +"/"+str(idd)+".jpg")




def get_duration(id):
    url1 = "https://api.twitter.com/1.1/videos/tweet/config/{}.json".format(id)
    try:
        r1 = session.get(url1, headers=header1)
        html1 = r1.json()
        #print(html1)
        if 'errors' in html1:
            print("Change Token")
            return None,''
        else:
            try:
                duration = html1['track']['durationMs'] / 1000
            except:
                duration = ""
            try:
                poster=html1['posterImage']
            except:
                poster=""
            return duration,poster

    except Exception as e:
        return False,''


session = HTMLSession()
f=open('tok.txt','r')
token=f.read()
print(token)
channel='TwitterTV'
#token="1048158871490052097"
paths="Twitter"

if not os.path.exists(paths):
  os.makedirs(paths)

url = 'https://twitter.com/i/profiles/show/{}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'.format(
    channel)

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Referer': 'https://twitter.com/twittervideo',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
           'X-Twitter-Active-User': 'yes',
           'X-Requested-With': 'XMLHttpRequest'}

header1 = {
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw',
    'Accept': '*/*; q=0.01', 'Referer': 'https://twitter.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'X-Twitter-Active-User': 'yes', 'x-guest-token': token
    }

r = session.get(url, headers=headers)
html = HTML(html=r.json()['items_html'], url='bunk', default_encoding='utf-8')

# print(dir(session))
# print(session.cookies)

for tweet in html.find('.stream-item'):
    try:
        name = tweet.find('.FullNameGroup')[0].full_text
        if 'Verified' in name:
            name = name[:-17]
    except:
        name = ""
    try:
        text = tweet.find('.tweet-text')[0].full_text
        loc1 = text.find('pic.')
        text = text[:loc1]
    except:
        text = ""
    title = name + ' - ' + text
    try:
        tweetId = tweet.find('.js-permalink')[0].attrs['data-conversation-id']
    except:
        tweetId = ""
    #print(tweetId)
    try:
        time = datetime.fromtimestamp(int(tweet.find('._timestamp')[0].attrs['data-time-ms']) / 1000.0)
    except:
        time = ""
    try:
        link = "https://twitter.com" + tweet.find('.tweet-timestamp')[0].attrs['href']
    except:
        link = ""
    '''
    try:
        thumb = tweet.find('.PlayableMedia-player')[0].attrs['style']
        t1 = thumb.find("('")
        t2 = thumb.find("')")
        thumb = thumb[t1 + 2:t2]
    except:
        thumb =""
    '''
    '''Check if video id already exists'''
    if os.path.exists( paths + "/" + str(tweetId) + ".no"):
        print("Skipping (novideo) -> " + tweetId)
    else:
        if os.path.exists( paths + "/" + str(tweetId) + ".json"):
            print("Skipping (already there) -> " + tweetId)
        else:
            duration,thumb = get_duration(tweetId)
            if duration == False:
                print("Not A Video (skipping)")
                '''Creating Temp File So Ignore This Next Time'''
                fh = open(str(tweetId) + ".no", "w")
                fh.close()
                os.rename(str(tweetId) + ".no", paths + "/" + str(tweetId) + ".no")
            else:
                save_json(tweetId, title, time,duration,link)
                if '' != thumb:
                    save_thumbnail(tweetId, thumb)
                else:
                    print("No Image:"+title)