# Prometheus + Alertmanager pour Coolify

Surveillance du chat PHP et envoi d'alertes Discord en cas de down.

## 1. Créer le webhook Discord

1. Ouvrez votre serveur Discord
2. Paramètres du salon où vous voulez recevoir les alertes
3. **Intégrations** → **Webhooks** → **Nouveau webhook**
4. Donnez un nom (ex. "Coolify Alertes")
5. Cliquez sur **Copier l'URL du webhook**

## 2. Configurer Alertmanager

1. Éditez `alertmanager.yml`
2. Remplacez `https://discord.com/api/webhooks/VOTRE_WEBHOOK_ID/VOTRE_WEBHOOK_TOKEN` par l'URL copiée

## 3. Déployer sur Coolify

1. Dans Coolify : **+ New** → **Docker Compose**
2. Nom : `prometheus-alertmanager`
3. **Base Directory :** `prometheus-alertmanager` (ou `/` si tout est à la racine)
4. **Docker Compose Location :** `docker-compose.yaml`
5. Source Git : ce dépôt
6. **Deploy**

## 4. Vérifier

- **Prometheus :** http://localhost:9090 (ou le port exposé) → Status → Targets
- **Alertmanager :** http://localhost:9093
- L'alerte **ChatApplicationDown** se déclenche quand le chat est inaccessible pendant 1 minute

## Cible surveillée

Par défaut : `http://host.docker.internal:8081/` (l'application chat sur le port 8081).

Si le chat est sur une autre machine, modifiez `prometheus.yml` et remplacez par l'URL de votre chat (ex. `http://chat.phasna.courses.studalya.net`).
