"""
PrizePicks scraper for player props.

Starting with mock data as per MVP plan, will replace with real scraping later.
"""

from typing import List, Dict, Any
from datetime import datetime
from utils.line_schema import create_line_schema


def scrape_prizepicks() -> List[Dict[str, Any]]:
    """
    Scrape player props from PrizePicks.
    
    Currently returns mock data for testing. Will be replaced with real scraping.
    
    Returns:
        List of betting lines in standardized format
    """
    # Mock PrizePicks data for testing
    mock_props = [
        {
            "player": "LeBron James",
            "market": "points", 
            "line": 25.5,
            "odds": -110,
            "sport": "NBA",
            "event": "Lakers vs Warriors"
        },
        {
            "player": "Stephen Curry",
            "market": "points",
            "line": 28.5, 
            "odds": -105,
            "sport": "NBA",
            "event": "Lakers vs Warriors"
        },
        {
            "player": "Anthony Davis",
            "market": "rebounds",
            "line": 11.5,
            "odds": -115,
            "sport": "NBA", 
            "event": "Lakers vs Warriors"
        },
        {
            "player": "LeBron James",
            "market": "assists",
            "line": 7.5,
            "odds": +100,
            "sport": "NBA",
            "event": "Lakers vs Warriors"
        },
        {
            "player": "Draymond Green", 
            "market": "rebounds",
            "line": 8.5,
            "odds": -120,
            "sport": "NBA",
            "event": "Lakers vs Warriors"
        }
    ]
    
    # Convert to standardized format
    standardized_lines = []
    
    for prop in mock_props:
        line = create_line_schema(
            sportsbook="PrizePicks",
            sport=prop["sport"],
            league=prop["sport"],  # Using sport as league for now
            event_name=prop["event"],
            player_name=prop["player"],
            market_type=prop["market"],
            line_value=prop["line"],
            odds=prop["odds"],
            over_under="over",  # PrizePicks is typically "more/less" which maps to over/under
            event_date=datetime.now()  # Mock date for testing
        )
        standardized_lines.append(line)
    
    return standardized_lines


def get_available_sports() -> List[str]:
    """
    Get list of sports available on PrizePicks.
    
    Returns:
        List of sport names
    """
    return ["NBA", "NFL", "MLB", "NHL"]  # Mock data


# Example usage and testing
if __name__ == "__main__":
    print("=== PrizePicks Scraper Test ===")
    
    # Test scraping
    lines = scrape_prizepicks()
    print(f"✅ Scraped {len(lines)} lines from PrizePicks")
    
    # Show sample lines
    print("\nSample lines:")
    for i, line in enumerate(lines[:3], 1):
        print(f"{i}. {line['player_name']} - {line['market_type']} {line['over_under']} {line['line_value']}")
        print(f"   Odds: {line['odds']} | ID: {line['unique_id']}")
    
    # Test sports
    sports = get_available_sports()
    print(f"\n✅ Available sports: {', '.join(sports)}")
    
    print(f"\n🎯 Mock PrizePicks scraper working! Ready for integration.") 