from textblob import TextBlob
import random
import re

# ════════════════════════════════════════════════════
# CATEGORY-WISE KEYWORDS — Extracted From Real Dataset
# ════════════════════════════════════════════════════

CATEGORY_KEYWORDS = {
    'Entertainment'       : ['Episode', 'Promo', 'Serial', 'Teaser', 'Trailer', 'Zee', 'Comedy', 'Prank'],
    'Music'               : ['Song', 'Punjabi', 'Hindi','Latest', 'Official', 'Audio', 'Singh', 'New Song', 'Full Video', 'Mashup'],
    'Gaming'              : ['Minecraft', 'BGMI', 'PUBG', 'Gameplay', 'Challenge', 'GTA', 'Free Fire', 'Epic', 'Win', 'Ranked'],
    'Comedy'              : ['Comedy', 'Episode', 'Part', 'Series', 'Web Series', 'Stand Up', 'Funny', 'Prank'],
    'People & Blogs'      : ['Vlog', 'Day', 'Challenge', 'Family', 'Birthday', 'Vlogs', 'Home'],
    'News & Politics'     : ['Live', 'Breaking', 'India', 'Election', 'BBC', 'Speech', 'Update', 'Latest News'],
    'Sports'              : ['Highlights', 'Match', 'India', 'IPL', 'Cup', 'World Cup', 'Test', 'Pakistan'],
    'Film & Animation'    : ['Trailer', 'Teaser', 'Movie', 'Review', 'Hindi', 'Official', 'Release'],
    'Howto & Style'       : ['Recipe', 'Cooking', 'Easy', 'Village', 'Kitchen', 'Tips', 'How To'],
    'Science & Technology': ['Unboxing', 'Review', 'iPhone', 'Pro', 'Apple', 'India', 'First Look', 'Phone', 'Samsung'],
    'Education'           : ['Current Affairs', 'Exam', 'SSC', 'Challenge', 'Hindi', 'Tips', 'Learn'],
    'Autos & Vehicles'    : ['Review', 'Mahindra', 'Tata', 'First Look', 'India', 'JCB', 'Tractor', 'Bike', 'Car'],
    'Travel & Events'     : ['Day', 'Food', 'Street', 'First', 'Vlog', 'Tour', 'Travel'],
    'Pets & Animals'      : ['Cute', 'Funny', 'Satisfying', 'Animals', 'Pets', 'Cat', 'Dog']
}

# ════════════════════════════════════════════════════
# MAIN FUNCTION
# ════════════════════════════════════════════════════

def analyze_title(title, category=None):
    title = str(title).strip()
    score = 0
    suggestions = []

    # ── Rule 1: Title Length (25 pts) ────────────────
    length = len(title)

    if 50 <= length <= 90:
        score += 25

    elif 35 <= length < 50:
        score += 15
        suggestions.append("Title is too short — ideal length is 50-90 characters")

    elif 90 < length <= 100:
        score += 18
        suggestions.append("Title is near the limit — removing 2-3 words")
    
    else:
        score += 5
        suggestions.append("Title is too short — make it more descriptive")


    # ── Rule 2: Word Count (25 pts) ──────────────────
    words = title.split()
    word_count = len(words)
    
    if 10 <= word_count <= 17:
        score += 25

    elif 7 <= word_count < 10:
        score += 15
        suggestions.append("Add 2-3 more keywords to your title")

    elif word_count > 17:
        score += 12
        suggestions.append("Too many words — remove unnecessary ones")

    else:
        score += 5


    # ── Rule 3: Pipe Count (20 pts) ──────────────────
    pipe_count = title.count('|')

    if 1 <= pipe_count <= 4:
        score += 20

    elif pipe_count == 0:
        score += 7
        suggestions.append("Use '|' separator in title — common in Indian YouTube")

    else:
        score += 10
        suggestions.append("Too many '|' separators — keep it between 1 to 4")

    # ── Rule 4: Has Numbers (15 pts) ─────────────────
    has_number = bool(re.search(r'\d', title))

    if has_number:
        score += 15

    else:
        score += 10

        # Give suggestions in specific category
        if category in ['News & Politics', 'Education', 'Science & Technology', 'People & Blogs']:
            suggestions.append("Adding a year or number can boost clicks — e.g. '2024'")

    # ── Rule 6: Sentiment (15 pts) ───────────────────
    sentiment_score = TextBlob(title).sentiment.polarity

    SKIP_SENTIMENT_CATEGORIES = ['Gaming', 'Sports', 'Comedy']

    if category in SKIP_SENTIMENT_CATEGORIES:
        score += 15

    elif sentiment_score > 0.1:
        score += 15
        
    elif sentiment_score < -0.1:
        score += 8
        suggestions.append("Title has negative tone — try making it more positive")

    else:
        score += 10
        suggestions.append("Add an emotional hook — e.g. Amazing, Best, Must Watch")


    # ── Final Label ───────────────────────────────────
    if score >= 88:
        label = "🔥 Excellent"
    
    elif score >= 75:
        label = "⚡ Good"

    elif score >= 50:
        label = "🟠 Normal"

    else:
        label = "❌ Bad"
    

    # ── Suggestions ───────────────────────────────────
    # Remove same suggestions
    suggestions = list(dict.fromkeys(suggestions))

    # Print max Suggestions
    suggestions = suggestions[:4]


    # ── Category Keywords Suggestion ───────────────
    # Check input category(1) in category_keyword
    if category and category in CATEGORY_KEYWORDS:
        title_lower = title.lower()
        all_keywords = CATEGORY_KEYWORDS[category]

        missing_keywords = [kw for kw in all_keywords if kw.lower() not in title_lower]

        # 5 Keyword Suggested
        if len(missing_keywords) >= 5:
            keyword_suggestions = random.sample(missing_keywords, 5)

        else:
            keyword_suggestions = missing_keywords

    else:
        keyword_suggestions = []

    return {
        'score'               : score,
        'label'               : label,
        'suggestions'         : suggestions,
        'keyword_suggestions' : keyword_suggestions
    }


# ════════════════════════════════════════════════════
# TEST
# ════════════════════════════════════════════════════

result = analyze_title("Battlefield", "Gaming")

print(f"Score       : {result['score']} / 100")
print(f"Label       : {result['label']}")

print(f"\nSuggestions :")
for i, s in enumerate(result['suggestions'], start=1):
    print(f" {i}. {s}")

print(f"\nKeywords to add:")
print(f" {' | '.join(result['keyword_suggestions'])}")
