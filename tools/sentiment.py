from typing import List, Dict
from textblob import TextBlob

# ==========================================
# TOOL: sentiment analyzer
# ==========================================
def analyze(texts: List[str]) -> List[Dict[str, object]]:
    """
    Performs sentiment analysis on a list of text posts.

    Args:
        texts (List[str]): A list of text strings to analyze.

    Returns:
        List[Dict[str, object]]: A list of dictionaries, one for each post, containing:
            - 'post' (str): The original text.
            - 'polarity' (float): Sentiment polarity score, ranging from -1 (negative) to 1 (positive).
            - 'subjectivity' (float): Subjectivity score, ranging from 0 (objective) to 1 (subjective).
            - 'label' (str): Sentiment classification: 'positive', 'negative', or 'neutral'.

    Description:
        This function uses TextBlob to compute the polarity and subjectivity of each text.
        It also categorizes each post into one of three sentiment labels based on polarity:
        - polarity > 0 → 'positive'
        - polarity < 0 → 'negative'
        - polarity = 0 → 'neutral'
        Use this function whenever you need to understand the sentiment of a list of text posts.
    """
    results = []
    for post in texts:
        blob = TextBlob(post)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        label = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
        results.append({
            "post": post,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "label": label
        })
    return results