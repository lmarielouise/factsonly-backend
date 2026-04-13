import feedparser
import json
from datetime import datetime
import time

# Configuration des flux RSS
RSS_FEEDS = {
    "francophone": [
        {"name": "Le Monde", "url": "https://www.lemonde.fr/rss/une.xml"},
        {"name": "France Info", "url": "https://www.francetvinfo.fr/titres.rss"},
        {"name": "Le Figaro", "url": "https://www.lefigaro.fr/rss/figaro_une.xml"},
        {"name": "Libération", "url": "https://www.liberation.fr/arc/outboundfeeds/rss-all/"}
    ],
    "anglophone": [
        {"name": "Reuters", "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"},
        {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
        {"name": "The Guardian", "url": "https://www.theguardian.com/world/rss"},
        {"name": "Associated Press", "url": "https://apnews.com/feed"},
        {"name": "NPR", "url": "https://feeds.npr.org/1001/rss.xml"}
    ]
}

def extract_excerpt(text, max_length=200):
    """Extrait un résumé du texte"""
    if not text:
        return ""
    # Enlever les balises HTML basiques
    text = text.replace('<p>', '').replace('</p>', ' ')
    text = text.replace('<br>', ' ').replace('<br/>', ' ')
    # Tronquer
    if len(text) > max_length:
        return text[:max_length].strip() + "..."
    return text.strip()

def get_time_ago(pub_date):
    """Calcule le temps écoulé"""
    try:
        pub_time = time.mktime(pub_date)
        now = time.time()
        diff = int(now - pub_time)
        
        if diff < 60:
            return "À l'instant"
        elif diff < 3600:
            return f"Il y a {diff // 60} min"
        elif diff < 86400:
            return f"Il y a {diff // 3600}h"
        elif diff < 604800:
            return f"Il y a {diff // 86400}j"
        else:
            return datetime.fromtimestamp(pub_time).strftime("%d %b")
    except:
        return "Récemment"

def fetch_feed(feed_info):
    """Récupère un flux RSS"""
    articles = []
    try:
        print(f"Fetching {feed_info['name']}...")
        feed = feedparser.parse(feed_info['url'])
        
        for entry in feed.entries[:10]:  # Limiter à 10 articles par source
            article = {
                "id": f"{feed_info['name']}-{hash(entry.get('link', ''))}",
                "source": feed_info['name'],
                "title": entry.get('title', 'Sans titre'),
                "excerpt": extract_excerpt(entry.get('summary', entry.get('description', ''))),
                "link": entry.get('link', ''),
                "time": get_time_ago(entry.get('published_parsed', time.localtime())),
                "pubDate": time.mktime(entry.get('published_parsed', time.localtime()))
            }
            articles.append(article)
        
        print(f"✓ {feed_info['name']}: {len(articles)} articles")
    except Exception as e:
        print(f"✗ Erreur {feed_info['name']}: {e}")
    
    return articles

def calculate_similarity(title1, title2):
    """Calcule la similarité entre deux titres"""
    words1 = set(title1.lower().split())
    words2 = set(title2.lower().split())
    
    # Filtrer les mots courts
    words1 = {w for w in words1 if len(w) > 3}
    words2 = {w for w in words2 if len(w) > 3}
    
    if not words1 or not words2:
        return 0
    
    common = words1.intersection(words2)
    total = words1.union(words2)
    
    return len(common) / len(total)

def remove_duplicates(articles):
    """Supprime les doublons et fusionne les sources"""
    unique_articles = []
    processed = set()
    
    for i, article in enumerate(articles):
        if i in processed:
            continue
        
        similar = [article]
        
        # Chercher les articles similaires
        for j in range(i + 1, len(articles)):
            if j in processed:
                continue
            
            similarity = calculate_similarity(article['title'], articles[j]['title'])
            
            if similarity > 0.5:  # 50% de similarité
                similar.append(articles[j])
                processed.add(j)
        
        # Fusionner si plusieurs sources
        if len(similar) > 1:
            article['sources'] = [a['source'] for a in similar]
            article['multiSource'] = True
            article['sourceCount'] = len(similar)
        
        unique_articles.append(article)
        processed.add(i)
    
    return unique_articles

def main():
    """Fonction principale"""
    print("🚀 FactsOnly RSS Fetcher")
    print("=" * 50)
    
    all_data = {}
    
    for language, feeds in RSS_FEEDS.items():
        print(f"\n📰 Fetching {language} sources...")
        articles = []
        
        for feed in feeds:
            articles.extend(fetch_feed(feed))
        
        # Trier par date
        articles.sort(key=lambda x: x['pubDate'], reverse=True)
        
        # Supprimer les doublons
        articles = remove_duplicates(articles)
        
        # Limiter à 30 articles
        articles = articles[:30]
        
        all_data[language] = articles
        print(f"✓ {language}: {len(articles)} articles uniques")
    
    # Ajouter le timestamp
    all_data['lastUpdate'] = datetime.now().isoformat()
    
    # Sauvegarder en JSON
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ articles.json créé avec succès!")
    print(f"📊 Total: {sum(len(v) for k, v in all_data.items() if k != 'lastUpdate')} articles")

if __name__ == "__main__":
    main()
