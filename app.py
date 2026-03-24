import streamlit as st
import joblib
import pandas as pd
from textblob import TextBlob
import plotly.graph_objects as go
import datetime

# Title analyzer banaya vo function import kiya
from Title_Analyzer import analyze_title

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title= "YouTube Video & Title Analyzer", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
        [data-testid="stTab"] {
            font-size: 20px !important;
            padding: 12px 23px !important;
            font-weight: 600 !important;
        }
        [data-testid="stTab"] p {
            font-size: 20px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title ----------------
st.title("🎬 YouTube Video & Title Analyzer")
st.markdown("Predict your video's potential reach and optimize your title — based on **250k India Trending Videos**")

st.divider()

# ==========================================
# LOAD AI MODELS
# ==========================================

# @st.cache_resource lagane se model baar-baar load nahi hota, website fast chalti hai
@st.cache_resource
def load_model():
    return joblib.load("youtube_views_model.pkl")

package = load_model()
model = package["model"]
bins = package["bins"]
range_dict = package["range_dict"]
feature_names = package["feature_names"]

# ==========================================
# Creating Tabs
# ==========================================

tab1, tab2 = st.tabs(["📊 Views Predictor", "✍️ Title Analyzer"])

with tab1:
    st.header("📊 Views Predictor")
    st.write("Fill in your video details to predict potential views")

    # Form banao
    with st.form("prediction_form"):
        st.subheader("📋 Video Details")

        # 2 columns form ke andar
        f1, f2 = st.columns(2)

        with f1:
            category = st.selectbox(
                "Select Category",
                options=[
                    'Entertainment', 'Music', 'Gaming', 'Comedy',
                    'People & Blogs', 'News & Politics', 'Sports',
                    'Film & Animation', 'Howto & Style',
                    'Science & Technology', 'Education',
                    'Autos & Vehicles', 'Travel & Events',
                    'Pets & Animals'
                ]
            )
            subscribers = st.number_input(
                "Channel Subscribers",
                min_value=0,
                max_value=500000000,
                value=100000,
                step=1000
            )
            channel_videos = st.number_input(
                "Total Videos on Channel",
                min_value=0,
                max_value=100000,
                value=50,
                step=1
            )
            tags_count = st.number_input(
                "Number of Tags",
                min_value=0,
                max_value=50,
                value=10,
                step=1
            )

        with f2:
            title = st.text_input(
                "Video Title",
                placeholder="Enter your video title here..."
            )
            publish_hour = st.slider(
                "Upload Time",
                min_value=0,
                max_value=23,
                value=18,
                format="%d:00"
            )
            publish_day = st.selectbox(
                "Upload Day",
                options=[
                    'Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday'
                ]
            )
            day_map = {
                'Monday':0, 'Tuesday':1, 'Wednesday':2,
                'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6
            }
            publish_day_num = day_map[publish_day]

        # Form submit button
        predict_button = st.form_submit_button(
            "🔍 Predict Views",
            use_container_width=True
        )


    if predict_button:
        if not title.strip():
            st.warning("⚠️ Please enter a video title first!")
        else:
            # Features calculate karo
            title_length          = len(title)
            title_uppercase_count = sum(1 for c in str(title) if c.isupper())
            title_pipe_count      = title.count('|')
            title_sentiment       = TextBlob(str(title)).sentiment.polarity

            # Input DataFrame
            input_data = pd.DataFrame([{
                'subscriber_count'      : subscribers,
                'channel_video_count'   : channel_videos,
                'Title_Length'          : title_length,
                'Title_Uppercase_Count' : title_uppercase_count,
                'Title_Pipe_Count'      : title_pipe_count,
                'Title_Sentiment'       : title_sentiment,
                'Tags_Count'            : tags_count,
                'Publish_Hour'          : publish_hour,
                'Publish_Day'           : publish_day_num,
            }])

            # Category encoding
            all_categories = [
                'Comedy', 'Education', 'Entertainment',
                'Film & Animation', 'Gaming', 'Howto & Style',
                'Music', 'News & Politics', 'People & Blogs',
                'Pets & Animals', 'Science & Technology',
                'Sports', 'Travel & Events'
            ]
            for cat in all_categories:
                input_data[f'category_name_{cat}'] = 1 if category == cat else 0

            input_data = input_data[feature_names]

            # Prediction
            predicted_label = model.predict(input_data)[0]
            probabilities   = model.predict_proba(input_data)[0]
            confidence      = round(max(probabilities) * 100, 2)
            view_range      = range_dict[predicted_label]

            # Colors
            dot_colors = {
                'Low'    : '#FF4444',
                'Average': '#FFA500',
                'Hit'    : '#FFD700',
                'Viral'  : '#00C851'
            }
            dot_color = dot_colors[predicted_label]

            output_html = f"""
                <div style="border: 2px solid {dot_color}; border-radius: 15px; padding: 25px; margin-top: 20px; max-width: 750px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 20px; height: 20px; border-radius: 50%; background-color: {dot_color};"></div>
                        <h2 style="margin: 0; color: {dot_color};">{predicted_label}</h2>
                    </div>
                    <h1 style="color: white; margin: 0;">Expected Views: {view_range}</h1>
                    <h2 style="font-size: 48px; margin: 10px 0; color: white;">{confidence}% Confidence</h2>
                    <hr style="border-color: {dot_color}; margin: 15px 0;">
                </div>
            """

            st.markdown(output_html, unsafe_allow_html=True)

            st.info("⚠️ Note: Prediction is based on channel strength, subscribers & category patterns.  Actual views also depend on content quality, thumbnail, and promotion.")



        

# ==========================================
# Title Analyzer
# ==========================================

with tab2:
    st.header("✍️ Title Analyzer")
    st.write("Analyze your video title and get optimization suggestions")

    with st.form("title_form", width="stretch"):
        st.subheader("📋 Title Details")

        user_title = st.text_input("Video Title", placeholder="Enter your video title here...")

        user_category = st.selectbox("Select Category",
                options=['Entertainment', 'Music', 'Gaming', 'Comedy',
                    'People & Blogs', 'News & Politics', 'Sports',
                    'Film & Animation', 'Howto & Style','Science & Technology', 
                    'Education','Autos & Vehicles', 'Travel & Events',
                    'Pets & Animals'])
        
        analyze_button = st.form_submit_button("🔍 Analyze Title")

    if analyze_button:
        if not user_title.strip():
            st.warning("⚠️ Please enter a video title first!")
        else:
            result = analyze_title(user_title, user_category)

            score = result['score']
            label       = result['label']
            suggestions = result['suggestions']
            keywords    = result['keyword_suggestions']

            # score wise color decode
            if score >= 88:
                gauge_color = "#00C851"    # Green
            elif score >= 75:
                gauge_color = "#2196F3"    # Blue
            elif score >= 50:
                gauge_color = "#FFA600"    # Orange
            else:
                gauge_color = "#FF4444"    # Red

            # Plotly Gauge Chart
            fig = go.Figure(go.Indicator(
                mode  = "gauge+number",
                value = score,
                title = {'text': "Title Score", 'font': {'size': 20}},
                gauge = {
                    'axis'    : {'range': [0, 100]},
                    'bar'     : {'color': gauge_color},
                    'bgcolor' : "gray",
                    'steps'   : [
                        {'range': [0, 50],   'color': '#2d2d2d'},
                        {'range': [50, 75],  'color': '#2d2d2d'},
                        {'range': [75, 88],  'color': '#2d2d2d'},
                        {'range': [88, 100], 'color': '#2d2d2d'},
                    ],
                    'threshold': {
                        'line' : {'color': gauge_color, 'width': 4},
                        'thickness': 0.75,
                        'value': score
                    }
                }
            ))

            fig.update_layout(
                height          = 200,
                width           = 280,
                margin          = dict(t=40, b=0, l=20, r=20),
                paper_bgcolor   = "rgba(0,0,0,0)",
                font_color      = "white"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Label
            st.markdown(f"""
                <h2 style="text-align: center; color: {gauge_color};">
                    {label}
                </h2>
            """, unsafe_allow_html=True)

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                # Suggestions
                if suggestions:
                    st.markdown("### 💡 Suggestions")
                    for i, s in enumerate(suggestions, 1):
                        st.markdown(f"""
                            <p style="font-size: 20px; 
                                    line-height: 2.0; 
                                    margin: 8px 0;">
                                {i}. {s}
                            </p>
                        """, unsafe_allow_html=True)

            st.divider()

            with col2:

                # Keywords
                if keywords:
                    st.markdown("### 🔑 Keywords to Add")
                    spaced_keywords = ' &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; '.join(keywords)
                    st.markdown(f"""
                        <p style="font-size: 20px; 
                                line-height: 2.0;
                                letter-spacing: 0.5px;">
                            {spaced_keywords}
                        </p>
                    """, unsafe_allow_html=True)