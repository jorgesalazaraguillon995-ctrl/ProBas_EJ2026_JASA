"""
╔══════════════════════════════════════════════════════╗
║   🔴  IRON MAN CLAP DETECTOR  —  GUI Edition        ║
║   Requiere:  pip install pyaudio numpy matplotlib    ║
║   Corre:     python3 ironman_gui.py                  ║
╚══════════════════════════════════════════════════════╝
"""
import numpy as np
import matplotlib
# Intenta backends en orden hasta que uno funcione
for _backend in ["Qt5Agg", "Qt6Agg", "TkAgg", "WXAgg", "MacOSX"]:
    try:
        matplotlib.use(_backend)
        import matplotlib.pyplot as _test_plt
        _test_plt.figure(); _test_plt.close("all")
        break
    except Exception:
        continue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe
import threading, time, random, math, wave, sys, os

# ── PyAudio opcional ──────────────────────────────────
try:
    import pyaudio
    AUDIO_OK = True
except ImportError:
    AUDIO_OK = False

# ══════════════════════════════════════════════════════
#  SÍNTESIS IRON MAN RIFF
# ══════════════════════════════════════════════════════
SR = 44100

def note_freq(note):
    notes = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,
             "F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
    name = note[:-1]; octave = int(note[-1])
    return 440.0 * (2 ** ((notes[name] + (octave+1)*12 - 69) / 12))

def synth_note(freq, dur, vol=0.6):
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    sig  = np.sin(2*np.pi*freq*t)
    sig += 0.4*np.sin(2*np.pi*freq*2*t)
    sig += 0.25*np.sin(2*np.pi*freq*3*t)
    sig += 0.12*np.sin(2*np.pi*freq*4*t)
    clip = 0.55
    sig  = np.clip(sig, -clip, clip) / clip
    # ADSR
    a,d = int(0.008*n), int(0.05*n)
    s   = int(0.80*n)
    r   = max(n-a-d-s, 1)
    env = np.concatenate([
        np.linspace(0,1,a), np.linspace(1,.75,d),
        np.full(s,.75), np.linspace(.75,0,r)
    ])[:n]
    return (sig * env * vol).astype(np.float32)

def build_riff():
    beat = 60/120
    seq  = [("E2",.4),("E2",.4),("G2",.4),("E2",.6),
            ("A2",.4),("G2",.4),("E2",.9),
            ("E2",.25),
            ("E2",.4),("E2",.4),("G2",.4),("E2",.6),
            ("A2",.4),("G2",.4),("E2",1.2)]
    parts = []
    for note, b in seq:
        f  = note_freq(note)
        dur= b*beat
        lo = synth_note(f,     dur, .45)
        hi = synth_note(f*2,   dur, .55)
        n  = max(len(lo),len(hi))
        lo = np.pad(lo,(0,n-len(lo))); hi = np.pad(hi,(0,n-len(hi)))
        parts.append(lo*.4 + hi*.6)
    arr = np.concatenate(parts)
    peak = np.max(np.abs(arr))
    return arr/peak if peak>0 else arr

def play_riff(pa, riff):
    stream = pa.open(format=pyaudio.paInt16,channels=1,
                     rate=SR,output=True,frames_per_buffer=1024)
    stream.write((riff*32767).astype(np.int16).tobytes())
    stream.stop_stream(); stream.close()

def save_wav_and_play(riff):
    path = "iron_man_riff.wav"
    arr16 = (riff*32767).astype(np.int16)
    with wave.open(path,"w") as f:
        f.setnchannels(1); f.setsampwidth(2)
        f.setframerate(SR); f.writeframes(arr16.tobytes())
    if sys.platform=="darwin":    os.system(f"afplay {path} &")
    elif sys.platform.startswith("linux"): os.system(f"aplay {path} 2>/dev/null &")
    elif sys.platform=="win32":   os.system(f"start /min wmplayer {path}")

# ══════════════════════════════════════════════════════
#  ESTADO GLOBAL
# ══════════════════════════════════════════════════════
state = {
    "rms":        0.0,
    "threshold":  2000.0,
    "clap_count": 0,
    "triggered":  False,
    "trigger_t":  0.0,
    "greeting":   "APLAUDE PARA ACTIVAR",
    "energy":     0,
    "riff_data":  None,
    "history":    np.zeros(200),
    "calibrating":False,
    "status":     "STANDBY",  # STANDBY | LISTENING | TRIGGERED | PLAYING
}

