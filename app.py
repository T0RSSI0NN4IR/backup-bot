import os
import requests
from flask import Flask, redirect, request, jsonify
import json

app = Flask(__name__)

CLIENT_ID = "1482750395221541099"
CLIENT_SECRET = "l2C2fTe6im9DS9wNdSZkDKsLq3Iu6dwg"
REDIRECT_URI = "https://backup-bot-f8rl.onrender.com/callback"
BOT_TOKEN = "MTQ4Mjc1MDM5NTIyMTU0MTA5OQ.GFzZfZ.R2PH3CmsjO9Lz8Vcooe2A3pRYE6bf2Cg-G0P-s"
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
    <link href="https://fonts.googleapis.com/css2?family=MedievalSharp&family=Cinzel:wght@400;600&family=Crimson+Text:ital@0;1&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #060606;
            min-height: 100vh;
            font-family: 'Crimson Text', serif;
            color: #fff;
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
            opacity: 0.9;
            filter: brightness(0.85) contrast(1.1);
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
            font-size: 64px;
            color: #ffffff;
            letter-spacing: 4px;
            margin-bottom: 5px;
            text-shadow: 0 0 30px rgba(255,255,255,0.15), 0 0 60px rgba(180,150,220,0.1);
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .cursor-blink {
            display: inline-block;
            width: 3px; height: 55px;
            background: #fff;
            margin-left: 3px;
            animation: blink 0.8s infinite;
        }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        .subtitle {
            font-family: 'Cinzel', serif;
            font-size: 11px;
            color: #444;
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
        .divider-icon { color: #444; font-size: 12px; }
        .description {
            font-size: 16px;
            color: #888;
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
            color: #555;
            line-height: 1.8;
            text-align: left;
        }
        .notice strong { color: #777; }
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #111, #181818);
            color: #aaa;
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
            background: rgba(255,255,255,0.04);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        .btn:hover::after { width: 300px; height: 300px; }
        .btn:hover { border-color: #333; color: #fff; }
        .footer {
            margin-top: 25px;
            font-family: 'Cinzel', serif;
            font-size: 10px;
            color: #222;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        .success-icon { font-size: 40px; margin-bottom: 15px; color: #5a8a6a; }
        .success-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 40px; color: #6a9a7a; margin-bottom: 10px; }
        .error-icon { font-size: 40px; margin-bottom: 15px; color: #8a5a5a; }
        .error-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 40px; color: #9a6a6a; margin-bottom: 10px; }
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

// ── ARAIGNEE ──
const canvas = document.getElementById('spiderCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const WEB_MAX = 400;
const webTrail = [];

const spider = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    vx: 0, vy: 0,
    angle: 0,
    scale: 2.5,
};

const LEGS = 8;
const legPos = [];
const legTarget = [];
const legPhase = [];
for (let i = 0; i < LEGS; i++) {
    const a = (i / LEGS) * Math.PI * 2;
    legPos.push({ x: spider.x + Math.cos(a)*50, y: spider.y + Math.sin(a)*50 });
    legTarget.push({ x: spider.x + Math.cos(a)*50, y: spider.y + Math.sin(a)*50 });
    legPhase.push(i * (Math.PI / LEGS));
}

let frame = 0;

function drawBody(x, y, angle, scale) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.scale(scale, scale);

    // Abdomen
    const g1 = ctx.createRadialGradient(0, 10, 2, 0, 10, 18);
    g1.addColorStop(0, '#2d2d2d');
    g1.addColorStop(1, '#0d0d0d');
    ctx.beginPath();
    ctx.ellipse(0, 10, 11, 16, 0, 0, Math.PI*2);
    ctx.fillStyle = g1;
    ctx.fill();
    ctx.strokeStyle = 'rgba(80,80,80,0.3)';
    ctx.lineWidth = 0.5;
    ctx.stroke();

    // Motif abdomen
    ctx.beginPath();
    ctx.ellipse(0, 10, 5, 9, 0, 0, Math.PI*2);
    ctx.fillStyle = 'rgba(80,20,20,0.35)';
    ctx.fill();

    // Sablier abdomen
    for(let s = 0; s < 3; s++) {
        ctx.beginPath();
        ctx.ellipse(0, 5 + s*5, 3-s*0.5, 1.5, 0, 0, Math.PI*2);
        ctx.fillStyle = `rgba(100,30,30,${0.3-s*0.08})`;
        ctx.fill();
    }

    // Cephalothorax
    const g2 = ctx.createRadialGradient(0, -5, 1, 0, -5, 10);
    g2.addColorStop(0, '#3a3a3a');
    g2.addColorStop(1, '#111');
    ctx.beginPath();
    ctx.ellipse(0, -5, 7, 9, 0, 0, Math.PI*2);
    ctx.fillStyle = g2;
    ctx.fill();
    ctx.stroke();

    // Tete
    ctx.beginPath();
    ctx.ellipse(0, -16, 5, 6, 0, 0, Math.PI*2);
    ctx.fillStyle = '#1e1e1e';
    ctx.fill();

    // 8 yeux
    const eyes = [[-3,-19],[3,-19],[-2,-17],[2,-17],[-4,-16],[4,-16],[-1.5,-15],[1.5,-15]];
    eyes.forEach(([ex,ey]) => {
        ctx.beginPath();
        ctx.arc(ex, ey, 0.9, 0, Math.PI*2);
        ctx.fillStyle = '#dd1100';
        ctx.fill();
        ctx.beginPath();
        ctx.arc(ex-0.3, ey-0.3, 0.3, 0, Math.PI*2);
        ctx.fillStyle = 'rgba(255,100,100,0.6)';
        ctx.fill();
    });

    // Cheliceres
    ctx.strokeStyle = '#444';
    ctx.lineWidth = 1.2;
    [[-2.5,1],[2.5,1]].forEach(([cx,cy]) => {
        ctx.beginPath();
        ctx.moveTo(cx, -22);
        ctx.quadraticCurveTo(cx*1.8, -26, cx*1.2, -29);
        ctx.stroke();
    });

    // Filiere (arriere)
    ctx.beginPath();
    ctx.ellipse(0, 26, 2.5, 3, 0, 0, Math.PI*2);
    ctx.fillStyle = '#222';
    ctx.fill();

    ctx.restore();
}

function drawLeg(ax, ay, tx, ty, side, legIdx) {
    const angle = Math.atan2(ty-ay, tx-ax);
    const len = Math.hypot(tx-ax, ty-ay);
    const jx = ax + Math.cos(angle)*len*0.45 + Math.cos(angle + side*1.2)*len*0.25;
    const jy = ay + Math.sin(angle)*len*0.45 + Math.sin(angle + side*1.2)*len*0.25;
    const j2x = jx + Math.cos(angle)*len*0.35;
    const j2y = jy + Math.sin(angle)*len*0.35;

    ctx.beginPath();
    ctx.moveTo(ax, ay);
    ctx.lineTo(jx, jy);
    ctx.lineTo(j2x, j2y);
    ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(60,60,60,0.95)';
    ctx.lineWidth = 1.8;
    ctx.lineJoin = 'round';
    ctx.stroke();

    // Poils
    ctx.lineWidth = 0.6;
    ctx.strokeStyle = 'rgba(50,50,50,0.7)';
    [[ax,ay,jx,jy],[jx,jy,j2x,j2y],[j2x,j2y,tx,ty]].forEach(([x1,y1,x2,y2]) => {
        for(let t = 0.15; t < 0.9; t += 0.18) {
            const px = x1+(x2-x1)*t;
            const py = y1+(y2-y1)*t;
            const nx = -(y2-y1); const ny = (x2-x1);
            const nm = Math.hypot(nx,ny)||1;
            const hl = 4 + Math.random()*2;
            ctx.beginPath();
            ctx.moveTo(px, py);
            ctx.lineTo(px+nx/nm*hl*side, py+ny/nm*hl*side);
            ctx.stroke();
        }
    });
}

function drawWeb() {
    if (webTrail.length < 2) return;
    ctx.save();

    // Fil principal
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 0.6;
    ctx.beginPath();
    ctx.moveTo(webTrail[0].x, webTrail[0].y);
    for (let i = 1; i < webTrail.length; i++) {
        ctx.lineTo(webTrail[i].x, webTrail[i].y);
    }
    ctx.stroke();

    // Fils transversaux toile
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 0.3;
    for (let i = 0; i < webTrail.length; i += 8) {
        for (let j = i+6; j < webTrail.length && j < i+40; j += 6) {
            const dx = webTrail[i].x - webTrail[j].x;
            const dy = webTrail[i].y - webTrail[j].y;
            if (Math.hypot(dx,dy) < 150) {
                ctx.beginPath();
                ctx.moveTo(webTrail[i].x, webTrail[i].y);
                ctx.lineTo(webTrail[j].x, webTrail[j].y);
                ctx.stroke();
            }
        }
    }

    // Fil vers araignee depuis dernier point
    if (webTrail.length > 0) {
        ctx.strokeStyle = 'rgba(255,255,255,0.18)';
        ctx.lineWidth = 0.7;
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

    // Mouvement
    spider.vx += (mouseX - spider.x) * 0.035;
    spider.vy += (mouseY - spider.y) * 0.035;
    spider.vx *= 0.72;
    spider.vy *= 0.72;
    spider.x += spider.vx;
    spider.y += spider.vy;

    const speed = Math.hypot(spider.vx, spider.vy);
    if (speed > 0.2) spider.angle = Math.atan2(spider.vy, spider.vx) + Math.PI/2;

    // Toile
    const last = webTrail[webTrail.length-1];
    const dist = last ? Math.hypot(spider.x-last.x, spider.y-last.y) : 999;
    if (dist > 10) {
        webTrail.push({ x: spider.x, y: spider.y });
        if (webTrail.length > WEB_MAX) webTrail.shift();
    }

    // Pattes
    for (let i = 0; i < LEGS; i++) {
        const side = i < LEGS/2 ? -1 : 1;
        const pairIdx = i % (LEGS/2);
        const baseAngle = spider.angle + side*(0.5 + pairIdx*0.3);
        const reach = (28 + pairIdx*6) * spider.scale;
        const wave = Math.sin(frame*0.09 + legPhase[i]) * 8;
        legTarget[i].x = spider.x + Math.cos(baseAngle)*reach + wave;
        legTarget[i].y = spider.y + Math.sin(baseAngle)*reach + wave;
        legPos[i].x += (legTarget[i].x - legPos[i].x) * 0.18;
        legPos[i].y += (legTarget[i].y - legPos[i].y) * 0.18;
    }

    drawWeb();

    // Dessin pattes
    for (let i = 0; i < LEGS; i++) {
        const side = i < LEGS/2 ? -1 : 1;
        const attachAngle = spider.angle + side*0.4;
        const ax = spider.x + Math.cos(attachAngle)*6*spider.scale;
        const ay = spider.y + Math.sin(attachAngle)*6*spider.scale;
        drawLeg(ax, ay, legPos[i].x, legPos[i].y, side, i);
    }

    drawBody(spider.x, spider.y, spider.angle, spider.scale);

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
            Bienvenue <strong style="color:#aaa">{username}</strong>.<br>
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
