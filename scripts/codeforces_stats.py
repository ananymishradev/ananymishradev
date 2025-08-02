import requests
from datetime import datetime
import json
from pathlib import Path

# Config
USERNAME = "ananymishradev"  # Replace with your Codeforces handle
OUTPUT_DIR = Path("stats")
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_codeforces_data():
    try:
        # Fetch user info
        user_info = requests.get(
            f"https://codeforces.com/api/user.info?handles={USERNAME}"
        ).json()
        
        # Fetch user submissions
        submissions = requests.get(
            f"https://codeforces.com/api/user.status?handle={USERNAME}"
        ).json()
        
        # Fetch contest history
        contests = requests.get(
            f"https://codeforces.com/api/user.rating?handle={USERNAME}"
        ).json()
        
        return {
            "user_info": user_info,
            "submissions": submissions,
            "contests": contests
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def process_data(raw_data):
    if not raw_data:
        return None
    
    try:
        # Process user info
        user = raw_data["user_info"]["result"][0]
        submissions = raw_data["submissions"]["result"]
        contests = raw_data["contests"]["result"]
        
        # Calculate solved problems (unique)
        solved_problems = set()
        for sub in submissions:
            if sub["verdict"] == "OK":
                problem = sub["problem"]
                solved_problems.add(f"{problem['contestId']}{problem['index']}")
        
        # Calculate contest stats
        contest_stats = {
            "count": len(contests),
            "best_rank": min((c["rank"] for c in contests), 
            "rating": user.get("rating", 0),
            "max_rating": user.get("maxRating", 0),
            "rank": user.get("rank", "unrated")
        }
        
        return {
            "handle": USERNAME,
            "solved": len(solved_problems),
            "contests": contest_stats,
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def generate_svg(stats):
    if not stats:
        stats = {
            "handle": USERNAME,
            "solved": 0,
            "contests": {
                "count": 0,
                "best_rank": 0,
                "rating": 0,
                "max_rating": 0,
                "rank": "error"
            }
        }
    
    rating_color = {
        "unrated": "#000000",
        "newbie": "#808080",
        "pupil": "#008000",
        "specialist": "#03a89e",
        "expert": "#0000ff",
        "candidate master": "#aa00aa",
        "master": "#ff8c00",
        "international master": "#ff8c00",
        "grandmaster": "#ff0000",
        "international grandmaster": "#ff0000",
        "legendary grandmaster": "#ff0000"
    }.get(stats["contests"]["rank"].lower(), "#000000")
    
    svg = f'''
    <svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
      <style>
        .background {{ fill: #0d1117; }}
        .header {{ font: bold 18px 'Segoe UI', sans-serif; fill: #58a6ff; }}
        .stat-label {{ font: 14px 'Segoe UI', sans-serif; fill: #8b949e; }}
        .stat-value {{ font: bold 14px 'Segoe UI', sans-serif; fill: #c9d1d9; }}
        .rating {{ fill: {rating_color}; font-weight: bold; }}
      </style>
      
      <rect width="100%" height="100%" rx="5" class="background"/>
      
      <text x="20" y="30" class="header">Codeforces Stats</text>
      <text x="20" y="55" class="stat-value">@{stats["handle"]}</text>
      
      <text x="20" y="85" class="stat-label">Problems Solved:</text>
      <text x="180" y="85" class="stat-value">{stats["solved"]}</text>
      
      <text x="20" y="115" class="stat-label">Contest Rating:</text>
      <text x="180" y="115" class="rating">{stats["contests"]["rating"]}</text>
      
      <text x="20" y="145" class="stat-label">Max Rating:</text>
      <text x="180" y="145" class="rating">{stats["contests"]["max_rating"]}</text>
      
      <text x="20" y="175" class="stat-label">Contests:</text>
      <text x="180" y="175" class="stat-value">{stats["contests"]["count"]} (Best Rank: #{stats["contests"]["best_rank"]})</text>
    </svg>
    '''
    
    with open(OUTPUT_DIR / "codeforces.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    raw_data = fetch_codeforces_data()
    stats = process_data(raw_data)
    generate_svg(stats)
    
    # Save raw data for debugging
    with open(OUTPUT_DIR / "codeforces_raw.json", "w") as f:
        json.dump(raw_data, f)
