"""
Underdog Fantasy scraper for player props using The Odds API.

Real API integration - no mock data needed!
"""

from typing import List, Dict, Any
from datetime import datetime
from utils.line_schema import create_line_schema
from market_odds.odds_api import OddsAPIClient


class UnderdogScraper:
    """Real Underdog Fantasy data scraper using The Odds API."""
    
    def __init__(self, api_key: str):
        """Initialize with API key."""
        self.client = OddsAPIClient(api_key)
        
    def scrape_underdog(self, sports: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get real player props from Underdog Fantasy via The Odds API.
        
        Args:
            sports: List of sports to scrape (defaults to active sports)
            
        Returns:
            List of betting lines in standardized format
        """
        if sports is None:
            sports = ['basketball_nba', 'americanfootball_nfl', 'baseball_mlb']
            
        all_lines = []
        
        for sport in sports:
            try:
                # Get Underdog odds for this sport
                odds_data = self.client.get_odds(
                    sport=sport,
                    regions='us_dfs',
                    bookmakers='underdog'
                )
                
                lines = self._parse_odds_to_lines(odds_data, sport)
                all_lines.extend(lines)
                
            except Exception as e:
                print(f"⚠️  Could not get {sport} from Underdog: {e}")
                continue
        
        return all_lines
    
    def _parse_odds_to_lines(self, odds_data: List[Dict], sport: str) -> List[Dict[str, Any]]:
        """Parse Odds API response into standardized line format."""
        lines = []
        
        for game in odds_data:
            event_name = f"{game.get('away_team')} @ {game.get('home_team')}"
            event_date = datetime.fromisoformat(game.get('commence_time', '').replace('Z', '+00:00'))
            
            for bookmaker in game.get('bookmakers', []):
                if bookmaker.get('key') != 'underdog':
                    continue
                    
                for market in bookmaker.get('markets', []):
                    market_key = market.get('key', '')
                    
                    # Parse player props markets
                    if 'player' in market_key:
                        lines.extend(self._parse_player_market(
                            market, event_name, event_date, sport
                        ))
        
        return lines
    
    def _parse_player_market(self, market: Dict, event_name: str, event_date: datetime, sport: str) -> List[Dict[str, Any]]:
        """Parse a player props market into standardized lines."""
        lines = []
        market_key = market.get('key', '')
        
        # Extract market type (points, rebounds, assists, etc.)
        market_type = market_key.replace('player_', '').replace('_alternate', '')
        
        for outcome in market.get('outcomes', []):
            player_name = outcome.get('name', '')
            odds = outcome.get('price', 0)
            line_value = outcome.get('point')
            description = outcome.get('description', '')
            
            # Determine over/under from description or default to over
            over_under = 'over'
            if 'under' in description.lower() or 'less' in description.lower():
                over_under = 'under'
            elif 'over' in description.lower() or 'more' in description.lower():
                over_under = 'over'
            
            if player_name and line_value is not None:
                line = create_line_schema(
                    sportsbook="Underdog",
                    sport=self._convert_sport_key(sport),
                    league=self._convert_sport_key(sport),
                    event_name=event_name,
                    player_name=player_name,
                    market_type=market_type,
                    line_value=float(line_value),
                    odds=odds,
                    over_under=over_under,
                    event_date=event_date
                )
                lines.append(line)
        
        return lines
    
    def _convert_sport_key(self, sport_key: str) -> str:
        """Convert API sport key to readable format."""
        mapping = {
            'basketball_nba': 'NBA',
            'americanfootball_nfl': 'NFL', 
            'baseball_mlb': 'MLB',
            'icehockey_nhl': 'NHL'
        }
        return mapping.get(sport_key, sport_key.upper())


# Convenience functions
def scrape_underdog() -> List[Dict[str, Any]]:
    """
    Scrape player props from Underdog Fantasy using real API data.
    
    Returns:
        List of betting lines in standardized format
    """
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    scraper = UnderdogScraper(api_key)
    return scraper.scrape_underdog()


# Example usage and testing
if __name__ == "__main__":
    print("=== Underdog Fantasy Real API Scraper Test ===")
    
    # Test scraping with real data
    lines = scrape_underdog()
    print(f"✅ Scraped {len(lines)} REAL lines from Underdog")
    
    # Show sample lines
    print("\nSample real lines:")
    for i, line in enumerate(lines[:5], 1):
        print(f"{i}. {line['player_name']} - {line['market_type']} {line['over_under']} {line['line_value']}")
        print(f"   Odds: {line['odds']} | Event: {line['event_name']}")
    
    print(f"\n🎯 REAL Underdog API scraper working!") 