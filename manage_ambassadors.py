import csv
import os

# 1. Target URL Configurations
# Replace this with your true live website branch or main site url later
MAIN_FUND_SITE = "https://your-main-fund-site.org" 
GTAG_ID = "G-CVGCBXJ2L0"

# Experience Point (XP) Thresholds
TIER_1_MAX = 499
TIER_2_MAX = 999
TIER_3_MAX = 2499

def calculate_tier(xp):
    if xp <= TIER_1_MAX: return 1
    elif xp <= TIER_2_MAX: return 2
    elif xp <= TIER_3_MAX: return 3
    else: return 4

def generate_redirect_html(username):
    """Creates the mobile tracker template that fires Google Analytics and jumps to your site."""
    destination_url = f"{MAIN_FUND_SITE}?utm_source=ambassador&utm_medium=mobile_qr&utm_campaign={username}"
    
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

  <!-- Redirect mapping tracking campaign data directly to your real domain -->
  <meta http-equiv="refresh" content="0; url={destination_url}">
</head>
<body>
</body>
</html>
"""
    return html_content

def process_roster(csv_path, public_engine_dir):
    print("🎣 Running LFF Operations Sync...")
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: Private roster missing at: {csv_path}")
        return

    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            username = row['username']
            tracking_id = row['tracking_id']
            xp = int(row['xp'])

            tier = calculate_tier(xp)
            print(f"👤 Syncing: {username} (Tier {tier}) -> Track Route: /{tracking_id}")

            # Build the custom mobile tracker text block
            html_blueprint = generate_redirect_html(username)
            
            # Map directly into the path structure for your tracking engine
            user_track_dir = os.path.join(public_engine_dir, tracking_id)
            os.makedirs(user_track_dir, exist_ok=True)
            
            with open(os.path.join(user_track_dir, "index.html"), "w", encoding="utf-8") as out_file:
                out_file.write(html_blueprint)
                
    print("✅ Public tracker routes successfully compiled!")

if __name__ == "__main__":
    # Point this directly to where you have cloned your local public LFF-QR-Engine folder
    # Example relative setup assumes they live side-by-side in your workspace
    PUBLIC_ENGINE_PATH = "../LFF-QR-Engine" 
    
    process_roster("data/ambassadors.csv", PUBLIC_ENGINE_PATH)
