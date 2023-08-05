import user_tweet_downloader.tweet_download as td
import user_tweet_downloader.accounts as ac

users = ac.USERS

def main(users):
	print(users)
	for user in users:
		        td.tweet_retrieve(user)


if __name__ == "__main__":
    main(users)


