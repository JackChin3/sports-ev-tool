"""
Sports Betting EV Tool - Streamlit Dashboard

Displays positive expected value opportunities from DFS platforms.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# Import our modules
from scrapers.prizepicks import scrape_prizepicks
from scrapers.underdog import scrape_underdog
from scrapers.fliff import scrape_fliff
from market_odds.odds_api import OddsAPIClient
from utils.ev_calculator import calculate_ev


def main():
    """Main Streamlit app."""
    
    # Page config
    st.set_page_config(
        page_title="Sports Betting EV Tool",
        page_icon="🎯",
        layout="wide"
    )
    
    # Header
    st.title("🎯 Sports Betting Expected Value Tool")
    st.markdown("Find profitable betting opportunities across DFS platforms")
    
    # Sidebar filters
    st.sidebar.header("⚙️ Filters")
    
    # Load cached data
    cached_data = load_cached_data()
    
    # Apply filters
    filtered_data = apply_filters(cached_data)
    
    # Instructions
    with st.expander("📖 How it works"):
        st.markdown("""
        1. **Scrapes** real odds from PrizePicks, Underdog, and Fliff
        2. **Compares** to market odds from major sportsbooks  
        3. **Calculates** Expected Value (EV) for each bet
        4. **Displays** only positive EV opportunities (profitable bets)
        
        **Positive EV** = Your expected profit over time from this bet
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Current Opportunities")
        
        # Show filter summary
        if cached_data:
            show_filter_summary(cached_data, filtered_data)
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Fetching latest odds..."):
                new_data = fetch_fresh_data()
                save_cached_data(new_data)
                st.rerun()  # Refresh the app
        
        # Display opportunities table
        if filtered_data:
            display_opportunities_table(filtered_data)
        elif cached_data:
            st.info("📋 No opportunities match current filters. Adjust filters or refresh data.")
        else:
            st.info("📋 No opportunities cached. Click 'Refresh Data' to load latest odds.")
            
            # Show sample data structure
            with st.expander("💡 Sample Data"):
                sample_data = create_sample_data()
                display_opportunities_table(sample_data)
    
    with col2:
        st.header("📈 Statistics")
        
        # Calculate and display metrics
        if filtered_data:
            display_statistics(filtered_data)
        else:
            st.metric("Total Opportunities", 0)
            st.metric("Best EV", "0.0%")
            st.metric("Platforms Checked", 3)
        
        st.header("🎰 Platform Status")
        display_platform_status(cached_data)


def apply_filters(data):
    """Apply sidebar filters to the data."""
    
    if not data:
        return []
    
    df = pd.DataFrame(data)
    
    # Sport filter
    available_sports = ["All"] + list(df['sport'].unique()) if 'sport' in df.columns else ["All"]
    selected_sport = st.sidebar.selectbox(
        "🏈 Sport",
        available_sports,
        help="Filter by sport"
    )
    
    if selected_sport != "All" and 'sport' in df.columns:
        df = df[df['sport'] == selected_sport]
    
    # EV percentage filter
    min_ev = st.sidebar.slider(
        "📈 Minimum EV %",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.5,
        help="Only show opportunities with EV above this threshold"
    )
    
    if 'ev_percentage' in df.columns:
        df = df[df['ev_percentage'] >= min_ev]
    
    # Platform filter
    available_platforms = df['sportsbook'].unique().tolist() if 'sportsbook' in df.columns else []
    if available_platforms:
        selected_platforms = st.sidebar.multiselect(
            "🎰 Platforms",
            available_platforms,
            default=available_platforms,
            help="Select which platforms to include"
        )
        
        if selected_platforms:
            df = df[df['sportsbook'].isin(selected_platforms)]
    
    # Market type filter
    available_markets = df['market_type'].unique().tolist() if 'market_type' in df.columns else []
    if available_markets:
        selected_markets = st.sidebar.multiselect(
            "🎯 Markets",
            available_markets,
            default=available_markets,
            help="Select which market types to include"
        )
        
        if selected_markets:
            df = df[df['market_type'].isin(selected_markets)]
    
    return df.to_dict('records')


def show_filter_summary(original_data, filtered_data):
    """Show summary of applied filters."""
    
    original_count = len(original_data)
    filtered_count = len(filtered_data)
    
    if filtered_count < original_count:
        st.caption(f"🔍 Showing {filtered_count} of {original_count} opportunities (filters applied)")
    else:
        st.caption(f"📊 Showing all {original_count} opportunities")


