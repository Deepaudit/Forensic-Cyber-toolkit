<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PABLO CYBER — Forensics Toolkit README</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:        #0a0c0f;
    --bg2:       #0d1117;
    --bg3:       #111820;
    --card:      #0f1923;
    --border:    #1a2a3a;
    --green:     #00ff88;
    --green2:    #00cc6a;
    --cyan:      #00d4ff;
    --cyan2:     #00a8cc;
    --purple:    #bf5af2;
    --purple2:   #9a3fcf;
    --orange:    #ff9500;
    --orange2:   #cc7700;
    --red:       #ff3b30;
    --red2:      #cc2f26;
    --yellow:    #ffd60a;
    --dim:       #4a6070;
    --text:      #c8d8e8;
    --textdim:   #5a7080;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    overflow-x: hidden;
  }

  /* SCANLINE overlay */
  body::before {
    content: '';
    position: fixed; inset: 0; z-index: 9999; pointer-events: none;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px);
  }

  /* ── HERO ── */
  .hero {
    position: relative;
    background: linear-gradient(160deg, #060b10 0%, #0d1b2a 40%, #0a1520 100%);
    border-bottom: 1px solid #1a3050;
    overflow: hidden;
    padding: 0;
  }

  /* grid lines background */
  .hero::after {
    content: '';
    position: absolute; inset: 0; pointer-events: none;
    background-image:
      linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: gridScroll 20s linear infinite;
  }
  @keyframes gridScroll { from { background-position: 0 0; } to { background-position: 40px 40px; } }

  .hero-inner {
    position: relative; z-index: 2;
    display: grid;
    grid-template-columns: 1fr 420px;
    gap: 0;
    align-items: stretch;
    min-height: 520px;
  }

  .hero-left {
    padding: 60px 50px 60px 60px;
    display: flex; flex-direction: column; justify-content: center;
  }

  .hero-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: var(--cyan);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 20px;
    opacity: 0.8;
  }
  .hero-eyebrow::before { content: '▶ '; color: var(--green); }

  .hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 54px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 8px;
    background: linear-gradient(135deg, var(--green) 0%, var(--cyan) 60%, var(--purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
  }

  .hero-sub {
    font-family: 'Orbitron', monospace;
    font-size: 18px;
    color: var(--cyan2);
    letter-spacing: 6px;
    margin-bottom: 28px;
    text-transform: uppercase;
  }

  .hero-desc {
    font-size: 17px;
    color: #7a9ab5;
    max-width: 460px;
    line-height: 1.7;
    margin-bottom: 36px;
  }

  .badges {
    display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 40px;
  }
  .badge {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    padding: 5px 12px;
    border-radius: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: 1px solid;
  }
  .badge-green  { background: rgba(0,255,136,0.08); color: var(--green);  border-color: rgba(0,255,136,0.25); }
  .badge-cyan   { background: rgba(0,212,255,0.08); color: var(--cyan);   border-color: rgba(0,212,255,0.25); }
  .badge-purple { background: rgba(191,90,242,0.08); color: var(--purple); border-color: rgba(191,90,242,0.25); }
  .badge-orange { background: rgba(255,149,0,0.08); color: var(--orange); border-color: rgba(255,149,0,0.25); }
  .badge-red    { background: rgba(255,59,48,0.08);  color: var(--red);   border-color: rgba(255,59,48,0.25); }

  .hero-stats {
    display: flex; gap: 32px;
  }
  .stat { text-align: center; }
  .stat-num {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--green);
    display: block;
  }
  .stat-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: var(--textdim);
    text-transform: uppercase;
    letter-spacing: 2px;
  }

  /* Kali Art Panel */
  .hero-right {
    position: relative;
    background: #050c12;
    border-left: 1px solid #1a3050;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
    padding: 30px;
  }
  .hero-right::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at center, rgba(0,212,255,0.06) 0%, transparent 70%);
  }

  /* ── TERMINAL BLOCK ── */
  .terminal {
    background: #040810;
    border: 1px solid #1a3050;
    border-radius: 8px;
    margin: 0 auto 40px;
    max-width: 900px;
    box-shadow: 0 0 40px rgba(0,212,255,0.06), inset 0 0 20px rgba(0,0,0,0.5);
    overflow: hidden;
  }
  .terminal-bar {
    background: #0c1520;
    padding: 10px 16px;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid #1a3050;
  }
  .term-dot { width: 12px; height: 12px; border-radius: 50%; }
  .term-dot-r { background: #ff3b30; }
  .term-dot-y { background: #ffd60a; }
  .term-dot-g { background: #28ca41; }
  .term-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #4a6070;
    margin-left: 8px;
    letter-spacing: 1px;
  }
  .terminal-body {
    padding: 24px 28px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    line-height: 2;
  }
  .t-prompt { color: var(--green); }
  .t-cmd    { color: var(--text); }
  .t-out    { color: #4a8070; }
  .t-hl-green  { color: var(--green); }
  .t-hl-cyan   { color: var(--cyan); }
  .t-hl-purple { color: var(--purple); }
  .t-hl-orange { color: var(--orange); }
  .t-hl-red    { color: var(--red); }
  .t-hl-yellow { color: var(--yellow); }
  .t-dim       { color: var(--dim); }
  .t-cursor::after {
    content: '█';
    animation: blink 1.2s step-end infinite;
    color: var(--green);
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

  /* ── SECTION ── */
  .section {
    max-width: 1100px;
    margin: 0 auto;
    padding: 60px 40px;
  }

  .section-header {
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 1px solid #1a2a3a;
  }

  .section-icon {
    width: 44px; height: 44px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }
  .icon-green  { background: rgba(0,255,136,0.12); border: 1px solid rgba(0,255,136,0.2); }
  .icon-cyan   { background: rgba(0,212,255,0.12); border: 1px solid rgba(0,212,255,0.2); }
  .icon-purple { background: rgba(191,90,242,0.12); border: 1px solid rgba(191,90,242,0.2); }
  .icon-orange { background: rgba(255,149,0,0.12); border: 1px solid rgba(255,149,0,0.2); }
  .icon-red    { background: rgba(255,59,48,0.12);  border: 1px solid rgba(255,59,48,0.2); }

  .section-title {
    font-family: 'Orbitron', monospace;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 2px;
  }
  .section-title.green  { color: var(--green); }
  .section-title.cyan   { color: var(--cyan); }
  .section-title.purple { color: var(--purple); }
  .section-title.orange { color: var(--orange); }
  .section-title.red    { color: var(--red); }

  .section-mono {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: var(--textdim);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* ── MODULE CARDS ── */
  .modules-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .module-card {
    background: var(--card);
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
  }
  .module-card:hover {
    transform: translateY(-3px);
  }
  .module-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
  }
  .module-card.green::before  { background: linear-gradient(90deg, var(--green), var(--cyan)); box-shadow: 0 0 8px rgba(0,255,136,0.4); }
  .module-card.cyan::before   { background: linear-gradient(90deg, var(--cyan), var(--purple)); box-shadow: 0 0 8px rgba(0,212,255,0.4); }
  .module-card.purple::before { background: linear-gradient(90deg, var(--purple), var(--red)); box-shadow: 0 0 8px rgba(191,90,242,0.4); }
  .module-card.orange::before { background: linear-gradient(90deg, var(--orange), var(--yellow)); box-shadow: 0 0 8px rgba(255,149,0,0.4); }

  .module-card:hover.green  { box-shadow: 0 8px 30px rgba(0,255,136,0.12); }
  .module-card:hover.cyan   { box-shadow: 0 8px 30px rgba(0,212,255,0.12); }
  .module-card:hover.purple { box-shadow: 0 8px 30px rgba(191,90,242,0.12); }
  .module-card:hover.orange { box-shadow: 0 8px 30px rgba(255,149,0,0.12); }

  .module-head {
    padding: 22px 24px 16px;
    display: flex; align-items: flex-start; gap: 16px;
    border-bottom: 1px solid #1a2a3a;
  }
  .module-emoji { font-size: 28px; line-height: 1; }
  .module-name {
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }
  .module-name.green  { color: var(--green); }
  .module-name.cyan   { color: var(--cyan); }
  .module-name.purple { color: var(--purple); }
  .module-name.orange { color: var(--orange); }
  .module-file {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: var(--textdim);
  }
  .module-body { padding: 16px 24px 20px; }
  .module-desc { font-size: 14px; color: #7a9ab5; margin-bottom: 16px; line-height: 1.6; }

  .func-list { list-style: none; display: flex; flex-direction: column; gap: 6px; }
  .func-item {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    display: flex; align-items: center; gap: 8px;
    color: var(--text);
  }
  .func-item::before { content: '→'; color: var(--dim); flex-shrink: 0; }
  .func-name.green  { color: var(--green); }
  .func-name.cyan   { color: var(--cyan); }
  .func-name.purple { color: var(--purple); }
  .func-name.orange { color: var(--orange); }

  /* ── API TABLE ── */
  .api-table-wrap {
    overflow-x: auto;
    border: 1px solid #1a2a3a;
    border-radius: 8px;
  }
  .api-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
  }
  .api-table thead tr {
    background: #0c1520;
    border-bottom: 1px solid #1a2a3a;
  }
  .api-table th {
    padding: 14px 20px;
    text-align: left;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--textdim);
    font-weight: 400;
  }
  .api-table td {
    padding: 12px 20px;
    border-bottom: 1px solid #0f1820;
    color: var(--text);
    vertical-align: middle;
  }
  .api-table tbody tr:last-child td { border-bottom: none; }
  .api-table tbody tr:hover td { background: rgba(0,212,255,0.03); }
  .api-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 10px;
    letter-spacing: 1px;
  }
  .tag-free   { background: rgba(0,255,136,0.1); color: var(--green); border: 1px solid rgba(0,255,136,0.2); }
  .tag-key    { background: rgba(255,149,0,0.1); color: var(--orange); border: 1px solid rgba(255,149,0,0.2); }
  .tag-native { background: rgba(0,212,255,0.1); color: var(--cyan); border: 1px solid rgba(0,212,255,0.2); }

  /* ── INSTALL BLOCK ── */
  .install-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 30px;
  }
  .install-step {
    background: var(--card);
    border: 1px solid #1a2a3a;
    border-radius: 8px;
    padding: 20px;
    position: relative;
  }
  .step-num {
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    color: var(--textdim);
    letter-spacing: 2px;
    margin-bottom: 12px;
  }
  .step-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--cyan);
    margin-bottom: 10px;
  }
  .step-code {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: var(--green);
    background: #030609;
    padding: 8px 12px;
    border-radius: 4px;
    border-left: 2px solid var(--green2);
    word-break: break-all;
  }

  /* ── USAGE EXAMPLES ── */
  .example-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .example-card {
    background: #040810;
    border: 1px solid #1a2a3a;
    border-radius: 8px;
    overflow: hidden;
  }
  .example-head {
    padding: 12px 16px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid #1a2a3a;
  }
  .example-head.green  { color: var(--green);  background: rgba(0,255,136,0.05); }
  .example-head.cyan   { color: var(--cyan);   background: rgba(0,212,255,0.05); }
  .example-head.purple { color: var(--purple); background: rgba(191,90,242,0.05); }
  .example-head.orange { color: var(--orange); background: rgba(255,149,0,0.05); }
  .example-head.red    { color: var(--red);    background: rgba(255,59,48,0.05); }
  .example-body {
    padding: 16px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    line-height: 2;
  }

  /* ── ALERT BOX ── */
  .alert {
    background: rgba(255,59,48,0.06);
    border: 1px solid rgba(255,59,48,0.25);
    border-left: 3px solid var(--red);
    border-radius: 6px;
    padding: 16px 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: #d0a0a0;
    margin: 40px 0;
  }
  .alert-head { color: var(--red); font-size: 11px; letter-spacing: 3px; margin-bottom: 8px; }

  .info-box {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-left: 3px solid var(--cyan);
    border-radius: 6px;
    padding: 16px 20px;
    font-size: 14px;
    color: #7ab0c8;
    margin: 30px 0;
  }
  .info-box-head { color: var(--cyan); font-family: 'Share Tech Mono', monospace; font-size: 10px; letter-spacing: 3px; margin-bottom: 8px; }

  /* ── DIVIDER ── */
  .section-divider {
    max-width: 1100px;
    margin: 0 auto;
    border: none;
    border-top: 1px solid #0f1820;
    position: relative;
  }
  .section-divider::after {
    content: '◈';
    position: absolute; top: -10px; left: 50%; transform: translateX(-50%);
    color: #1a2a3a;
    background: var(--bg);
    padding: 0 12px;
    font-size: 14px;
  }

  /* ── FOOTER ── */
  .footer {
    background: #050b10;
    border-top: 1px solid #1a2a3a;
    padding: 40px;
    text-align: center;
  }
  .footer-logo {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 900;
    background: linear-gradient(90deg, var(--green), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
  }
  .footer-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: var(--textdim);
    letter-spacing: 3px;
    margin-bottom: 20px;
  }
  .footer-disclaimer {
    font-size: 12px;
    color: #2a3a48;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.8;
  }

  /* responsive */
  @media(max-width: 900px) {
    .hero-inner { grid-template-columns: 1fr; }
    .hero-right { display: none; }
    .modules-grid { grid-template-columns: 1fr; }
    .install-grid { grid-template-columns: 1fr; }
    .example-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 36px; }
  }
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════
     HERO
