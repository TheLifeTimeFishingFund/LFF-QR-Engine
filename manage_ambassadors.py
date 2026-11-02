import csv
import os

# Configuration Parameters
ENGINE_BASE_URL = "https://github.io"
GTAG_ID = "G-CVGCBXJ2L0"

# Experience Point (XP) Thresholds
TIER_1_MAX = 499
TIER_2_MAX = 999
TIER_3_MAX = 2499

def calculate_tier(xp):
    """Calculates active assignment boundaries based on user engagement metrics."""
    if xp <= TIER_1_MAX: 
        return 1
    elif xp <= TIER_2_MAX: 
        return 2
    elif xp <= TIER_3_MAX: 
        return 3
    else: 
        return 4

def generate_tiered_redirect(username, tier):
    """Creates an index page that bounces scanners to their unlocked dashboard configuration."""
    # Fixed the variable assignment and stitched the matching tier file pattern cleanly
    destination_url = f"{ENGINE_BASE_URL}/dashboards/tier{tier}.html?utm_source=lff_ambassador&utm_campaign={username}"
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://googletagmanager.com{GTAG_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GTAG_ID}');
  </script>

  <!-- Automated Routing Parameter -->
  <meta http-equiv="refresh" content="0; url={destination_url}">
</head>
<body>
</body>
</html>
"""
    return html_content


def process_roster(csv_path, output_dir):
    print("🎣 Executing LifeTime Fishing Fund Routing Compilation...")
    
    if not os.path.exists(csv_path):
        print(f"❌ Operational Failure: Cannot locate private database at {csv_path}")
        return

    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            username = row['username']
            tracking_id = row['tracking_id']
            xp = int(row['xp'])

            # Determine Tier Routing Assignment
            current_tier = calculate_tier(xp)
            print(f"👤 Mapping: {username} ({xp} XP) -> Accessing Tier {current_tier} via /{tracking_id}")

            # Compile individual meta-refresh script files
            html_blueprint = generate_tiered_redirect(username, current_tier)
            
            # Form clean subdirectory configurations inside the tracking engine space
            user_track_dir = os.path.join(output_dir, tracking_id)
            os.makedirs(user_track_dir, exist_ok=True)
            
            with open(os.path.join(user_track_dir, "index.html"), "w", encoding="utf-8") as out_file:
                out_file.write(html_blueprint)
                
    print("✅ Public routing profiles updated successfully!")

if __name__ == "__main__":
    # Point this to where the workflow will drop the temporary private spreadsheet file
    process_roster("ambassadors.csv", ".")
