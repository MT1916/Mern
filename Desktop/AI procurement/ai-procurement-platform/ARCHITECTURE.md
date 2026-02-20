# 🏗️ System Architecture & Design

## Overview

The **AI Procurement and Pricing Platform** is architected for modularity, scalability, and AI/ML readiness.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Input Module (Selectbox, Slider, Radio)           │   │
│  │ • Recommendation Panel (Visualization)              │   │
│  │ • Analysis Dashboard (Charts & Tables)              │   │
│  │ • Market Data View (Raw Data Display)               │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│              APPLICATION LOGIC LAYER (src/)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Decision Engine                                      │   │
│  │ • Rule-based decision logic                         │   │
│  │ • Price calculations                                │   │
│  │ • Supplier comparison                               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Data Processor                                       │   │
│  │ • Data loading & validation                         │   │
│  │ • Filtering & aggregation                           │   │
│  │ • Statistics calculation                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Utils & Helpers                                      │   │
│  │ • Formatting (currency, percentages)               │   │
│  │ • Charting (Plotly)                                │   │
│  │ • UI components                                     │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                  DATA LAYER                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ CSV Database (Phase 1)                              │   │
│  │ • sample_data.csv                                  │   │
│  │ • 10 items × 5 suppliers                           │   │
│  │ • Real pricing & stock data                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Module Structure

### 1. UI Layer (app.py)

**Responsibilities:**
- User input collection (sidebar controls)
- Data visualization (tabs & charts)
- Session management
- Error handling for user feedback

**Key Components:**
```python
1. Page Configuration
   - Streamlit settings, CSS styling

2. Session State Initialization
   - Data loading caching
   - State management

3. Sidebar Controls (INPUT MODULE)
   - Item selection dropdown
   - Supplier selection
   - Stock level slider
   - Demand level radio buttons

4. Main Content Tabs (VISUALIZATION)
   - Recommendation tab (Primary decision + insights)
   - Analysis tab (Charts, statistics, market data)
   - Market Data tab (Raw supplier table)

5. Footer & Help
   - Metadata display
   - Documentation links
```

**Design Patterns:**
- ✅ Streamlit caching for data loading
- ✅ Modular tab structure for future features
- ✅ Responsive 2-column layouts
- ✅ Expandable sections for advanced info

**Extension Points:**
```python
# Add new tab for Phase 2 analytics
tab4 = st.tabs(["Price Trends", "Supplier Scores", ...])

# Add sidebar section for filters
st.sidebar.multiselect("Filter by Demand Level", [...])

# Add new metric cards
st.metric("AI Prediction", "...", "...")
```

### 2. Decision Engine (src/decision_engine.py)

**Responsibilities:**
- Rule-based procurement decision logic
- Price calculations and analysis
- Supplier recommendations
- Reasoning generation

**Core Functions & Flow:**
```
generate_recommendation()
├── calculate_average_price()
├── identify_best_supplier()
├── make_procurement_decision()
│   └── apply_decision_rules()
├── calculate_negotiation_price()
└── generate_decision_reasoning()
    └── SupplierRecommendation object
```

**Decision Rules (Phase 1):**
```
IF Stock < 50 AND Demand = High
   → BUY_NOW

ELSE IF 50 ≤ Stock < 150 AND Demand = High
   → CONSIDER_BUYING

ELSE IF Stock ≥ 150
   → WAIT (unless price_below_average(15%) AND Demand = High)

ELSE
   → WAIT (conservative default)
```

**Data Structures:**
```python
@dataclass
SupplierRecommendation:
    best_supplier: str
    best_price: float
    average_price: float
    suggested_purchase_price: float
    decision: ProcurementDecision
    reasoning: str
```

**Phase 2 Extensions:**
```python
# Add ML-based decision
from ml_models import predict_optimal_timing

# Add supplier scoring
from analytics import calculate_supplier_score

# Add price forecasting
from forecasting import predict_price_trend
```

### 3. Data Processor (src/data_processor.py)

**Responsibilities:**
- CSV data loading and validation
- Data filtering and aggregation
- Statistical calculations
- Supplier analysis

**Core Classes:**

#### ProcurementDataLoader
```python
- load_data()           # Load CSV, validate schema
- get_all_items()       # Get available items
- get_item_name_by_id() # Lookup item name
```

#### ItemDataProcessor
```python
- get_item_data()                    # Filter by item
- get_supplier_prices()              # Extract price mapping
- get_item_summary()                 # Aggregate statistics
- get_supplier_comparison_table()    # Format for display
- get_price_statistics()             # Calculate stats
```

#### SupplierFilter
```python
- get_suppliers_by_price_range()  # Filter by price threshold
- get_reliable_suppliers()         # Filter by stock level
- get_best_value_suppliers()       # Top N cheapest suppliers
```

