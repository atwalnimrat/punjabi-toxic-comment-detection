import re
import pandas as pd

OUTPUT_FILE = "data/clean_comments.csv"

GURMUKHI_RANGE = r"\u0A00-\u0A7F"
EMOJI_REGEX = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]+",
    flags=re.UNICODE,
)

def reduce_repeated_chars(text):
    return re.sub(r'(.)\1{3,}', r'\1\1', text)

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = EMOJI_REGEX.sub("", text)                                # remove emojis
    text = re.sub(r"http\S+", "", text)                             # remove links
    text = re.sub(rf"[^a-zA-Z{GURMUKHI_RANGE}\s.]", "", text)       # keep roman letters and gurmukhi
    text = re.sub(r"\s+", " ", text).strip()
    text = reduce_repeated_chars(text)                              # remove excessive repetition
    return text

df = pd.read_csv("data/raw_comments.csv")
df["text"] = df["text"].fillna("").astype(str)
df["clean_text"] = df["text"].apply(clean_text)
clean_df = df[["text", "clean_text", "published_at"]]

clean_df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(clean_df)} clean comments")
