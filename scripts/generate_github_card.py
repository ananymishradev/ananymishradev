import json
from datetime import datetime
from pathlib import Path

# Config
OUTPUT_DIR = Path("github_stats")
DATA_FILE = OUTPUT_DIR / "compiled.json"
SVG_FILE = OUTPUT_DIR / "github_card.svg"

# Design Config
COLORS = {
    "background": "#0d1117",
    "header": "#58a6ff",
    "text": "#c9d1d9",
    "secondary": "#8b949e",
    "accent": "#1f6feb",
    "success": "#2ea043",
    "warning": "#d29922",
    "danger": "#f85149"
}

# Load data with defaults
try:
    with open(DATA_FILE) as f:
        data = json.load(f)
except:
    data = {
        "profile": {
            "followers": 0,
            "following": 0,
            "public_repos": 0,
            "stars": 0,
            "created_at": "N/A",
            "company": "N/A",
            "location": "N/A"
        },
        "activity": {
            "yearly_contributions": 0,
            "last_active": "N/A"
        },
        "languages": {}
    }

# Calculate account age
account_age = "N/A"
if data["profile"]["created_at"] != "N/A":
    delta = datetime.now() - datetime.strptime(
        data["profile"]["created_at"], "%Y-%m-%dT%H:%M:%SZ"
    )
    years = delta.days // 365
    months = (delta.days % 365) // 30
    account_age = f"{years}y {months}m"

# Generate language bars
def generate_language_bars(languages):
    if not languages:
        return ""
    
    total = sum(languages.values())
    bars = []
    for i, (lang, count) in enumerate(sorted(
        languages.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:3]):  # Top 3 languages
        percent = (count / total) * 100
        bars.append(f"""
        <text x="20" y="{220 + i*25}" class="stat-label">
            {lang}: <tspan class="stat-value">{percent:.1f}%</tspan>
        </text>
        <rect x="120" y="{215 + i*25}" width="{percent*2.5}" height="10" 
              fill="{list(COLORS.values())[i+3]}" rx="2"/>
        """)
    return "\n".join(bars)

# SVG Template
svg = f"""
<svg width="540" height="320" xmlns="http://www.w3.org/2000/svg">
  <style>
    .background {{ fill: {COLORS["background"]}; }}
    .header {{ 
      font: bold 22px 'Segoe UI', Arial, sans-serif; 
      fill: {COLORS["header"]};
    }}
    .stat-label {{
      font: 14px 'Segoe UI', Arial, sans-serif;
      fill: {COLORS["secondary"]};
    }}
    .stat-value {{
      font: bold 14px 'Segoe UI', Arial, sans-serif;
      fill: {COLORS["text"]};
    }}
    .highlight {{ fill: {COLORS["accent"]}; }}
    .success {{ fill: {COLORS["success"]}; }}
    .grid {{ stroke: #30363d; stroke-width: 0.5; }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="5" class="background"/>

  <!-- Header -->
  <text x="20" y="40" class="header">GitHub Profile Overview</text>
  <line x1="20" x2="520" y1="50" y2="50" class="grid"/>

  <!-- Profile Section -->
  <text x="20" y="80" class="stat-label">Account:</text>
  <text x="100" y="80" class="stat-value">
    <tspan class="highlight">{account_age}</tspan> old • 
    <tspan class="success">{data["profile"]["public_repos"]} repos</tspan>
  </text>

  <!-- Social Stats -->
  <text x="20" y="110" class="stat-label">Community:</text>
  <text x="120" y="110" class="stat-value">
    <tspan class="highlight">👥 {data["profile"]["followers"]} followers</tspan> • 
    <tspan class="success">🤝 {data["profile"]["following"]} following</tspan> • 
    <tspan>⭐ {data["profile"]["stars"]} stars</tspan>
  </text>

  <!-- Activity -->
  <text x="20" y="140" class="stat-label">Activity:</text>
  <text x="100" y="140" class="stat-value">
    <tspan class="highlight">📌 {data["activity"]["yearly_contributions"]} commits (1y)</tspan> • 
    Last active: {data["activity"]["last_active"]}
  </text>

  <!-- Languages -->
  <text x="20" y="180" class="stat-label">Top Languages:</text>
  {generate_language_bars(data["languages"])}

  <!-- Footer -->
  <line x1="20" x2="520" y1="280" y2="280" class="grid"/>
  <text x="20" y="300" class="stat-label" font-size="12">
    Updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
  </text>
  <text x="400" y="300" class="stat-label" font-size="12">
    @{data["profile"]["username"]}
  </text>
</svg>
"""

# Save SVG
OUTPUT_DIR.mkdir(exist_ok=True)
with open(SVG_FILE, "w") as f:
    f.write(svg)
