import os
from googleapiclient.discovery import build
import pandas as pd
from tqdm import tqdm

from config import API_KEY

OUTPUT_FILE = "crawler/data/raw_comments.csv"

youtube = build("youtube", "v3", developerKey=API_KEY)

def load_existing_ids():
    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE)
        return set(df["comment_id"].astype(str))
    return set()


def save_comments(new_comments):
    df_new = pd.DataFrame(new_comments)

    if os.path.exists(OUTPUT_FILE):
        df_existing = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(OUTPUT_FILE, index=False)

def search_videos(query, max_results=50):
    request = youtube.search().list(q=query, part="id", type="video", maxResults=max_results)
    response = request.execute()
    return [item["id"]["videoId"] for item in response["items"]]

def fetch_comments(video_id, existing_ids, max_comments=500):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100, textFormat="plainText")

    while request and len(comments) < max_comments:
        response = request.execute()
        for item in response["items"]:
            # Check if exists
            comment_id = item["id"]
            if comment_id in existing_ids:
                continue

            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "video_id": video_id,
                "text": snippet["textDisplay"],
                "published_at": snippet["publishedAt"],
                "like_count": snippet["likeCount"]
            })
            existing_ids.add(comment_id)
        request = youtube.commentThreads().list_next(request, response)

    return comments

def main():
    queries = ("Punjabi song", "ਪੰਜਾਬੀ", "Punjabi news")

    existing_ids = load_existing_ids()
    print(f"Loaded {len(existing_ids)} existing comments")
    
    new_comments = []

    for query in queries:
        video_ids = search_videos(query)
        for vid in tqdm(video_ids, desc=f"Query: {query}"):
            try:
                new_comments.extend(fetch_comments(vid, existing_ids))
            except Exception as e:
                print(f"Error with video {vid}: {e}")

    save_comments(new_comments)
    print(f"Saved {len(new_comments)} new comments")

if __name__ == "__main__":
    main()
