import praw
import reddit_globals
from datetime import date, datetime, timedelta
import time

def post_to_reddit(episode_list):
    today = date.today()

    r = praw.Reddit(client_id=reddit_globals.app_id, 
                    client_secret=reddit_globals.app_secret,
                    password=reddit_globals.password,
                    user_agent=reddit_globals.app_ua,
                    username=reddit_globals.username)

    r.validate_on_submit = True

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M:%S")

    for episode in episode_list:
        # If new episode today, continue
        if episode.air_date == str(today):
            previous_submission = None
            new_submission = None


            ## Get previous submission reference
            previous_ep = episode_list[episode_list.index(episode) - 1]
            previous_title = "Season %s Episode %s Discussion Thread - %s" % (previous_ep.season, previous_ep.episode_number, previous_ep.episode_name)
            search_list = r.subreddit(reddit_globals.subreddit).search(previous_title)
            for search_res in search_list:
                if search_res.author == reddit_globals.username:
                    previous_submission = search_res


            ## Generate new post description with previous episode link
            new_title = "Season %s Episode %s Discussion Thread - %s" % (episode.season, episode.episode_number, episode.episode_name)
            new_description = episode.overview
            if previous_submission is not None:
                new_description = new_description + "\n\n[Previous Episode](%s)" % previous_submission.url


            ## Unsticky previously stickied posts, will resticky later to set correct order
            subreddit = r.subreddit(reddit_globals.subreddit).hot(limit=25)
            for post in subreddit:
                if post.stickied:
                    post.mod.sticky(state=False)


            ## Create new post, generate comments from TVDB episode description and sticky/distinguish
            new_submission = r.subreddit(reddit_globals.subreddit).submit(new_title, selftext=new_description)
            test1 = episode.overview.replace(reddit_globals.begin_keyword, "")
            test2 = test1.split(reddit_globals.end_keyword)[0].rstrip()
            test3 = test2.split(', ')
            name_list = []
            for name in test3:
                if "and " in name:
                    name_list.append(name.replace("and ", ""))
                else:
                    name_list.append(name)

            name_list.append(reddit_globals.append_name)

            index = 0
            for name in name_list:
                if index == 0:
                    comment = new_submission.reply("**%s**%s" % name, reddit_globals.post_end_text)
                if index == 1:
                    comment = new_submission.reply("**%s**%s" % name, reddit_globals.post_end_text)
                if index == 2:
                    comment = new_submission.reply("**%s**%s" % name, reddit_globals.post_end_text)
                if index == 3:
                    comment = new_submission.reply("**%s**%s" % name, reddit_globals.post_end_text)
                if index == 4:
                    comment = new_submission.reply("**%s**%s" % name, reddit_globals.post_end_text)
                
                comment.mod.distinguish(how="yes")
                index += 1

            new_submission.mod.sticky(state=True)
            new_submission.mod.distinguish(how="yes")


            ## Update previous episode post with Next Episode link
            if previous_submission is not None:
                previous_description = previous_submission.selftext
                previous_description = previous_description + "\n\n[Next Episode](%s)" % new_submission.url
                previous_submission.edit(previous_description)
            previous_submission.mod.sticky(state=True)
            if not previous_submission.distinguished:
            previous_submission.mod.distinguish(how="yes")