**Phase 2 Extensions:**
```python
# Replace CSV with database
class DatabaseDataLoader(ProcurementDataLoader):
    def load_data(self):
        query = "SELECT * FROM procurement_data"
        self.df = pd.read_sql(query, db_connection)

# Add trend analysis
class TrendAnalyzer:
    def get_price_history()
    def calculate_trend_line()
    def predict_future_price()
```

### 4. Utils (src/utils.py)

**Responsibilities:**
- Data formatting (currency, percentages)
- Chart generation (Plotly)
- UI component builders
- Display helpers

**Key Functions:**
```python
Formatting:
- format_currency()
- format_percentage()
- get_demand_color()
- get_decision_color()
- get_stock_color()

Charting:
- create_price_comparison_chart()
- create_price_distribution_chart()
- create_demand_vs_stock_matrix()

UI Components:
- display_key_insight_cards()
- display_decision_highlight()
- display_metadata()
- create_insights_text()
```

**Phase 2 Extensions:**
```python
# Add advanced charts
def create_trend_chart()
def create_supplier_scorecard()
def create_forecast_chart()

# Add export utilities
def export_to_excel()
def export_to_pdf()
```

## Data Flow

### 1. User Interaction Flow
```
User Input (Sidebar)
├── Item Selection
├── Supplier Selection
├── Stock Level (Slider)
└── Demand Level (Radio)
           ↓
        app.py
           ↓
   ItemDataProcessor
           ↓
   Decision Engine
           ↓
   SupplierRecommendation
           ↓
    Streamlit Display
```

### 2. Recommendation Generation Flow
```
Selected Item & Supplier
           ↓
get_supplier_prices() → Dict[supplier_name, price]
           ↓
make_procurement_decision(stock, demand, price, avg_price)
           ↓
Decision Engine Rules
           ↓
ProcurementDecision enum
           ↓
generate_decision_reasoning()
           ↓
SupplierRecommendation object
           ↓
Display to User
```

### 3. Data Processing Flow
```
CSV File
    ↓
ProcurementDataLoader.load_data()
    ↓
Pandas DataFrame (cached)
    ↓
ItemDataProcessor
    ├── Filter by item_id
    ├── Calculate statistics
    ├── Sort suppliers
    └── Prepare display format
    ↓
Dict/DataFrame ready for UI
```

## Extensibility Patterns

### Pattern 1: Adding New Decision Rules

**Current Implementation:**
```python
def make_procurement_decision(...):
    if stock_category == "Low" and demand_level == "High":
        return ProcurementDecision.BUY_NOW.value
    # ... more rules
```

**Phase 2 Extension:**
```python
def make_procurement_decision_v2(...):
    # Call Phase 1 logic
    basic_decision = make_procurement_decision(...)
    
    # Add ML prediction
    ml_score = predict_optimal_timing(...)
    
    # Add supplier risk
    risk_score = calculate_supplier_risk(...)
    
    # Return enhanced decision
    return adjust_decision(basic_decision, ml_score, risk_score)
```

### Pattern 2: Adding Data Sources

**Phase 1: CSV Only**
```python
class ProcurementDataLoader:
    def load_data(self):
        return pd.read_csv(self.csv_path)
```

**Phase 2/3: Database**
```python
class DatabaseDataLoader(ProcurementDataLoader):
    def load_data(self):
        query = "SELECT * FROM procurement WHERE active = 1"
        return pd.read_sql(query, self.db_connection)

# Use strategy pattern
loader = DatabaseDataLoader(config)  # Phase 3
# vs
loader = ProcurementDataLoader(csv_path)  # Phase 1
```

### Pattern 3: Adding Analytics

**Phase 1: Current State**
```python
# Calculate current metrics only
average_price = item_data['unit_price'].mean()
```

**Phase 2: With Trends**
```python
# Import new module
from analytics import PriceAnalyzer

analyzer = PriceAnalyzer(item_data)
avg_7day = analyzer.moving_average(days=7)
trend = analyzer.trend_direction()
forecast = analyzer.predict_next_30_days()
```

### Pattern 4: Adding Alerts

**Phase 1: No Alerts**
```python
# Display recommendation, user takes action
```

**Phase 3: Automated Alerts**
```python
from alerts import AlertManager

alert_mgr = AlertManager()
if recommendation.decision == "Buy Now":
    alert_mgr.send_email("Urgent procurement needed")
    alert_mgr.send_slack("@procure-team: Action needed")
```

## Configuration & Customization

### Stock Level Categories
Located in: `src/decision_engine.py`
```python
def get_stock_level_category(stock):
    if stock < 50:        # Configurable threshold
        return "Low"
    elif stock < 150:     # Configurable threshold
        return "Medium"
    else:
        return "High"
```

### Negotiation Margin
Located in: `src/decision_engine.py`
```python
def calculate_negotiation_price(
    average_price,
    negotiation_margin=0.05  # Change to 0.10 for 10%
):
```

### Decision Rule Thresholds
Located in: `src/decision_engine.py`
```python
# Price difference threshold for preferred supplier
threshold=0.1  # 10% below average

# Adjust to 0.15 for 15% threshold
```

