import json
from datetime import datetime
from pathlib import Path
import math

# Configuration
OUTPUT_DIR = Path("outputs/stats")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Color Scheme
COLORS = {
    "background": "#0d1117",
    "header": "#58a6ff",
    "text": "#c9d1d9",
    "secondary": "#8b949e",
    "accent": "#1f6feb",
    "success": "#2ea043",
    "danger": "#f85149",
    "warning": "#d29922"
}

# Default data
DEFAULT_DATA = {
    "profile": {
        "followers": 0,
        "following": 0,
        "repos": 0,
        "stars": 0,
        "created_at": "N/A",
        "company": "N/A",
        "location": "N/A"
    },
    "activity": {
        "contributions": 0,
        "streak": 0,
        "last_contribution": "N/A"
    },
    "repositories": {
        "top_language": "N/A",
        "language_distribution": {},
        "total_commits": 0,
        "total_prs": 0,
        "total_issues": 0
    }
}

def load_data():
    """Load and merge GitHub data with defaults"""
    try:
        with open(OUTPUT_DIR / "github.json") as f:
            data = json.load(f)
        
        # Deep merge with defaults
        def merge(dict1, dict2):
            for key, value in dict2.items():
                if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                    merge(dict1[key], value)
                else:
                    dict1[key] = dict1.get(key, value)
            return dict1
        
        return merge(DEFAULT_DATA, data)
    except Exception as e:
        print(f"Error loading data: {e}")
        return DEFAULT_DATA

def format_date(date_str):
    """Format ISO date to readable format"""
    if date_str == "N/A":
        return date_str
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%b %d, %Y")
    except:
        return date_str

def create_language_chart(languages):
    """Generate SVG language distribution chart"""
    if not languages or languages.get("N/A"):
        return ""
    
    total = sum(languages.values())
    chart_width = 350
    current_x = 0
    
    # Sort languages by percentage
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    
    # Generate SVG rectangles
    rects = []
    for i, (lang, count) in enumerate(sorted_langs[:5]):  # Top 5 languages
        percentage = count / total
        width = math.ceil(chart_width * percentage)
        
        # Different colors for each language
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
        color = colors[i] if i < len(colors) else "#8c564b"
        
        rects.append(
            f'<rect x="{current_x}" y="0" width="{width}" height="8" fill="{color}" '
            f'rx="2" ry="2" data-tooltip="{lang}: {percentage:.1%}"/>'
        )
        current_x += width
    
    return f'''
    <svg width="{chart_width}" height="10" viewBox="0 0 {chart_width} 10">
        {"".join(rects)}
    </svg>
    '''

def generate_svg(data):
    """Generate complete GitHub stats SVG"""
    # Calculate account age
    created_at = format_date(data["profile"]["created_at"])
    account_age = "N/A"
    if created_at != "N/A":
        delta = datetime.now() - datetime.strptime(data["profile"]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        account_age = f"{delta.days // 365} years, {(delta.days % 365) // 30} months"
    
    # Generate language chart
    language_chart = create_language_chart(data["repositories"]["language_distribution"])
    
    return f'''
<svg width="540" height="320" xmlns="http://www.w3.org/2000/svg">
  <style>
    /* Base styles */
    .background {{ fill: {COLORS["background"]}; }}
    .header {{ font: bold 20px 'Segoe UI', Arial, sans-serif; fill: {COLORS["header"]}; }}
    .stat-label {{ font: 14px 'Segoe UI', Arial, sans-serif; fill: {COLORS["secondary"]}; }}
    .stat-value {{ font: bold 14px 'Segoe UI', Arial, sans-serif; fill: {COLORS["text"]}; }}
    .accent {{ fill: {COLORS["accent"]}; }}
    .success {{ fill: {COLORS["success"]}; }}
    .warning {{ fill: {COLORS["warning"]}; }}
    .danger {{ fill: {COLORS["danger"]}; }}
    .grid {{ stroke: #30363d; stroke-width: 0.5; }}
    
    /* Tooltip styles */
    .tooltip-box {{
      fill: #161b22;
      stroke: #30363d;
      stroke-width: 1;
      opacity: 0.9;
    }}
    .tooltip-text {{
      font: 12px 'Segoe UI', Arial;
      fill: #f0f6fc;
    }}
  </style>
  
  <!-- Background -->
  <rect width="100%" height="100%" rx="5" class="background"/>
  
  <!-- Header -->
  <text x="20" y="35" class="header">GitHub Profile Stats</text>
  <line x1="20" x2="520" y1="45" y2="45" class="grid"/>
  
  <!-- Profile Section -->
  <text x="20" y="75" class="stat-label">Profile:</text>
  <text x="100" y="75" class="stat-value">
    <tspan class="accent">👥 {data["profile"]["followers"]} followers</tspan>
    <tspan dx="15">•</tspan>
    <tspan dx="15">🤝 {data["profile"]["following"]} following</tspan>
    <tspan dx="15">•</tspan>
    <tspan dx="15">📅 {account_age}</tspan>
  </text>
  
  <!-- Repositories Section -->
  <text x="20" y="105" class="stat-label">Repositories:</text>
  <text x="120" y="105" class="stat-value">
    <tspan class="success">📦 {data["profile"]["repos"]} public</tspan>
    <tspan dx="15">•</tspan>
    <tspan dx="15">⭐ {data["profile"]["stars"]} stars</tspan>
  </text>
  
  <!-- Language Distribution -->
  <text x="20" y="135" class="stat-label">Top Language:</text>
  <text x="120" y="135" class="stat-value accent">{data["repositories"]["top_language"]}</text>
  
  <foreignObject x="20" y="150" width="350" height="20">
    {language_chart}
  </foreignObject>
  
  <!-- Activity Section -->
  <text x="20" y="190" class="stat-label">Activity:</text>
  <text x="100" y="190" class="stat-value">
    <tspan class="success">📌 {data["activity"]["contributions"]} contributions</tspan>
    <tspan dx="15">•</tspan>
    <tspan dx="15">🔥 {data["activity"]["streak"]} day streak</tspan>
  </text>
  
  <text x="20" y="220" class="stat-label">Last Contribution:</text>
  <text x="150" y="220" class="stat-value">{format_date(data["activity"]["last_contribution"])}</text>
  
  <!-- Repository Stats -->
  <text x="20" y="250" class="stat-label">Repository Stats:</text>
  <text x="150" y="250" class="stat-value">
    <tspan>📝 {data["repositories"]["total_commits"]} commits</tspan>
    <tspan dx="15">•</tspan>
    <tspan dx="15">🔀 {data["repositories"]["total_prs"]} PRs</tspan>
    <tspan dx="15">•</tspan>
    <tspan dx="15">🐛 {data["repositories"]["total_issues"]} issues</tspan>
  </text>
  
  <!-- Footer -->
  <line x1="20" x2="520" y1="275" y2="275" class="grid"/>
  <text x="20" y="295" class="stat-label" font-size="12">
    Updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
  </text>
  <text x="400" y="295" class="stat-label" font-size="12">
    GitHub: @ananymishradev
  </text>
  
  <!-- Tooltip container (for hover effects) -->
  <rect width="100%" height="100%" fill="transparent">
    <title>GitHub Profile Statistics</title>
  </rect>
</svg>
'''

def main():
    data = load_data()
    svg_content = generate_svg(data)
    
    try:
        with open(OUTPUT_DIR / "github.svg", "w") as f:
            f.write(svg_content)
        print("GitHub stats SVG generated successfully")
    except Exception as e:
        print(f"Error saving SVG: {e}")

if __name__ == "__main__":
    main()