════════════════════════════════════════════════════════════ -->
<header class="hero">
  <div class="hero-inner">
    <div class="hero-left">
      <div class="hero-eyebrow">Pablo Cyber — Forensics Suite v2.0</div>
      <div class="hero-title">PABLO CYBER</div>
      <div class="hero-sub">Forensics Toolkit</div>
      <p class="hero-desc">
        Suite completa de ferramentas de forense digital, OSINT, análise de memória RAM e forense de rede — construída sobre APIs públicas e técnicas éticas de investigação.
      </p>
      <div class="badges">
        <span class="badge badge-green">Python 3.9+</span>
        <span class="badge badge-cyan">OSINT</span>
        <span class="badge badge-purple">Memória RAM</span>
        <span class="badge badge-orange">Rede / PCAP</span>
        <span class="badge badge-red">Ethical Only</span>
      </div>
      <div class="hero-stats">
        <div class="stat"><span class="stat-num">4</span><span class="stat-label">Módulos</span></div>
        <div class="stat"><span class="stat-num">30+</span><span class="stat-label">Funções</span></div>
        <div class="stat"><span class="stat-num">8</span><span class="stat-label">APIs</span></div>
        <div class="stat"><span class="stat-num">100%</span><span class="stat-label">Open Source</span></div>
      </div>
    </div>

    <!-- Kali Dragon + Forense Art -->
    <div class="hero-right">
      <svg viewBox="0 0 380 460" width="100%" style="max-width:380px; position:relative; z-index:2;" xmlns="http://www.w3.org/2000/svg">
        <!-- Outer glow ring -->
        <circle cx="190" cy="195" r="155" fill="none" stroke="#00d4ff" stroke-width="0.5" stroke-dasharray="4 6" opacity="0.3"/>
        <circle cx="190" cy="195" r="140" fill="none" stroke="#00ff88" stroke-width="0.3" stroke-dasharray="2 8" opacity="0.2"/>

        <!-- BG hex pattern -->
        <g opacity="0.07">
          <text x="10" y="30" fill="#00d4ff" font-family="monospace" font-size="9">01101011 01100001 01101100 01101001</text>
          <text x="10" y="44" fill="#00d4ff" font-family="monospace" font-size="9">10110100 01101111 01110010 01100101</text>
          <text x="10" y="58" fill="#00ff88" font-family="monospace" font-size="9">01101110 01110011 01101001 01100011</text>
          <text x="10" y="72" fill="#bf5af2" font-family="monospace" font-size="9">01110011 01100101 01100011 01110101</text>
        </g>

        <!-- ── Kali Dragon (stylized SVG) ── -->
        <!-- Body -->
        <ellipse cx="190" cy="210" rx="72" ry="90" fill="#0d1b2a" stroke="#1a3a5a" stroke-width="1"/>

        <!-- Dragon scales pattern -->
        <g opacity="0.6">
          <ellipse cx="165" cy="175" rx="18" ry="12" fill="none" stroke="#00ff88" stroke-width="0.8"/>
          <ellipse cx="195" cy="170" rx="18" ry="12" fill="none" stroke="#00ff88" stroke-width="0.8"/>
          <ellipse cx="180" cy="192" rx="18" ry="12" fill="none" stroke="#00d4ff" stroke-width="0.8"/>
          <ellipse cx="210" cy="188" rx="18" ry="12" fill="none" stroke="#00d4ff" stroke-width="0.8"/>
          <ellipse cx="167" cy="210" rx="16" ry="11" fill="none" stroke="#bf5af2" stroke-width="0.8"/>
          <ellipse cx="197" cy="207" rx="16" ry="11" fill="none" stroke="#bf5af2" stroke-width="0.8"/>
          <ellipse cx="177" cy="228" rx="16" ry="10" fill="none" stroke="#ff9500" stroke-width="0.8"/>
          <ellipse cx="205" cy="225" rx="14" ry="10" fill="none" stroke="#ff9500" stroke-width="0.8"/>
        </g>

        <!-- Head -->
        <ellipse cx="190" cy="130" rx="42" ry="48" fill="#0d1b2a" stroke="#1a3a5a" stroke-width="1.2"/>

        <!-- Eyes - glowing -->
        <ellipse cx="174" cy="120" rx="9" ry="11" fill="#00ff88" opacity="0.9"/>
        <ellipse cx="206" cy="120" rx="9" ry="11" fill="#00ff88" opacity="0.9"/>
        <ellipse cx="174" cy="121" rx="5" ry="7" fill="#030c08"/>
        <ellipse cx="206" cy="121" rx="5" ry="7" fill="#030c08"/>
        <!-- Eye glow -->
        <ellipse cx="174" cy="120" rx="11" ry="13" fill="none" stroke="#00ff88" stroke-width="1" opacity="0.5"/>
        <ellipse cx="206" cy="120" rx="11" ry="13" fill="none" stroke="#00ff88" stroke-width="1" opacity="0.5"/>

        <!-- Horns -->
        <polygon points="160,90 148,45 170,88" fill="#1a3050" stroke="#00d4ff" stroke-width="0.8"/>
        <polygon points="220,90 232,45 210,88" fill="#1a3050" stroke="#00d4ff" stroke-width="0.8"/>
        <!-- Horn detail lines -->
        <line x1="155" y1="80" x2="150" y2="52" stroke="#00d4ff" stroke-width="0.5" opacity="0.6"/>
        <line x1="225" y1="80" x2="230" y2="52" stroke="#00d4ff" stroke-width="0.5" opacity="0.6"/>

        <!-- Snout -->
        <ellipse cx="190" cy="148" rx="22" ry="14" fill="#0a1520" stroke="#1a3050" stroke-width="1"/>
        <!-- Nostrils -->
        <circle cx="182" cy="147" r="3" fill="#00ff88" opacity="0.5"/>
        <circle cx="198" cy="147" r="3" fill="#00ff88" opacity="0.5"/>

        <!-- Wings outline (stylized) -->
        <path d="M150,175 Q80,140 60,190 Q90,220 130,205 Z" fill="#0a1525" stroke="#00d4ff" stroke-width="0.8" opacity="0.7"/>
        <path d="M230,175 Q300,140 320,190 Q290,220 250,205 Z" fill="#0a1525" stroke="#00d4ff" stroke-width="0.8" opacity="0.7"/>

        <!-- Wing veins -->
        <path d="M150,175 Q100,165 70,185" fill="none" stroke="#00d4ff" stroke-width="0.5" opacity="0.4"/>
        <path d="M145,182 Q95,180 68,195" fill="none" stroke="#00d4ff" stroke-width="0.5" opacity="0.4"/>
        <path d="M230,175 Q280,165 310,185" fill="none" stroke="#00d4ff" stroke-width="0.5" opacity="0.4"/>
        <path d="M235,182 Q285,180 312,195" fill="none" stroke="#00d4ff" stroke-width="0.5" opacity="0.4"/>

        <!-- Claws -->
        <path d="M165,295 Q155,310 148,320 M165,295 Q160,315 155,326 M165,295 Q165,312 163,324" fill="none" stroke="#00ff88" stroke-width="1.2" opacity="0.8"/>
        <path d="M215,295 Q225,310 232,320 M215,295 Q220,315 225,326 M215,295 Q215,312 217,324" fill="none" stroke="#00ff88" stroke-width="1.2" opacity="0.8"/>

        <!-- Tail -->
        <path d="M190,298 Q220,330 240,360 Q255,385 235,390 Q215,395 210,375" fill="none" stroke="#1a3a5a" stroke-width="3"/>
        <path d="M190,298 Q220,330 240,360 Q255,385 235,390 Q215,395 210,375" fill="none" stroke="#00d4ff" stroke-width="0.8" opacity="0.5"/>

        <!-- KALI text on chest -->
        <text x="190" y="256" text-anchor="middle" fill="#00ff88" font-family="monospace" font-size="13" font-weight="bold" letter-spacing="5" opacity="0.9">KALI</text>
        <text x="190" y="272" text-anchor="middle" fill="#00d4ff" font-family="monospace" font-size="9" letter-spacing="3" opacity="0.6">LINUX</text>

        <!-- Circuit lines on body -->
        <g opacity="0.3">
          <path d="M175,230 H160 V245 H150" fill="none" stroke="#00ff88" stroke-width="0.5"/>
          <circle cx="150" cy="245" r="2" fill="#00ff88"/>
          <path d="M205,235 H220 V250 H230" fill="none" stroke="#bf5af2" stroke-width="0.5"/>
          <circle cx="230" cy="250" r="2" fill="#bf5af2"/>
        </g>

        <!-- Bottom section — forensics tools floating -->
        <!-- Magnifier icon -->
        <circle cx="75" cy="370" r="22" fill="none" stroke="#00ff88" stroke-width="1.5" opacity="0.7"/>
        <circle cx="75" cy="370" r="14" fill="none" stroke="#00ff88" stroke-width="1" opacity="0.5"/>
        <line x1="91" y1="386" x2="103" y2="398" stroke="#00ff88" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
        <text x="75" y="375" text-anchor="middle" fill="#00ff88" font-family="monospace" font-size="9" opacity="0.8">OSINT</text>

        <!-- Network icon -->
        <circle cx="190" cy="378" r="8" fill="#0a1525" stroke="#00d4ff" stroke-width="1.2" opacity="0.8"/>
        <circle cx="165" cy="398" r="5" fill="#0a1525" stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
        <circle cx="215" cy="398" r="5" fill="#0a1525" stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
        <circle cx="190" cy="415" r="5" fill="#0a1525" stroke="#00d4ff" stroke-width="1" opacity="0.7"/>
        <line x1="190" y1="386" x2="168" y2="394" stroke="#00d4ff" stroke-width="0.8" opacity="0.6"/>
        <line x1="190" y1="386" x2="212" y2="394" stroke="#00d4ff" stroke-width="0.8" opacity="0.6"/>
        <line x1="190" y1="386" x2="190" y2="410" stroke="#00d4ff" stroke-width="0.8" opacity="0.6"/>

        <!-- Memory chip icon -->
        <rect x="283" y="355" width="52" height="36" rx="3" fill="#0a1525" stroke="#bf5af2" stroke-width="1.2" opacity="0.8"/>
        <g opacity="0.6">
          <line x1="291" y1="355" x2="291" y2="349" stroke="#bf5af2" stroke-width="1"/>
          <line x1="300" y1="355" x2="300" y2="349" stroke="#bf5af2" stroke-width="1"/>
          <line x1="309" y1="355" x2="309" y2="349" stroke="#bf5af2" stroke-width="1"/>
          <line x1="318" y1="355" x2="318" y2="349" stroke="#bf5af2" stroke-width="1"/>
          <line x1="291" y1="391" x2="291" y2="397" stroke="#bf5af2" stroke-width="1"/>
          <line x1="300" y1="391" x2="300" y2="397" stroke="#bf5af2" stroke-width="1"/>
          <line x1="309" y1="391" x2="309" y2="397" stroke="#bf5af2" stroke-width="1"/>
          <line x1="318" y1="391" x2="318" y2="397" stroke="#bf5af2" stroke-width="1"/>
        </g>
        <text x="309" y="377" text-anchor="middle" fill="#bf5af2" font-family="monospace" font-size="8" opacity="0.8">RAM</text>

        <!-- author watermark -->
        <text x="190" y="450" text-anchor="middle" fill="#1a2a3a" font-family="monospace" font-size="10" letter-spacing="3">PABLO CYBER © 2024</text>
      </svg>
    </div>
  </div>
