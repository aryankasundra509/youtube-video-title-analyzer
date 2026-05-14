import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from textblob import TextBlob
import joblib
import time

df = pd.read_csv("Cleaned_With_Subscribers.csv")

# ── Dates convert karo ───────────────────────────────────────
df["publishedAt"]   = pd.to_datetime(df["publishedAt"], errors="coerce").dt.tz_localize(None)
df["trending_date"] = pd.to_datetime(df["trending_date"], errors="coerce").dt.tz_localize(None)

# ── Feature 1: Days to Trend ─────────────────────────────────
df["Days_to_Trend"] = (df["trending_date"] - 
                        df["publishedAt"]).dt.days
df["Days_to_Trend"] = df["Days_to_Trend"].clip(lower=0)

# ── Feature 2: Publish Hour ──────────────────────────────────
# Kab upload kiya — ye creator control karta hai
df["Publish_Hour"] = df["publishedAt"].dt.hour

# ── Feature 3: Title Features ────────────────────────────────
df["Title_Length"] = df["title"].apply(lambda x: len(str(x)))

df["Title_Uppercase_Count"] = df["title"].apply(
    lambda x: sum(1 for c in str(x) if c.isupper()))

df["Title_Pipe_Count"] = df["title"].str.count(r'\|')

def get_sentiment(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0.0

df["Title_Sentiment"] = df["title"].apply(get_sentiment)

# ── Feature 4: Tags Count ────────────────────────────────────
df["Tags_Count"] = df["tags"].apply(
    lambda x: len(str(x).split('|')) if pd.notna(x) else 0)

# ── Sirf ye columns rakhenge ─────────────────────────────────
# Channel_Avg_Views NAHI — leakage tha
# subscriber_count  — ye pre-upload available hai ✅

columns_to_keep = [
    'category_name',        # pre-upload ✅
    'subscriber_count',     # pre-upload ✅
    'channel_video_count',  # pre-upload ✅
    'Title_Length',         # pre-upload ✅
    'Title_Uppercase_Count',# pre-upload ✅
    'Title_Pipe_Count',     # pre-upload ✅
    'Title_Sentiment',      # pre-upload ✅
    'Tags_Count',           # pre-upload ✅
    'Publish_Hour',         # pre-upload ✅
    'view_count',           # TARGET (predict karna hai)
    'Days_to_Trend'         # TARGET (predict karna hai)
]

df_clean = df[columns_to_keep].dropna().copy()

# ── Category Encoding ────────────────────────────────────────
df_encoded = pd.get_dummies(df_clean, 
             columns=["category_name"], drop_first=True)

# ── X aur y banao ────────────────────────────────────────────
X = df_encoded.drop(columns=["view_count", "Days_to_Trend"])

# ── View Range bins banao ────────────────────────────────────
_, bins = pd.qcut(df_encoded["view_count"], q=4,
          labels=['Low','Average','Hit','Viral'], retbins=True)

range_dict = {
    'Low':     f"0 to {int(bins[1]):,}",
    'Average': f"{int(bins[1]):,} to {int(bins[2]):,}",
    'Hit':     f"{int(bins[2]):,} to {int(bins[3]):,}",
    'Viral':   f"More than {int(bins[3]):,}"
}

y_views_ranges = pd.qcut(df_encoded["view_count"], q=4,
                 labels=["Low","Average","Hit","Viral"])

# ── Train Test Split ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y_views_ranges, test_size=0.2, random_state=42)

print(f"Train size: {X_train.shape}")
print(f"Test size:  {X_test.shape}")
print(f"Features:   {list(X.columns)}")


rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    max_depth=25,      
    min_samples_leaf=2,     
    random_state=42,
    n_jobs=-1
)

start = time.time()
rf_classifier.fit(X_train, y_train)
print(f"\nTraining done in {round(time.time()-start, 2)} sec")

# ── Evaluate ─────────────────────────────────────────────────
y_pred = rf_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n====================================")
print("MODEL KI MARKSHEET")
print("====================================")
print(f"Accuracy: {round(accuracy * 100, 2)}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred))

# ── Feature Importance ───────────────────────────────────────
import pandas as pd
feat_imp = pd.Series(rf_classifier.feature_importances_,
                     index=rf_classifier.feature_names_in_)
print("\nTop Features:")
print(feat_imp.sort_values(ascending=False).head(10))

# ── Sample Prediction ────────────────────────────────────────
sample = X_test.iloc[[0]]
pred_label = rf_classifier.predict(sample)[0]
probs = rf_classifier.predict_proba(sample)[0]
confidence = round(max(probs) * 100, 2)

print(f"\nSample Prediction: {pred_label}")
print(f"Expected Views: {range_dict[pred_label]}")
print(f"Confidence: {confidence}%")

# ── Save ─────────────────────────────────────────────────────
package = {
    'model': rf_classifier,
    'bins': bins,
    'range_dict': range_dict,
    'feature_names': list(X.columns)
}

joblib.dump(package, 'youtube_views_model.pkl', compress=3)

import os
size = os.path.getsize('youtube_views_model.pkl')
print(f"\nFile size: {round(size/(1024*1024), 2)} MB")
print("Model saved!")


