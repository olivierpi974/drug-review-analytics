# Loading Essential Libraries
import pandas as pd
import numpy as np
import re


# =================================================================
# I. FUNCTION DEFINITION (CLEANING AND PREPROCESSING)
# =================================================================

def clean_condition(df, col_name):
    """ Cleans the 'condition' column: removes HTML tags, counters, and normalizes spaces. """

    # Pattern to remove counters like "10 users found this helpful..."
    pattern_counter = re.compile(r'\d+\s*(?:</span?>\s*users?(?:\s+found.*?(?:helpful))?\s*\.{0,3})', re.IGNORECASE)

    def clean_one(t):
        if isinstance(t, str):
            # Suppression of the counter
            t = re.sub(pattern_counter, "", t)
            # Suppression of ellipses
            t = re.sub(r'\.\.\.', "", t)
            # Removal of multiple spaces and trim
            t = re.sub(r'\s+', ' ', t).strip()
        return t

    df[col_name] = df[col_name].apply(clean_one)
    return df

def clean_review(df, col_name):
    """ Cleans the 'review' column: handles HTML, punctuation, and text normalization. """

    # 1. Convert to lowercase and string type
    df_review_cleaned = df[col_name].astype(str).str.lower()

    # 2. Handling of HTML entities
    df_review_cleaned = df_review_cleaned.str.replace(r'&#039', '', regex=True) # HTML apostrophe
    df_review_cleaned = df_review_cleaned.str.replace(r'&amp', ' ', regex=True) # &
    df_review_cleaned = df_review_cleaned.str.replace(r'&lt', ' ', regex=True)  # <
    df_review_cleaned = df_review_cleaned.str.replace(r'<.*?>', ' ', regex=True) # General tags

    # 3. Punctuation removal (keeps letters, numbers, and spaces)
    df_review_cleaned = df_review_cleaned.str.replace(r'[^\w\s]', ' ', regex=True)

    # 4. Cleaning multiple spaces and trimming
    df_review_cleaned = df_review_cleaned.str.replace(r'\s+', ' ', regex=True).str.strip()

    # Adding the new column to the DataFrame
    df[col_name + '_cleaned'] = df_review_cleaned

    return df


# =================================================================
# II. PIPELINE EXECUTION AND FEATURE ENGINEERING
# =================================================================

# 1. DATA LOADING (Use the FULL dataset)
df = pd.read_csv('data/drugsComTrain_raw.csv',parse_dates=[5])

# 2. TEXTUAL COLUMN CLEANING
df = clean_condition(df, 'condition')
df = clean_review(df, 'review')


# 3. CREATING KEY INDICATORS

# a) Simplified Sentiment Analysis (based on 'rating')
conditions_sent = [
    (df['rating'] >= 7), # Positive
    (df['rating'] <= 3)  # Negative
]
choices_sent = ['Positive', 'Negative']
df['sentiment_simple'] = np.select(conditions_sent, choices_sent, default='Neutral')

# b) Security Alert Indicator (PV)
alert_word = [
    'hospitaliz', 'emergency room', 'urgent care', 'fatal', 'death', 'died',
    'suicidal', 'overdose', 'recalled', 'withdrawal', 'stopped immediately',
    'discontinued', 'cannot tolerate', 'intolerable'
]
pattern_research = '|'.join(alert_word)
df['security_alert'] = df['review_cleaned'].str.contains(pattern_research, regex=True).astype(int)

# c) Date Conversion
df['date'] = pd.to_datetime(df['date'], format='%d-%b-%Y', errors='coerce')


# 4. STRATEGIC DRUG GROUPING (PV Clustering)

# i. Identifying Frequent Drugs (threshold >= 10 reviews)
drug_count = df['drugName'].value_counts()
frequent_drug_names = drug_count[drug_count >= 10].index.tolist()

# ii. Defining classification conditions
cond_rare_alert = (
    ~df['drugName'].isin(frequent_drug_names) &
    (df['security_alert'] == 1)
)

cond_other_niche = (
    ~df['drugName'].isin(frequent_drug_names) &
    (df['security_alert'] == 0)
)

# iii. Applying numpy.select (Robust Assignment)
conditions = [cond_rare_alert, cond_other_niche]
choices = ['RARE_ALERT_TO_CHECK', 'OTHER_NICHE_DRUGS']

# The default value keeps the original drug name (for frequent drugs)
df['drug_name_grouped'] = np.select(
    condlist=conditions,
    choicelist=choices,
    default=df['drugName']
)

# =================================================================
# III. EXPORT
# =================================================================
# Liste des colonnes nécessaires pour l'analyse dans Power BI
COLUMNS_TO_KEEP = [
    'uniqueID', 'drugName', 'condition', 'rating',
    'review_cleaned', 'security_alert', 'sentiment_simple',
    'drug_name_grouped', 'date'
]

# Suppression des colonnes non nécessaires (y compris la colonne 'review' brute et 'date' non convertie si elles existent encore)
df = df[COLUMNS_TO_KEEP]
# 5. EXPORTING THE FINAL DELIVERABLE FOR POWER BI
df.to_csv('data/drug_reviews_for_powerbi_final.csv', index=False)

print("✅ Pipeline finished. 'drug_reviews_for_powerbi_final.csv' is ready for Power BI.")
