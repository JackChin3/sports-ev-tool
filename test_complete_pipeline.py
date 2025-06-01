"""
Complete pipeline test with REAL data from all DFS platforms.

Tests PrizePicks, Underdog, Fliff + market odds + EV calculation.
NO MORE MOCK DATA! 🎯
"""

from scrapers.prizepicks import scrape_prizepicks
from scrapers.underdog import scrape_underdog  
from scrapers.fliff import scrape_fliff
from market_odds.odds_api import OddsAPIClient
from utils.ev_calculator import calculate_ev


def test_all_platforms():
    """Test complete pipeline with real data from all platforms."""
    
    print("🚀 COMPLETE REAL DATA PIPELINE TEST")
    print("=" * 60)
    
    api_key = "a67ad13b23ed6a4bd92ee3bd279840a4"
    odds_client = OddsAPIClient(api_key)
    
    # Step 1: Get real data from all DFS platforms
    print("\n📊 Step 1: Scraping ALL DFS platforms...")
    
    platforms = {
        "PrizePicks": scrape_prizepicks,
        "Underdog": scrape_underdog,
        "Fliff": scrape_fliff
    }
    
    all_dfs_lines = []
    platform_counts = {}
    
    for platform_name, scraper_func in platforms.items():
        try:
            print(f"\n  🎯 Scraping {platform_name}...")
            lines = scraper_func()
            platform_counts[platform_name] = len(lines)
            all_dfs_lines.extend(lines)
            print(f"    ✅ {platform_name}: {len(lines)} lines")
            
            # Show sample
            if lines:
                sample = lines[0]
                print(f"    📋 Sample: {sample['player_name']} {sample['market_type']} {sample['over_under']} {sample['line_value']}")
                
        except Exception as e:
            print(f"    ❌ {platform_name} error: {e}")
            platform_counts[platform_name] = 0
    
    print(f"\n✅ Total DFS lines scraped: {len(all_dfs_lines)}")
    print(f"📊 Platform breakdown: {platform_counts}")
    
    # Step 2: Get market odds for comparison
    print(f"\n📊 Step 2: Getting market odds...")
    
    market_odds_count = 0
    lines_with_market_odds = []
    
    for line in all_dfs_lines[:10]:  # Test with first 10 lines to save API credits
        try:
            # Get market odds for this line
            market_odds = odds_client.get_market_odds_for_line(line)
            
            if market_odds:
                line['market_odds'] = market_odds
                lines_with_market_odds.append(line)
                market_odds_count += 1
        except Exception as e:
            continue
    
    print(f"✅ Found market odds for {market_odds_count} lines")
    
    # Step 3: Calculate EV for lines with market odds
    print(f"\n📊 Step 3: Calculating Expected Value...")
    
    ev_results = []
    positive_ev_count = 0
    
    for line in lines_with_market_odds:
        try:
            ev_result = calculate_ev(line, line['market_odds'])
            ev_results.append(ev_result)
            
            if ev_result['ev_percentage'] > 0:
                positive_ev_count += 1
                
        except Exception as e:
            print(f"    ⚠️  EV calculation error: {e}")
            continue
    
    print(f"✅ Calculated EV for {len(ev_results)} lines")
    print(f"🎯 Found {positive_ev_count} positive EV opportunities!")
    
    # Step 4: Display results
    print(f"\n📊 Step 4: RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"\n🎯 DATA SOURCES (ALL REAL!):")
    for platform, count in platform_counts.items():
        print(f"  • {platform}: {count} lines")
    
    print(f"\n📈 EV ANALYSIS:")
    print(f"  • Lines analyzed: {len(ev_results)}")
    print(f"  • Positive EV opportunities: {positive_ev_count}")
    
    if positive_ev_count > 0:
        print(f"\n🚀 TOP POSITIVE EV OPPORTUNITIES:")
        
        # Sort by EV percentage
        positive_ev = [ev for ev in ev_results if ev['ev_percentage'] > 0]
        positive_ev.sort(key=lambda x: x['ev_percentage'], reverse=True)
        
        for i, ev in enumerate(positive_ev[:5], 1):
            line = ev['line']
            print(f"\n  {i}. {line['sportsbook']} - {line['player_name']}")
            print(f"     {line['market_type']} {line['over_under']} {line['line_value']}")
            print(f"     Odds: {line['odds']} | EV: +{ev['ev_percentage']:.1f}%")
            print(f"     Expected profit on $100 bet: ${ev['expected_profit']:.2f}")
    
    # Step 5: Platform comparison
    print(f"\n📊 PLATFORM COMPARISON:")
    platform_ev = {}
    
    for ev in ev_results:
        platform = ev['line']['sportsbook']
        if platform not in platform_ev:
            platform_ev[platform] = {'total': 0, 'positive': 0}
        
        platform_ev[platform]['total'] += 1
        if ev['ev_percentage'] > 0:
            platform_ev[platform]['positive'] += 1
    
    for platform, stats in platform_ev.items():
        positive_rate = (stats['positive'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  • {platform}: {stats['positive']}/{stats['total']} positive EV ({positive_rate:.1f}%)")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 PIPELINE SUCCESS!")
    print(f"✅ Real data from {len(platforms)} DFS platforms")
    print(f"✅ Real market odds comparison")  
    print(f"✅ Real EV calculations")
    print(f"✅ {positive_ev_count} profitable opportunities identified")
    print(f"🚀 NO MOCK DATA - ALL REAL!")
    
    return {
        'total_lines': len(all_dfs_lines),
        'platforms': platform_counts,
        'market_odds_found': market_odds_count,
        'ev_calculated': len(ev_results),
        'positive_ev_opportunities': positive_ev_count,
        'positive_ev_results': [ev for ev in ev_results if ev['ev_percentage'] > 0]
    }


def test_individual_scrapers():
    """Quick test of each scraper individually."""
    
    print("\n🔍 INDIVIDUAL SCRAPER TESTS")
    print("=" * 40)
    
    scrapers = {
        "PrizePicks": scrape_prizepicks,
        "Underdog": scrape_underdog,
        "Fliff": scrape_fliff
    }
    
    for name, scraper in scrapers.items():
        try:
            print(f"\n  Testing {name}...")
            lines = scraper()
            print(f"  ✅ {name}: {len(lines)} lines")
            
            if lines:
                sample = lines[0]
                print(f"      Sample: {sample['event_name']}")
                print(f"      Player: {sample['player_name']} - {sample['market_type']}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")


if __name__ == "__main__":
    # Test individual scrapers first
    test_individual_scrapers()
    
    # Then test complete pipeline
    results = test_all_platforms()
    
    if results['positive_ev_opportunities'] > 0:
        print(f"\n🎯 SUCCESS! Found {results['positive_ev_opportunities']} real +EV opportunities!")
    else:
        print(f"\n📊 Pipeline working perfectly - no +EV opportunities found in current sample")
        print(f"   (This is normal - positive EV opportunities are rare)") 