"""
Expected Value (EV) calculator for sports betting lines.

This module calculates the expected value of betting lines by comparing
sportsbook odds to fair market odds.
"""

from typing import Dict, Any, Optional


def american_to_decimal(american_odds: float) -> float:
    """
    Convert American odds to decimal odds.
    
    Args:
        american_odds: American odds (e.g., -110, +150)
        
    Returns:
        Decimal odds (e.g., 1.91, 2.50)
    """
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1


def decimal_to_probability(decimal_odds: float) -> float:
    """
    Convert decimal odds to implied probability.
    
    Args:
        decimal_odds: Decimal odds (e.g., 1.91, 2.50)
        
    Returns:
        Implied probability as a decimal (e.g., 0.524, 0.40)
    """
    return 1 / decimal_odds


def calculate_ev(
    sportsbook_odds: float,
    market_odds: float,
    bet_amount: float = 100.0,
    odds_format: str = "american"
) -> Dict[str, float]:
    """
    Calculate expected value of a betting line.
    
    Args:
        sportsbook_odds: Odds offered by the sportsbook
        market_odds: Fair market odds for comparison
        bet_amount: Amount to bet (default $100)
        odds_format: Format of odds ("american" or "decimal")
        
    Returns:
        Dictionary containing EV calculations:
        - ev_dollars: Expected value in dollars
        - ev_percentage: Expected value as percentage
        - win_probability: Market implied probability of winning
        - payout_if_win: Payout if bet wins
        - breakeven_probability: Probability needed to break even
    """
    # Convert to decimal odds if needed
    if odds_format == "american":
        sportsbook_decimal = american_to_decimal(sportsbook_odds)
        market_decimal = american_to_decimal(market_odds)
    else:
        sportsbook_decimal = sportsbook_odds
        market_decimal = market_odds
    
    # Calculate probabilities
    market_probability = decimal_to_probability(market_decimal)
    breakeven_probability = decimal_to_probability(sportsbook_decimal)
    
    # Calculate potential payout
    payout_if_win = bet_amount * sportsbook_decimal
    profit_if_win = payout_if_win - bet_amount
    
    # Calculate expected value
    ev_dollars = (market_probability * profit_if_win) - ((1 - market_probability) * bet_amount)
    ev_percentage = (ev_dollars / bet_amount) * 100
    
    return {
        "ev_dollars": round(ev_dollars, 2),
        "ev_percentage": round(ev_percentage, 2),
        "win_probability": round(market_probability, 4),
        "payout_if_win": round(payout_if_win, 2),
        "breakeven_probability": round(breakeven_probability, 4),
        "sportsbook_decimal_odds": round(sportsbook_decimal, 3),
        "market_decimal_odds": round(market_decimal, 3)
    }


def is_positive_ev(
    sportsbook_odds: float,
    market_odds: float,
    min_ev_threshold: float = 0.0,
    odds_format: str = "american"
) -> bool:
    """
    Check if a betting line has positive expected value above threshold.
    
    Args:
        sportsbook_odds: Odds offered by the sportsbook
        market_odds: Fair market odds for comparison
        min_ev_threshold: Minimum EV percentage required (default 0%)
        odds_format: Format of odds ("american" or "decimal")
        
    Returns:
        True if EV is above threshold, False otherwise
    """
    ev_result = calculate_ev(sportsbook_odds, market_odds, odds_format=odds_format)
    return ev_result["ev_percentage"] > min_ev_threshold


def calculate_line_ev(line_data: Dict[str, Any], market_odds: float) -> Dict[str, Any]:
    """
    Calculate EV for a betting line using the standardized line schema.
    
    Args:
        line_data: Betting line in standardized format (from line_schema.py)
        market_odds: Market odds for comparison
        
    Returns:
        Original line data enhanced with EV calculations
    """
    # Calculate EV using the line's odds
    ev_result = calculate_ev(
        sportsbook_odds=line_data["odds"],
        market_odds=market_odds,
        odds_format="american"
    )
    
    # Add EV data to the line
    enhanced_line = line_data.copy()
    enhanced_line.update({
        "market_odds": market_odds,
        "ev_dollars": ev_result["ev_dollars"],
        "ev_percentage": ev_result["ev_percentage"],
        "win_probability": ev_result["win_probability"],
        "payout_if_win": ev_result["payout_if_win"],
        "is_positive_ev": ev_result["ev_percentage"] > 0
    })
    
    return enhanced_line


# Example usage and testing
if __name__ == "__main__":
    # Test EV calculation
    print("=== EV Calculator Test ===")
    
    # Example: Sportsbook has -110, market suggests it should be +100 (better odds)
    sportsbook_odds = -110  # Paying less (worse for bettor)
    market_odds = +100      # Fair odds suggest this should pay more
    
    ev_result = calculate_ev(sportsbook_odds, market_odds)
    
    print(f"Sportsbook odds: {sportsbook_odds}")
    print(f"Market odds: {market_odds}")
    print(f"Expected Value: ${ev_result['ev_dollars']} ({ev_result['ev_percentage']}%)")
    print(f"Win probability: {ev_result['win_probability']*100}%")
    print(f"Positive EV?: {is_positive_ev(sportsbook_odds, market_odds)}")
    
    print("\n=== Line Schema Integration Test ===")
    
    # Test with line schema format
    from line_schema import create_line_schema
    from datetime import datetime
    
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
    
    enhanced_line = calculate_line_ev(sample_line, market_odds=+120)
    
    print(f"Player: {enhanced_line['player_name']}")
    print(f"Market: {enhanced_line['market_type']} {enhanced_line['over_under']} {enhanced_line['line_value']}")
    print(f"Sportsbook odds: {enhanced_line['odds']}")
    print(f"Market odds: {enhanced_line['market_odds']}")
    print(f"EV: ${enhanced_line['ev_dollars']} ({enhanced_line['ev_percentage']}%)")
    print(f"Positive EV?: {enhanced_line['is_positive_ev']}") 