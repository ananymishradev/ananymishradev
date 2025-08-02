import json
from datetime import datetime

# Load stats with error handling
try:
    with open('stats.json') as f:
        data = json.load(f)
except:
    data = {
        "solved": 0,
        "easySolved": 0,
        "mediumSolved": 0, 
        "hardSolved": 0,
        "ranking": "N/A"
    }

# SVG Template
svg = f'''
<svg width="380" height="180" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: bold 18px 'Segoe UI', sans-serif; fill: #58a6ff; }}
    .stat {{ font: 14px 'Segoe UI', sans-serif; fill: #c9d1d9; }}
    .value {{ font-weight: bold; }}
    .easy {{ fill: #2ecc71; }} 
    .medium {{ fill: #f39c12; }}
    .hard {{ fill: #e74c3c; }}
  </style>
  
  <!-- Background -->
  <rect width="100%" height="100%" rx="5" fill="#0d1117" />
  
  <!-- Title -->
  <text x="20" y="30" class="title">LeetCode Stats</text>
  
  <!-- Stats -->
  <text x="20" y="60" class="stat">Total Solved: <tspan class="value">{data["solved"]}</tspan></text>
  <text x="20" y="90" class="stat">
    <tspan class="easy">Easy: {data["easySolved"]}</tspan>
    <tspan dx="20" class="medium">Medium: {data["mediumSolved"]}</tspan>
    <tspan dx="20" class="hard">Hard: {data["hardSolved"]}</tspan>
  </text>
  <text x="20" y="120" class="stat">Contest Rank: <tspan class="value">{data["ranking"]}</tspan></text>
  
  <!-- Footer -->
  <text x="20" y="160" class="stat" font-size="12">
    Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
  </text>
</svg>
'''

# Save SVG
with open('stats.svg', 'w') as f:
    f.write(svg)
