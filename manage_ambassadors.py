import csv
import os

# =====================================================
# CONFIGURATION
# =====================================================

# GitHub Pages root for the repository
ENGINE_BASE_URL = "https://thelifetimefishingfund.github.io/LFF-QR-Engine"

# Google Analytics Measurement ID
GTAG_ID = "G-CVGCBXJ2L0"

# XP Thresholds
TIER_1_MAX = 499
TIER_2_MAX = 999
TIER_3_MAX = 2499


# =====================================================
# TIER CALCULATION
# =====================================================

def calculate_tier(xp):
    """Determine user tier based on XP."""

    if xp <= TIER_1_MAX:
        return 1
    elif xp <= TIER_2_MAX:
        return 2
    elif xp <= TIER_3_MAX:
        return 3
    else:
        return 4


# =====================================================
# HTML GENERATION
# =====================================================

def generate_tiered_redirect(username, tier):
    """
    Generate redirect page for a user's QR code.
    """

    destination_url = (
       