</header>


<!-- ═══════════════════════════════════════════════════════════
     TERMINAL INTRO
════════════════════════════════════════════════════════════ -->
<div style="background: var(--bg2); border-top: 1px solid #0f1820; border-bottom: 1px solid #0f1820; padding: 50px 40px;">
<div style="max-width: 900px; margin: 0 auto;">
<div class="terminal">
  <div class="terminal-bar">
    <div class="term-dot term-dot-r"></div>
    <div class="term-dot term-dot-y"></div>
    <div class="term-dot term-dot-g"></div>
    <span class="term-title">pablo@kali: ~/forensics-toolkit — bash</span>
  </div>
  <div class="terminal-body">
    <div><span class="t-prompt">┌──(pablo㉿kali)-[~/pablo-cyber-forensics]</span></div>
    <div><span class="t-prompt">└─$ </span><span class="t-cmd">python3 forensics_engine.py --sysinfo</span></div>
    <div class="t-out" style="padding-left:20px">
      <span class="t-hl-green">██ [INIT]</span> ForensicsEngine v2.0 initialized | Session: 20241201_143022
    </div>
    <div class="t-out" style="padding-left:20px">
      <span class="t-hl-cyan">✔ [INFO]</span> Collecting system baseline for: pablo-kali
    </div>
    <div><span class="t-prompt">┌──(pablo㉿kali)-[~/pablo-cyber-forensics]</span></div>
    <div><span class="t-prompt">└─$ </span><span class="t-cmd">python3 osint_engine.py --domain <span class="t-hl-cyan">target.com</span></span></div>
    <div class="t-out" style="padding-left:20px"><span class="t-hl-green">▶ [OSINT]</span> Starting full domain investigation...</div>
    <div class="t-out" style="padding-left:20px"><span class="t-hl-cyan">▶ [CRT.SH]</span> target.com: <span class="t-hl-yellow">47</span> subdomains found</div>
    <div class="t-out" style="padding-left:20px"><span class="t-hl-cyan">▶ [HACKERTARGET]</span> target.com: <span class="t-hl-yellow">12</span> hosts</div>
    <div><span class="t-prompt">┌──(pablo㉿kali)-[~/pablo-cyber-forensics]</span></div>
    <div><span class="t-prompt">└─$ </span><span class="t-cmd">python3 memory_forensics.py --processes</span></div>
    <div class="t-out" style="padding-left:20px"><span class="t-hl-purple">⚠ [ALERT]</span> Suspicious process detected: <span class="t-hl-red">nc</span> [SUSPICIOUS_NAME:nc]</div>
    <div><span class="t-prompt">┌──(pablo㉿kali)-[~/pablo-cyber-forensics]</span></div>
    <div><span class="t-prompt">└─$ </span><span class="t-cmd">python3 network_forensics.py --analyze capture.pcap</span></div>
    <div class="t-out" style="padding-left:20px"><span class="t-hl-orange">▶ [PCAP]</span> Loaded 2847 packets | Unique IPs: <span class="t-hl-yellow">34</span></div>
    <div><span class="t-prompt">┌──(pablo㉿kali)-[~/pablo-cyber-forensics]</span></div>
    <div><span class="t-prompt">└─$ </span><span class="t-cursor"></span></div>
  </div>
