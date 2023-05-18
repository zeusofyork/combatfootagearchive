import praw
import requests
import os

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id='fpM8_rryL1RZB2Mfkbxk1w',
    client_secret='VhCXoPYQ_LzIMO690d7ixwo7J6nu4g',
    user_agent='chrome',
)

# Specify the subreddit you want to download videos from
subreddit_name = 'combatfootage'

# Get all posts from the subreddit
subreddit = reddit.subreddit(subreddit_name)
posts = subreddit.new(limit=None)  # Fetch all posts

# Download videos from each post
for post in posts:
    # Check if the post has a video
    if post.is_video:
        video_url = post.media['reddit_video']['fallback_url']
        title = str('post_title: ' + post.title)
        #post_id = str('post_id: ' + post.id)
        post_url = str('post_url: ' + 'reddit.it/' + post.id)
        post_info = [title, post_url]
        # Remove the extension from the URL to get the filename
        filename = str(post.id)
        print(f"Downloading video: {filename}")

        # Create a folder for each video using the filename
        folder_name = os.path.join('downloads', filename)
        os.makedirs(folder_name, exist_ok=True)
        with open((os.getcwd() + '/downloads/' + filename + '/' + filename +'.txt') , 'w') as post_details:
            for item in post_info:
                post_details.write(item)
                post_details.write('\n')
        
        # Send a request to download the video
        response = requests.get(video_url)

        
        # Save the video to a file inside the folder
        file_path = os.path.join(folder_name, f"{filename}.mp4")
        with open(file_path, 'wb') as file:
            file.write(response.content)
            

        print(f"Video downloaded: {filename}")

