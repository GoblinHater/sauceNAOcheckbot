import praw
import time

from SauceNAO import GetSauce

TIME_BETWEEN_MENTION_CHECK = 1200   # 20 minutes

# All subreddits bot will automatically reply to
PASSED_SUBREDDIT = ["Animefoot",
                   "Hentai4Everyone",
                    "AnimeBooty",
                    "AnimeFeets",
                    "sauceNAOcheckbot",
                    "AzurLaneXXX"]

MODERATING_SUBREDDIT = ["sauceNAOcheckbot",
                       "AnimeFeets"]


print("Authenticating......")
reddit = praw.Reddit('BOTNAME', user_agent='u/sauceNAOcheckbot by u/GoblinHater')
print("Authenticated as ", reddit.user.me())

# print(reddit.user.me())
# subreddit = reddit.subreddit("memes")


# Will convert the list object to appropriate string object to stream submissions from
def stringify():
    s = ""
    for i in range(0, len(PASSED_SUBREDDIT)-1):
        s += PASSED_SUBREDDIT[i] + "+"
    s += PASSED_SUBREDDIT[len(PASSED_SUBREDDIT)-1]
    return s


PASSED_SUBREDDIT = stringify()
print(PASSED_SUBREDDIT)


def Unread_list():
    unreads = list(reddit.inbox.unread(limit=None))
    return unreads


def Clear_inbox(inbox_list):
    reddit.inbox.mark_read(inbox_list)


# Function to reply to username mentions
def getMentions(Allunreads):
    print("Checkin mentions....")
    for item in Allunreads:
        if "u/saucenaocheckbot" in item.body.lower():
            print(item.submission.url)
            submission_url = item.submission.url
            if str(submission_url)[-3::] == "jpg" or str(submission_url)[-3::] == "png" or str(submission_url)[-4::] == "jpeg" or str(submission_url)[-3::] == "gif":
                answer = GetSauce(submission_url)
                time.sleep(5)
                print("Replying.......")
                item.reply(answer)
                print("Replied")
            else:
                item.reply("The image is not of a format compatible with sauceNAO \n\n ^I ^am ^a ^bot. ^give ^feedback ^to u/GoblinHater.^Wrong ^sauce? ^Reply ^with ^wrong")
        if item.body.lower() == "wrong":
            print("Incorrect sauce detected")
            parent_comment = item.parent()
            parent_comment.delete()
            item.reply("Thanks for notifying. I have deleted my comment")
            print("Incorrect sauce deleted")
    print("Got mentions")
    Clear_inbox(Unread_list())



# Function to reply in Passed subreddits
def subredditReply():
    allids = get_submission_ids_set()
    # print(allids)
    for post in reddit.subreddit(PASSED_SUBREDDIT).stream.submissions():
        # print(dir(post))
        if post.id not in allids:
            # print(allids)
            # allids.add(post.id)
            print(post.url)
            print("New post in "+str(post.subreddit))
            print(post.id)
            LogID(str(post.id))
            print("logged")
            if str(post.url)[-3::] == "jpg" or str(post.url)[-3::] == "png" or str(post.url)[-4::] == "jpeg" or str(post.url)[-3::] == "gif":
                answer = GetSauce(post.url, True)
                time.sleep(7)
                if answer:
                    print("replying......")
                    if str(post.subreddit) in MODERATING_SUBREDDIT:
                        post.reply(answer).mod.distinguish(sticky=True)
                    else:
                        post.reply(answer)
                    print("replied")
                else:
                    print("Not Results")
            else:
                print("Not an image")


# To log new submission id in the text file
def LogID(givenid):
    file = open("postid.txt", 'a')
    file.write("\n"+givenid)
    file.close()
# If new subreddit is added to PASSED_SUBREDDITS do a dry run and log some recent submission
# ids to prevent spamming old submissions


# Goes through the text file and stores all ids in a set
# Occasionally remove older, redundant ids from the text file
def get_submission_ids_set():
    submissions_id = set()
    # submissions_id = dict()
    file = open("postid.txt", 'r')
    lines = file.readlines()
    for line in lines:
        if "\n" in line:
            line = line[0:len(line)-1]
        submissions_id.add(line)
        # submissions_id.add(line)
    file.close()
    return submissions_id
# I used a set so that in the subredditReply function I can have a constant lookup time

# To update ids if a new subreddit is passed
# Remove all ids that are in the text document already to eliminate duplicates(redundant)
# Now automatically removes old entries and appends new ones
def update_ids_text():
    deletion = open("postid.txt", 'w')
    deletion.write("IDS OF ALL COMMENTS IVE REPLIED TO")
    deletion.close()
    file = open("postid.txt", 'a')
    i = 0
    for submission in reddit.subreddit(PASSED_SUBREDDIT).stream.submissions():
        i += 1
        file.write("\n"+submission.id)
        if i == 100:
            break
    file.close()

def run_bot():
    lastCheckedMentionsTime = time.time()
    for post in reddit.subreddit(PASSED_SUBREDDIT).stream.submissions():
        if post:
            if time.time() - lastCheckedMentionsTime > TIME_BETWEEN_MENTION_CHECK:
                getMentions(Unread_list())
                lastCheckedMentionsTime = time.time()
            subredditReply(post)


run_bot()
#update_ids_text(PASSED_SUBREDDIT)