</div>
</div>
</div>


<!-- ═══════════════════════════════════════════════════════════
     MÓDULOS
════════════════════════════════════════════════════════════ -->
<div class="section">
  <div class="section-header">
    <div class="section-icon icon-green">🧩</div>
    <div>
      <div class="section-title green">MÓDULOS DO TOOLKIT</div>
      <div class="section-mono">04 motores especializados</div>
    </div>
  </div>

  <div class="modules-grid">

    <!-- OSINT ENGINE -->
    <div class="module-card green">
      <div class="module-head">
        <div class="module-emoji">🔍</div>
        <div>
          <div class="module-name green">OSINT ENGINE</div>
          <div class="module-file">osint_engine.py</div>
        </div>
      </div>
      <div class="module-body">
        <p class="module-desc">
          Motor de inteligência de fontes abertas usando APIs públicas. Investiga domínios, usuários GitHub, e-mails e infraestrutura de rede sem nenhuma ferramenta paga.
        </p>
        <ul class="func-list">
          <li class="func-item"><span class="func-name green">investigate_domain()</span> — OSINT completo de domínio</li>
          <li class="func-item"><span class="func-name green">github_user_profile()</span> — perfil + repos + eventos</li>
          <li class="func-item"><span class="func-name green">crtsh_domain_search()</span> — subdomínios via crt.sh</li>
          <li class="func-item"><span class="func-name green">haveibeenpwned()</span> — vazamentos de e-mail</li>
          <li class="func-item"><span class="func-name green">hackertarget_whois()</span> — WHOIS + DNS + ASN</li>
          <li class="func-item"><span class="func-name green">email_gravatar()</span> — perfil vinculado a e-mail</li>
        </ul>
      </div>
    </div>

    <!-- FORENSICS ENGINE -->
    <div class="module-card cyan">
      <div class="module-head">
        <div class="module-emoji">🔬</div>
        <div>
          <div class="module-name cyan">FORENSICS ENGINE</div>
          <div class="module-file">forensics_engine.py</div>
        </div>
      </div>
      <div class="module-body">
        <p class="module-desc">
          Motor central de forense digital. Hashing criptográfico, linha do tempo de arquivos, extração de strings e coleta de baseline do sistema para análise forense.
        </p>
        <ul class="func-list">
          <li class="func-item"><span class="func-name cyan">hash_file()</span> — MD5/SHA1/SHA256/SHA512</li>
          <li class="func-item"><span class="func-name cyan">collect_system_info()</span> — baseline do host</li>
          <li class="func-item"><span class="func-name cyan">build_file_timeline()</span> — MACtimes de arquivos</li>
          <li class="func-item"><span class="func-name cyan">extract_strings()</span> — strings de binários</li>
          <li class="func-item"><span class="func-name cyan">generate_report()</span> — relatório JSON completo</li>
        </ul>
      </div>
    </div>

    <!-- MEMORY FORENSICS -->
    <div class="module-card purple">
      <div class="module-head">
        <div class="module-emoji">🧠</div>
        <div>
          <div class="module-name purple">MEMORY FORENSICS</div>
          <div class="module-file">memory_forensics.py</div>
        </div>
      </div>
      <div class="module-body">
        <p class="module-desc">
          Análise de memória RAM em tempo real. Lista processos, detecta atividade suspeita, extrai strings de memória de processo e inspeciona bibliotecas carregadas.
        </p>
        <ul class="func-list">
          <li class="func-item"><span class="func-name purple">list_processes()</span> — heurística de suspeitos</li>
          <li class="func-item"><span class="func-name purple">dump_process_strings()</span> — strings do /proc/mem</li>
          <li class="func-item"><span class="func-name purple">get_loaded_modules()</span> — .so/.dylib por PID</li>
          <li class="func-item"><span class="func-name purple">get_network_connections()</span> — conns por PID</li>
          <li class="func-item"><span class="func-name purple">generate_memory_report()</span> — dump completo</li>
        </ul>
      </div>
    </div>

    <!-- NETWORK FORENSICS -->
    <div class="module-card orange">
      <div class="module-head">
        <div class="module-emoji">🌐</div>
        <div>
          <div class="module-name orange">NETWORK FORENSICS</div>
          <div class="module-file">network_forensics.py</div>
        </div>
      </div>
      <div class="module-body">
        <p class="module-desc">
          Análise de capturas de tráfego de rede (PCAP). Extrai IPs únicos, protocolos, sessões HTTP/DNS e detecta padrões anômalos em tráfego de rede.
        </p>
        <ul class="func-list">
          <li class="func-item"><span class="func-name orange">analyze_pcap()</span> — sumário de captura</li>
          <li class="func-item"><span class="func-name orange">extract_http_sessions()</span> — requests/responses</li>
          <li class="func-item"><span class="func-name orange">extract_dns_queries()</span> — domínios consultados</span></li>
          <li class="func-item"><span class="func-name orange">get_unique_ips()</span> — mapa de IPs únicos</li>
          <li class="func-item"><span class="func-name orange">detect_anomalies()</span> — padrões suspeitos</li>
        </ul>
      </div>
    </div>

  </div>
