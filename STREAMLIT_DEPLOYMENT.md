# SOULFRIEND V3.0 - Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud

### Prerequisites:
1. GitHub repository: `NhatNgo246/Mentalhealth`
2. Streamlit Cloud account
3. Google Gemini API key

### Steps to Deploy:

#### 1. Go to Streamlit Cloud
Visit: https://share.streamlit.io

#### 2. Connect GitHub Repository
- Click "New app"
- Choose "From existing repo"
- Repository: `NhatNgo246/Mentalhealth`
- Branch: `codespace-supreme-space-waffle-697prx45r6v624776` or `main`
- Main file path: `SOULFRIEND.py`

#### 3. Configure Secrets
In your Streamlit Cloud app settings:
- Go to Settings > Secrets
- Add the following:

```toml
[gemini]
api_key = "AIzaSyCAX2r_vMJE7-41bpBb6MBMEyLDBkmO6BE"
```

#### 4. Deploy
Click "Deploy" and wait for the app to build!

## 🌟 Features Included:
- 💬 CHUN Chatbot with enhanced personality
- ⚡ Enter key support for messaging
- 🔤 Typing animation effects
- 🎭 Bipolar disorder survivor personality
- 📱 Responsive design
- 🔧 Admin panel
- 📊 Analytics dashboard
- 🌍 Multi-language support

## 🔗 Live App URL:
Your app will be available at: `https://{app-name}.streamlit.app`

## 🛠️ Troubleshooting:
- If deployment fails, check the logs in Streamlit Cloud
- Ensure all dependencies are in `requirements.txt`
- Verify API key is correctly set in secrets

## 📧 Support:
Contact for deployment issues or questions about SOULFRIEND V3.0