GREETINGS = [
    "¡HOLA, GENIO!",
    "JARVIS EN LÍNEA ⚡",
    "REACTOR AL 100%",
    "¡STARK APPROVES!",
    "TRAJE LISTO 🦾",
    "INICIANDO SISTEMAS",
    "¡EH, TÚ! HOLA 👋",
]

# ══════════════════════════════════════════════════════
#  MICRÓFONO / SIMULACIÓN
# ══════════════════════════════════════════════════════
CHUNK = 1024
COOLDOWN = 2.5
last_clap_t = 0

def mic_thread(pa):
    global last_clap_t
    try:
        stream = pa.open(format=pyaudio.paInt16,channels=1,
                         rate=SR,input=True,frames_per_buffer=CHUNK)
    except Exception as e:
        state["greeting"] = "ERROR MIC"
        return

    # calibrar 2s
    state["calibrating"] = True
    state["status"]      = "CALIBRANDO"
    samples = []
    for _ in range(int(SR/CHUNK*2)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        arr  = np.frombuffer(data,dtype=np.int16).astype(np.float32)
        samples.append(np.sqrt(np.mean(arr**2)))
    noise = np.mean(samples)
    state["threshold"]   = max(1800, noise*6)
    state["calibrating"] = False
    state["status"]      = "LISTENING"

    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        arr  = np.frombuffer(data,dtype=np.int16).astype(np.float32)
        rms  = float(np.sqrt(np.mean(arr**2)))
        state["rms"] = rms
        # rolling history
        state["history"] = np.roll(state["history"], -1)
        state["history"][-1] = rms

        now = time.time()
        if (rms > state["threshold"] and
                now - last_clap_t > COOLDOWN and
                state["status"] == "LISTENING"):
            last_clap_t = now
            state["clap_count"] += 1
            state["energy"]     = min(100, state["clap_count"]*20)
            state["greeting"]   = random.choice(GREETINGS)
            state["triggered"]  = True
            state["trigger_t"]  = now
            state["status"]     = "PLAYING"

            def play_and_reset():
                if AUDIO_OK and state["riff_data"] is not None:
                    play_riff(pa, state["riff_data"])
                else:
                    save_wav_and_play(state["riff_data"])
                time.sleep(0.3)
                state["status"]  = "LISTENING"
                state["triggered"] = False

            threading.Thread(target=play_and_reset, daemon=True).start()

def sim_thread():
    """Simula audio cuando no hay pyaudio"""
    t0 = time.time()
    while True:
        t = time.time()-t0
        rms = abs(math.sin(t*1.7))*600 + random.uniform(0,200)
        state["rms"] = rms
        state["history"] = np.roll(state["history"],-1)
        state["history"][-1] = rms
        state["status"] = "DEMO MODE"
        time.sleep(0.05)

# ══════════════════════════════════════════════════════
#  DIBUJO MÁSCARA IRON MAN
# ══════════════════════════════════════════════════════
def draw_ironman_mask(ax, cx, cy, size, glow=0.0):
    """Dibuja la máscara de Iron Man centrada en (cx,cy)"""
    s = size

    # Glow exterior cuando se activa
    if glow > 0:
        for r in np.linspace(s*1.6, s*1.1, 8):
            alpha = glow * 0.08 * (1 - (r-s*1.1)/(s*0.5))
            circle = Circle((cx,cy), r, color="#FF6600",
                            alpha=max(0,alpha), zorder=1)
            ax.add_patch(circle)

    # Cabeza — forma trapezoidal con rectángulo redondeado
    head = FancyBboxPatch((cx-s*.55, cy-s*.65), s*1.1, s*1.3,
                          boxstyle="round,pad=0.05",
                          linewidth=2, edgecolor="#CC2200",
                          facecolor="#8B0000", zorder=2)
    ax.add_patch(head)

    # Frente dorada
    forehead = FancyBboxPatch((cx-s*.4, cy+s*.2), s*.8, s*.4,
                              boxstyle="round,pad=0.03",
                              linewidth=1.5, edgecolor="#AA8800",
                              facecolor="#C8A000", zorder=3)
    ax.add_patch(forehead)

    # Mejillas / mandíbula
    for sx in [-1, 1]:
        cheek = FancyBboxPatch((cx+sx*s*.1, cy-s*.35), s*.42, s*.5,
                               boxstyle="round,pad=0.02",
                               linewidth=1, edgecolor="#AA1100",
                               facecolor="#6B0000", zorder=3)
        ax.add_patch(cheek)

    # Ojos — efecto glowing
    eye_color  = "#00FFFF" if glow < 0.1 else "#FFFFFF"
    eye_glow_c = "#00AAFF"
    for ex in [-s*.22, s*.22]:
        # glow del ojo
        for r in [s*.14, s*.10]:
            alpha = 0.15 if glow < 0.1 else 0.35
            ax.add_patch(Circle((cx+ex, cy+s*.08), r,
                                color=eye_glow_c, alpha=alpha, zorder=4))
        # ojo principal — forma ovalada inclinada
        eye = mpatches.Ellipse((cx+ex, cy+s*.08),
                               s*.22, s*.10,
                               angle=-15 if ex<0 else 15,
                               color=eye_color, zorder=5)
        ax.add_patch(eye)
        # brillo
        ax.add_patch(Circle((cx+ex+s*.03, cy+s*.10), s*.03,
                             color="white", alpha=0.6, zorder=6))

    # Nariz / separador central
    nose = FancyBboxPatch((cx-s*.04, cy-s*.05), s*.08, s*.2,
                          boxstyle="round,pad=0.01",
                          facecolor="#AA1100", edgecolor="none", zorder=4)
    ax.add_patch(nose)

    # Boca — líneas
    for my in [cy-s*.22, cy-s*.30]:
        ax.plot([cx-s*.35, cx+s*.35], [my, my],
                color="#CC2200", linewidth=2.5, zorder=5)
    # ventilaciones laterales
    for sx in [-1, 1]:
        for i in range(3):
            vy = cy - s*.18 - i*s*.05
            ax.plot([cx+sx*s*.18, cx+sx*s*.38],
                    [vy, vy],
                    color="#AA1100", linewidth=1.5, zorder=5)

    # Líneas de detalle en frente
    ax.plot([cx-s*.15, cx+s*.15], [cy+s*.48, cy+s*.48],
            color="#AA8800", linewidth=2, zorder=6)
    ax.plot([cx, cx], [cy+s*.35, cy+s*.55],
            color="#AA8800", linewidth=1.5, zorder=6)

# ══════════════════════════════════════════════════════
#  DIBUJO REACTOR ARC
# ══════════════════════════════════════════════════════
def draw_reactor(ax, cx, cy, r, energy=0, pulse=0.0):
    """Reactor arc con energía y pulso"""
    brightness = 0.4 + 0.6*(energy/100) + 0.3*pulse
    brightness = min(1.0, brightness)

    # Anillos exteriores
    for i, (rad, alpha) in enumerate([(r*1.8,.08),(r*1.5,.12),(r*1.2,.18)]):
        ax.add_patch(Circle((cx,cy), rad,
                            color="#00CCFF",
                            alpha=alpha*brightness, zorder=2))

    # Cuerpo del reactor
    ax.add_patch(Circle((cx,cy), r,
                        facecolor="#001133",
                        edgecolor="#0088CC",
                        linewidth=2.5, zorder=3))

    # Segmentos internos (estilo hexágono)
    for i in range(6):
        angle = math.radians(i*60 + pulse*360)
        x1 = cx + r*.45*math.cos(angle)
        y1 = cy + r*.45*math.sin(angle)
        x2 = cx + r*.85*math.cos(angle)
        y2 = cy + r*.85*math.sin(angle)
        ax.plot([x1,x2],[y1,y2],
                color="#00AAFF",
                alpha=0.6*brightness,
                linewidth=2, zorder=4)

    # Núcleo brillante
    core_color = (0.0, brightness*0.8, brightness, 1.0)
    ax.add_patch(Circle((cx,cy), r*.35,
                        color=core_color, zorder=5))
    ax.add_patch(Circle((cx,cy), r*.18,
                        color="white",
                        alpha=0.9*brightness, zorder=6))

    # Rayos de energía cuando hay pulso
    if pulse > 0.3:
        for i in range(8):
            angle = math.radians(i*45 + pulse*180)
            length = r*(0.4 + pulse*0.8)
            ax.annotate("",
                xy=(cx+length*math.cos(angle), cy+length*math.sin(angle)),
                xytext=(cx, cy),
                arrowprops=dict(arrowstyle="-",
                               color="#00FFFF",
                               alpha=pulse*0.6,
                               lw=1.5),
                zorder=4)

# ══════════════════════════════════════════════════════
#  BARRA DE ENERGÍA ESTILO STARK
# ══════════════════════════════════════════════════════
def draw_energy_bar(ax, x, y, w, h, value, max_val=100):
    pct = value / max_val
    # Fondo
    ax.add_patch(FancyBboxPatch((x,y), w, h,
                                boxstyle="round,pad=0.005",
                                facecolor="#001122",
                                edgecolor="#004488",
                                linewidth=1.5, zorder=3))
    if pct > 0:
        # Gradiente simulado con barras
        segments = 20
        seg_w    = (w - 0.01) / segments
        for i in range(int(pct * segments)):
            ratio = i / segments
            r = ratio * 0.3
            g = 0.5 + ratio * 0.5
            b = 1.0
            ax.add_patch(FancyBboxPatch(
                (x + 0.005 + i*seg_w, y+0.005),
                seg_w*0.85, h-0.01,
                boxstyle="round,pad=0.002",
                facecolor=(r, g, b),
                alpha=0.85, zorder=4))

# ══════════════════════════════════════════════════════
#  WAVEFORM VISUALIZER
# ══════════════════════════════════════════════════════
def draw_waveform(ax, history, threshold, triggered=False):
    ax.clear()
    ax.set_facecolor("#000811")
    ax.set_xlim(0, len(history))
    ymax = max(threshold * 1.5, np.max(history) * 1.2, 500)
    ax.set_ylim(0, ymax)
    ax.axis("off")

    x = np.arange(len(history))
    norm = history / ymax

    # Color dinámico: azul → cian → blanco cuando supera threshold
    colors = []
    for v in history:
        ratio = min(v / threshold, 1.5)
        if ratio < 0.5:
            colors.append((0.0, ratio*0.8, 0.8+ratio*0.2))
        elif ratio < 1.0:
            colors.append((0.0, 0.4+ratio*0.6, 1.0))
        else:
            colors.append((min(1,(ratio-1)*2), 1.0, 1.0))

    for i in range(1, len(x)):
        ax.plot([x[i-1], x[i]],
                [history[i-1], history[i]],
                color=colors[i], linewidth=1.5,
                alpha=0.85, solid_capstyle="round")
        # espejo inferior
        ax.plot([x[i-1], x[i]],
                [-history[i-1]*0.3, -history[i]*0.3],
                color=colors[i], linewidth=0.8,
                alpha=0.3)

    # línea de threshold
    ax.axhline(threshold, color="#FF4400", linewidth=1.2,
               linestyle="--", alpha=0.7)
    ax.text(5, threshold*1.05, "THRESHOLD",
            color="#FF4400", fontsize=7, alpha=0.8,
            fontfamily="monospace")

    if triggered:
        ax.set_facecolor("#001100")

# ══════════════════════════════════════════════════════
#  SETUP FIGURA
# ══════════════════════════════════════════════════════
plt.rcParams.update({
    "figure.facecolor":  "#000811",
    "text.color":        "white",
    "font.family":       "monospace",
})

fig = plt.figure(figsize=(14, 8), facecolor="#000811")
fig.canvas.manager.set_window_title("⚡ IRON MAN CLAP DETECTOR")

# Layout: máscara izquierda, waveform arriba derecha, info abajo derecha
ax_mask  = fig.add_axes([0.02, 0.05, 0.42, 0.92])   # máscara
ax_wave  = fig.add_axes([0.47, 0.55, 0.50, 0.38])   # waveform
ax_info  = fig.add_axes([0.47, 0.05, 0.50, 0.45])   # info panel

for ax in [ax_mask, ax_info]:
    ax.set_facecolor("#000811")
    ax.axis("off")

# ══════════════════════════════════════════════════════
#  FRAME DE ANIMACIÓN
# ══════════════════════════════════════════════════════
frame_counter = [0]

def animate(frame):
    fc = frame_counter[0]
    frame_counter[0] += 1
    t  = fc / 30.0  # tiempo en segundos (30fps aprox)

    triggered = state["triggered"]
    status    = state["status"]
    energy    = state["energy"]
    rms       = state["rms"]
    thresh    = state["threshold"]
    claps     = state["clap_count"]
    greeting  = state["greeting"]

    # Pulso del reactor
    base_pulse  = 0.5 + 0.5*math.sin(t*2.5)
    glow_factor = 0.0

    if triggered or status == "PLAYING":
        elapsed    = time.time() - state["trigger_t"]
        glow_factor = max(0, 1.0 - elapsed/1.5)
        pulse      = base_pulse + glow_factor

    else:
        pulse = base_pulse * (0.3 + 0.7*(energy/100 + 0.1))

    pulse = min(1.0, pulse)

    # ── MÁSCARA ───────────────────────────────────────
    ax_mask.clear()
    ax_mask.set_facecolor("#000811")
    ax_mask.set_xlim(-1, 1); ax_mask.set_ylim(-1.1, 1.2)
    ax_mask.set_aspect("equal"); ax_mask.axis("off")

    # Fondo hexagonal tenue
    for i in range(0, 360, 30):
        r = 0.9 + 0.05*math.sin(math.radians(i+t*20))
        ax_mask.plot([0, r*math.cos(math.radians(i))],
                     [0, r*math.sin(math.radians(i))],
                     color="#001133", linewidth=0.5, alpha=0.4)

    draw_ironman_mask(ax_mask, 0, 0.1, 0.75, glow_factor)
    draw_reactor(ax_mask, 0, -0.72, 0.18,
                 energy=energy, pulse=pulse)

    # Texto de estado debajo
    status_colors = {
        "STANDBY":   "#004488",
        "CALIBRANDO":"#AAAA00",
        "LISTENING": "#00AA44",
        "PLAYING":   "#FF4400",
        "DEMO MODE": "#AA00AA",
    }
    sc = status_colors.get(status, "#FFFFFF")
    ax_mask.text(0, -0.95, f"[ {status} ]",
                 ha="center", va="center",
                 fontsize=11, color=sc, fontweight="bold",
                 fontfamily="monospace",
                 path_effects=[pe.withStroke(linewidth=3,
                                             foreground="black")])

    # ── WAVEFORM ──────────────────────────────────────
    draw_waveform(ax_wave, state["history"], thresh,
                  triggered=(status=="PLAYING"))

    ax_wave.set_title("  AUDIO INPUT  ──  CLAP DETECTOR",
                      color="#004488", fontsize=9,
                      fontfamily="monospace", loc="left", pad=4)

    # ── INFO PANEL ────────────────────────────────────
    ax_info.clear()
    ax_info.set_facecolor("#000811")
    ax_info.set_xlim(0,1); ax_info.set_ylim(0,1)
    ax_info.axis("off")

    # Título del panel
    ax_info.text(0.05, 0.95,
                 "STARK INDUSTRIES  //  JARVIS v3.0",
                 fontsize=9, color="#003366",
                 fontfamily="monospace", va="top")
    ax_info.axhline(0.90, color="#002244", linewidth=1)

    # Saludo principal
    saludo_color = "#FF6600" if (triggered or status=="PLAYING") else "#00CCFF"
    saludo_size  = 18 if len(greeting) < 16 else 14
    ax_info.text(0.5, 0.76, greeting,
                 ha="center", va="center",
                 fontsize=saludo_size, color=saludo_color,
                 fontweight="bold", fontfamily="monospace",
                 path_effects=[pe.withStroke(linewidth=4,
                                             foreground="#000011")])

    # Barra de energía del reactor
    ax_info.text(0.05, 0.62, "ARC REACTOR ENERGY",
                 fontsize=8, color="#004488", fontfamily="monospace")
    draw_energy_bar(ax_info, 0.05, 0.53, 0.90, 0.06, energy)
    ax_info.text(0.97, 0.56, f"{energy}%",
                 ha="right", fontsize=9, color="#00CCFF",
                 fontfamily="monospace")

    # Stats en dos columnas
    ax_info.axhline(0.50, color="#002244", linewidth=0.8)

    stats_left = [
        ("APLAUSOS",  f"{claps:>5}",      "#FF6600"),
        ("RMS",       f"{int(rms):>5}",   "#00CCFF"),
        ("THRESHOLD", f"{int(thresh):>5}","#FF4400"),
    ]
    stats_right = [
        ("MODO",    "MIC" if AUDIO_OK else "DEMO",   "#00FF88"),
        ("SAMPLE",  f"{SR//1000}kHz",                "#AAAAFF"),
        ("STATUS",  status[:8],                      status_colors.get(status,"#FFF")),
    ]

    for i, (label, val, color) in enumerate(stats_left):
        y = 0.43 - i*0.11
        ax_info.text(0.05, y, label, fontsize=8,
                     color="#446688", fontfamily="monospace")
        ax_info.text(0.35, y, val, fontsize=9,
                     color=color, fontfamily="monospace",
                     fontweight="bold")

    for i, (label, val, color) in enumerate(stats_right):
        y = 0.43 - i*0.11
        ax_info.text(0.55, y, label, fontsize=8,
                     color="#446688", fontfamily="monospace")
        ax_info.text(0.82, y, val, fontsize=9,
                     color=color, fontfamily="monospace",
                     fontweight="bold")

    # Instrucción
    ax_info.axhline(0.13, color="#002244", linewidth=0.8)
    if AUDIO_OK and status=="LISTENING":
        hint = "👏  APLAUDE PARA ACTIVAR  👏"
        hc   = "#00FF44"
    elif status == "PLAYING":
        hint = "♪ ♫  IRON MAN — BLACK SABBATH  ♫ ♪"
        hc   = "#FF6600"
    elif status == "CALIBRANDO":
        dots = "." * (int(t*3) % 4)
        hint = f"CALIBRANDO MICRÓFONO{dots}"
        hc   = "#FFFF00"
    else:
        hint = "[ MODO DEMO ]  PRESIONA ESPACIO"
        hc   = "#AA44FF"

    ax_info.text(0.5, 0.07, hint,
                 ha="center", fontsize=10, color=hc,
                 fontfamily="monospace", fontweight="bold",
                 path_effects=[pe.withStroke(linewidth=3,
                                             foreground="black")])

    # Nota musical animada cuando toca
    if status == "PLAYING":
        notes_pos = ["E", "E", "G", "E", "A", "G", "E"]
        elapsed   = time.time() - state["trigger_t"]
        note_idx  = int(elapsed / 0.25) % len(notes_pos)
        note_str  = "  ".join(
            f"[{n}]" if i==note_idx else f" {n} "
            for i, n in enumerate(notes_pos)
        )
        ax_info.text(0.5, 0.20, note_str,
                     ha="center", fontsize=9,
                     color="#FF8800", fontfamily="monospace")

    return []

# ══════════════════════════════════════════════════════
#  TECLA ESPACIO → simular aplauso en modo demo
# ══════════════════════════════════════════════════════
def on_key(event):
    global last_clap_t
    if event.key == " " and not AUDIO_OK:
        now = time.time()
        if now - last_clap_t > COOLDOWN:
            last_clap_t = now
            state["clap_count"] += 1
            state["energy"]     = min(100, state["clap_count"]*20)
            state["greeting"]   = random.choice(GREETINGS)
            state["triggered"]  = True
            state["trigger_t"]  = now
            state["status"]     = "PLAYING"
            # simular RMS alto
            state["history"][-1] = state["threshold"] * 2

            def reset():
                if state["riff_data"] is not None:
                    save_wav_and_play(state["riff_data"])
                time.sleep(0.3)
                state["status"]   = "DEMO MODE"
                state["triggered"] = False

            threading.Thread(target=reset, daemon=True).start()

fig.canvas.mpl_connect("key_press_event", on_key)

# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    print("⚡ Sintetizando riff de Iron Man...")
    state["riff_data"] = build_riff()
    print(f"✔ Riff listo ({len(state['riff_data'])/SR:.1f}s)")

    if AUDIO_OK:
        pa = pyaudio.PyAudio()
        threading.Thread(target=mic_thread, args=(pa,), daemon=True).start()
        print("✔ Micrófono iniciado")
    else:
        print("⚠ PyAudio no encontrado — MODO DEMO")
        print("  Instala con: pip install pyaudio")
        print("  En la ventana presiona ESPACIO para simular aplauso")
        threading.Thread(target=sim_thread, daemon=True).start()
        state["status"] = "DEMO MODE"

    ani = animation.FuncAnimation(
        fig, animate, interval=33,   # ~30 fps
        blit=False, cache_frame_data=False
    )

    plt.tight_layout(pad=0)
    plt.show()

    if AUDIO_OK:
        pa.terminate()