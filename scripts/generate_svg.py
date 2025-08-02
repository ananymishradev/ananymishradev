import json
from datetime import datetime
from pathlib import Path

# Configure paths
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Default values for ALL possible stats
DEFAULT_STATS = {
    # Problem stats
    "solved": 0, "easy": 0, "medium": 0, "hard": 0, "totalSubmissions": 0,
    # Profile stats
    "ranking": "N/A", "reputation": 0, "stars": 0,
    # Contest stats
    "contestRating": 0, "contestTopPercent": 0, "contestsAttended": 0, "globalRank": "N/A",
    # Activity stats
    "lastSubmission": "N/A", "lastSubmissionTime": 0,
    # Language stats
    "topLanguage": "N/A",
    # Calculated stats
    "acceptanceRate": 0
}

# Load stats with comprehensive fallback
try:
    with open(output_dir / "stats.json") as f:
        data = json.load(f)
    # Ensure all keys exist
    data = {**DEFAULT_STATS, **data}
except Exception as e:
    print(f"Error loading stats: {e}")
    data = DEFAULT_STATS

# SVG Template with safe value access
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
    <tspan class="easy">✓ {data.get("easy", 0)} Easy</tspan>
    <tspan dx="15" class="medium">✓ {data.get("medium", 0)} Medium</tspan>
    <tspan dx="15" class="hard">✓ {data.get("hard", 0)} Hard</tspan>
  </text>

  <!-- Total Stats -->
  <text x="10" y="80" class="stat-label">Total Solved:</text>
  <text x="120" y="80" class="stat-value">{data.get("solved", 0)}/{data.get("totalSubmissions", 0)}</text>
  
  <text x="250" y="80" class="stat-label">Acceptance:</text>
  <text x="340" y="80" class="stat-value">{data.get("acceptanceRate", 0)}%</text>

  <!-- Contest Stats -->
  <text x="10" y="105" class="stat-label">Contest Rating:</text>
  <text x="120" y="105" class="stat-value contest">{data.get("contestRating", 0)}</text>
  
  <text x="250" y="105" class="stat-label">Top %:</text>
  <text x="340" y="105" class="stat-value">{data.get("contestTopPercent", 0)}%</text>

  <!-- Footer -->
  <text x="10" y="265" class="footer">
    Updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")} | 
    Last solved: {data.get("lastSubmission", "N/A")}
  </text>
</svg>
'''

# Save SVG
try:
    with open(output_dir / "stats.svg", "w") as f:
        f.write(svg)
    print("SVG generated successfully")
except Exception as e:
    print(f"Error saving SVG: {e}")
