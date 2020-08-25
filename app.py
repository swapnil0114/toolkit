from flask import Flask, redirect, url_for, render_template, request
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from selenium.webdriver.firefox.options import Options

app = Flask(__name__, static_folder="static/")


from datetime import datetime, date, timedelta
#from twitterscraper import query_tweets
import tweepy
import csv
#import pandas as pd
####input your credentials here
consumer_key = "IsJYvwi5Ev61lyCovBZIxRiV8"
consumer_secret = "fq8R5Obzcc8ji28rXzLtzeQLP6jNs4ZN3k8dKd1wIvKlPLbz6b"
access_key = "903575593463119873-L2ltlrCQywULEd4WUReYSMdvZiWeH98"
access_secret = "dKLIeq9ciiAy2SiJR86a5hk4Ttv5TFW3yyknM5msh2EOb"
list_tweets = []


# def get_last_month_tweets(query, limit=1000, lang="en"):
#     start_date = date.today() - timedelta(30)
#     tweets = query_tweets(query, 10,poolsize=5, lang=lang, begindate=start_date)
#     print(tweets)
#     print(f"got {len(tweets)} tweet.")
#     return tweets
def Facebook_data(query):

    query = re.findall(r'\w+', query)
    for user_input in query:
        print(user_input)
        opts = Options()
        opts.set_headless()
        assert opts.headless
        browser = webdriver.Firefox(options=opts)
        # Go to the Facebook URL

        before_routing = browser.get("http://www.facebook.com")
        # Enter the username and Password
        browser.maximize_window()
        uname = browser.find_element_by_id("email")
        psword = browser.find_element_by_id("pass")
        submit = browser.find_element_by_id("u_0_b")
        # Send the details to respective fields
        uname.send_keys("8777355971")
        psword.send_keys("SWAP7871nil")
        # Automate Click Login
        submit.click()
        browser.get('https://www.facebook.com/search/posts/?q={0}&epa=SEARCH_BOX'.format(user_input))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        # see_all = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div/a')
        see_all = browser.find_elements_by_link_text('See All')[0]
        see_all.click()
        for _ in range(2):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        time.sleep(12)

        # x = browser.find_elements_by_xpath('//*[@id="u_ps_0_3_b"]')
        # y = browser.find_elements_by_xpath('//*[@id="u_ps_0_3_f"]')
        # z = browser.find_elements_by_xpath('//*[@id="u_ps_0_3_j"]')
        # a = browser.find_elements_by_xpath('//*[@id="u_ps_0_3_n"]')
        # b = browser.find_elements_by_xpath('//*[@id="u_ps_0_3_r"]')
        # c = browser.find_elements_by_xpath('//*[@id="u_ps_0_3_v"]')
        # #list_of_val = browser.find_element_by_id('_19_p')
        # #print(list_of_val)
        # html = browser.page_source
        # soup=BeautifulSoup(html, 'html.parser')
        # likes = browser.find_elements_by_class_name('_81hb')
        # print(likes)
        # for i in y:
        #     print(i.text)
        #     print(likes)
        # for i in x:
        #
        #     print(i.text)
        # for i in z:
        #     print(i.text)
        # for i in a:
        #     print(i.text)
        # for i in b:
        #     print(i.text)
        # for i in c:
        #     print(i.text)

        profile_pic = browser.find_elements_by_class_name('_19_p')
        print(profile_pic)
        profile_datas = browser.find_elements_by_id('u_ps_0_3_2')
        print(profile_datas)
        for profile_data in profile_pic[0:-1]:
            share = ''
            comments = ''
            likes = ''
            post_img = ''
            profile_snap = ''
            post_text = ''
            name = profile_data.find_elements_by_tag_name('a')[0].get_attribute('title')
            # likes = profile_data.find_element_by_class_name('_81hb').text
            try:
                profile_snap = (profile_data.find_elements_by_tag_name('img')[0].get_attribute('src'))
                post_img = (profile_data.find_elements_by_tag_name('img')[1].get_attribute('src'))
            except:
                print("Error in pnr or both field")
            details = (profile_data.text)
            detail = (details.split('\n'))
            if profile_data.find_element_by_class_name('_6-cm'):
                post_text = profile_data.find_element_by_class_name('_6-cp').text

            for i in detail:
                if re.findall(r'\d+$', str(i)):
                    likes = re.findall(r'\d+$', str(i))[0]
            if re.findall(r'\d+ share', details):
                share = re.findall(r'\d+ share', details)[0]
            if re.findall(r'\d+ comments', details):
                comments = re.findall(r'\d+ comments', details)[0]
            if name == '':
                name = profile_data.text.split('\n')[0]

            list_values = [profile_snap, name, post_text, post_img, likes, share, comments]
            print(post_text)
            print(name)
            print(likes)
            print(share)
            print(comments)
            print("######################################################################################")
            yield list_values











