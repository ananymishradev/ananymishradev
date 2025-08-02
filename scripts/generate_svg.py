import json
from datetime import datetime

# Load data with fallback
try:
    with open('stats.json') as f:
        data = json.load(f)
except:
    data = {
        "solved": 0, "easy": 0, "medium": 0, "hard": 0,
        "ranking": "N/A", "contestRating": 0, "contestTopPercent": 0,
        "contestsAttended": 0, "lastSubmission": "N/A", "acceptanceRate": 0
    }

# SVG Template
svg = f'''
<svg width="460" height="240" xmlns="http://www.w3.org/2000/svg">
  <style>
    .background {{ fill: #0d1117; }}
    .header {{ font: bold 20px 'Segoe UI', Arial; fill: #58a6ff; }}
    .stat-label {{ font: 14px 'Segoe UI', Arial; fill: #8b949e; }}
    .stat-value {{ font: bold 14px 'Segoe UI', Arial; fill: #c9d1d9; }}
    .easy {{ fill: #2ecc71; }} 
    .medium {{ fill: #f1c40f; }}
    .hard {{ fill: #e74c3c; }}
    .contest {{ fill: #9b59b6; }}
    .footer {{ font: 12px 'Segoe UI', Arial; fill: #484f58; }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="5" class="background"/>

  <!-- Header -->
  <text x="20" y="35" class="header">LeetCode Stats (@ananymishradev)</text>

  <!-- Problems Solved -->
  <text x="20" y="70" class="stat-label">Problems Solved:</text>
  <text x="150" y="70" class="stat-value">
    <tspan class="easy">✓ {data["easy"]} Easy</tspan>
    <tspan dx="10" class="medium">✓ {data["medium"]} Medium</tspan>
    <tspan dx="10" class="hard">✓ {data["hard"]} Hard</tspan>
  </text>

  <!-- Total Stats -->
  <text x="20" y="100" class="stat-label">Total Solved:</text>
  <text x="150" y="100" class="stat-value">{data["solved"]}</text>

  <text x="20" y="130" class="stat-label">Acceptance Rate:</text>
  <text x="150" y="130" class="stat-value">{data["acceptanceRate"]}%</text>

  <!-- Contest Stats -->
  <text x="20" y="160" class="stat-label">Contest Rating:</text>
  <text x="150" y="160" class="stat-value contest">{data["contestRating"]}</text>

  <text x="20" y="190" class="stat-label">Top Percentage:</text>
  <text x="150" y="190" class="stat-value">{data["contestTopPercent"]}%</text>

  <!-- Footer -->
  <text x="20" y="220" class="footer">
    Last update: {datetime.now().strftime("%Y-%m-%d %H:%M")} | 
    Last solved: {data["lastSubmission"]}
  </text>
</svg>
'''

# Save SVG
with open('stats.svg', 'w') as f:
    f.write(svg)