### UI Styling
Located in: `app.py`
```python
st.markdown("""
    <style>
    .main { padding: 2rem; }
    /* Add custom CSS here */
    </style>
""")
```

## Performance Considerations

### Phase 1 Performance
- CSV load: ~50ms (first load)
- Data filtering: ~5ms (by item)
- Recommendation generation: ~10ms
- Total: ~65ms for complete operation

### Phase 2+ Optimizations
```python
# Database indexing for faster lookups
CREATE INDEX idx_item_id ON procurement_data(item_id);
CREATE INDEX idx_supplier_id ON procurement_data(supplier_id);

# Caching intermediate results
@cache
def get_supplier_prices(item_id):
    # Will cache results for 1 hour
    return fetch_from_db(item_id)

# Async data loading for background updates
async def fetch_latest_prices():
    # Update in background without blocking UI
```

### Scalability Path
```
Phase 1: CSV (10 items) → ~100ms
         ↓
Phase 2: PostgreSQL (1K items) → ~50ms (with indexing)
         ↓
Phase 3: Redis Cache on top of DB → ~10ms (cached)
         ↓
Phase 4: Distributed cache (Memcached) → handles 100K+ items
```

## Error Handling Strategy

### Error Categories

1. **Data Loading Errors**
   ```python
   try:
       df = pd.read_csv(path)
   except FileNotFoundError:
       st.error("Data file not found")
   except ValueError:
       st.error("Invalid CSV format")
   ```

2. **Missing Data Errors**
   ```python
   if item_data.empty:
       return {
           'item_id': item_id,
           'item_name': 'Unknown',
           # ... defaults
       }
   ```

3. **Calculation Errors**
   ```python
   if not prices:
       return 0.0  # Safe default
   
   if average_price > 0:
       savings_pct = savings / average_price * 100
   else:
       savings_pct = 0  # Avoid division by zero
   ```

## Testing Strategy (Phase 1)

### Manual Testing
1. Load each item in dropdown
2. Try all supplier combinations
3. Test stock slider range
4. Verify demand level changes
5. Check all three tabs load correctly

### Unit Testing (Phase 2)
```python
def test_procurement_decision():
    # Low stock + High demand = Buy Now
    result = make_procurement_decision(10, "High", 100, 120)
    assert result == "Buy Now"

def test_price_calculation():
    prices = [100, 110, 90]
    avg = calculate_average_price(prices)
    assert avg == 100.0
```

### Integration Testing (Phase 2)
```python
def test_full_recommendation_flow():
    loader = ProcurementDataLoader(csv_path)
    processor = ItemDataProcessor(loader.df)
    
    recommendation = generate_recommendation(
        "TechSupplies Inc.",
        850,
        {"TechSupplies Inc.": 850, "PowerTech": 780},
        45,
        "High"
    )
    
    assert recommendation.decision == "Buy Now"
```

## Security Considerations

### Phase 1
- ✅ No authentication needed (internal tool)
- ✅ CSV data only (no sensitive data in production)
- ✅ No network calls (local execution)

### Phase 2+
- 🔒 Add user authentication to Streamlit
- 🔒 Encrypt database credentials
- 🔒 Implement audit logging for decisions
- 🔒 Add role-based access control

```python
# Phase 3: Add authentication
from streamlit_authenticator import Authenticate

authenticator = Authenticate(
    credentials,
    session_cookie_name='auth',
    key='auth_key'
)

authenticator.login()
if st.session_state["authentication_status"]:
    show_app()  # Show only if authenticated
```

## Deployment Considerations

### Phase 1: Local Deployment
```bash
streamlit run app.py  # Direct execution
```

### Phase 2: Streamlit Cloud
```bash
# Push to GitHub, connect to Streamlit Cloud
# Automatic deployment on push
```

### Phase 3: Docker Containerization
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Phase 4: Enterprise Deployment
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: procurement-app
spec:
  replicas: 3
  # ... scaling, load balancing, monitoring
```

## Documentation Map

| Document | Purpose | Audience |
|---|---|---|
| README.md | Full documentation | All users |
| QUICKSTART.md | 5-minute setup guide | New users |
| ARCHITECTURE.md | System design (this file) | Developers |
| Code comments | Implementation details | Developers |
| Docstrings | Function reference | Developers |

## Summary: Ready for Future Growth

✅ **Phase 1 Foundation:**
- Clean modular architecture
- Reusable components
- Clear extension points
- Comprehensive documentation

✅ **Phase 2-Ready:**
- Data layer abstraction (switch CSV ↔ Database)
- Decision logic isolation (add new rules/ML)
- Analytics hooks (add new metrics)
- UI sections (add new tabs/panels)

✅ **Enterprise-Ready Patterns:**
- Error handling
- Scalability design
- Security considerations
- Performance optimization path

---

**The platform is architected for 5-phase evolution while maintaining simplicity and clarity in Phase 1.**
