"""
NLP Utilities and Analytics for News Classification System
"""

import pandas as pd
import numpy as np
from collections import Counter
import re

def analyze_text_features(df):
    """Analyze text features of articles"""
    df['word_count'] = df['article'].apply(lambda x: len(x.split()))
    df['char_count'] = df['article'].apply(lambda x: len(x))
    df['avg_word_length'] = df['article'].apply(lambda x: np.mean([len(w) for w in x.split()]))
    df['unique_words'] = df['article'].apply(lambda x: len(set(x.split())))
    
    return df

def generate_category_statistics(df):
    """Generate statistics by category"""
    stats = []
    
    for category in df['category'].unique():
        category_df = df[df['category'] == category]
        
        stat = {
            'Category': category,
            'Article Count': len(category_df),
            'Avg Word Count': category_df['word_count'].mean(),
            'Avg Char Count': category_df['char_count'].mean(),
            'Avg Unique Words': category_df['unique_words'].mean(),
            'Percentage': (len(category_df) / len(df)) * 100
        }
        stats.append(stat)
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/category_statistics.csv', index=False)
    print("✓ Category statistics saved")
    return stats_df

def extract_keywords_by_category(df):
    """Extract top keywords for each category"""
    keywords_data = []
    
    for category in df['category'].unique():
        category_articles = df[df['category'] == category]['article'].str.lower()
        
        # Extract words
        all_words = []
        for article in category_articles:
            words = re.findall(r'\b\w+\b', article)
            all_words.extend(words)
        
        # Get top 10 keywords
        word_freq = Counter(all_words)
        top_keywords = word_freq.most_common(10)
        
        for idx, (keyword, freq) in enumerate(top_keywords, 1):
            keywords_data.append({
                'Category': category,
                'Rank': idx,
                'Keyword': keyword,
                'Frequency': freq
            })
    
    keywords_df = pd.DataFrame(keywords_data)
    keywords_df.to_csv('/home/ubuntu/category_keywords.csv', index=False)
    print("✓ Category keywords saved")
    return keywords_df

def analyze_text_complexity(df):
    """Analyze text complexity metrics"""
    complexity_data = []
    
    for idx, row in df.iterrows():
        article = row['article']
        words = article.split()
        
        # Calculate metrics
        word_count = len(words)
        unique_words = len(set(words))
        avg_word_length = np.mean([len(w) for w in words]) if words else 0
        
        # Lexical diversity (Type-Token Ratio)
        lexical_diversity = unique_words / word_count if word_count > 0 else 0
        
        complexity_data.append({
            'Category': row['category'],
            'Word Count': word_count,
            'Unique Words': unique_words,
            'Avg Word Length': avg_word_length,
            'Lexical Diversity': lexical_diversity
        })
    
    complexity_df = pd.DataFrame(complexity_data)
    complexity_df.to_csv('/home/ubuntu/text_complexity.csv', index=False)
    print("✓ Text complexity analysis saved")
    return complexity_df

def identify_category_patterns(df):
    """Identify patterns in each category"""
    patterns = []
    
    for category in df['category'].unique():
        category_df = df[df['category'] == category]
        
        pattern = {
            'Category': category,
            'Total Articles': len(category_df),
            'Min Word Count': category_df['word_count'].min(),
            'Max Word Count': category_df['word_count'].max(),
            'Median Word Count': category_df['word_count'].median(),
            'Std Dev Word Count': category_df['word_count'].std(),
            'Min Unique Words': category_df['unique_words'].min(),
            'Max Unique Words': category_df['unique_words'].max(),
            'Median Unique Words': category_df['unique_words'].median()
        }
        patterns.append(pattern)
    
    patterns_df = pd.DataFrame(patterns)
    patterns_df.to_csv('/home/ubuntu/category_patterns.csv', index=False)
    print("✓ Category patterns saved")
    return patterns_df