</div>

<hr class="section-divider">

<!-- ═══════════════════════════════════════════════════════════
     APIs INTEGRADAS
════════════════════════════════════════════════════════════ -->
<div class="section">
  <div class="section-header">
    <div class="section-icon icon-cyan">🔌</div>
    <div>
      <div class="section-title cyan">APIs INTEGRADAS</div>
      <div class="section-mono">fontes públicas e pagas</div>
    </div>
  </div>

  <div class="api-table-wrap">
    <table class="api-table">
      <thead>
        <tr>
          <th>API / Serviço</th>
          <th>Módulo</th>
          <th>Capacidade</th>
          <th>Auth</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="t-hl-green">GitHub API</span></td>
          <td><span class="t-hl-cyan">osint_engine</span></td>
          <td>Perfis, repos, eventos, busca de código</td>
          <td><span class="api-tag tag-free">Token opcional</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-green">crt.sh</span></td>
          <td><span class="t-hl-cyan">osint_engine</span></td>
          <td>Certificate Transparency — subdomínios</td>
          <td><span class="api-tag tag-free">Free</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-green">HackerTarget</span></td>
          <td><span class="t-hl-cyan">osint_engine</span></td>
          <td>DNS, WHOIS, reverse IP, ASN, traceroute</td>
          <td><span class="api-tag tag-free">Free</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-orange">HaveIBeenPwned</span></td>
          <td><span class="t-hl-cyan">osint_engine</span></td>
          <td>Verificação de vazamentos por e-mail</td>
          <td><span class="api-tag tag-key">API Key</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-green">Gravatar API</span></td>
          <td><span class="t-hl-cyan">osint_engine</span></td>
          <td>Perfil vinculado a hash MD5 do e-mail</td>
          <td><span class="api-tag tag-free">Free</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-purple">/proc filesystem</span></td>
          <td><span class="t-hl-purple">memory_forensics</span></td>
          <td>Processos, mapas de memória, módulos</td>
          <td><span class="api-tag tag-native">Linux Nativo</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-orange">Scapy / PCAP</span></td>
          <td><span class="t-hl-orange">network_forensics</span></td>
          <td>Análise de pacotes, sessões, DNS, HTTP</td>
          <td><span class="api-tag tag-native">Local</span></td>
        </tr>
        <tr>
          <td><span class="t-hl-cyan">hashlib / stdlib</span></td>
          <td><span class="t-hl-cyan">forensics_engine</span></td>
          <td>MD5, SHA1, SHA256, SHA512, strings</td>
          <td><span class="api-tag tag-native">Built-in</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<hr class="section-divider">