def display_opportunities_table(data):
    """Display opportunities in a formatted table."""
    
    if not data:
        st.info("No positive EV opportunities found")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Format the data for display
    if len(df) > 0:
        display_df = df.copy()
        
        # Format columns for better display
        if 'ev_percentage' in display_df.columns:
            display_df['EV %'] = display_df['ev_percentage'].apply(lambda x: f"+{x:.1f}%" if x > 0 else f"{x:.1f}%")
        
        if 'expected_profit' in display_df.columns:
            display_df['Profit ($100)'] = display_df['expected_profit'].apply(lambda x: f"${x:.2f}")
        
        # Select and rename columns for display
        display_columns = {
            'sportsbook': 'Platform',
            'player_name': 'Player',
            'market_type': 'Market',
            'line_value': 'Line',
            'over_under': 'O/U',
            'odds': 'Odds',
            'EV %': 'EV %',
            'Profit ($100)': 'Profit ($100)',
            'event_name': 'Game'
        }
        
        # Filter to available columns
        available_cols = {k: v for k, v in display_columns.items() if k in display_df.columns}
        display_df = display_df[list(available_cols.keys())].rename(columns=available_cols)
        
        # Sort by EV percentage (highest first)
        if 'EV %' in display_df.columns:
            display_df = display_df.sort_values('EV %', ascending=False)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.caption(f"📊 Showing {len(display_df)} positive EV opportunities")
    else:
        st.info("No data to display")


def display_statistics(data):
    """Display summary statistics."""
    
    if not data:
        st.metric("Total Opportunities", 0)
        st.metric("Best EV", "0.0%")
        st.metric("Platforms Checked", 0)
        return
    
    df = pd.DataFrame(data)
    
    # Total opportunities
    total_opps = len(df)
    
    # Best EV
    if 'ev_percentage' in df.columns and len(df) > 0:
        best_ev = df['ev_percentage'].max()
        best_ev_str = f"+{best_ev:.1f}%"
    else:
        best_ev_str = "0.0%"
    
    # Platforms with data
    if 'sportsbook' in df.columns:
        platforms_count = df['sportsbook'].nunique()
    else:
        platforms_count = 0
    
    st.metric("Total Opportunities", total_opps)
    st.metric("Best EV", best_ev_str)
    st.metric("Platforms Checked", platforms_count)
    
    # Additional stats
    if len(df) > 0 and 'expected_profit' in df.columns:
        avg_profit = df['expected_profit'].mean()
        st.metric("Avg Profit ($100)", f"${avg_profit:.2f}")


def display_platform_status(data):
    """Display status of each platform."""
    
    platforms = ["PrizePicks", "Underdog", "Fliff"]
    
    if data:
        df = pd.DataFrame(data)
        platform_counts = df['sportsbook'].value_counts() if 'sportsbook' in df.columns else {}
        
        for platform in platforms:
            count = platform_counts.get(platform, 0)
            if count > 0:
                st.write(f"✅ {platform}: {count} opportunities")
            else:
                st.write(f"⚪ {platform}: No opportunities")
    else:
        for platform in platforms:
            st.write(f"🔄 {platform}: Checking...")


def fetch_fresh_data():
    """Fetch fresh data from all platforms and calculate EV."""
    
    try:
        # Import scheduler functions
        from scheduler.run_scrapers import run_all_scrapers, get_market_odds_for_lines, calculate_ev_for_lines
        
        # Run the full pipeline
        st.info("📊 Running scrapers...")
        all_lines = run_all_scrapers()
        
        if not all_lines:
            st.warning("No lines scraped from any platform")
            return create_sample_data()  # Fallback to sample data
        
        st.info("🏦 Getting market odds...")
        lines_with_odds = get_market_odds_for_lines(all_lines)
        
        if not lines_with_odds:
            st.warning("No market odds found")
            return create_sample_data()  # Fallback to sample data
        
        st.info("🧮 Calculating EV...")
        opportunities = calculate_ev_for_lines(lines_with_odds)
        
        st.success(f"✅ Found {len(opportunities)} positive EV opportunities!")
        return opportunities
        
    except Exception as e:
        st.error(f"Error fetching fresh data: {e}")
        st.info("Using sample data as fallback")
        return create_sample_data()


def create_sample_data():
    """Create sample data for demonstration."""
    
    return [
        {
            'sportsbook': 'PrizePicks',
            'player_name': 'Sample Player 1',
            'market_type': 'points',
            'line_value': 25.5,
            'over_under': 'over',
            'odds': -110,
            'ev_percentage': 6.1,
            'expected_profit': 6.06,
            'event_name': 'Team A @ Team B'
        },
        {
            'sportsbook': 'Underdog',
            'player_name': 'Sample Player 2', 
            'market_type': 'assists',
            'line_value': 7.5,
            'over_under': 'over',
            'odds': +100,
            'ev_percentage': 3.2,
            'expected_profit': 3.20,
            'event_name': 'Team C @ Team D'
        }
    ]


def load_cached_data():
    """Load cached opportunity data."""
    cache_file = Path("data/lines_cache.json")
    
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                
            # Handle both old format (list) and new format (dict with metadata)
            if isinstance(cache_data, list):
                return cache_data
            elif isinstance(cache_data, dict) and 'opportunities' in cache_data:
                return cache_data['opportunities']
        except Exception as e:
            st.error(f"Error loading cache: {e}")
    
    return []


def save_cached_data(data):
    """Save opportunity data to cache."""
    cache_dir = Path("data")
    cache_dir.mkdir(exist_ok=True)
    
    cache_file = cache_dir / "lines_cache.json"
    
    # Save with metadata
    timestamp = datetime.now().isoformat()
    cache_data = {
        "timestamp": timestamp,
        "opportunities": data,
        "total_count": len(data)
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2, default=str)


if __name__ == "__main__":
    main() 