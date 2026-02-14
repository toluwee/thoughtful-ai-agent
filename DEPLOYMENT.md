# 🚀 Deployment Guide

## Thoughtful AI Customer Support Agent

This guide provides step-by-step instructions for deploying the Thoughtful AI Customer Support Agent.

---

## 📋 Pre-Deployment Checklist

- [ ] Python 3.8+ installed (`python --version` or `python3 --version`)
- [ ] pip package manager available
- [ ] Git installed (for cloning repository)
- [ ] 50MB free disk space
- [ ] Internet connection (for installing dependencies)

---

## 🖥️ Local Deployment

### Option 1: Standard Installation

```bash
# Navigate to the project directory
cd thoughtful-ai-agent

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will start at `http://localhost:8501`

### Option 2: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

---

## ☁️ Cloud Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)

**Advantages:**
- Free hosting
- Automatic HTTPS
- Easy deployment from GitHub
- Auto-reload on git push

**Steps:**

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Thoughtful AI Support Agent"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file path: `app.py`
   - Click "Deploy"

3. **Access your app**
   - Your app will be available at: `https://<your-app-name>.streamlit.app`

### Option 2: Repl.it (For Quick Demo)

**Advantages:**
- No installation required
- Share with a link
- Browser-based IDE

**Steps:**

1. **Create a new Repl**
   - Go to [repl.it](https://repl.it)
   - Create new Repl
   - Choose "Python" template

2. **Upload files**
   - Upload all project files
   - Ensure directory structure matches

3. **Configure Run Command**
   - Create `.replit` file:
   ```toml
   run = "streamlit run app.py --server.headless true --server.port 8501"
   ```

4. **Install Dependencies**
   - Repl.it will automatically install from `requirements.txt`

5. **Run and Share**
   - Click "Run" button
   - Use "Share" link to distribute

### Option 3: Heroku

**Steps:**

1. **Create `Procfile`**
   ```
   web: streamlit run app.py --server.port=$PORT --server.headless=true
   ```

2. **Create `runtime.txt`**
   ```
   python-3.11.0
   ```

3. **Deploy**
   ```bash
   heroku create thoughtful-ai-agent
   git push heroku main
   heroku open
   ```

### Option 4: Docker

**Create `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

**Build and run:**
```bash
docker build -t thoughtful-ai-agent .
docker run -p 8501:8501 thoughtful-ai-agent
```

---

## 🔧 Configuration

### Environment Variables

For production deployment, consider these optional configurations:

```bash
# .streamlit/config.toml
[server]
port = 8501
headless = true
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Knowledge Base Updates

To update the knowledge base in production:

1. **Edit `data/knowledge_base.json`**
2. **Restart the application**

For zero-downtime updates:
- Use environment variables for KB path
- Implement hot-reloading
- Use external database

---

## 🧪 Testing Deployment

### Health Check

Visit these endpoints after deployment:

1. **Main App**: `http://your-domain:8501`
2. **Health Check**: `http://your-domain:8501/_stcore/health`

### Functional Tests

Run these test questions:

```
✅ "What does the eligibility verification agent (EVA) do?"
   Expected: Detailed answer about EVA

✅ "Tell me about CAM"
   Expected: Information about Claims Processing Agent

✅ "What's the weather?"
   Expected: Fallback response with sample questions
```

---

## 📊 Monitoring

### Streamlit Cloud Metrics

- View logs in Streamlit Cloud dashboard
- Monitor app health and uptime
- Track resource usage

### Custom Logging

Add logging to `app.py`:

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## 🔒 Security Considerations

### Production Checklist

- [ ] Remove debug logging
- [ ] Add rate limiting
- [ ] Implement input sanitization
- [ ] Add HTTPS (automatic with Streamlit Cloud)
- [ ] Set up authentication if needed
- [ ] Regular dependency updates
- [ ] Monitor for security vulnerabilities

### Rate Limiting (Advanced)

```python
from streamlit_autorefresh import st_autorefresh
import time

# Add to app.py
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0

current_time = time.time()
if current_time - st.session_state.last_request_time < 1:
    st.warning("Please wait a moment before sending another message.")
    st.stop()

st.session_state.last_request_time = current_time
```

---

## 🚨 Troubleshooting Deployment

### Common Issues

**1. Module Not Found Error**
```bash
# Solution: Verify requirements.txt installed
pip install -r requirements.txt --upgrade
```

**2. Port Already in Use**
```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

**3. Knowledge Base Not Found**
```bash
# Solution: Check file paths
ls -la data/knowledge_base.json
```

**4. Slow Loading**
```bash
# Solution: Enable caching in app.py
@st.cache_resource
def initialize_agent():
    # ... existing code
```

---

## 📈 Performance Optimization

### Caching

Add to `app.py`:

```python
@st.cache_resource
def initialize_agent():
    """Cache the agent initialization"""
    kb_path = Path(__file__).parent / "data" / "knowledge_base.json"
    kb = KnowledgeBase(str(kb_path))
    return ThoughtfulAIResponder(kb, similarity_threshold=0.6)
```

### Resource Limits

For Streamlit Cloud:
- Max file size: 1GB
- Max RAM: 1GB
- Max CPU: Shared

---

## 🔄 Continuous Deployment

### GitHub Actions (Example)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger Streamlit Deploy
        run: echo "Streamlit Cloud auto-deploys on push"
```

---

## 📝 Post-Deployment Checklist

- [ ] Test all sample questions
- [ ] Verify fallback responses work
- [ ] Check mobile responsiveness
- [ ] Test error handling
- [ ] Verify conversation history works
- [ ] Test clear chat functionality
- [ ] Check sidebar sample questions
- [ ] Verify confidence badges display
- [ ] Test with different browsers
- [ ] Share link with team for feedback

---

## 🎯 Next Steps After Deployment

1. **Gather User Feedback**
   - Monitor usage patterns
   - Collect common questions
   - Identify missing Q&A pairs

2. **Expand Knowledge Base**
   - Add more Q&A pairs based on feedback
   - Improve existing answers
   - Add follow-up question handling

3. **Enhance Features**
   - Add analytics dashboard
   - Implement user feedback mechanism
   - Add export conversation feature
   - Integrate with ticketing system

4. **Scale**
   - Move to production-grade hosting
   - Add database for conversation history
   - Implement A/B testing
   - Add multi-language support

---

**Deployment Support:**
- For Streamlit Cloud issues: [docs.streamlit.io](https://docs.streamlit.io)
- For Python issues: Check Python version compatibility
- For dependency issues: Update requirements.txt versions

**Good luck with your deployment! 🚀**
