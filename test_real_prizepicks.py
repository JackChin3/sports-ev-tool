"""
Test real PrizePicks data via The Odds API.

This eliminates the need for scraping entirely!
"""

from market_odds.odds_api import OddsAPIClient


def test_real_prizepicks_api():
    """Test getting real PrizePicks data via The Odds API."""
    
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    client = OddsAPIClient(api_key)
    
    print("🎯 TESTING REAL PRIZEPICKS DATA VIA API")
    print("=" * 50)
    
    try:
        # Test 1: Get PrizePicks NBA odds specifically  
        print("\n1️⃣ Getting PrizePicks NBA data...")
        nba_odds = client.get_odds(
            'basketball_nba', 
            regions='us_dfs', 
            bookmakers='prizepicks'
        )
        
        print(f"✅ PrizePicks NBA: {len(nba_odds)} games found")
        
        if nba_odds:
            print("\n📊 Sample PrizePicks data:")
            game = nba_odds[0]
            print(f"Game: {game.get('away_team')} @ {game.get('home_team')}")
            print(f"Start: {game.get('commence_time')}")
            
            for bookmaker in game.get('bookmakers', []):
                if bookmaker.get('key') == 'prizepicks':
                    print(f"\n✅ Found PrizePicks data!")
                    print(f"Bookmaker: {bookmaker.get('title')}")
                    print(f"Last updated: {bookmaker.get('last_update')}")
                    
                    for market in bookmaker.get('markets', []):
                        print(f"\n  Market: {market.get('key')}")
                        for outcome in market.get('outcomes', [])[:5]:
                            name = outcome.get('name', 'N/A')
                            price = outcome.get('price', 'N/A') 
                            point = outcome.get('point', 'N/A')
                            desc = outcome.get('description', 'N/A')
                            print(f"    {name}: {price} (line: {point}) - {desc}")
                    break
        else:
            print("⚠️  No PrizePicks NBA data available right now")
        
        # Test 2: Try other sports
        print(f"\n2️⃣ Testing other sports...")
        sports_to_try = ['americanfootball_nfl', 'baseball_mlb']
        
        for sport in sports_to_try:
            try:
                odds = client.get_odds(sport, regions='us_dfs', bookmakers='prizepicks')
                print(f"✅ {sport}: {len(odds)} games with PrizePicks data")
            except Exception as e:
                print(f"❌ {sport}: {e}")
        
        # Test 3: Get all DFS sites  
        print(f"\n3️⃣ Testing all DFS platforms...")
        try:
            all_dfs = client.get_odds('basketball_nba', regions='us_dfs')
            print(f"✅ All DFS platforms: {len(all_dfs)} games found")
            
            if all_dfs and all_dfs[0].get('bookmakers'):
                dfs_platforms = [bm.get('title') for bm in all_dfs[0]['bookmakers']]
                print(f"Available DFS platforms: {', '.join(dfs_platforms)}")
        except Exception as e:
            print(f"❌ DFS platforms error: {e}")
            
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False
    
    print(f"\n" + "=" * 50)
    print(f"🎯 CONCLUSION:")
    if nba_odds:
        print(f"✅ SUCCESS: Real PrizePicks data available via API!")
        print(f"✅ NO SCRAPING NEEDED!")
        print(f"✅ Can replace mock scraper with real API calls!")
    else:
        print(f"⚠️  PrizePicks data not available for current games")
        print(f"   (This could be timing - may be available during active seasons)")
    
    return len(nba_odds) > 0


if __name__ == "__main__":
    success = test_real_prizepicks_api()
    
    if success:
        print(f"\n🚀 NEXT STEP: Replace mock scraper with real PrizePicks API!")
        print(f"🚀 This will give us 100% real, live data!")
    else:
        print(f"\n📝 Keep mock scraper as fallback until PrizePicks season starts") 