def get_last_month_tweets(querys):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print(api)
    #####United Airlines
    # Open/Create a file to append data
    # csvFile = open('ua.csv', 'a')
    # #Use csv Writer
    # csvWriter = csv.writer(csvFile)
    querys = re.findall(r'\w+', querys)
    for query in querys:
        print(query)

        for tweet in tweepy.Cursor(api.search, q=str(query), count=2,
                                   lang="en",
                                   since="2020-07-03").items(1):
            x = ''
            tweets = []
            id  = str(tweet.id)
            print(id)
            fullname = tweet.user.screen_name
            is_retweet = ''
            likes = str(int(tweet.favorite_count))
            replies = ''
            retweet_id = ''
            retweeter_userid = ''
            retweeter_username = ''
            retweets = str(int(tweet.retweet_count))
            print(retweets)
            text = str(tweet.text)
            timestamp = str(tweet.created_at)
            tweet_id = str(tweet.id)
            user_id = tweet.in_reply_to_user_id
            username = tweet.user.screen_name
            tweet_url = tweet.source_url
            url = 'https://twitter.com/i/web/status/'+ str(tweet.id)
            opts = Options()
            opts.set_headless()
            assert opts.headless
            browser = webdriver.Firefox(options=opts)
            response = browser.get(url)
            browser.maximize_window()
            time.sleep(6)
            x = browser.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[4]/div/div/article/div/div/div/div[3]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/video')
            if x:
                x = x[0].get_attribute('src')
            if not x:
                #if browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[2]/div/div/div[1]/a/div/div[2]/div/img'):
                try:
                    x = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[2]/div/div/div[1]/a/div/div[2]/div/img').get_attribute('src')
                except Exception:
                    print(Exception)

            if not x:
                x = 'No Photo'

            soup = bs(browser.page_source, 'html.parser')
            print(x)
            print(type(x))
            #x =browser.find_elements_by_class_name('r-1p0dtai').text
            #element = browser.find_element_by_class_name('css-1dbjc4n').screenshot('D://Media_Tool_kit//venv//static//images//'+ str(tweet.id) + '.png')
            tweets = [fullname,is_retweet, likes, replies,retweeter_userid,x,retweeter_username, retweets,text, timestamp, tweet_id, user_id, username, tweet_url, id]
            browser.close()
            yield tweets


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        check_box_2 = ''
        check_box_1 = ''
        if 'fb' in dict(request.form).keys():
            check_box_2 = request.form['fb']

        if 'tweet' in dict(request.form).keys():
            check_box_1 = request.form['tweet']

        print(check_box_2)
        users = request.form["query"].split(' ')
        # if check_box_1 and check_box_2:
        #     return redirect(url_for("Facebook_Twitter", usr=users))
        if check_box_2 and not check_box_1:
            return redirect(url_for("Facebook", usr=users))
        elif check_box_1 and not check_box_2:
            print('Hello')
            tweets = get_last_month_tweets(str(users))
            return render_template('twiter_no_temp.html', content=tweets)
        else:
            fb_data = Facebook_data(str(users))
            tweets = get_last_month_tweets(str(users))
            return render_template('facebook_twitter.html', content=tweets, content1=fb_data)




    else:
        return render_template("login.html")

# @app.route("/<usr>")
# def Facebook_Twitter(usr):
#     # tweets = get_last_month_tweets(usr)
#     # return render_template('twiter_no_temp.html', content=tweets)
#     fb_data = Facebook_data(usr)
#     tweets = get_last_month_tweets(usr)
#     return render_template('facebook_twitter.html', content=fb_data, content1 = tweets)






@app.route("/<usr>")
def Facebook(usr):
    # tweets = get_last_month_tweets(usr)
    # return render_template('twiter_no_temp.html', content=tweets)
    fb_data = Facebook_data(usr)
    return render_template('facebook.html', content=fb_data)


# @app.route("/user")
# def Twitter(usr):
#     # tweets = get_last_month_tweets(usr)
#     # return render_template('twiter_no_temp.html', content=tweets)
#     tweets = get_last_month_tweets(usr)
#     return render_template('twiter_no_temp.html', content=tweets)


if __name__ == "__main__":
    app.run(debug=True)