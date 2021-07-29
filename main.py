import signal
import praw
import prawcore
import requests
import random
import face_recognition
import ai
from socket import gaierror
from time import sleep
from PIL import UnidentifiedImageError


class TimeoutException(Exception):
    pass

class RedditBot: 
    def __init__(self):
#        self.repeat_count = 0

        self.reddit = praw.Reddit(client_id="CLIENT_ID", client_secret="CLIENT_SECRET", user_agent="Linux:KenobIdentifier:v0.1.4 (by u/tvcz and u/valiantseal)", username="ObIdentifier", password="PASSWORD")

        self.prequel_memes = self.reddit.subreddit("prequelmemes")
        with open("submission_record.csv", "r+") as submission_record:
            self.submission_record = submission_record.read().split(",")

        signal.signal(signal.SIGALRM, self.timeout_handler);

    def find_images(self):
        print("\n\nScanning top 1000 posts of hot...\n")
        for submission in self.prequel_memes.hot(limit=1000):
            self.kenobidentify(submission)

        print("\n\nStreaming new posts...\n")
        for submission in self.prequel_memes.stream.submissions():
            self.kenobidentify(submission)
            

    def kenobidentify(self, submission):
        if submission.id in self.submission_record:
#           self.repeat_count += 1
#           print("\n", submission.id, submission.url, f"\n-> Post already scanned ({self.repeat_count})")
            return
            
        image_data = requests.get(submission.url, stream=True)

        try:
            image = face_recognition.load_image_file(image_data.raw)
            print("\n", submission.id, submission.url, "ValidImage")
            if ai.scan_image(image):
                signal.alarm(30)
                try:
                    self.make_comment(submission)
                except TimeoutException:
                    pass
                else:
                    signal.alarm(0)
            self.submission_record.append(submission.id)
            self.save_submission_record()

        except UnidentifiedImageError:
            print("\n", submission.id, submission.url, "NotValidImage")
            self.submission_record.append(submission.id)
            self.save_submission_record()

    def make_comment(self, submission):
        with open("kenobi_quotes.txt", "r+") as kenobi_quotes:
            quote = ""
            while quote == "":
                quote = random.choice(kenobi_quotes.read().split("\n"))
            print(quote)
            submission.reply(quote)

    def save_submission_record(self):
        with open("submission_record.csv", "w+") as submission_record:
            submission_record.write(",".join(self.submission_record))

    def timeout_handler(self, signum, frame):
        raise TimeoutException

reddit_bot = RedditBot()
while True:
    try:
        print("\nMain loop (re)starting...")
        reddit_bot.find_images()
    except praw.exceptions.RedditAPIException:
        print("\n", "Error: praw.exceptions.RedditAPIException")
        sleep(480)
    except gaierror:
        print("\n", "Error: socket.GaiError")
        sleep(30)
    except prawcore.exceptions.RequestException:
        print("\n", "Error: prawcore.exceptions.RequestException")
        sleep(480)
    
