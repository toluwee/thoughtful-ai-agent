# Deployment Guide

## Quick Start

### Local Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Windows One-Click

Double-click `RUN_APP.bat` in the project root.

## Cloud Deployment

### Streamlit Community Cloud (Recommended)

1. Push to GitHub
2. Go to: https://share.streamlit.io
3. Deploy: Select your repository
4. Configure: Main file = app.py
5. Launch: Click Deploy

### Repl.it (Preferred for Demos)

1. Go to: https://replit.com
2. Import: From GitHub repository
3. Click: Run button

## Troubleshooting

### Port Already in Use
streamlit run app.py --server.port 8502

### Dependencies Issues
pip install --upgrade -r requirements.txt
