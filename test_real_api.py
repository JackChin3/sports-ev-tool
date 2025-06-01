"""
Test script for real Odds API integration.
"""

import os
from market_odds.odds_api import OddsAPIClient, get_mock_market_odds

def test_real_api():
    """Test the real Odds API with the provided key."""
    
    # Set API key
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    
    print("=== Testing Real Odds API ===")
    print(f"API Key: {api_key[:8]}...")
    
    try:
        client = OddsAPIClient(api_key)
        
        # Test 1: Get available sports
        print("\n1. Getting available sports...")
        sports = client.get_sports()
        print(f"✅ Found {len(sports)} sports available")
        
        if sports:
            print("Available sports (first 5):")
            for sport in sports[:5]:
                print(f"  - {sport.get('key')}: {sport.get('title')}")
        
            # Test 2: Get NBA odds
            print("\n2. Testing NBA odds...")
            nba_odds = client.get_odds('basketball_nba')
            print(f"✅ Found {len(nba_odds)} NBA games with odds")
            
            if nba_odds:
                game = nba_odds[0]
                print(f"Sample game: {game.get('away_team')} @ {game.get('home_team')}")
                print(f"Start time: {game.get('commence_time')}")
                print(f"Bookmakers: {len(game.get('bookmakers', []))}")
                
                # Show first bookmaker's odds
                if game.get('bookmakers'):
                    bookmaker = game['bookmakers'][0]
                    print(f"Sample odds from {bookmaker.get('title')}:")
                    for market in bookmaker.get('markets', [])[:2]:
                        print(f"  Market: {market.get('key')}")
                        for outcome in market.get('outcomes', [])[:2]:
                            print(f"    {outcome.get('name')}: {outcome.get('price')}")
            
            # Test 3: Try player props (if available)
            print("\n3. Testing NBA player props...")
            props = client.get_player_props('basketball_nba')
            print(f"✅ Found {len(props)} NBA games with player props")
            
            if props:
                print("Player props are available!")
                prop_game = props[0]
                if prop_game.get('bookmakers'):
                    prop_book = prop_game['bookmakers'][0]
                    print(f"Sample props from {prop_book.get('title')}:")
                    for market in prop_book.get('markets', [])[:1]:
                        print(f"  Market: {market.get('key')}")
                        for outcome in market.get('outcomes', [])[:3]:
                            desc = outcome.get('description', 'N/A')
                            price = outcome.get('price', 'N/A')
                            point = outcome.get('point', 'N/A')
                            print(f"    {desc}: {price} (line: {point})")
            
        print("\n=== API Test Summary ===")
        print("✅ API connection: SUCCESS")
        print("✅ Sports data: SUCCESS") 
        print("✅ Game odds: SUCCESS")
        print("✅ Player props: SUCCESS" if props else "⚠️  Player props: LIMITED/UNAVAILABLE")
        
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False


if __name__ == "__main__":
    success = test_real_api()
    if success:
        print("\n🎯 Ready to integrate with EV calculator!")
    else:
        print("\n⚠️  Will fall back to mock data for testing") 