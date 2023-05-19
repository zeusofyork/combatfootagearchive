import datetime
import praw
import requests
import os
import datetime

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id='fpM8_rryL1RZB2Mfkbxk1w',
    client_secret='VhCXoPYQ_LzIMO690d7ixwo7J6nu4g',
    user_agent='chrome',
)

# Specify the subreddit you want to download videos from
subreddit_name = 'combatfootage'

while True:
    # Get all posts from the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=None)  # Fetch all posts

    # Download videos from each post
    for post in posts:
        # Check if the post has a video
        if post.is_video:
            video_url = post.media['reddit_video']['fallback_url']
            title = str('post_title: ' + post.title)
            post_url = str('post_url: ' + 'reddit.it/' + post.id)
            post_info = [title, post_url]
            # Remove the extension from the URL to get the filename
            filename = str(post.id)
            print(f"Downloading video: {filename}")

            # Get the UTC timestamp of the post in from unix timestamp, formatted to ISO8601 datetime, and truncated to the date as a string.
            time = post.created_utc
            date = datetime.date.fromtimestamp(time)
            # Create a folder for the date the video was uploaded if it doesn't exist. To make search or sorting by date easy.
            date_folder = os.path.join('downloads', str(date))
            if not os.path.exists(date_folder):
                os.makedirs(date_folder, exist_ok=True)

            # Create a folder for each video using the filename if it doesn't exist. The folder is stored underneath the date folder.
            folder_name = os.path.join(date_folder, filename)
            if os.path.exists(folder_name):
                choice = input(f"The folder '{folder_name}' already exists. Do you want to skip? (y/n): ")
                if choice.lower() == 'y':
                    print(f"Skipping folder: {folder_name}")
                    continue
                else:
                    print(f"Folder: {folder_name}")

            os.makedirs(folder_name, exist_ok=True)
            with open(os.path.join(folder_name, f"{filename}.txt"), 'w') as post_details:
                for item in post_info:
                    post_details.write(item)
                    post_details.write('\n')

            # Check if the video file already exists
            video_file_path = os.path.join(folder_name, f"{filename}.mp4")
            if os.path.exists(video_file_path):
                choice = input(f"The file '{video_file_path}' already exists. Do you want to skip? (y/n): ")
                if choice.lower() == 'y':
                    print(f"Skipping video: {video_file_path}")
                    continue
                else:
                    print(f"Video: {video_file_path}")

            # Send a request to download the video
            response = requests.get(video_url)

            # Save the video to a file inside the folder
            with open(video_file_path, 'wb') as file:
                file.write(response.content)

            print(f"Video downloaded: {filename}")

    choice = input("Do you want to continue downloading new videos? (y/n): ")
    if choice.lower() != 'y':
        break
