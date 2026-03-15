import os
import requests
from flask import Flask, redirect, request, jsonify
import json

app = Flask(__name__)

CLIENT_ID = "1482750395221541099"
CLIENT_SECRET = "sSWdYDu-Ehf9qJChcVfoPhkxUET_WLfJ"
REDIRECT_URI = "https://backup-bot-f8rl.onrender.com/callback"
BOT_TOKEN = "MTQ4Mjc1MDM5NTIyMTU0MTA5OQ.Gg9tUv.AfsnrTlpCXd2DxQ3BstptnP-ZOoOF2JIEvYoqY"
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
    <link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Cinzel:wght@400;600&family=Crimson+Text:ital@0;1&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: #060606;
            min-height: 100vh;
            font-family: 'Crimson Text', serif;
            color: #ccc;
            overflow-x: hidden;
            cursor: none;
        }

        canvas {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .cursor {
            position: fixed;
            width: 10px;
            height: 10px;
            background: #fff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transform: translate(-50%, -50%);
            transition: transform 0.1s;
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
            max-width: 650px;
            border-radius: 10px;
            margin-bottom: 40px;
            opacity: 0.85;
            filter: brightness(0.8) contrast(1.1);
        }

        .card {
            background: linear-gradient(160deg, #0a0a0a, #0d0d0d);
            border: 1px solid #1a1a1a;
            border-radius: 20px;
            padding: 55px 45px;
            max-width: 500px;
            width: 100%;
            text-align: center;
            box-shadow: 0 0 60px rgba(0,0,0,0.9), inset 0 0 30px rgba(0,0,0,0.5);
        }

        .title {
            font-family: 'UnifrakturMaguntia', cursive;
            font-size: 58px;
            color: #e8e8e8;
            letter-spacing: 3px;
            margin-bottom: 5px;
            text-shadow: 0 0 30px rgba(180,150,220,0.2), 0 0 60px rgba(100,50,150,0.1);
            min-height: 70px;
        }

        .cursor-blink {
            display: inline-block;
            width: 3px;
            height: 50px;
            background: #aaa;
            margin-left: 2px;
            vertical-align: middle;
            animation: blink 0.8s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        .subtitle {
            font-family: 'Cinzel', serif;
            font-size: 11px;
            color: #333;
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-bottom: 35px;
        }

        .divider {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 30px;
        }

        .divider-line {
            flex: 1;
            height: 1px;
            background: linear-gradient(to right, transparent, #222, transparent);
        }

        .divider-icon { color: #333; font-size: 12px; }

        .description {
            font-size: 16px;
            color: #555;
            line-height: 2;
            margin-bottom: 10px;
            font-style: italic;
        }

        .notice {
            background: rgba(255,255,255,0.02);
            border: 1px solid #1a1a1a;
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 35px;
            font-size: 13px;
            color: #3a3a3a;
            line-height: 1.8;
            text-align: left;
        }

        .notice strong { color: #444; }

        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #111, #181818);
            color: #888;
            padding: 17px 45px;
            border-radius: 10px;
            text-decoration: none;
            font-family: 'Cinzel', serif;
            font-size: 14px;
            letter-spacing: 3px;
            border: 1px solid #222;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .btn::after {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            width: 0; height: 0;
            background: rgba(255,255,255,0.03);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .btn:hover::after { width: 300px; height: 300px; }
        .btn:hover { border-color: #2a2a2a; color: #bbb; }

        .footer {
            margin-top: 25px;
            font-family: 'Cinzel', serif;
            font-size: 10px;
            color: #1e1e1e;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .success-icon { font-size: 40px; margin-bottom: 15px; filter: grayscale(1); }
        .success-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 40px; color: #5a8a6a; margin-bottom: 10px; }
        .error-icon { font-size: 40px; margin-bottom: 15px; }
        .error-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 40px; color: #8a5a5a; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="cursor" id="cursor"></div>
    <canvas id="spiderCanvas"></canvas>

    <script>
    // ── CURSEUR ──
    const cursor = document.getElementById('cursor');
    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', e => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursor.style.left = mouseX + 'px';
        cursor.style.top = mouseY + 'px';
    });

    // ── ARAIGNEE + TOILE ──
    const canvas = document.getElementById('spiderCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Points d'ancrage des fils de toile
    const webPoints = [];
    const MAX_WEB = 200;

    // Corps araignee
    const spider = {
        x: canvas.width / 2,
        y: canvas.height / 2,
        targetX: mouseX,
        targetY: mouseY,
        legs: [],
        bodyR: 8,
        headR: 5,
    };

    // Positions des pattes
    const LEG_COUNT = 8;
    for (let i = 0; i < LEG_COUNT; i++) {
        spider.legs.push({
            x: spider.x + Math.cos(i * Math.PI / 4) * 20,
            y: spider.y + Math.sin(i * Math.PI / 4) * 20,
            targetX: spider.x,
            targetY: spider.y,
            phase: i * 0.3,
        });
    }

    let lastWebX = spider.x;
    let lastWebY = spider.y;
    let frameCount = 0;

    function drawSpider() {
        const s = spider;

        // Corps
        ctx.save();
        ctx.globalAlpha = 0.85;

        // Abdomen
        ctx.beginPath();
        ctx.ellipse(s.x, s.y, s.bodyR * 1.5, s.bodyR, 0, 0, Math.PI * 2);
        ctx.fillStyle = '#1a1a1a';
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 0.5;
        ctx.stroke();

        // Tete
        const angle = Math.atan2(s.targetY - s.y, s.targetX - s.x);
        const hx = s.x + Math.cos(angle) * (s.bodyR + s.headR);
        const hy = s.y + Math.sin(angle) * (s.bodyR + s.headR);
        ctx.beginPath();
        ctx.arc(hx, hy, s.headR, 0, Math.PI * 2);
        ctx.fillStyle = '#222';
        ctx.fill();
        ctx.stroke();

        // Yeux
        for (let i = -1; i <= 1; i += 2) {
            const ex = hx + Math.cos(angle + i * 0.4) * 3;
            const ey = hy + Math.sin(angle + i * 0.4) * 3;
            ctx.beginPath();
            ctx.arc(ex, ey, 1, 0, Math.PI * 2);
            ctx.fillStyle = '#cc0000';
            ctx.fill();
        }

        // Pattes
        ctx.strokeStyle = '#2a2a2a';
        ctx.lineWidth = 1;
        for (let i = 0; i < LEG_COUNT; i++) {
            const side = i < LEG_COUNT / 2 ? -1 : 1;
            const legAngle = angle + side * (0.3 + (i % (LEG_COUNT / 2)) * 0.25);
            const legLen1 = 14;
            const legLen2 = 12;
            const jx = s.x + Math.cos(legAngle) * legLen1;
            const jy = s.y + Math.sin(legAngle) * legLen1;
            const wave = Math.sin(frameCount * 0.1 + i) * 4;
            const ex = jx + Math.cos(legAngle + side * 0.8) * legLen2 + wave;
            const ey = jy + Math.sin(legAngle + side * 0.8) * legLen2 + wave;

            ctx.beginPath();
            ctx.moveTo(s.x, s.y);
            ctx.quadraticCurveTo(jx, jy, ex, ey);
            ctx.stroke();
        }

        ctx.restore();
    }

    function drawWeb() {
        if (webPoints.length < 2) return;
        ctx.save();
        ctx.globalAlpha = 0.12;
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 0.4;

        for (let i = 1; i < webPoints.length; i++) {
            ctx.beginPath();
            ctx.moveTo(webPoints[i-1].x, webPoints[i-1].y);
            ctx.lineTo(webPoints[i].x, webPoints[i].y);
            ctx.stroke();

            // Fils transversaux
            if (i % 8 === 0 && i >= 8) {
                ctx.beginPath();
                ctx.moveTo(webPoints[i].x, webPoints[i].y);
                ctx.lineTo(webPoints[i-8].x, webPoints[i-8].y);
                ctx.stroke();
            }
        }

        ctx.restore();
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        frameCount++;

        // Araignee suit la souris
        spider.targetX = mouseX;
        spider.targetY = mouseY;
        spider.x += (spider.targetX - spider.x) * 0.04;
        spider.y += (spider.targetY - spider.y) * 0.04;

        // Ajoute des points de toile
        const dist = Math.hypot(spider.x - lastWebX, spider.y - lastWebY);
        if (dist > 15) {
            webPoints.push({ x: spider.x, y: spider.y });
            if (webPoints.length > MAX_WEB) webPoints.shift();
            lastWebX = spider.x;
            lastWebY = spider.y;
        }

        drawWeb();
        drawSpider();

        requestAnimationFrame(animate);
    }

    animate();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    // ── EFFET FRAPPE TITRE ──
    const texts = ['Sherlook', 'Backup', 'Sherlook'];
    let textIdx = 0;
    let charIdx = 0;
    let deleting = false;
    const titleEl = document.getElementById('typeTitle');

    function typeEffect() {
        if (!titleEl) return;
        const current = texts[textIdx];
        if (!deleting) {
            charIdx++;
            titleEl.textContent = current.substring(0, charIdx);
            if (charIdx === current.length) {
                deleting = true;
                setTimeout(typeEffect, 1800);
                return;
            }
        } else {
            charIdx--;
            titleEl.textContent = current.substring(0, charIdx);
            if (charIdx === 0) {
                deleting = false;
                textIdx = (textIdx + 1) % texts.length;
            }
        }
        setTimeout(typeEffect, deleting ? 60 : 110);
    }

    typeEffect();
    </script>
"""

@app.route("/")
def index():
    return HTML_BASE + """
    <div class="content">
        <img src="https://i.postimg.cc/5t1c4k63/image-(3).webp" class="banner" alt="Sherlook">
        <div class="card">
            <div class="title"><span id="typeTitle"></span><span class="cursor-blink"></span></div>
            <div class="subtitle">Système de Sauvegarde</div>
            <div class="divider">
                <div class="divider-line"></div>
                <div class="divider-icon">✦</div>
                <div class="divider-line"></div>
            </div>
            <p class="description">Protège ton accès au serveur.</p>
            <div class="notice">
                <strong>🔒 Ce que nous pouvons faire :</strong><br>
                — T'ajouter automatiquement au nouveau serveur en cas de suppression ou de raid.<br><br>
                <strong>🚫 Ce que nous ne pouvons PAS faire :</strong><br>
                — Accéder à ton compte, tes messages, tes serveurs ou toute autre information personnelle.<br>
                — Agir en ton nom sur Discord.<br><br>
                Nous stockons uniquement un token d'accès limité permettant de t'ajouter à un serveur.
            </div>
            <a href="/verify" class="btn">⚔ Vérifier maintenant</a>
            <div class="footer">Sherlook — Protection du Serveur</div>
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
            <div class="error-icon">✖</div>
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
            <div class="error-icon">✖</div>
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
        <div class="success-icon">✓</div>
        <div class="success-title">Sauvegardé</div>
        <div class="divider">
            <div class="divider-line"></div>
            <div class="divider-icon">✦</div>
            <div class="divider-line"></div>
        </div>
        <p class="description">
            Bienvenue <strong style="color:#777">{username}</strong>.<br>
            Tu seras automatiquement ajouté<br>
            au nouveau serveur si nécessaire.
        </p>
        <div class="footer">Sherlook — Protection du Serveur</div>
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
