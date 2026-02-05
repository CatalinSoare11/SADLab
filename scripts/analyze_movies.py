import csv
import math
import os
import random
import statistics
import urllib.request
from collections import defaultdict
from datetime import datetime

DATA_URL = "https://raw.githubusercontent.com/PromptCloud/IMDb-Movie-Database/master/IMDbMovies.csv"
RAW_PATH = "data/imdb_movies_raw.csv"
SUBSET_PATH = "data/last_1000_movies_dataset.csv"
SUMMARY_PATH = "data/genre_summary.csv"
CHART_PATH = "images/genre_weighted_score.svg"
SOURCE_NOTES_PATH = "data/README.md"

os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)

source_note = ""

# Attempt to download dataset
try:
    if not os.path.exists(RAW_PATH) or os.path.getsize(RAW_PATH) <= 1000:
        print(f"Downloading dataset from {DATA_URL}...")
        urllib.request.urlretrieve(DATA_URL, RAW_PATH)
    if os.path.exists(RAW_PATH) and os.path.getsize(RAW_PATH) > 1000:
        source_note = (
            "Source: PromptCloud IMDb Movies Dataset (https://github.com/PromptCloud/IMDb-Movie-Database)."
        )
    else:
        raise ValueError("Downloaded dataset was empty or too small.")
except Exception as exc:  # pragma: no cover - best effort download
    source_note = (
        "Source: Synthetic dataset generated locally because outbound network access was blocked "
        f"({exc}). Replace by downloading the IMDb Movies dataset when network access is available."
    )

rows = []
if os.path.exists(RAW_PATH) and os.path.getsize(RAW_PATH) > 1000:
    with open(RAW_PATH, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                year = int(row.get("Year") or 0)
            except ValueError:
                continue
            rating = row.get("Rating")
            votes = row.get("Votes")
            try:
                rating_val = float(rating) if rating else None
            except ValueError:
                rating_val = None
            try:
                votes_val = int(votes.replace(",", "")) if votes else None
            except ValueError:
                votes_val = None
            rows.append(
                {
                    "Title": row.get("Title", "").strip(),
                    "Year": year,
                    "Genre": row.get("Genre", "").strip(),
                    "Rating": rating_val,
                    "Votes": votes_val,
                }
            )
else:
    random.seed(42)
    genres_pool = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Crime",
        "Drama",
        "Family",
        "Fantasy",
        "Horror",
        "Mystery",
        "Romance",
        "Sci-Fi",
        "Thriller",
    ]
    current_year = datetime.utcnow().year
    for idx in range(1200):
        year = random.randint(current_year - 9, current_year)
        rating_val = round(random.uniform(4.5, 8.6), 1)
        votes_val = random.randint(5000, 450000)
        genre_count = random.randint(1, 3)
        genre = ", ".join(random.sample(genres_pool, genre_count))
        rows.append(
            {
                "Title": f"Synthetic Movie {idx + 1:04d}",
                "Year": year,
                "Genre": genre,
                "Rating": rating_val,
                "Votes": votes_val,
            }
        )

rows = [row for row in rows if row["Year"] > 0 and row["Rating"] is not None]
rows.sort(key=lambda r: (r["Year"], r["Votes"] or 0), reverse=True)
last_1000 = rows[:1000]

with open(SUBSET_PATH, "w", newline="", encoding="utf-8") as handle:
    fieldnames = ["Title", "Year", "Genre", "Rating", "Votes"]
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(last_1000)

# Aggregate by genre
stats = defaultdict(lambda: {"ratings": [], "votes": []})

for row in last_1000:
    genres = [g.strip() for g in row["Genre"].split(",") if g.strip()]
    for genre in genres:
        stats[genre]["ratings"].append(row["Rating"])
        if row["Votes"] is not None:
            stats[genre]["votes"].append(row["Votes"])

summary = []
for genre, values in stats.items():
    ratings = values["ratings"]
    votes = values["votes"] or [0]
    avg_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)
    avg_votes = statistics.mean(votes)
    weighted_score = avg_rating * math.log10(avg_votes + 1)
    summary.append(
        {
            "Genre": genre,
            "Titles": len(ratings),
            "AvgRating": round(avg_rating, 2),
            "MedianRating": round(median_rating, 2),
            "AvgVotes": int(round(avg_votes, 0)),
            "WeightedScore": round(weighted_score, 2),
        }
    )

summary.sort(key=lambda r: r["WeightedScore"], reverse=True)

with open(SUMMARY_PATH, "w", newline="", encoding="utf-8") as handle:
    fieldnames = ["Genre", "Titles", "AvgRating", "MedianRating", "AvgVotes", "WeightedScore"]
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(summary)

# SVG chart (top 10)
chart_width = 900
chart_height = 480
top = summary[:10]
max_score = max([row["WeightedScore"] for row in top] or [1])
bar_height = 32
bar_gap = 12
left_margin = 180
right_margin = 40
chart_body_height = len(top) * (bar_height + bar_gap)
chart_height = max(chart_height, chart_body_height + 120)

svg_lines = [
    f"<svg xmlns='http://www.w3.org/2000/svg' width='{chart_width}' height='{chart_height}'>",
    "<style>text{font-family:Arial, sans-serif; font-size:14px; fill:#1a202c;} .title{font-size:18px; font-weight:bold;}</style>",
    "<rect width='100%' height='100%' fill='#ffffff'/>",
    "<text x='30' y='40' class='title'>Top Genres by Weighted Score (Last 1,000 Releases)</text>",
]

origin_y = 80
for idx, row in enumerate(top):
    y = origin_y + idx * (bar_height + bar_gap)
    bar_width = (chart_width - left_margin - right_margin) * (row["WeightedScore"] / max_score)
    svg_lines.append(
        f"<text x='30' y='{y + 20}'>{row['Genre']}</text>"
    )
    svg_lines.append(
        f"<rect x='{left_margin}' y='{y}' width='{bar_width:.1f}' height='{bar_height}' fill='#2b6cb0'/>"
    )
    svg_lines.append(
        f"<text x='{left_margin + bar_width + 8:.1f}' y='{y + 20}'>{row['WeightedScore']}</text>"
    )

svg_lines.append("</svg>")

with open(CHART_PATH, "w", encoding="utf-8") as handle:
    handle.write("\n".join(svg_lines))

with open(SOURCE_NOTES_PATH, "w", encoding="utf-8") as handle:
    handle.write("# Data Source Notes\n\n")
    handle.write(source_note + "\n")

print("Analysis complete.")
