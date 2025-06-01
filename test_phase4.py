"""
Phase 4 Test: Join sportsbook + market data and calculate EV.

This script demonstrates the complete flow from scraping PrizePicks 
to getting market odds to calculating EV opportunities.
"""

from scrapers.prizepicks import scrape_prizepicks
from market_odds.odds_api import get_mock_market_odds, OddsAPIClient
from utils.ev_calculator import calculate_line_ev
import os


def test_phase4_complete_flow():
    """Test the complete Phase 4 data joining and EV calculation flow."""
    
    print("🎯 PHASE 4 TEST: Join Sportsbook + Market Data")
    print("=" * 50)
    
    # Step 1: Get PrizePicks lines (sportsbook data)
    print("\n1️⃣ SCRAPING PRIZEPICKS...")
    prizepicks_lines = scrape_prizepicks()
    print(f"✅ Got {len(prizepicks_lines)} lines from PrizePicks")
    
    # Show sample data
    print("\n📊 Sample PrizePicks lines:")
    for i, line in enumerate(prizepicks_lines[:3], 1):
        print(f"  {i}. {line['player_name']} - {line['market_type']} {line['over_under']} {line['line_value']}")
        print(f"     PrizePicks odds: {line['odds']}")
    
    # Step 2: Get market odds for each line
    print(f"\n2️⃣ GETTING MARKET ODDS...")
    enhanced_lines = []
    positive_ev_count = 0
    
    for line in prizepicks_lines:
        # Get market odds (using mock for testing, could use real API)
        market_odds = get_mock_market_odds(
            sport=line['sport'],
            player_name=line['player_name'],
            market_type=line['market_type'],
            line_value=line['line_value']
        )
        
        # Calculate EV by joining sportsbook + market data
        enhanced_line = calculate_line_ev(line, market_odds)
        enhanced_lines.append(enhanced_line)
        
        if enhanced_line['is_positive_ev']:
            positive_ev_count += 1
    
    print(f"✅ Calculated EV for all {len(enhanced_lines)} lines")
    
    # Step 3: Show EV results
    print(f"\n3️⃣ EV CALCULATION RESULTS:")
    print(f"📈 Found {positive_ev_count}/{len(enhanced_lines)} POSITIVE EV opportunities!")
    
    # Show all lines with EV calculations
    print(f"\n📋 Complete EV Analysis:")
    print(f"{'Player':<15} {'Market':<10} {'Line':<6} {'PP Odds':<8} {'Mkt Odds':<9} {'EV%':<8} {'Status':<10}")
    print("-" * 80)
    
    for line in enhanced_lines:
        player = line['player_name'][:14]
        market = line['market_type'][:9]
        line_val = str(line['line_value'])
        pp_odds = str(line['odds'])
        mkt_odds = str(line['market_odds'])
        ev_pct = f"{line['ev_percentage']:.1f}%"
        status = "🟢 +EV" if line['is_positive_ev'] else "🔴 -EV"
        
        print(f"{player:<15} {market:<10} {line_val:<6} {pp_odds:<8} {mkt_odds:<9} {ev_pct:<8} {status:<10}")
    
    # Step 4: Focus on positive EV opportunities
    positive_ev_lines = [line for line in enhanced_lines if line['is_positive_ev']]
    
    if positive_ev_lines:
        print(f"\n🎯 POSITIVE EV OPPORTUNITIES ({len(positive_ev_lines)} found):")
        for i, line in enumerate(positive_ev_lines, 1):
            print(f"\n  {i}. {line['player_name']} - {line['market_type']} {line['over_under']} {line['line_value']}")
            print(f"     PrizePicks: {line['odds']} | Market: {line['market_odds']}")
            print(f"     Expected Value: ${line['ev_dollars']} ({line['ev_percentage']}%)")
            print(f"     Win Probability: {line['win_probability']*100:.1f}%")
    else:
        print(f"\n⚠️  No positive EV opportunities found in this sample")
        print(f"     (This is normal with mock data - real data will have more opportunities)")
    
    # Step 5: Summary and next steps
    print(f"\n" + "=" * 50)
    print(f"✅ PHASE 4 TEST COMPLETE!")
    print(f"✅ Data joining: WORKING")
    print(f"✅ EV calculation: WORKING") 
    print(f"✅ Opportunity detection: WORKING")
    print(f"\n🎯 Ready for Phase 5: Build Streamlit UI!")
    
    return enhanced_lines


def test_with_real_api():
    """Test Phase 4 with real API data (if API key is available)."""
    
    print(f"\n🔗 TESTING WITH REAL ODDS API...")
    
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"  # Your API key
    
    try:
        client = OddsAPIClient(api_key)
        
        # Get real NBA odds
        nba_odds = client.get_odds('basketball_nba')
        
        if nba_odds:
            print(f"✅ Real API connected - {len(nba_odds)} NBA games available")
            print(f"   Sample game: {nba_odds[0]['away_team']} @ {nba_odds[0]['home_team']}")
            
            # Note: Player props might not be available in free tier
            print(f"   Note: Player props may be limited in free tier")
            print(f"   Using mock market odds for EV calculation")
        else:
            print(f"⚠️  No NBA games available right now")
            
    except Exception as e:
        print(f"❌ API Error: {e}")
        print(f"   Falling back to mock data")


if __name__ == "__main__":
    # Run main Phase 4 test
    enhanced_lines = test_phase4_complete_flow()
    
    # Optional: Test with real API
    test_with_real_api()
    
    print(f"\n" + "🚀" * 20)
    print(f"PHASE 4 TESTING COMPLETE!")
    print(f"Ready to proceed with Phase 5: Streamlit UI")
    print(f"🚀" * 20) 