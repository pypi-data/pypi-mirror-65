import requests

class YTchannel:
    def __init__(self,channel_id,api_key):
        self.cha_id = channel_id
        self.api = api_key
        self.URL ='https://www.googleapis.com/youtube/v3/channels?part=brandingSettings,statistics,snippet&id='+self.cha_id+'&key='+self.api
        self.name = ''
        self.icon = ''
        self.subs = ''
        self.country = None
        self.subhidden = False
        self.videos = ''
        self.des = ''
        self.channelArt = ''
        self.response = ''
        self.result = False
        

    def start(self):
        self.response = requests.get(self.URL)
        self.json = self.response.json()
        if int(self.json['pageInfo']['totalResults']) == 1:
            self.result = True
            self.name = self.json['items'][0]['snippet']['title']
            self.des = self.json['items'][0]['snippet']['description']
            self.icon = self.json['items'][0]['snippet']['thumbnails']['high']['url']
            self.channelArt = self.json['items'][0]['brandingSettings']['image']['bannerImageUrl']
            if self.json['items'][0]['statistics']['hiddenSubscriberCount'] == 'true':
                self.subhidden = True
            self.subs = self.json['items'][0]['statistics']['subscriberCount']
            self.videos = self.json['items'][0]['statistics']['videoCount']
            if 'country' in self.json['items'][0]['snippet']:
                self.country = self.json['items'][0]['snippet']['country']
        
