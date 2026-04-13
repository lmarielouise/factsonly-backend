# FactsOnly Backend

Backend automatisé pour FactsOnly qui récupère les flux RSS toutes les 5 minutes via GitHub Actions.

## 🚀 Installation

### 1. Créer un nouveau repository GitHub

1. Allez sur https://github.com/new
2. Nommez-le : `factsonly-backend`
3. Cochez "Public"
4. Créez le repository

### 2. Uploader les fichiers

Uploadez ces fichiers dans le repository :
- `fetch_rss.py` (script principal)
- `requirements.txt` (dépendances)
- `.github/workflows/update-rss.yml` (workflow GitHub Actions)

### 3. Activer GitHub Actions

1. Allez dans l'onglet **Actions** de votre repo
2. Activez les workflows si demandé
3. Le script se lancera automatiquement toutes les 5 minutes !

### 4. Premier lancement manuel

1. Allez dans **Actions** → **Update RSS Feeds**
2. Cliquez sur **Run workflow** → **Run workflow**
3. Attendez ~30 secondes
4. Le fichier `articles.json` sera créé !

## 📊 Récupérer les données

L'URL de votre fichier JSON sera :
```
https://raw.githubusercontent.com/VOTRE_USERNAME/factsonly-backend/main/articles.json
```

Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub.

## 🔧 Modifier la fréquence

Dans `.github/workflows/update-rss.yml`, ligne 5 :
```yaml
- cron: '*/5 * * * *'  # Toutes les 5 minutes
- cron: '*/10 * * * *' # Toutes les 10 minutes
- cron: '0 * * * *'    # Toutes les heures
```

## 📝 Structure du JSON

```json
{
  "francophone": [
    {
      "id": "...",
      "source": "Le Monde",
      "title": "Titre de l'article",
      "excerpt": "Résumé...",
      "link": "https://...",
      "time": "Il y a 2h",
      "pubDate": 1234567890,
      "multiSource": true,
      "sources": ["Le Monde", "Le Figaro"],
      "sourceCount": 2
    }
  ],
  "anglophone": [...],
  "lastUpdate": "2024-01-15T10:30:00"
}
```

## ✅ Avantages

- ✅ **Gratuit** : GitHub Actions offre 2000 minutes/mois gratuitement
- ✅ **Automatique** : Mise à jour toutes les 5 minutes sans intervention
- ✅ **Rapide** : Chargement instantané pour les utilisateurs
- ✅ **Pas de CORS** : Le JSON est accessible publiquement
- ✅ **Dédupliqué** : Les doublons sont déjà supprimés côté serveur
