import os
import requests
from flask import Flask, redirect, request, jsonify
import json

app = Flask(__name__)

CLIENT_ID = "1482750395221541099"
CLIENT_SECRET = "BCproPARbAfH0X4smGr9XgZ1HiF2Z9tI"
REDIRECT_URI = "https://backup-bot.onrender.com/callback"
BOT_TOKEN = "MTQ4Mjc1MDM5NTIyMTU0MTA5OQ.G5tDwh.Jg45PuhB_04tXptgtpiF3RAzpt88UBXcylztcc"
BACKUP_FILE = "backup_members.json"

def charger_backup():
    if not os.path.exists(BACKUP_FILE):
        return {}
    with open(BACKUP_FILE, "r") as f:
        return json.load(f)

def sauvegarder_backup(data):
    with open(BACKUP_FILE, "w") as f:
        json.dump(data, f, indent=2)

HTML_BASE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sherlook — Backup</title>
    <link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Crimson+Text:ital@0;1&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: #080808;
            min-height: 100vh;
            font-family: 'Crimson Text', serif;
            color: #ccc;
            overflow-x: hidden;
        }

        /* TOILE D'ARAIGNEE */
        canvas {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            pointer-events: none;
            opacity: 0.15;
        }

        .content {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 40px 20px;
        }

        .banner {
            width: 100%;
            max-width: 700px;
            border-radius: 12px;
            margin-bottom: 40px;
            opacity: 0.9;
            filter: brightness(0.85);
        }

        .card {
            background: linear-gradient(145deg, #0f0f0f, #111);
            border: 1px solid #1e1e1e;
            border-radius: 16px;
            padding: 50px 40px;
            max-width: 480px;
            width: 100%;
            text-align: center;
            box-shadow: 0 0 40px rgba(0,0,0,0.8), 0 0 80px rgba(80,0,80,0.05);
        }

        .title {
            font-family: 'UnifrakturMaguntia', cursive;
            font-size: 52px;
            color: #fff;
            letter-spacing: 2px;
            margin-bottom: 8px;
            text-shadow: 0 0 20px rgba(150,100,200,0.3);
        }

        .subtitle {
            font-size: 13px;
            color: #444;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 30px;
        }

        .divider {
            width: 60px;
            height: 1px;
            background: linear-gradient(to right, transparent, #333, transparent);
            margin: 0 auto 30px;
        }

        .description {
            font-size: 16px;
            color: #666;
            line-height: 1.8;
            margin-bottom: 35px;
            font-style: italic;
        }

        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #1a1a1a, #222);
            color: #aaa;
            padding: 16px 40px;
            border-radius: 8px;
            text-decoration: none;
            font-family: 'Crimson Text', serif;
            font-size: 17px;
            letter-spacing: 2px;
            border: 1px solid #2a2a2a;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
            transition: left 0.5s;
        }

        .btn:hover::before { left: 100%; }

        .btn:hover {
            border-color: #3a3a3a;
            color: #ddd;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }

        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #2a2a2a;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* SUCCESS */
        .success { color: #4a7a5a; font-size: 48px; margin-bottom: 15px; }
        .success-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 36px; color: #6a9a7a; margin-bottom: 10px; }

        /* ERROR */
        .error { color: #7a4a4a; font-size: 48px; margin-bottom: 15px; }
        .error-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 36px; color: #9a6a6a; margin-bottom: 10px; }
    </style>
</head>
<body>
    <canvas id="spider"></canvas>
    <script>
        const canvas = document.getElementById('spider');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const nodes = [];
        const NUM = 60;

        for (let i = 0; i < NUM; i++) {
            nodes.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 0.4;

            for (let i = 0; i < NUM; i++) {
                const a = nodes[i];
                a.x += a.vx;
                a.y += a.vy;
                if (a.x < 0 || a.x > canvas.width) a.vx *= -1;
                if (a.y < 0 || a.y > canvas.height) a.vy *= -1;

                for (let j = i + 1; j < NUM; j++) {
                    const b = nodes[j];
                    const dist = Math.hypot(a.x - b.x, a.y - b.y);
                    if (dist < 180) {
                        ctx.globalAlpha = 1 - dist / 180;
                        ctx.beginPath();
                        ctx.moveTo(a.x, a.y);
                        ctx.lineTo(b.x, b.y);
                        ctx.stroke();
                    }
                }

                ctx.globalAlpha = 0.5;
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(a.x, a.y, 1, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.globalAlpha = 1;
            requestAnimationFrame(draw);
        }

        draw();

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    </script>
"""

@app.route("/")
def index():
    return HTML_BASE + """
    <div class="content">
        <img src="https://i.postimg.cc/5t1c4k63/image-(3).webp" class="banner" alt="Sherlook">
        <div class="card">
            <div class="title">Sherlook</div>
            <div class="subtitle">Système de sauvegarde</div>
            <div class="divider"></div>
            <p class="description">
                Sauvegarde ton accès au serveur.<br>
                En cas de suppression, tu seras automatiquement<br>
                ajouté au serveur de remplacement.
            </p>
            <a href="/verify" class="btn">⚔ Vérifier maintenant</a>
            <div class="footer">Sherlook — Protection du serveur</div>
        </div>
    </div>
    </body></html>
    """

@app.route("/verify")
def verify():
    oauth_url = (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify+guilds.join"
    )
    return redirect(oauth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return HTML_BASE + """
        <div class="content"><div class="card">
            <div class="error">✖</div>
            <div class="error-title">Erreur</div>
            <p class="description">Aucun code reçu.</p>
        </div></div></body></html>
        """, 400

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    tokens = r.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if not access_token:
        return HTML_BASE + """
        <div class="content"><div class="card">
            <div class="error">✖</div>
            <div class="error-title">Échec</div>
            <p class="description">Authentification échouée.</p>
        </div></div></body></html>
        """, 400

    user_r = requests.get("https://discord.com/api/users/@me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    user = user_r.json()
    user_id = user.get("id")
    username = user.get("username")

    backup = charger_backup()
    backup[user_id] = {
        "username": username,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    sauvegarder_backup(backup)

    return HTML_BASE + f"""
    <div class="content"><div class="card">
        <div class="success">✓</div>
        <div class="success-title">Sauvegardé</div>
        <div class="divider"></div>
        <p class="description">
            Bienvenue <strong style="color:#aaa">{username}</strong>.<br>
            Tu seras automatiquement ajouté<br>
            au nouveau serveur si nécessaire.
        </p>
        <div class="footer">Sherlook — Protection du serveur</div>
    </div></div></body></html>
    """

@app.route("/restore/<guild_id>")
def restore(guild_id):
    secret = request.args.get("secret")
    if secret != "TON_SECRET_ADMIN":
        return "Non autorisé", 403

    backup = charger_backup()
    resultats = {"succes": 0, "echec": 0}

    for user_id, data in backup.items():
        try:
            r = requests.put(
                f"https://discord.com/api/guilds/{guild_id}/members/{user_id}",
                headers={
                    "Authorization": f"Bot {BOT_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={"access_token": data["access_token"]}
            )
            if r.status_code in [200, 201, 204]:
                resultats["succes"] += 1
            else:
                resultats["echec"] += 1
        except:
            resultats["echec"] += 1

    return jsonify(resultats)

@app.route("/count")
def count():
    backup = charger_backup()
    return jsonify({"membres_sauvegardes": len(backup)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
