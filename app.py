import os
import requests
from flask import Flask, redirect, request, jsonify
import json

app = Flask(__name__)

CLIENT_ID = "1482750395221541099"
CLIENT_SECRET = "u_FzW241fiP18ArNUlHDBkZIcEPSYK7E"
REDIRECT_URI = "https://backup-bot-f8rl.onrender.com/callback"
BOT_TOKEN = "MTQ4Mjc1MDM5NTIyMTU0MTA5OQ.GPmvif.cVhoNlkZWB4HGl3MEnejxO3yDwOROhk24gy4Do"
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
            width: 8px; height: 8px;
            background: #fff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transform: translate(-50%, -50%);
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
            text-shadow: 0 0 30px rgba(180,150,220,0.2);
            min-height: 75px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .cursor-blink {
            display: inline-block;
            width: 3px; height: 52px;
            background: #888;
            margin-left: 3px;
            animation: blink 0.8s infinite;
        }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
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
            flex: 1; height: 1px;
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
        .success-icon { font-size: 40px; margin-bottom: 15px; }
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
let mouseX = window.innerWidth/2, mouseY = window.innerHeight/2;
document.addEventListener('mousemove', e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursor.style.left = mouseX + 'px';
    cursor.style.top = mouseY + 'px';
});

// ── ARAIGNEE REALISTE ──
const canvas = document.getElementById('spiderCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const WEB_MAX = 300;
const webTrail = [];
let lastWebDist = 0;

const spider = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    px: canvas.width / 2,
    py: canvas.height / 2,
    vx: 0, vy: 0,
    angle: 0,
};

// 4 paires de pattes = 8 pattes
const LEGS = 8;
const legTargets = [];
const legPositions = [];
const legPhase = [];
for (let i = 0; i < LEGS; i++) {
    const a = (i / LEGS) * Math.PI * 2;
    legTargets.push({ x: spider.x + Math.cos(a)*30, y: spider.y + Math.sin(a)*30 });
    legPositions.push({ x: spider.x + Math.cos(a)*30, y: spider.y + Math.sin(a)*30 });
    legPhase.push(i * (Math.PI / LEGS));
}

let frame = 0;

