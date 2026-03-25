import os

import requests
from flask import Flask, request

app = Flask(__name__)


def _format_alert(alert: dict) -> str:
    status = (alert.get("status") or "unknown").upper()
    labels = alert.get("labels") or {}
    annotations = alert.get("annotations") or {}

    name = labels.get("alertname", "alert")
    instance = labels.get("instance") or labels.get("pod") or labels.get("host") or ""
    summary = annotations.get("summary") or annotations.get("message") or ""
    description = annotations.get("description") or ""

    header = f"**{status}** `{name}`" + (f" — `{instance}`" if instance else "")
    body_parts = [p for p in [summary, description] if p]
    return "\n".join([header, *body_parts]).strip()


@app.post("/alertmanager")
def alertmanager_webhook():
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not discord_webhook_url:
        return ("DISCORD_WEBHOOK_URL is not set", 500)

    payload = request.get_json(force=True, silent=True) or {}
    alerts = payload.get("alerts") or []

    if not alerts:
        content = "Alertmanager notification (no alerts in payload)."
    else:
        # Keep under Discord 2000 char limit.
        lines = []
        for alert in alerts[:20]:
            lines.append(_format_alert(alert))
        content = "\n\n".join([l for l in lines if l]).strip()[:1900]

    r = requests.post(discord_webhook_url, json={"content": content}, timeout=10)
    if r.status_code >= 400:
        return (f"Discord webhook error: {r.status_code} {r.text}", 502)

    return ("ok", 200)


@app.get("/healthz")
def healthz():
    return ("ok", 200)

