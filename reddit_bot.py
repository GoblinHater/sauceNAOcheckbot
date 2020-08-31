import praw
import time

from SauceNAO import getSauce

print("Authenticating......")
reddit = praw.Reddit(client_id='id',
                     client_secret='secret',
                     password='password',
                     user_agent='/u/sauceNAOcheckbot by /u/GoblinHater',
                     username='sauceNAOcheckbot')
print("Authenticated as ", reddit.user.me())

# print(reddit.user.me())
# subreddit = reddit.subreddit("memes")


def Unread_list():
    unreads = list(reddit.inbox.unread(limit=None))
    return unreads


def Clear_inbox(inbox_list):
    reddit.inbox.mark_read(inbox_list)


def main(Allunreads):
    for item in Allunreads:
        if "u/sauceNAOcheckbot" in item.body:
            print(item.submission.url)
            submission_url = item.submission.url
            answer = getSauce(submission_url)
            print("Replying.......")
            item.reply(answer)
            print("Replied")
    Clear_inbox(Unread_list())
    time.sleep(5)


main(Unread_list())