def generate_classification_insights(df):
    """Generate insights for classification"""
    insights = []
    
    # Overall statistics
    insights.append({
        'Metric': 'Total Articles',
        'Value': len(df),
        'Description': 'Total number of articles in dataset'
    })
    
    insights.append({
        'Metric': 'Total Categories',
        'Value': df['category'].nunique(),
        'Description': 'Number of news categories'
    })
    
    insights.append({
        'Metric': 'Avg Article Length',
        'Value': f"{df['word_count'].mean():.2f}",
        'Description': 'Average words per article'
    })
    
    # Category distribution
    category_dist = df['category'].value_counts()
    most_common = category_dist.idxmax()
    least_common = category_dist.idxmin()
    
    insights.append({
        'Metric': 'Most Common Category',
        'Value': most_common,
        'Description': f"{category_dist[most_common]} articles ({category_dist[most_common]/len(df)*100:.1f}%)"
    })
    
    insights.append({
        'Metric': 'Least Common Category',
        'Value': least_common,
        'Description': f"{category_dist[least_common]} articles ({category_dist[least_common]/len(df)*100:.1f}%)"
    })
    
    insights_df = pd.DataFrame(insights)
    insights_df.to_csv('/home/ubuntu/classification_insights.csv', index=False)
    print("✓ Classification insights saved")
    return insights_df

def generate_model_recommendations(results):
    """Generate model recommendations based on performance"""
    recommendations = []
    
    best_model = max(results, key=lambda x: results[x]['accuracy'])
    
    recommendations.append({
        'Recommendation': 'Best Performing Model',
        'Model': best_model,
        'Accuracy': f"{results[best_model]['accuracy']:.4f}",
        'Action': 'Deploy this model for production use'
    })
    
    # Check for overfitting
    for model_name, result in results.items():
        if result['accuracy'] > 0.99:
            recommendations.append({
                'Recommendation': 'Potential Overfitting',
                'Model': model_name,
                'Accuracy': f"{result['accuracy']:.4f}",
                'Action': 'Validate on independent test set'
            })
    
    # Balanced performance
    for model_name, result in results.items():
        precision = result['precision']
        recall = result['recall']
        if abs(precision - recall) < 0.05:
            recommendations.append({
                'Recommendation': 'Balanced Performance',
                'Model': model_name,
                'Accuracy': f"{result['accuracy']:.4f}",
                'Action': 'Good balance between precision and recall'
            })
    
    rec_df = pd.DataFrame(recommendations)
    rec_df.to_csv('/home/ubuntu/model_recommendations.csv', index=False)
    print("✓ Model recommendations saved")
    return rec_df

def main():
    print("="*80)
    print("NEWS CLASSIFICATION NLP UTILITIES")
    print("="*80)
    
    # Load dataset
    print("\n[Step 1] Loading news dataset...")
    df = pd.read_csv('/home/ubuntu/news_articles.csv')
    print(f"✓ Dataset loaded: {len(df)} articles")
    
    # Analyze text features
    print("\n[Step 2] Analyzing text features...")
    df = analyze_text_features(df)
    print("✓ Text features analyzed")
    
    # Generate category statistics
    print("\n[Step 3] Generating category statistics...")
    stats_df = generate_category_statistics(df)
    print(stats_df.to_string(index=False))
    
    # Extract keywords
    print("\n[Step 4] Extracting category keywords...")
    keywords_df = extract_keywords_by_category(df)
    print("✓ Keywords extracted for each category")
    
    # Analyze text complexity
    print("\n[Step 5] Analyzing text complexity...")
    complexity_df = analyze_text_complexity(df)
    print("✓ Text complexity metrics calculated")
    
    # Identify patterns
    print("\n[Step 6] Identifying category patterns...")
    patterns_df = identify_category_patterns(df)
    print(patterns_df.to_string(index=False))
    
    # Generate insights
    print("\n[Step 7] Generating classification insights...")
    insights_df = generate_classification_insights(df)
    print(insights_df.to_string(index=False))
    
    print("\n" + "="*80)
    print("NLP UTILITIES ANALYSIS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main()
