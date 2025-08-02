import requests
from datetime import datetime
from collections import Counter

HANDLE = "ananymishradev"

def fetch_profile():
    url = f"https://codeforces.com/api/user.info?handles={HANDLE}"
    r = requests.get(url).json()
    if r["status"] != "OK":
        raise Exception("Error fetching profile")
    return r["result"][0]

def fetch_submissions():
    url = f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=1000"
    r = requests.get(url).json()
    if r["status"] != "OK":
        raise Exception("Error fetching submissions")
    return r["result"]

def calculate_streak(dates):
    if not dates:
        return 0
    dates = sorted(set(dates))
    streak = max_streak = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
        else:
            max_streak = max(max_streak, streak)
            streak = 1
    return max(max_streak, streak)

def generate_readme(profile, solved_count, streak):
    with open("README.md", "r") as f:
        lines = f.readlines()

    start = "<!--START-CF-STATS-->"
    end = "<!--END-CF-STATS-->"
    cf_block = f"""{start}
**Codeforces Stats for [{HANDLE}](https://codeforces.com/profile/{HANDLE})**
- Rank: {profile.get("rank", "Unrated").capitalize()}
- Current Rating: {profile.get("rating", "N/A")}
- Max Rating: {profile.get("maxRating", "N/A")} ({profile.get("maxRank", "").capitalize()})
- Total Problems Solved: {solved_count}
- Longest Streak: {streak} days
{end}
"""

    try:
        start_idx = lines.index(start + "\n")
        end_idx = lines.index(end + "\n") + 1
        lines[start_idx:end_idx] = [cf_block + "\n"]
    except ValueError:
        lines.append("\n" + cf_block + "\n")

    with open("README.md", "w") as f:
        f.writelines(lines)

def main():
    profile = fetch_profile()
    submissions = fetch_submissions()
    ac_dates = [datetime.fromtimestamp(s['creationTimeSeconds']).date()
                for s in submissions if s.get("verdict") == "OK"]
    solved_count = len({f"{s['problem']['contestId']}-{s['problem']['index']}" for s in submissions if s.get("verdict") == "OK"})
    streak = calculate_streak(ac_dates)
    generate_readme(profile, solved_count, streak)

if __name__ == "__main__":
    main()
