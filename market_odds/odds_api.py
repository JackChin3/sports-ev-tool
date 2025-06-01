"""
Market odds integration using The Odds API.

This module fetches market odds from major sportsbooks via The Odds API
to provide fair market prices for EV calculation.
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import time


class OddsAPIClient:
    """Client for The Odds API to fetch market odds data."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Odds API client.
        
        Args:
            api_key: Your API key from https://the-odds-api.com/
        """
        self.api_key = api_key
        self.base_url = "https://api.the-odds-api.com/v4"
        self.session = requests.Session()
        
    def get_sports(self) -> List[Dict[str, Any]]:
        """
        Get list of available sports.
        
        Returns:
            List of available sports with their keys and details
        """
        url = f"{self.base_url}/sports"
        params = {
            "apiKey": self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sports: {e}")
            return []
    
    def get_odds(
        self, 
        sport: str, 
        regions: str = "us",
        markets: str = "h2h,spreads,totals",
        oddsFormat: str = "american",
        bookmakers: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get odds for a specific sport.
        
        Args:
            sport: Sport key (e.g., 'americanfootball_nfl', 'basketball_nba')
            regions: Regions to get odds for ('us', 'uk', 'eu', 'au')
            markets: Markets to get odds for ('h2h', 'spreads', 'totals')
            oddsFormat: Format for odds ('american', 'decimal')
            bookmakers: Specific bookmakers to include (optional)
            
        Returns:
            List of games with odds from various bookmakers
        """
        url = f"{self.base_url}/sports/{sport}/odds"
        params = {
            "apiKey": self.api_key,
            "regions": regions,
            "markets": markets,
            "oddsFormat": oddsFormat,
            "dateFormat": "iso"
        }
        
        if bookmakers:
            params["bookmakers"] = bookmakers
            
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching odds for {sport}: {e}")
            return []
    
    def get_player_props(
        self,
        sport: str,
        regions: str = "us",
        markets: str = "player_points,player_rebounds,player_assists",
        oddsFormat: str = "american"
    ) -> List[Dict[str, Any]]:
        """
        Get player prop odds for a specific sport.
        
        Args:
            sport: Sport key (e.g., 'basketball_nba')
            regions: Regions to get odds for
            markets: Player prop markets to get
            oddsFormat: Format for odds
            
        Returns:
            List of games with player prop odds
        """
        url = f"{self.base_url}/sports/{sport}/odds"
        params = {
            "apiKey": self.api_key,
            "regions": regions,
            "markets": markets,
            "oddsFormat": oddsFormat,
            "dateFormat": "iso"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching player props for {sport}: {e}")
            return []


def find_market_consensus(odds_data: List[Dict[str, Any]], target_market: str) -> Optional[float]:
    """
    Find consensus market odds for a specific market across bookmakers.
    
    Args:
        odds_data: Odds data from The Odds API
        target_market: Market to find consensus for ('h2h', 'spreads', 'totals')
        
    Returns:
        Consensus odds value (American format) or None if not found
    """
    all_odds = []
    
    for game in odds_data:
        for bookmaker in game.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market['key'] == target_market:
                    for outcome in market.get('outcomes', []):
                        all_odds.append(outcome['price'])
    
    if not all_odds:
        return None
    
    # Simple average for consensus (could be weighted by bookmaker reliability)
    return sum(all_odds) / len(all_odds)


def get_market_odds_for_player(
    api_client: OddsAPIClient,
    sport: str,
    player_name: str,
    market_type: str,
    line_value: float
) -> Optional[float]:
    """
    Get market consensus odds for a specific player prop.
    
    Args:
        api_client: Configured OddsAPIClient instance
        sport: Sport key
        player_name: Player name to find odds for
        market_type: Type of market ('points', 'rebounds', etc.)
        line_value: The line value to find odds for
        
    Returns:
        Market consensus odds or None if not found
    """
    # Map our internal market types to API market types
    market_mapping = {
        'points': 'player_points',
        'rebounds': 'player_rebounds', 
        'assists': 'player_assists',
        'touchdowns': 'player_touchdowns'
    }
    
    api_market = market_mapping.get(market_type.lower())
    if not api_market:
        print(f"Market type '{market_type}' not supported yet")
        return None
    
    try:
        odds_data = api_client.get_player_props(sport, markets=api_market)
        
        # Find matching player and line value
        for game in odds_data:
            for bookmaker in game.get('bookmakers', []):
                for market in bookmaker.get('markets', []):
                    if market['key'] == api_market:
                        for outcome in market.get('outcomes', []):
                            if (player_name.lower() in outcome.get('description', '').lower() and
                                outcome.get('point') == line_value):
                                return outcome['price']
        
        return None
        
    except Exception as e:
        print(f"Error getting market odds for {player_name}: {e}")
        return None


# Mock data for testing when API key is not available
def get_mock_market_odds(sport: str, player_name: str, market_type: str, line_value: float) -> float:
    """
    Generate mock market odds for testing purposes.
    
    This function provides realistic odds for testing when API access is unavailable.
    """
    import random
    
    # Generate realistic odds based on market type
    base_odds_ranges = {
        'points': (-120, +100),
        'rebounds': (-115, +105), 
        'assists': (-110, +110),
        'touchdowns': (+150, -180)
    }
    
    odds_range = base_odds_ranges.get(market_type.lower(), (-110, +110))
    return random.randint(odds_range[0], odds_range[1])


# Example usage and testing
if __name__ == "__main__":
    print("=== Odds API Integration Test ===")
    
    # Test with mock data (no API key required)
    print("\n--- Mock Data Test ---")
    mock_odds = get_mock_market_odds("NBA", "LeBron James", "points", 25.5)
    print(f"Mock market odds for LeBron James 25.5 points: {mock_odds}")
    
    # Test with real API (requires API key)
    print("\n--- Real API Test (requires API key) ---")
    print("To test with real API:")
    print("1. Get free API key from https://the-odds-api.com/")
    print("2. Set API_KEY environment variable")
    print("3. Uncomment and run the code below")
    
    # Uncomment to test with real API:
    # import os
    # api_key = os.getenv('ODDS_API_KEY')
    # if api_key:
    #     client = OddsAPIClient(api_key)
    #     sports = client.get_sports()
    #     print(f"Available sports: {len(sports)}")
    #     
    #     if sports:
    #         nba_odds = client.get_odds('basketball_nba')
    #         print(f"NBA games with odds: {len(nba_odds)}")
    # else:
    #     print("No API key found. Set ODDS_API_KEY environment variable.") 