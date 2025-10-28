# BMW Sales Dashboard (2010-2024) 🚗

An interactive dashboard for visualizing BMW sales data from 2010 to 2024, built with Streamlit and Plotly.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)

## 🌟 Features

- 📈 **Sales Trends**: Visualize sales volume and price trends over time
- 🏆 **Top Models**: Analyze best-selling BMW models and their distribution
- 🌍 **Geographic Analysis**: Interactive world map showing sales by country
- 🔍 **Correlations**: Explore relationships between different features
- 📋 **Data Explorer**: Interactive data table with filtering and download options

## 🚀 Live Demo

[View Live Dashboard](https://your-app-url.streamlit.app) 

## 📋 Prerequisites

- Python 3.8 or higher
- BMW sales dataset CSV file

## 🛠️ Installation

### Local Development

1. Clone this repository:
```bash
git clone <your-repo-url>
cd Data_Visualization
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure your CSV file is in the same directory with the name:
   - `BMW sales data (2010-2024) (1).csv`

4. Run the Streamlit app:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`


## 📊 Dataset

The dashboard expects a CSV file with the following columns:
- `Year` - Sales year
- `Sales_Volume` - Number of units sold
- `Price_USD` - Price in USD
- `Model` - BMW model name
- `Country` - Country of sale
- `Fuel_Type` - Type of fuel
- `Transmission` - Transmission type
- `Engine_Size_L` - Engine size in liters

## 🎨 Features Overview

### Interactive Filters
- **Year Range Slider**: Filter data by specific years
- **Country Selector**: Focus on specific countries
- **Model Selector**: Analyze individual models

### Visualizations
1. **Sales Trends Tab**: Line charts showing temporal patterns
2. **Top Models Tab**: Bar charts and pie charts for model analysis
3. **Geographic Tab**: World map and market share visualizations
4. **Correlations Tab**: Heatmap and scatter plots
5. **Data Explorer Tab**: Raw data viewer with download functionality

## 🔧 Customization

To customize the dashboard:

1. **Change colors**: Modify the color schemes in the Plotly charts
2. **Add visualizations**: Add new tabs or charts in `app.py`
3. **Modify filters**: Update the sidebar filters section
4. **Update styling**: Edit the custom CSS in the markdown section

## 📝 File Structure

```
Data_Visualization/
│
├── app.py                                      # Main Streamlit application
├── requirements.txt                             # Python dependencies
├── BMW sales data (2010-2024) (1).csv          # Dataset
├── README.md                                    # Documentation
├── .gitignore                                   # Git ignore file
└── BMW.ipynb                                    # Original analysis notebook
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 🐛 Troubleshooting

### CSV File Not Found
- Ensure the CSV file is in the same directory as `app.py`
- Check that the filename matches exactly: `BMW sales data (2010-2024) (1).csv`

### Deployment Issues
- Verify all files are committed to GitHub
- Check that `requirements.txt` includes all dependencies
- Ensure the CSV file is not too large (max 200MB for free tier)

### Performance Issues
- The dashboard uses data sampling for large datasets
- Consider filtering data before visualization
- Use the year range filter to reduce data load

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and Plotly**
