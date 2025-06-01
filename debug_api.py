"""
Debug script to see what data is available from PrizePicks API.
"""

from market_odds.odds_api import OddsAPIClient
import json

def debug_prizepicks_api():
    """Debug what's available from PrizePicks API."""
    
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    client = OddsAPIClient(api_key)
    
    print("🔍 DEBUGGING PRIZEPICKS API")
    print("=" * 40)
    
    # Test 1: Get all available markets for NBA
    print("\n1️⃣ Testing NBA without market filter...")
    try:
        data = client.get_odds('basketball_nba', regions='us_dfs', bookmakers='prizepicks')
        print(f"✅ Found {len(data)} NBA games")
        
        if data:
            game = data[0]
            print(f"\nGame: {game.get('away_team')} @ {game.get('home_team')}")
            print(f"Start: {game.get('commence_time')}")
            
            for bookmaker in game.get('bookmakers', []):
                if bookmaker.get('key') == 'prizepicks':
                    print(f"\n✅ PrizePicks bookmaker found!")
                    print(f"Title: {bookmaker.get('title')}")
                    print(f"Markets: {len(bookmaker.get('markets', []))}")
                    
                    for market in bookmaker.get('markets', []):
                        print(f"\n  📊 Market: {market.get('key')}")
                        print(f"      Outcomes: {len(market.get('outcomes', []))}")
                        
                        # Show first few outcomes
                        for i, outcome in enumerate(market.get('outcomes', [])[:3]):
                            print(f"        {i+1}. {outcome}")
                            
                    break
            else:
                print("❌ No PrizePicks bookmaker found in response")
                print("Available bookmakers:", [bm.get('key') for bm in game.get('bookmakers', [])])
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Try different sports
    print(f"\n2️⃣ Testing other sports...")
    sports_to_test = ['americanfootball_nfl', 'baseball_mlb']
    
    for sport in sports_to_test:
        try:
            data = client.get_odds(sport, regions='us_dfs', bookmakers='prizepicks')
            prizepicks_games = 0
            
            for game in data:
                for bm in game.get('bookmakers', []):
                    if bm.get('key') == 'prizepicks':
                        prizepicks_games += 1
                        break
            
            print(f"✅ {sport}: {len(data)} total games, {prizepicks_games} with PrizePicks")
            
        except Exception as e:
            print(f"❌ {sport}: {e}")
    
    # Test 3: Try all DFS bookmakers to see what's available
    print(f"\n3️⃣ Testing all DFS bookmakers...")
    try:
        data = client.get_odds('basketball_nba', regions='us_dfs')
        print(f"✅ Found {len(data)} games from all DFS sites")
        
        if data:
            all_bookmakers = set()
            for game in data:
                for bm in game.get('bookmakers', []):
                    all_bookmakers.add(bm.get('key'))
            
            print(f"Available DFS bookmakers: {list(all_bookmakers)}")
            
            # Show sample data from first available DFS bookmaker
            for game in data:
                for bm in game.get('bookmakers', []):
                    if bm.get('key') in all_bookmakers:
                        print(f"\nSample from {bm.get('title')}:")
                        for market in bm.get('markets', [])[:2]:
                            print(f"  Market: {market.get('key')}")
                            for outcome in market.get('outcomes', [])[:2]:
                                print(f"    {outcome}")
                        break
                break
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    debug_prizepicks_api() 