function drawSpiderBody(x, y, angle) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);

    // Abdomen (gros, oval, poilu)
    const grad = ctx.createRadialGradient(0, 8, 2, 0, 8, 14);
    grad.addColorStop(0, '#2a2a2a');
    grad.addColorStop(1, '#111');
    ctx.beginPath();
    ctx.ellipse(0, 8, 9, 13, 0, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    // Motif abdomen
    ctx.beginPath();
    ctx.ellipse(0, 8, 4, 7, 0, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(60,20,20,0.4)';
    ctx.fill();

    // Thorax (céphalothorax)
    const grad2 = ctx.createRadialGradient(0, -5, 1, 0, -5, 8);
    grad2.addColorStop(0, '#333');
    grad2.addColorStop(1, '#111');
    ctx.beginPath();
    ctx.ellipse(0, -5, 6, 7, 0, 0, Math.PI * 2);
    ctx.fillStyle = grad2;
    ctx.fill();

    // Tête
    ctx.beginPath();
    ctx.ellipse(0, -14, 4, 5, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#222';
    ctx.fill();

    // Yeux (4 paires = 8 yeux comme vraie araignee)
    const eyePositions = [
        [-2.5, -16], [2.5, -16],
        [-1.5, -14], [1.5, -14],
        [-3, -13], [3, -13],
        [-2, -12], [2, -12],
    ];
    eyePositions.forEach(([ex, ey]) => {
        ctx.beginPath();
        ctx.arc(ex, ey, 0.8, 0, Math.PI * 2);
        ctx.fillStyle = '#cc2200';
        ctx.fill();
    });

    // Chélicères (crochets)
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(-2, -19);
    ctx.quadraticCurveTo(-4, -23, -2, -25);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(2, -19);
    ctx.quadraticCurveTo(4, -23, 2, -25);
    ctx.stroke();

    ctx.restore();
}

function drawLeg(sx, sy, ex, ey, side) {
    const mx = (sx + ex) / 2 + side * 12;
    const my = (sy + ey) / 2 - 5;

    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.quadraticCurveTo(mx, my, ex, ey);
    ctx.strokeStyle = 'rgba(50,50,50,0.9)';
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // Poils sur les pattes
    for (let t = 0.2; t < 0.9; t += 0.2) {
        const px = sx + (ex - sx) * t;
        const py = sy + (ey - sy) * t;
        const nx = -(ey - sy);
        const ny = (ex - sx);
        const len = 2;
        const nm = Math.hypot(nx, ny) || 1;
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(px + nx/nm*len*side, py + ny/nm*len*side);
        ctx.strokeStyle = 'rgba(40,40,40,0.7)';
        ctx.lineWidth = 0.5;
        ctx.stroke();
    }
}

function drawWeb() {
    if (webTrail.length < 2) return;
    ctx.save();

    // Fil principal
    ctx.strokeStyle = 'rgba(255,255,255,0.08)';
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.moveTo(webTrail[0].x, webTrail[0].y);
    for (let i = 1; i < webTrail.length; i++) {
        ctx.lineTo(webTrail[i].x, webTrail[i].y);
    }
    ctx.stroke();

    // Fils transversaux
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 0.3;
    for (let i = 0; i < webTrail.length; i += 10) {
        for (let j = i + 5; j < webTrail.length && j < i + 30; j += 5) {
            const dx = webTrail[i].x - webTrail[j].x;
            const dy = webTrail[i].y - webTrail[j].y;
            if (Math.hypot(dx, dy) < 120) {
                ctx.beginPath();
                ctx.moveTo(webTrail[i].x, webTrail[i].y);
                ctx.lineTo(webTrail[j].x, webTrail[j].y);
                ctx.stroke();
            }
        }
    }

    // Fil vers le curseur
    if (webTrail.length > 0) {
        ctx.strokeStyle = 'rgba(255,255,255,0.15)';
        ctx.lineWidth = 0.6;
        ctx.beginPath();
        ctx.moveTo(webTrail[webTrail.length-1].x, webTrail[webTrail.length-1].y);
        ctx.lineTo(spider.x, spider.y);
        ctx.stroke();
    }

    ctx.restore();
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    frame++;

    // Mouvement araignee vers curseur
    spider.vx += (mouseX - spider.x) * 0.03;
    spider.vy += (mouseY - spider.y) * 0.03;
    spider.vx *= 0.75;
    spider.vy *= 0.75;
    spider.px = spider.x;
    spider.py = spider.y;
    spider.x += spider.vx;
    spider.y += spider.vy;

    const speed = Math.hypot(spider.vx, spider.vy);
    if (speed > 0.1) {
        spider.angle = Math.atan2(spider.vy, spider.vx) + Math.PI / 2;
    }

    // Trace de toile
    const distMoved = Math.hypot(spider.x - (webTrail.length ? webTrail[webTrail.length-1].x : spider.x),
                                  spider.y - (webTrail.length ? webTrail[webTrail.length-1].y : spider.y));
    if (distMoved > 8) {
        webTrail.push({ x: spider.x, y: spider.y });
        if (webTrail.length > WEB_MAX) webTrail.shift();
    }

    // Pattes
    for (let i = 0; i < LEGS; i++) {
        const side = i < LEGS/2 ? -1 : 1;
        const pairIdx = i % (LEGS/2);
        const baseAngle = spider.angle + side * (0.4 + pairIdx * 0.28);
        const reach = 22 + pairIdx * 3;
        const wave = Math.sin(frame * 0.08 + legPhase[i]) * 5;
        legTargets[i].x = spider.x + Math.cos(baseAngle) * reach + wave;
        legTargets[i].y = spider.y + Math.sin(baseAngle) * reach + wave;
        legPositions[i].x += (legTargets[i].x - legPositions[i].x) * 0.2;
        legPositions[i].y += (legTargets[i].y - legPositions[i].y) * 0.2;
    }

    drawWeb();

    // Pattes
    for (let i = 0; i < LEGS; i++) {
        const side = i < LEGS/2 ? -1 : 1;
        const attachX = spider.x + Math.cos(spider.angle + side * 0.3) * 5;
        const attachY = spider.y + Math.sin(spider.angle + side * 0.3) * 5;
        drawLeg(attachX, attachY, legPositions[i].x, legPositions[i].y, side);
    }

    drawSpiderBody(spider.x, spider.y, spider.angle);

    requestAnimationFrame(animate);
}

animate();

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// ── EFFET FRAPPE INFINI ──
const texts = ['Sherlook', 'Backup', 'Protection', 'Sherlook'];
let textIdx = 0, charIdx = 0, deleting = false;

function typeEffect() {
    const titleEl = document.getElementById('typeTitle');
    if (!titleEl) { setTimeout(typeEffect, 100); return; }
    const current = texts[textIdx];
    if (!deleting) {
        charIdx++;
        titleEl.textContent = current.substring(0, charIdx);
        if (charIdx === current.length) {
            deleting = true;
            setTimeout(typeEffect, 2000);
            return;
        }
        setTimeout(typeEffect, 100);
    } else {
        charIdx--;
        titleEl.textContent = current.substring(0, charIdx);
        if (charIdx === 0) {
            deleting = false;
            textIdx = (textIdx + 1) % texts.length;
        }
        setTimeout(typeEffect, 55);
    }
}

setTimeout(typeEffect, 500);
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
                — Envoyer des messages, rejoindre des serveurs ou agir en ton nom.<br>
                — Voir ton mot de passe ou modifier ton compte.<br><br>
                Nous stockons uniquement un token limité qui nous permet de t'ajouter à un serveur Discord, rien de plus.
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
