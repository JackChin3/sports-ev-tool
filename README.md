# 🎯 Sports Betting Expected Value Tool

An internal tool for finding profitable betting opportunities across DFS platforms by comparing to market odds and calculating Expected Value (EV).

## ✨ Features

- **Real-time data** from PrizePicks, Underdog, and Fliff via The Odds API
- **Market odds comparison** from major sportsbooks (FanDuel, DraftKings, BetMGM, etc.)
- **EV calculation** to identify profitable betting opportunities
- **Interactive dashboard** with filters and real-time updates
- **Automated refresh** via scheduler script

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- The Odds API key (free tier available)

### Installation

1. **Clone and setup**:
```bash
git clone https://github.com/JackChin3/sports-ev-tool.git
cd sports-ev-tool
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set API key** (optional - demo data works without it):
```bash
export ODDS_API_KEY="your_api_key_here"
```

### Usage

1. **Run the Streamlit dashboard**:
```bash
streamlit run app.py
```

2. **Manual data refresh**:
```bash
python scheduler/run_scrapers.py
```

3. **Open browser** to `http://localhost:8501`

## 📊 How It Works

1. **Scrapes odds** from DFS platforms (PrizePicks, Underdog, Fliff)
2. **Gets market odds** from major sportsbooks for comparison
3. **Calculates Expected Value** using implied probability differences
4. **Displays positive EV opportunities** in an interactive table
5. **Filters by sport, platform, market type, and minimum EV**

## 📁 Project Structure

```
sports_ev_app/
├── app.py                     # Streamlit dashboard
├── scrapers/                  # DFS platform scrapers
│   ├── prizepicks.py         # PrizePicks API integration
│   ├── underdog.py           # Underdog Fantasy API integration
│   └── fliff.py              # Fliff API integration
├── market_odds/              # Market odds data
│   └── odds_api.py           # The Odds API client
├── utils/                    # Core utilities
│   ├── line_schema.py        # Standardized data format
│   └── ev_calculator.py      # EV calculation logic
├── scheduler/                # Automation
│   └── run_scrapers.py       # Manual/scheduled refresh
├── data/                     # Cached data
│   └── lines_cache.json      # Cached opportunities
└── requirements.txt          # Dependencies
```

## 🎯 Key Metrics

- **EV Percentage**: Expected return on investment
- **Expected Profit**: Dollar profit per $100 bet
- **Platform Coverage**: PrizePicks, Underdog, Fliff
- **Market Comparison**: 10+ major sportsbooks

## 🔧 Configuration

### API Settings
- Default API key in code (demo purposes)
- Production: Use environment variables
- Free tier: 500 requests/month

### Filters Available
- **Sport**: NBA, NFL, MLB, NHL
- **Minimum EV**: 0% to 50%
- **Platforms**: Select/deselect any platform
- **Markets**: Points, rebounds, assists, etc.

## 📈 Sample Output

```
🚀 TOP POSITIVE EV OPPORTUNITIES:

1. PrizePicks - Jayson Tatum
   points over 28.5
   Odds: -110 | EV: +8.3%
   Expected profit on $100 bet: $8.27

2. Underdog - Tyrese Haliburton  
   assists over 9.5
   Odds: +105 | EV: +4.2%
   Expected profit on $100 bet: $4.18
```

## ⚠️ Important Notes

### Disclaimer
- **For educational/personal use only**
- **Past performance doesn't guarantee future results**
- **Always bet responsibly**
- **Verify odds before placing bets**

### Data Accuracy
- Real-time data when API is active
- Fallback to sample data during off-peak hours
- DFS platforms may not have odds available 24/7

## 🛠️ Development

### Architecture
- **100% API-based** (no web scraping)
- **Modular design** for easy platform additions
- **Standardized data format** across all sources
- **Error handling** with graceful fallbacks

### Adding New Platforms
1. Create new scraper in `scrapers/`
2. Follow existing pattern (see `prizepicks.py`)
3. Add to scheduler in `run_scrapers.py`
4. Test with sample data first

## 📝 MVP Milestones

- ✅ Phase 1: Basic Setup
- ✅ Phase 2: Data Models & Utilities  
- ✅ Phase 3: API Integration (PrizePicks, Underdog, Fliff)
- ✅ Phase 4: EV Calculation & Testing
- ✅ Phase 5: Streamlit UI with Filters
- ✅ Phase 6: Manual Refresh System
- ✅ Phase 7: Documentation & Cleanup

## 🔮 Future Enhancements

- **Automated scheduling** (cron jobs)
- **Email/SMS alerts** for high-EV opportunities  
- **Historical tracking** and performance metrics
- **Additional platforms** (DraftKings Pick6, etc.)
- **Line movement tracking**
- **Bankroll management** recommendations

## 📞 Support

For issues or questions:
1. Check the GitHub issues
2. Review API documentation
3. Test with sample data first
4. Verify API key and credits

---

**Built with ❤️ for profitable betting analysis** 