<!-- ═══════════════════════════════════════════════════════════
     INSTALAÇÃO
════════════════════════════════════════════════════════════ -->
<div class="section">
  <div class="section-header">
    <div class="section-icon icon-orange">⚡</div>
    <div>
      <div class="section-title orange">INSTALAÇÃO RÁPIDA</div>
      <div class="section-mono">setup em 3 passos</div>
    </div>
  </div>

  <div class="install-grid">
    <div class="install-step">
      <div class="step-num">PASSO 01 — CLONE</div>
      <div class="step-title">Clonar repositório</div>
      <div class="step-code">git clone https://github.com/pablo-cyber/forensics-toolkit<br>cd forensics-toolkit</div>
    </div>
    <div class="install-step">
      <div class="step-num">PASSO 02 — DEPENDÊNCIAS</div>
      <div class="step-title">Instalar pacotes</div>
      <div class="step-code">pip3 install scapy requests<br><br># Opcional: scapy para pcap<br>sudo apt install python3-scapy</div>
    </div>
    <div class="install-step">
      <div class="step-num">PASSO 03 — ENV VARS</div>
      <div class="step-title">Configurar tokens</div>
      <div class="step-code">export GITHUB_TOKEN="ghp_..."<br>export HIBP_KEY="sua-chave-hibp"</div>
    </div>
  </div>

  <div class="info-box">
    <div class="info-box-head">💡 KALI LINUX RECOMENDADO</div>
    Todos os módulos foram testados no Kali Linux 2024.x. No Kali, as dependências <code style="color:var(--cyan)">scapy</code>, <code style="color:var(--cyan)">python3</code> e acesso ao <code style="color:var(--cyan)">/proc</code> já estão disponíveis por padrão. Para uso completo do módulo de memória, execute como <strong>root</strong>.
  </div>
