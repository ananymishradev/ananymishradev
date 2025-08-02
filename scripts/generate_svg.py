import json
from datetime import datetime
from pathlib import Path

# Configure paths
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Load stats with fallback
try:
    with open(output_dir / "stats.json") as f:
        data = json.load(f)
except:
    data = {
        "solved": 0, "easy": 0, "medium": 0, "hard": 0,
        "ranking": "N/A", "contestRating": 0, "contestTopPercent": 0,
        "contestsAttended": 0, "lastSubmission": "N/A", "acceptanceRate": 0,
        "reputation": 0, "stars": 0, "globalRank": "N/A", "topLanguage": "N/A"
    }

# SVG Template with ALL stats
svg = f'''
<svg width="500" height="280" xmlns="http://www.w3.org/2000/svg">
  <style>
    .background {{ fill: #0d1117; }}
    .header {{ font: bold 18px 'Segoe UI'; fill: #58a6ff; }}
    .stat-label {{ font: 13px 'Segoe UI'; fill: #8b949e; }}
    .stat-value {{ font: bold 13px 'Segoe UI'; fill: #c9d1d9; }}
    .easy {{ fill: #2ecc71; }} .medium {{ fill: #f1c40f; }} .hard {{ fill: #e74c3c; }}
    .contest {{ fill: #9b59b6; }} .language {{ fill: #3498db; }}
    .footer {{ font: 11px 'Segoe UI'; fill: #484f58; }}
    .grid {{ stroke: #30363d; stroke-width: 0.5; }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="5" class="background"/>

  <!-- Header -->
  <text x="10" y="25" class="header">LeetCode Stats (@ananymishradev)</text>
  <line x1="10" x2="490" y1="35" y2="35" class="grid"/>

  <!-- Problem Stats -->
  <text x="10" y="55" class="stat-label">Problems Solved:</text>
  <text x="120" y="55" class="stat-value">
    <tspan class="easy">✓ {data["easy"]} Easy</tspan>
    <tspan dx="15" class="medium">✓ {data["medium"]} Medium</tspan>
    <tspan dx="15" class="hard">✓ {data["hard"]} Hard</tspan>
  </text>

  <!-- Total Stats -->
  <text x="10" y="80" class="stat-label">Total Solved:</text>
  <text x="120" y="80" class="stat-value">{data["solved"]}/{data["totalSubmissions"]}</text>
  
  <text x="250" y="80" class="stat-label">Acceptance:</text>
  <text x="340" y="80" class="stat-value">{data["acceptanceRate"]}%</text>

  <!-- Contest Stats -->
  <text x="10" y="105" class="stat-label">Contest Rating:</text>
  <text x="120" y="105" class="stat-value contest">{data["contestRating"]}</text>
  
  <text x="250" y="105" class="stat-label">Top %:</text>
  <text x="340" y="105" class="stat-value">{data["contestTopPercent"]}%</text>

  <text x="10" y="130" class="stat-label">Contests Attended:</text>
  <text x="120" y="130" class="stat-value">{data["contestsAttended"]}</text>
  
  <text x="250" y="130" class="stat-label">Global Rank:</text>
  <text x="340" y="130" class="stat-value">#{data["globalRank"]}</text>

  <!-- Profile Stats -->
  <line x1="10" x2="490" y1="145" y2="145" class="grid"/>
  
  <text x="10" y="165" class="stat-label">Profile Rank:</text>
  <text x="120" y="165" class="stat-value">#{data["ranking"]}</text>
  
  <text x="250" y="165" class="stat-label">Reputation:</text>
  <text x="340" y="165" class="stat-value">{data["reputation"]}</text>

  <text x="10" y="190" class="stat-label">Top Language:</text>
  <text x="120" y="190" class="stat-value language">{data["topLanguage"]}</text>
  
  <text x="250" y="190" class="stat-label">Stars:</text>
  <text x="340" y="190" class="stat-value">{"★" * int(data["stars"])}</text>

  <!-- Recent Activity -->
  <line x1="10" x2="490" y1="205" y2="205" class="grid"/>
  
  <text x="10" y="225" class="stat-label">Last Solved:</text>
  <text x="120" y="225" class="stat-value">{data["lastSubmission"]}</text>

  <!-- Footer -->
  <text x="10" y="265" class="footer">
    Updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
  </text>
</svg>
'''

# Save SVG
with open(output_dir / "stats.svg", "w") as f:
    f.write(svg)
