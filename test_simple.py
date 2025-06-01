"""
Simple test of real API scrapers.
"""

from scrapers.prizepicks import scrape_prizepicks

def test_prizepicks():
    print("🎯 Testing PrizePicks real API scraper...")
    lines = scrape_prizepicks()
    print(f"✅ PrizePicks: {len(lines)} real lines scraped")
    
    if lines:
        sample = lines[0]
        print(f"📋 Sample: {sample['player_name']} - {sample['market_type']} {sample['over_under']} {sample['line_value']}")
        print(f"    Event: {sample['event_name']}")
        print(f"    Odds: {sample['odds']}")
    
    return len(lines) > 0

if __name__ == "__main__":
    success = test_prizepicks()
    if success:
        print("🎉 SUCCESS: Real PrizePicks data working!")
    else:
        print("❌ No data found") 