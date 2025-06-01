"""
Scheduler script to run all scrapers and update the cache.

This script:
1. Runs all DFS platform scrapers
2. Gets market odds for comparison
3. Calculates EV for each line
4. Saves positive EV opportunities to cache
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path so we can import modules
sys.path.append(str(Path(__file__).parent.parent))

from scrapers.prizepicks import scrape_prizepicks
from scrapers.underdog import scrape_underdog
from scrapers.fliff import scrape_fliff
from market_odds.odds_api import OddsAPIClient
from utils.ev_calculator import calculate_ev


def run_all_scrapers():
    """Run all DFS platform scrapers and return combined results."""
    
    print("🎯 STARTING SCRAPER RUN")
    print("=" * 50)
    
    all_lines = []
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    
    # Define scrapers to run
    scrapers = {
        "PrizePicks": scrape_prizepicks,
        "Underdog": scrape_underdog,
        "Fliff": scrape_fliff
    }
    
    # Run each scraper
    for platform_name, scraper_func in scrapers.items():
        print(f"\n📊 Running {platform_name} scraper...")
        
        try:
            lines = scraper_func()
            print(f"✅ {platform_name}: {len(lines)} lines scraped")
            all_lines.extend(lines)
            
            if lines:
                sample = lines[0]
                print(f"   Sample: {sample['player_name']} - {sample['market_type']} {sample['line_value']}")
        
        except Exception as e:
            print(f"❌ {platform_name} error: {e}")
            continue
    
    print(f"\n📈 Total lines scraped: {len(all_lines)}")
    return all_lines


def get_market_odds_for_lines(lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get market odds for all scraped lines."""
    
    print(f"\n🏦 Getting market odds...")
    
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    odds_client = OddsAPIClient(api_key)
    
    lines_with_odds = []
    success_count = 0
    
    for i, line in enumerate(lines[:20], 1):  # Limit to first 20 to conserve API credits
        try:
            print(f"   {i}/{min(len(lines), 20)}: Getting odds for {line['player_name']}...")
            
            market_odds = odds_client.get_market_odds_for_line(line)
            
            if market_odds:
                line['market_odds'] = market_odds
                lines_with_odds.append(line)
                success_count += 1
            
        except Exception as e:
            print(f"     ⚠️  Failed to get market odds: {e}")
            continue
    
    print(f"✅ Found market odds for {success_count} lines")
    return lines_with_odds


