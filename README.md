# AICommHub - Telegram Bot with Multiple Integrations

*Made by Sawwax*

AICommHub est un bot Telegram multifonctionnel conçu pour offrir une expérience de communication intelligente et flexible.

## Description

AICommHub est une solution de communication tout-en-un qui combine l'intelligence artificielle, les SMS, les emails et la messagerie Telegram dans une interface unifiée. Il permet aux utilisateurs de gérer leurs communications à travers différents canaux tout en bénéficiant d'une assistance IA intelligente.

## Fonctionnalités

### 1. Intelligence Artificielle
- Traitement intelligent des messages avec OpenAI
- Réponses naturelles et contextuelles
- Assistance personnalisée pour les utilisateurs

### 2. Communication Multi-Canal
- **SMS**: Envoi de messages via Twilio
- **Email**: Communication par email via SendGrid
- **Telegram**: Interface principale du bot

### 3. Sécurité
- Authentification utilisateur via Firebase
- Protection des données sensibles
- Gestion sécurisée des sessions

### 4. Tableau de Bord
- Statistiques en temps réel
- Suivi des messages traités
- Monitoring des erreurs
- Graphiques d'activité
- Système de notifications
- Historique des messages
- État des services intégrés

## Guide des Commandes

### Commandes du Bot
- `/start` : Démarrer le bot
- `/auth` : S'authentifier
- `/help` : Afficher l'aide
- `/sms [numéro] [message]` : Envoyer un SMS
  ```
  Exemple: /sms +33612345678 Bonjour!
  ```
- `/email [destinataire] [sujet] [message]` : Envoyer un email
  ```
  Exemple: /email user@example.com "Mon sujet" Mon message
  ```

### Messages IA
Envoyez n'importe quel message au bot pour recevoir une réponse générée par l'IA.

## Tests Locaux

### Configuration de l'Environnement

1. Clonez le repository :
```bash
git clone https://github.com/Sawwwaxa/aicommhub.git
cd aicommhub
```

2. Créez un fichier `.env` à partir du template :
```bash
cp .env.example .env
```

3. Configurez les variables d'environnement requises dans `.env` :
```env
# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/aicommhub

# Bot Telegram (Requis)
TELEGRAM_BOT_TOKEN=votre_token_bot

# Firebase (Requis pour l'authentification)
FIREBASE_API_KEY=votre_api_key
FIREBASE_PROJECT_ID=votre_project_id
FIREBASE_APP_ID=votre_app_id

# OpenAI (Requis pour l'IA)
OPENAI_API_KEY=votre_api_key

# Services optionnels
TWILIO_ACCOUNT_SID=votre_sid
SENDGRID_API_KEY=votre_api_key
```

### Lancement de l'Application

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

2. Lancez l'application :
```bash
python main.py
```

3. Accédez à l'interface web :
- Ouvrez http://localhost:5000 dans votre navigateur
- Connectez-vous avec Google
- Le tableau de bord devrait afficher l'état des services

### Vérification des Fonctionnalités

1. Bot Telegram :
- Envoyez `/start` à votre bot
- Vérifiez que vous recevez une réponse

2. Tableau de bord :
- Vérifiez que les statistiques se mettent à jour
- Testez l'envoi de messages via les différents canaux
- Consultez l'historique des messages

3. Notifications :
- Les nouvelles interactions devraient apparaître dans le panneau de notifications
- Vérifiez que les compteurs se mettent à jour


## Configuration des Services

### Base de données PostgreSQL
1. Créez une base de données PostgreSQL
2. Configurez les variables d'environnement dans `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Firebase
1. Créez un projet sur [Firebase Console](https://console.firebase.google.com)
2. Activez l'authentification Google
3. Générez une clé privée dans les paramètres du projet
4. Ajoutez l'URL de votre application dans les domaines autorisés
5. Configurez les variables d'environnement :
```
FIREBASE_API_KEY=votre_api_key
FIREBASE_PROJECT_ID=votre_project_id
FIREBASE_APP_ID=votre_app_id
FIREBASE_PRIVATE_KEY_ID=votre_private_key_id
FIREBASE_PRIVATE_KEY=votre_private_key
FIREBASE_CLIENT_EMAIL=votre_client_email
FIREBASE_CLIENT_ID=votre_client_id
FIREBASE_CLIENT_CERT_URL=votre_client_cert_url
```

### OpenAI
1. Créez une clé API sur [OpenAI](https://platform.openai.com/account/api-keys)
2. Configurez la variable d'environnement :
```
OPENAI_API_KEY=votre_openai_api_key
```

### Twilio
1. Créez un compte [Twilio](https://www.twilio.com)
2. Récupérez le SID et le token d'authentification
3. Obtenez un numéro de téléphone Twilio
4. Configurez les variables d'environnement :
```
TWILIO_ACCOUNT_SID=votre_account_sid
TWILIO_AUTH_TOKEN=votre_auth_token
TWILIO_PHONE_NUMBER=votre_twilio_phone_number
```

### SendGrid
1. Créez un compte [SendGrid](https://sendgrid.com)
2. Générez une clé API
3. Vérifiez votre email d'envoi
4. Configurez les variables d'environnement :
```
SENDGRID_API_KEY=votre_sendgrid_api_key
SENDGRID_FROM_EMAIL=votre_verified_sender_email
```

### Telegram Bot
1. Créez un nouveau bot via [@BotFather](https://t.me/botfather)
2. Configurez la variable d'environnement :
```
TELEGRAM_BOT_TOKEN=votre_bot_token
```

## Développement
- Le projet utilise Flask pour le backend
- Les modèles de données sont gérés avec SQLAlchemy
- L'authentification utilise Flask-Login
- Le frontend utilise Bootstrap pour un design responsive
- Les graphiques sont générés avec Chart.js

## Sécurité
- Toutes les clés API doivent être stockées dans des variables d'environnement
- Les mots de passe sont hashés avant stockage
- L'authentification est requise pour toutes les fonctionnalités sensibles
- Les sessions sont sécurisées avec une clé secrète

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à soumettre des issues ou des pull requests.

## Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
