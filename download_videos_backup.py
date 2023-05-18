import praw
import requests

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
        # Remove the extension from the URL to get the filename
        filename = str(post.id)
        print(f"Downloading video: {filename}")
        
        # Send a request to download the video
        response = requests.get(video_url)
        
        # Save the video to a file
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Video downloaded: {filename}")
        