</div>

<hr class="section-divider">

<!-- ═══════════════════════════════════════════════════════════
     EXEMPLOS DE USO
════════════════════════════════════════════════════════════ -->
<div class="section">
  <div class="section-header">
    <div class="section-icon icon-purple">▶</div>
    <div>
      <div class="section-title purple">EXEMPLOS DE USO</div>
      <div class="section-mono">comandos CLI por módulo</div>
    </div>
  </div>

  <div class="example-grid">

    <div class="example-card">
      <div class="example-head green">🔍 OSINT — Domínio completo</div>
      <div class="example-body">
        <span class="t-prompt"># Investigação total de domínio</span><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--domain <span class="t-hl-cyan">alvo.com.br</span></span><br><br>
        <span class="t-prompt"># Buscar subdomínios apenas</span><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--subdomains <span class="t-hl-cyan">empresa.com</span></span><br><br>
        <span class="t-prompt"># OSINT completo de usuário GitHub</span><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--github-user <span class="t-hl-cyan">torvalds</span> \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--github-token <span class="t-hl-yellow">$GITHUB_TOKEN</span></span>
      </div>
    </div>

    <div class="example-card">
      <div class="example-head cyan">🔬 FORENSE — Hashing e Timeline</div>
      <div class="example-body">
        <span class="t-prompt"># Hash criptográfico de arquivo</span><br>
        <span class="t-cmd">python3 forensics_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--hash <span class="t-hl-cyan">/suspeito/malware.exe</span></span><br><br>
        <span class="t-prompt"># Timeline de modificação de dir</span><br>
        <span class="t-cmd">python3 forensics_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--timeline <span class="t-hl-cyan">/var/www/html</span></span><br><br>
        <span class="t-prompt"># Strings de binário suspeito</span><br>
        <span class="t-cmd">python3 forensics_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--strings <span class="t-hl-cyan">binario_suspeito</span></span>
      </div>
    </div>

    <div class="example-card">
      <div class="example-head purple">🧠 MEMÓRIA — Análise de processos</div>
      <div class="example-body">
        <span class="t-prompt"># Listar todos os processos</span><br>
        <span class="t-cmd">sudo python3 memory_forensics.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--processes</span><br><br>
        <span class="t-prompt"># Strings da memória de um PID</span><br>
        <span class="t-cmd">sudo python3 memory_forensics.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--strings <span class="t-hl-purple">1337</span></span><br><br>
        <span class="t-prompt"># Relatório de memória completo</span><br>
        <span class="t-cmd">sudo python3 memory_forensics.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--report --output <span class="t-hl-cyan">/evidencias/</span></span>
      </div>
    </div>

    <div class="example-card">
      <div class="example-head orange">🌐 REDE — PCAP e tráfego</div>
      <div class="example-body">
        <span class="t-prompt"># Analisar captura de rede</span><br>
        <span class="t-cmd">python3 network_forensics.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--analyze <span class="t-hl-cyan">captura.pcap</span></span><br><br>
        <span class="t-prompt"># Extrair queries DNS</span><br>
        <span class="t-cmd">python3 network_forensics.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--dns <span class="t-hl-cyan">captura.pcap</span></span><br><br>
        <span class="t-prompt"># IPs únicos no tráfego</span><br>
        <span class="t-cmd">python3 network_forensics.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--ips <span class="t-hl-cyan">captura.pcap</span></span>
      </div>
    </div>

    <div class="example-card">
      <div class="example-head red">📧 E-MAIL — Investigação</div>
      <div class="example-body">
        <span class="t-prompt"># OSINT completo de e-mail</span><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--email <span class="t-hl-cyan">alvo@exemplo.com</span> \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--hibp-key <span class="t-hl-yellow">$HIBP_KEY</span></span><br><br>
        <span class="t-out">&nbsp;→ Gravatar: encontrado (foto, bio)</span><br>
        <span class="t-out">&nbsp;→ HIBP: 3 vazamentos detectados</span><br>
        <span class="t-out">&nbsp;→ Breaches: LinkedIn, Adobe, RockYou</span>
      </div>
    </div>

    <div class="example-card">
      <div class="example-head cyan">🔎 GITHUB — Segredos expostos</div>
      <div class="example-body">
        <span class="t-prompt"># Buscar credenciais no GitHub</span><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--github-search <span class="t-hl-red">"AWS_SECRET_KEY"</span></span><br><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--github-search <span class="t-hl-red">"password=empresa123"</span></span><br><br>
        <span class="t-prompt"># Membros de organização</span><br>
        <span class="t-cmd">python3 osint_engine.py \</span><br>
        <span class="t-cmd">&nbsp;&nbsp;--github-org <span class="t-hl-cyan">nome-da-org</span></span>
      </div>
    </div>

  </div>
