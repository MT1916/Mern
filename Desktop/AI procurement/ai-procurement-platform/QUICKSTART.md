# 🚀 AI Procurement and Pricing - Quick Start

## ⚡ Get Started in 5 Minutes

### Prerequisites Checklist
- ✅ Python 3.8+ installed
- ✅ Windows PowerShell or Command Prompt
- ✅ ~500MB free disk space for dependencies

### Step 1: Navigate to Project
```powershell
cd "c:\Users\MT\Desktop\AI procurement\ai-procurement-platform"
```

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**Output should show**: `(venv)` prefix in terminal

### Step 3: Run the Application
```powershell
streamlit run app.py
```

**Success!** Browser opens to: http://localhost:8501

---

## 🎮 Using the Application

### 🏠 Dashboard Page
- **View**: Overall market metrics and visualizations
- **See**: Category distribution, brand popularity, price ranges
- **Time**: Takes 10 seconds to load

### 📦 Product Catalog Page
- **Search** for products by name
- **Filter** by category, brand, or supplier
- **View** complete product details and pricing
- **Compare** prices across suppliers

**Try this**: Search for "Milk" → See all milk products from different suppliers

### 💰 Pricing Analysis Page
- **Select** a product for detailed pricing analysis
- **View** fair market prices and savings opportunities
- **Compare** supplier prices visually
- **Identify** best deals

**Try this**: Select "Aeroplane Basmati Rice" → See price range ₹799-₹825

### 📊 Market Intelligence Page
- **Review** supplier performance rankings
- **Identify** strategic products
- **Analyze** price competitiveness
- **View** savings potential

### 🎯 Procurement Data Page
- **Export** AI-ready datasets in multiple formats
- **Download** category averages for negotiations
- **Get** supplier price matrix
- **Access** ML training data

---

## 📊 Sample Analysis Workflow

### Find Best Milk Supplier

1. **Go to**: Product Catalog
2. **Search**: "Milk"
3. **See**: Nandini Milk from 4 suppliers
4. **Prices**: BigBasket (₹65), Blinkit (₹68), Grofers (₹66)
5. **Decision**: Buy from BigBasket ✅

---

## 🆘 Troubleshooting

### Issue: `streamlit: command not found`
**Solution**: Activate venv first
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: `ModuleNotFoundError`
**Solution**: Install dependencies
```powershell
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution**: Use different port
```powershell
streamlit run app.py --server.port 8502
```

---

## 🚀 Next Steps

- [ ] Read ARCHITECTURE.md for system design
- [ ] Check README.md for full documentation
- [ ] Try exporting all data formats
- [ ] Download ML training data for analysis

**Ready to start? Run `streamlit run app.py` now!** 🚀

## 🚀 You're Ready!

Your AI Procurement Platform is ready to help with smarter purchasing decisions!

Happy procuring! 🏭
