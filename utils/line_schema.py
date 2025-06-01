"""
Standardized data schema for sportsbook lines.

This module defines the common data structure that all scrapers should use
to ensure consistency across different sportsbooks.
"""

from typing import Dict, Any, Optional
from datetime import datetime


def create_line_schema(
    sportsbook: str,
    sport: str,
    league: str,
    event_name: str,
    player_name: str,
    market_type: str,
    line_value: float,
    odds: float,
    over_under: str,
    event_date: datetime,
    scraped_at: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Create a standardized line object.
    
    Args:
        sportsbook: Name of the sportsbook (e.g., "PrizePicks", "Underdog", "Fliff")
        sport: Sport category (e.g., "NBA", "NFL", "MLB")
        league: League name (e.g., "NBA", "NFL", "Premier League")
        event_name: Game/match description (e.g., "Lakers vs Warriors")
        player_name: Player name for player props (e.g., "LeBron James")
        market_type: Type of bet (e.g., "points", "rebounds", "touchdowns")
        line_value: The betting line number (e.g., 25.5 points)
        odds: Decimal odds (e.g., -110 American becomes 1.91 decimal)
        over_under: Either "over" or "under"
        event_date: When the game/event takes place
        scraped_at: When this data was scraped (defaults to now)
    
    Returns:
        Standardized dictionary representing a betting line
    """
    if scraped_at is None:
        scraped_at = datetime.now()
    
    return {
        "sportsbook": sportsbook,
        "sport": sport,
        "league": league,
        "event_name": event_name,
        "player_name": player_name,
        "market_type": market_type,
        "line_value": line_value,
        "odds": odds,
        "over_under": over_under.lower(),
        "event_date": event_date.isoformat() if isinstance(event_date, datetime) else event_date,
        "scraped_at": scraped_at.isoformat() if isinstance(scraped_at, datetime) else scraped_at,
        "unique_id": f"{sportsbook}_{sport}_{player_name}_{market_type}_{line_value}_{over_under}".replace(" ", "_").lower()
    }


def validate_line_schema(line_data: Dict[str, Any]) -> bool:
    """
    Validate that a line object contains all required fields.
    
    Args:
        line_data: Dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "sportsbook", "sport", "league", "event_name", "player_name",
        "market_type", "line_value", "odds", "over_under", "event_date",
        "scraped_at", "unique_id"
    ]
    
    # Check all required fields exist
    for field in required_fields:
        if field not in line_data:
            return False
    
    # Check data types
    if not isinstance(line_data["line_value"], (int, float)):
        return False
    
    if not isinstance(line_data["odds"], (int, float)):
        return False
    
    if line_data["over_under"].lower() not in ["over", "under"]:
        return False
    
    return True


# Example usage for testing
if __name__ == "__main__":
    # Create a sample line
    sample_line = create_line_schema(
        sportsbook="PrizePicks",
        sport="NBA",
        league="NBA",
        event_name="Lakers vs Warriors",
        player_name="LeBron James",
        market_type="points",
        line_value=25.5,
        odds=-110,
        over_under="over",
        event_date=datetime(2024, 1, 15, 20, 0)
    )
    
    print("Sample line schema:")
    for key, value in sample_line.items():
        print(f"  {key}: {value}")
    
    print(f"\nValidation result: {validate_line_schema(sample_line)}") 