import requests
import pandas as pd
import time
import urllib.parse

SUBREDDITS = [
    "depresi", "depressed", "anxiety", "cemas", "stress", "stres", 
    "trauma", "suicide", "bunuh diri", "mental health", "burnout",
    "sedih", "tidak sanggup", "ingin mati", "overthinking", "lelah",
    "sad", "hopeless", "putus asa"
]

KEYWORDS = [
    "indonesia", "indonesian"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.reddit.com/",
    "Origin": "https://www.reddit.com"
}

def is_news(text):

    bad_keywords = [
        "detik",
        "kompas",
        "cnn",
        "tribun",
        "kemenkes",
        "viral",
        "ditemukan",
        "meninggal",
        "geger",
        "berita"
    ]

    return any(b in text.lower() for b in bad_keywords)


def is_news(text):

    bad_keywords = [
        "detik",
        "kompas",
        "cnn",
        "tribun",
        "kemenkes",
        "viral",
        "ditemukan",
        "meninggal",
        "geger",
        "berita"
    ]

    return any(b in text.lower() for b in bad_keywords)


def personal_score(text):

    personal_pronouns = ["aku", "saya", "gue", "gw", "i'm", "my", "i feel", "me"]
    
    context_keywords = [
        "keluarga", "ortu", "ayah", "ibu", "orang tua", "pacar", 
        "skripsi", "kuliah", "kerja", "kantor", "atasan", "bos",
        "hidup", "masalah", "capek", "bosen", "kesepian", "lonely", 
        "burnout", "hampa", "gagal"
    ]

    score = sum(k in text.lower() for k in personal_pronouns) * 3 
    score += sum(k in text.lower() for k in context_keywords) * 1
    return score


def mh_score(text):

    keywords = [
        "depresi", "depressed", "anxiety", "cemas", "stress", "stres", 
        "trauma", "suicide", "bunuh diri", "mental health", "burnout",
        "sedih", "tidak sanggup", "ingin mati", "overthinking", "lelah",
        "sad", "hopeless", "putus asa"
    ]

    return sum(k in text.lower() for k in keywords)


def total_score(text):

    return (
        personal_score(text) * 2
        + mh_score(text)
    )

# COLLECT POSTS

all_posts = []

session = requests.Session()

for subreddit in SUBREDDITS:

    print(f"\n========== SUBREDDIT: r/{subreddit} ==========")

    for keyword in KEYWORDS:

        print(f"\nSearching keyword: {keyword}")

        keyword_encoded = urllib.parse.quote(keyword)

        url = (
            f"https://www.reddit.com/r/"
            f"{subreddit}/search.json?"
            f"q={keyword_encoded}&restrict_sr=on&limit=100"
        )

        try:

            r = session.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            print("STATUS:", r.status_code)

            if r.status_code != 200:
                print("SKIPPED")
                continue

            data = r.json()

            children = data["data"]["children"]

            print("Posts found:", len(children))

            for child in children:

                post = child["data"]

                title = post.get("title", "")
                selftext = post.get("selftext", "")

                full_text = (
                    title + " " + selftext
                ).strip()

                # Skip empty posts
                if len(full_text) < 30:
                    continue

                # Skip obvious news
                if is_news(full_text):
                    continue

                # Keep only personal-ish posts
                score = total_score(full_text)

                if score < 3:
                    continue

                all_posts.append({
                    "subreddit": subreddit,
                    "keyword": keyword,
                    "title": title,
                    "selftext": selftext,
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "created_utc": post.get("created_utc", 0),
                    "personal_mh_score": score,
                    "url": (
                        "https://reddit.com"
                        + post.get("permalink", "")
                    )
                })

            # anti-rate-limit
            time.sleep(2)

        except Exception as e:

            print("ERROR:", e)


# BUILD DATAFRAME

df = pd.DataFrame(all_posts)

# remove duplicate posts
df = df.drop_duplicates(
    subset=["url"]
)

df["selftext"] = df["selftext"].str.replace("\n", " ", regex=False)
df["selftext"] = df["selftext"].str.replace("\r", " ", regex=False)
df["title"] = df["title"].str.replace("\n", " ", regex=False)


df.to_csv(
    "reddit_indonesia_mental_health.csv",
    index=False
)

print("\nSaved:")
print("reddit_indonesia_mental_health.csv")