</div>

<hr class="section-divider">

<!-- ═══════════════════════════════════════════════════════════
     ARQUITETURA
════════════════════════════════════════════════════════════ -->
<div class="section">
  <div class="section-header">
    <div class="section-icon icon-cyan">🏗️</div>
    <div>
      <div class="section-title cyan">ARQUITETURA DO PROJETO</div>
      <div class="section-mono">estrutura de arquivos</div>
    </div>
  </div>

  <div class="terminal" style="max-width:100%">
    <div class="terminal-bar">
      <div class="term-dot term-dot-r"></div>
      <div class="term-dot term-dot-y"></div>
      <div class="term-dot term-dot-g"></div>
      <span class="term-title">pablo@kali: tree pablo-cyber-forensics/</span>
    </div>
    <div class="terminal-body">
      <span class="t-hl-cyan">pablo-cyber-forensics/</span><br>
      <span class="t-dim">├── </span><span class="t-hl-green">forensics_engine.py</span>  <span class="t-dim">  ← Core: hash, timeline, strings, sysinfo</span><br>
      <span class="t-dim">├── </span><span class="t-hl-green">osint_engine.py</span>      <span class="t-dim">  ← OSINT: GitHub, crt.sh, HackerTarget, HIBP</span><br>
      <span class="t-dim">├── </span><span class="t-hl-purple">memory_forensics.py</span>  <span class="t-dim">  ← RAM: processos, /proc, módulos, netconn</span><br>
      <span class="t-dim">├── </span><span class="t-hl-orange">network_forensics.py</span> <span class="t-dim">  ← Rede: PCAP, HTTP, DNS, IPs únicos</span><br>
      <span class="t-dim">├── </span><span class="t-hl-cyan">README.html</span>          <span class="t-dim">  ← Esta documentação</span><br>
      <span class="t-dim">├── </span><span class="t-dim">forensics_output/</span>    <span class="t-dim">  ← Relatórios JSON gerados</span><br>
      <span class="t-dim">└── </span><span class="t-dim">mem_output/</span>          <span class="t-dim">  ← Dumps de memória</span><br><br>
      <span class="t-out">4 files Python  |  Zero dependências pagas  |  Kali Linux nativo</span>
    </div>
  </div>
</div>

<hr class="section-divider">

<!-- ═══════════════════════════════════════════════════════════
     DISCLAIMER
════════════════════════════════════════════════════════════ -->
<div class="section">
  <div class="alert">
    <div class="alert-head">⚠ DISCLAIMER — USO ÉTICO OBRIGATÓRIO</div>
    Esta suite de ferramentas é desenvolvida exclusivamente para fins legítimos: testes de penetração autorizados, resposta a incidentes, pesquisa de segurança e forense em sistemas próprios ou com permissão explícita por escrito. O uso não autorizado em sistemas de terceiros é <strong>ilegal</strong> e violará leis de crimes cibernéticos como a Lei Carolina Dieckmann (Brasil) e o Computer Fraud and Abuse Act (EUA). O autor não se responsabiliza por uso indevido. <strong>Hackeie com ética.</strong>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════
     FOOTER
════════════════════════════════════════════════════════════ -->
<footer class="footer">
  <div class="footer-logo">PABLO CYBER</div>
  <div class="footer-sub">Digital Forensics · OSINT · Memory Analysis · Network Forensics</div>
  <div style="display:flex; justify-content:center; gap:16px; margin-bottom:24px; flex-wrap:wrap;">
    <span class="badge badge-green">Python 3.9+</span>
    <span class="badge badge-cyan">Linux / Kali</span>
    <span class="badge badge-purple">Open Source</span>
    <span class="badge badge-orange">Ethical Use Only</span>
  </div>
  <p class="footer-disclaimer">
    Construído com 🖤 por PABLO CYBER. Ferramentas desenvolvidas para a comunidade de segurança ofensiva e defensiva.<br>
    <span style="color:#1a3050">Tested on Kali Linux 2024.x · Python 3.11 · Ubuntu 22.04</span>
  </p>
</footer>

</body>
</html>
