#!/usr/bin/env python

import sys
import time
import csv
import os
import getpass

import praw
import OAuth2Util
import logger
import webbrowser
import pprint

PURGE = False         # Delete contents from previous account
INTERACTIVE = False   # Do not ask questions, follow above setting
pp = pprint.PrettyPrinter(width=41, compact=True)

def print_dot():
    """Prints out a dot on the same line when called"""
    sys.stdout.write('. ')
    sys.stdout.flush()

def csv_file(fp, header):
    """Create or append a CSV file."""
    if os.path.exists(fp):
        f = open(fp, 'a')
        writer = csv.writer(f)
    else:
        f = open(fp, 'w')
        writer = csv.writer(f)
        writer.writerow(header)

    return f, writer

def format_time(created):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created)).encode('utf-8')

# Ask the user for a decision. 'y' and 'Y' will evaluate to True, anything else will equate to False.
# A better implementation is welcome, it's just a quick-n-dirty slap-together job! -ChainsawPolice
def y_or_n(decision):
    if decision.lower() == 'y': 
        return True
    else:                   
        return False




def init():
    pass

def deinit():
    pass

def take_a_nap():
    time.sleep(30)


def save_comments( user=None):
    print( '>> Saving all comments...')

    comment_file, comment_csv = csv_file(
        '{}_comments.csv'.format(user.name),
        ['Comment', "Posted on", "Thread"])

    with comment_file:
        for com in user.get_comments(limit=None):
            link = com.submission.permalink.encode('utf-8')
            body = com.body.encode('utf-8')
            row = [body, format_time(com.created), link]
            try:
                comment_csv.writerow(row)
            except Exception as e:
                print( 'Failed to store comment', link)
                print( e)
    print( '\n\t>> Saved to {0}_comments.csv'.format(user.name))


def delete_comments( user=None):
    print( '>> Deleting all comments...')
    removed = 1
    for com in user.get_comments(limit=None):
        link = com.submission.permalink.encode('utf-8')
        try:
            com.edit('.')
            removed += 1
            print_dot()
        except Exception as e:
            print( 'Failed to delete comment', link)
            print( e)


def save_posts( user=None):
    print( '>> Saving all posts...')
    submission_header = ['Title', "Body/Link", "Created", "Karma"]
    submission_file, submission_csv = csv_file(
        '{}_posts.csv'.format(user.name),
        submission_header)

    with submission_file:
        for sub in user.get_submitted(limit=None):
            submission = sub.url.encode('utf-8')
            title = sub.title.encode('utf-8')
            row = [title, submission, format_time(sub.created), '{}'.format(sub.score).encode('utf-8')]
            try:
                submission_csv.writerow(row)
                print_dot()
            except Exception as e:
                print( 'Failed to save post', e)
                pp.pprint(row)
        print( '\n\t>> Saved to {0}_posts.csv'.format(user.name))


def delete_posts( user=None):
    print( '>> Deleting all posts...')
    submission_header = ['Title', "Body/Link", "Created", "Karma"]
    submission_file, submission_csv = csv_file(
        '{}_submissions.csv'.format(user.name),
        submission_header)

    removed = 1
    while removed > 0:  # keep going until everything is gone
        removed = 0
        for sub in user.get_submitted(limit=None):
            if sub.is_self:
                submission = sub.selftext.encode('utf-8')
            else:
                submission = sub.url.encode('utf-8')
            try:
                sub.edit('.')
                removed += 1
                print_dot()
            except Exception as e:
                print( 'Failed to delete post', submission)
                print( e)


def save_subscriptions( user=None):
    print( '>> Saving all subscriptions...')
    submission_header = ['Title', "Link"]
    submission_file, submission_csv = csv_file(
        '{}_submissions.csv'.format(user.name),
        submission_header)

    with submission_file:
        for sub in user.get_my_subreddits()
            if sub.is_self:
                subreddit = sub.selftext.encode('utf-8')
            else:
                subreddit = sub.url.encode('utf-8')
            title = sub.title.encode('utf-8')
            row = [title, subreddit]
            try:
                submission_csv.writerow(row)
                print_dot()
            except Exception as e:
                print( 'Failed to store', subreddit)
                print( e)
    print( '\n\t>> Saved to {0}_subscriptions.csv'.format(user.name))



def do_work( reddit_client=None):
    print('>> Logging in to OLD account..')
    authenticated_user = reddit_client.get_me()

    print( '\t>>Login successful:', authenticated_user.name)
    old_user = reddit_client.user  # get a praw.objects.LoggedInRedditor object

    save_posts( old_user)
    if INTERACTIVE:
        print( 'Would you like to remove all your old posts? (y/n)')
        if y_or_n(raw_input('> ')):
            delete_posts( old_user)
    elif PURGE :
            delete_posts( old_user)

    save_comments( old_user)
    if INTERACTIVE:
        print( 'Would you like to delete all your old comments? (y/n)')
        if y_or_n(raw_input('> ')):
            delete_comments( old_user)
    elif PURGE :
            delete_comments( old_user)

    print( '\n\t>> Done migrating.')

    print( '>> Go to https://ssl.reddit.com/prefs/delete/',)
    print( 'to delete your old account.')


def main():

    reddit_client = praw.Reddit( user_agent='redditagain3')
    o = OAuth2Util.OAuth2Util(reddit_client)
    o.refresh(force=True)
    o.toggle_print()


    while True:
        try:
            do_work( reddit_client)
            quit()
        except praw.errors.OAuthInvalidToken:
            oauth_helper.refresh()

        take_a_nap()


if __name__ == '__main__':
    init()
    main()
    deinit()
