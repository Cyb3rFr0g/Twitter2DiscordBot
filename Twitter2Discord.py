##################################################
# Imports
import os
import asyncio
from dotenv import load_dotenv
##################################################
# Discord imports
#_________________________________________________
import discord
##################################################
# Twitter imports
#_________________________________________________
import tweepy

class Discord_Bot:
    def __init__(self):
        load_dotenv(verbose=True)
        #Twitter settings
        self.TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
        self.TWITTER_API_KEY_SECRET = os.environ['TWITTER_API_KEY_SECRET']
        self.TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
        self.TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
        self.TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        self.TWITTER_USERNAME = os.environ['TWITTER_USERNAME']
        self.LAST_SEEN_FILE = os.environ['LAST_SEEN_FILE']

        #Discord settings
        self.DISCORD_CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
        self.DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
        self.client = discord.Client()

        try:
            self.twitter_auth()
            self.client.loop.create_task(self.start_monitor())
            print("[+] Starting bot")
            self.client.run(self.DISCORD_TOKEN)
        except SystemExit:
            print("[!] Exiting bot")
            pass
        except KeyboardInterrupt:
            # Allows CTRL+c exit
            self.client.loop.close()
            print("[!] Fine be that way! Exiting!")

    def store_last_seen(self, tweet):
        '''
        Stores last tweet ID in the LAST_SEEN_FILE.
        #TODO: Store the last 10 tweets incase multiple tweets come in at the same time
        #TODO: Save tweet.id(s) in the .env file now
        '''
        with open(self.LAST_SEEN_FILE, 'w') as f:
            f.write(f'{tweet.id}')

    def read_last_seen(self):
        #TODO !BUG! Error returned if file is empty
        with open(self.LAST_SEEN_FILE, 'r') as f:
            return int(f.read().strip())

    def twitter_auth(self):
        self.auth = tweepy.OAuthHandler(self.TWITTER_API_KEY, self.TWITTER_API_KEY_SECRET)
        self.auth.set_access_token(self.TWITTER_ACCESS_TOKEN, self.TWITTER_ACCESS_TOKEN_SECRET)
        self.twitter_api = tweepy.API(self.auth)

    def get_tweet(self):
        tweet = self.twitter_api.user_timeline(screen_name=self.TWITTER_USERNAME, count=1)[0]
        return tweet

    async def start_monitor(self):
        while True:
            tweet = self.get_tweet()
            if tweet.id != self.read_last_seen():
                print("[+] New Exploit! Sending to discord...")
                await self.send_message(tweet.text)
                self.store_last_seen(tweet)
            await asyncio.sleep(30)

    async def send_message(self, tweet):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(self.DISCORD_CHANNEL_ID)
        await channel.send(tweet)

ribbit = Discord_Bot()
