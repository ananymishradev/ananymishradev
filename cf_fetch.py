import requests
import json

handle = "ananymishradev"
output_file = "output/codeforces_stats.svg"

response = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")
if response.status_code == 200:
    result = response.json()["result"][0]
    rank = result.get("rank", "unrated").title()
    rating = result.get("rating", "N/A")
    max_rank = result.get("maxRank", "N/A").title()
    max_rating = result.get("maxRating", "N/A")

    svg_content = f"""<svg xmlns='http://www.w3.org/2000/svg' width='380' height='100'>
    <rect width='100%' height='100%' fill='white'/>
    <text x='10' y='20' font-size='16'>Handle: {handle}</text>
    <text x='10' y='40' font-size='16'>Rank: {rank}</text>
    <text x='10' y='60' font-size='16'>Rating: {rating}</text>
    <text x='10' y='80' font-size='16'>Max: {max_rank} ({max_rating})</text>
    </svg>"""

    with open(output_file, "w") as f:
        f.write(svg_content)
else:
    print("Error fetching data from Codeforces API")
