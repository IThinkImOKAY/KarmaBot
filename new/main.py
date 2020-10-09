import time
import praw
import random
import config
import pyimgur

reddit = praw.Reddit(client_id=config.C_ID, client_secret=config.C_S, user_agent=config.U_A, username=config.UN, password=config.PW)
subreddit = reddit.subreddit(config.SUB)
imgur_id = config.I_ID
domains = ['i.redd.it', 'i.imgur.com']
limit = None
x = random.randint(0,2)
while True:
    try:
        subreddit = reddit.subreddit('random')
        print('Random Subreddit Is: ', subreddit)       
        submissions = list(subreddit.top('all', limit=limit))
        submission = random.choice(submissions)
        if submission.domain in domains:
            im = pyimgur.Imgur(imgur_id)
            uploaded_image = im.upload_image(url=submission.url)
            with open ('links.txt', "a") as f:
                f.write(uploaded_image.link + "\n")
            reddit.validate_on_submit = True
            subreddit.submit(submission.title, url=uploaded_image.link)
            print('success')          
        elif submission.domain not in domains:
            print('domain is not in domains :(')      
        for submission in subreddit.stream.submissions(skip_existing=True):
            for results in subreddit.search(submission.title): 
                similarity = difflib.SequenceMatcher(None, submission.title,results.title).ratio()
                if results.num_comments >= 3 and similarity >= .8:
                    comment = results.comments[x]
                    if comment.author not in config.usernames and comment.body != '[deleted]':
                        submission.reply(comment.body)
                        break
            
    except Exception as e:
        print(e)
        time.sleep(60)
        
    except KeyboardInterrupt:
        print('shutting down :(')
        quit()