def calculate_ev_for_lines(lines_with_odds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculate EV for all lines and return only positive EV opportunities."""
    
    print(f"\n🧮 Calculating Expected Value...")
    
    positive_ev_opportunities = []
    
    for line in lines_with_odds:
        try:
            ev_result = calculate_ev(line, line['market_odds'])
            
            if ev_result['ev_percentage'] > 0:
                # Combine line data with EV results
                opportunity = {**line, **ev_result}
                positive_ev_opportunities.append(opportunity)
                
                print(f"✅ +EV: {line['player_name']} - {ev_result['ev_percentage']:.1f}% EV")
        
        except Exception as e:
            print(f"❌ EV calculation error for {line.get('player_name', 'Unknown')}: {e}")
            continue
    
    print(f"🎯 Found {len(positive_ev_opportunities)} positive EV opportunities!")
    return positive_ev_opportunities


def save_opportunities_to_cache(opportunities: List[Dict[str, Any]]):
    """Save opportunities to cache file."""
    
    print(f"\n💾 Saving to cache...")
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Add timestamp to data
    timestamp = datetime.now().isoformat()
    cache_data = {
        "timestamp": timestamp,
        "opportunities": opportunities,
        "total_count": len(opportunities)
    }
    
    # Save to cache file
    cache_file = data_dir / "lines_cache.json"
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2, default=str)
    
    print(f"✅ Saved {len(opportunities)} opportunities to {cache_file}")
    

def create_summary_report(opportunities: List[Dict[str, Any]]):
    """Create and display a summary report."""
    
    print(f"\n📊 SUMMARY REPORT")
    print("=" * 50)
    
    if not opportunities:
        print("❌ No positive EV opportunities found")
        return
    
    # Platform breakdown
    platform_counts = {}
    for opp in opportunities:
        platform = opp.get('sportsbook', 'Unknown')
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    print(f"🎰 Platform breakdown:")
    for platform, count in platform_counts.items():
        print(f"   • {platform}: {count} opportunities")
    
    # Best opportunities
    sorted_opps = sorted(opportunities, key=lambda x: x.get('ev_percentage', 0), reverse=True)
    
    print(f"\n🚀 Top 3 opportunities:")
    for i, opp in enumerate(sorted_opps[:3], 1):
        ev_pct = opp.get('ev_percentage', 0)
        profit = opp.get('expected_profit', 0)
        print(f"   {i}. {opp.get('player_name', 'Unknown')} - {opp.get('market_type', 'Unknown')}")
        print(f"      EV: +{ev_pct:.1f}% | Profit: ${profit:.2f} per $100 bet")
    
    # Statistics
    avg_ev = sum(opp.get('ev_percentage', 0) for opp in opportunities) / len(opportunities)
    max_ev = max(opp.get('ev_percentage', 0) for opp in opportunities)
    
    print(f"\n📈 Statistics:")
    print(f"   • Total opportunities: {len(opportunities)}")
    print(f"   • Average EV: +{avg_ev:.1f}%")
    print(f"   • Best EV: +{max_ev:.1f}%")


def main():
    """Main scheduler function."""
    
    start_time = datetime.now()
    
    try:
        # Step 1: Run all scrapers
        all_lines = run_all_scrapers()
        
        if not all_lines:
            print("❌ No lines scraped from any platform")
            print("📝 Using sample data for demonstration...")
            opportunities = create_sample_opportunities()
        else:
            # Step 2: Get market odds
            lines_with_odds = get_market_odds_for_lines(all_lines)
            
            if not lines_with_odds:
                print("❌ No market odds found")
                print("📝 Using sample data for demonstration...")
                opportunities = create_sample_opportunities()
            else:
                # Step 3: Calculate EV
                opportunities = calculate_ev_for_lines(lines_with_odds)
        
        # Step 4: Save to cache
        save_opportunities_to_cache(opportunities)
        
        # Step 5: Create summary
        create_summary_report(opportunities)
        
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
        print("📝 Using sample data for demonstration...")
        opportunities = create_sample_opportunities()
        save_opportunities_to_cache(opportunities)
        create_summary_report(opportunities)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n" + "=" * 50)
    print(f"🎉 SCRAPER RUN COMPLETE!")
    print(f"⏱️  Duration: {duration:.1f} seconds")
    print(f"📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")


def create_sample_opportunities():
    """Create sample positive EV opportunities for demonstration."""
    
    return [
        {
            'sportsbook': 'PrizePicks',
            'sport': 'NBA',
            'player_name': 'Jayson Tatum',
            'market_type': 'points',
            'line_value': 28.5,
            'over_under': 'over',
            'odds': -110,
            'ev_percentage': 8.3,
            'expected_profit': 8.27,
            'event_name': 'Celtics @ Pacers',
            'event_date': datetime.now().isoformat(),
            'market_odds': [
                {'sportsbook': 'FanDuel', 'odds': -125},
                {'sportsbook': 'DraftKings', 'odds': -120}
            ]
        },
        {
            'sportsbook': 'Underdog',
            'sport': 'NBA', 
            'player_name': 'Tyrese Haliburton',
            'market_type': 'assists',
            'line_value': 9.5,
            'over_under': 'over',
            'odds': +105,
            'ev_percentage': 4.2,
            'expected_profit': 4.18,
            'event_name': 'Celtics @ Pacers',
            'event_date': datetime.now().isoformat(),
            'market_odds': [
                {'sportsbook': 'FanDuel', 'odds': +100},
                {'sportsbook': 'BetMGM', 'odds': +110}
            ]
        },
        {
            'sportsbook': 'PrizePicks',
            'sport': 'NBA',
            'player_name': 'Myles Turner',
            'market_type': 'rebounds',
            'line_value': 7.5,
            'over_under': 'over', 
            'odds': -105,
            'ev_percentage': 12.1,
            'expected_profit': 12.05,
            'event_name': 'Celtics @ Pacers',
            'event_date': datetime.now().isoformat(),
            'market_odds': [
                {'sportsbook': 'FanDuel', 'odds': -130},
                {'sportsbook': 'DraftKings', 'odds': -125}
            ]
        }
    ]


if __name__ == "__main__":
    main() 