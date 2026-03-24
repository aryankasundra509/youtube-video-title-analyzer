# 🎬 YouTube Video & Title Analyzer

A Machine Learning web app that predicts YouTube video's potential reach 
and analyzes video titles — trained on **248,000+ India Trending Videos**.

## 🚀 Live Demo
[Click here to open app](https://youtube-video-title-analyzer-u7zu2qg3hdvwppw5727u3a.streamlit.app)

## 📊 Features

### 1. Views Predictor
- Predicts potential view range before uploading
- Categories: Low / Average / Hit / Viral
- Shows AI Confidence %
- Based on: Category, Subscribers, Title, Tags, Upload Time

### 2. Title Analyzer
- Scores your title out of 100
- Labels: Excellent / Good / Normal / Bad
- Gives improvement suggestions
- Suggests missing keywords by category

## 🛠️ Tech Stack
- Python
- Scikit-learn (Random Forest Classifier)
- TextBlob (NLP Sentiment Analysis)
- Streamlit (Web App)
- Plotly (Gauge Chart)
- Pandas & NumPy

## 📁 Dataset
- Source: Kaggle — India YouTube Trending Videos
- Size: 248,672 rows after cleaning
- Extra: Subscriber count fetched via YouTube Data API v3

## 🤖 Model Details
- Algorithm: Random Forest Classifier
- Training Data: 198,937 rows
- Test Data: 49,735 rows
- Accuracy: 75.26%
- Classes: Low / Average / Hit / Viral

## ⚠️ Disclaimer
Predictions are based on historical patterns from India trending data.
Actual views depend on content quality, thumbnails, and promotion.

## 👨‍💻 Author
Aryan — Final Year Computer Engineering Student
