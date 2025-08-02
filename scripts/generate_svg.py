import json
from datetime import datetime

# Load LeetCode stats
with open('stats.json', 'r') as f:
    data = json.load(f)

# SVG Template (Customize colors, layout, etc.)
svg_template = f'''
<svg width="350" height="170" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="100%" height="100%" rx="5" fill="#0d1117" />
  
  <!-- Title -->
  <text x="20" y="30" font-family="Arial" font-size="18" fill="#58a6ff">
    LeetCode Stats (@ananymishradev)
  </text>
  
  <!-- Stats -->
  <text x="20" y="60" font-family="Arial" font-size="14" fill="#ffffff">
    Problems Solved: <tspan fill="#2ecc71">{data["solved"]}</tspan>
  </text>
  <text x="20" y="90" font-family="Arial" font-size="14" fill="#ffffff">
    Ranking: <tspan fill="#e74c3c">Top {data["ranking"]}</tspan>
  </text>
  <text x="20" y="120" font-family="Arial" font-size="14" fill="#ffffff">
    Acceptance Rate: <tspan fill="#3498db">{data["acceptanceRate"]}%</tspan>
  </text>
  
  <!-- Last Updated -->
  <text x="20" y="150" font-family="Arial" font-size="12" fill="#7d7d7d">
    Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
  </text>
</svg>
'''

# Save SVG
with open('stats.svg', 'w') as f:
    f.write(svg_template)
