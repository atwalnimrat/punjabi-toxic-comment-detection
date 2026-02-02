from googleapiclient.discovery import build
import pandas as pd
from tqdm import tqdm

from config import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)

def search_videos(query, max_results=100):
    request = youtube.search().list(q=query, part="id", type="video", maxResults=max_results)
    response = request.execute()
    return [item["id"]["videoId"] for item in response["items"]]

def fetch_comments(video_id, max_comments=1000):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100, textFormat="plainText")

    while request and len(comments) < max_comments:
        response = request.execute()
        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "video_id": video_id,
                "text": snippet["textDisplay"],
                "published_at": snippet["publishedAt"],
                "like_count": snippet["likeCount"]
            })
        request = youtube.commentThreads().list_next(request, response)

    return comments

def main():
    queries = ("Punjabi song", "ਪੰਜਾਬੀ", "Punjabi news")

    all_comments = []

    for query in queries:
        video_ids = search_videos(query)
        for vid in tqdm(video_ids, desc=f"Processing query: {query}"):
            try:
                all_comments.extend(fetch_comments(vid))
            except Exception as e:
                print(f"Error with video {vid}: {e}")

    df = pd.DataFrame(all_comments)
    df.to_csv("crawler/data/raw_comments.csv", index=False)
    print(f"Saved {len(df)} comments")

if __name__ == "__main__":
    main()
