import os, sys, time, random, math, shutil

# ══════════════════════════════════════════════════════════════
#  TERMINAL UTILS
# ══════════════════════════════════════════════════════════════
W = shutil.get_terminal_size((120, 40)).columns

class C:
    RST  = "\033[0m";  BOLD = "\033[1m";  DIM  = "\033[2m";  BLINK = "\033[5m"
    RED  = "\033[91m"; GRN  = "\033[92m"; YLW  = "\033[93m"; BLU  = "\033[94m"
    MAG  = "\033[95m"; CYN  = "\033[96m"; WHT  = "\033[97m"; BLK  = "\033[90m"
    BRED = "\033[41m"; BBLU = "\033[44m"; BMAG = "\033[45m"; BGRN = "\033[42m"
    BYLW = "\033[43m"

def clr():  os.system("cls" if os.name == "nt" else "clear")
def center(txt, w=None): return txt.center(w or W)
def p(txt=""): print(txt)
def sleep(n): time.sleep(n)

def typewrite(text, delay=0.018, color=""):
    for ch in text:
        sys.stdout.write(color + ch + C.RST)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def bar(val, maxv, width=20, color=C.GRN, bg=C.BLK):
    filled = int((val / maxv) * width)
    return color + "█" * filled + bg + "░" * (width - filled) + C.RST

def hline(ch="═", color=C.BLK): print(color + ch * W + C.RST)
def thinline(ch="─", color=C.BLK): print(color + ch * W + C.RST)

def gradient_title(text, chars="▓▒░"):
    colors = [C.RED, C.YLW, C.WHT, C.CYN, C.BLU, C.MAG]
    out = ""
    for i, ch in enumerate(text):
        out += colors[i % len(colors)] + C.BOLD + ch
    return out + C.RST

def animate_loading(text, duration=1.2):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {C.CYN}{frames[i % len(frames)]}{C.RST}  {text}  ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")

def flash_text(text, times=3, color=C.YLW):
    for _ in range(times):
        print(f"\r{color}{C.BOLD}{text}{C.RST}", end="", flush=True)
        time.sleep(0.15)
        print(f"\r{' '*len(text)}", end="", flush=True)
        time.sleep(0.1)
    print(f"{color}{C.BOLD}{text}{C.RST}")

# ══════════════════════════════════════════════════════════════
#  ASCII ART CARS  (ancho ~55 chars)
# ══════════════════════════════════════════════════════════════

ASCII_CARS = {

"rx7": r"""
      ______
   __/  ⚡  \___________
  /  .  .  .  .  .  .  \__
 | ●    MAZDA  RX-7    ● |>
  \__________________________/
     (●●)            (●●)
""",

"supra": r"""
       _________
    __/   ⚡    \________
   /  .  .  .  .  .  .  \_
  | ●   TOYOTA  SUPRA  ● |>
   \_________________________/
      (●●)           (●●)
""",

"gtr": r"""
      __________
   __/    ⚡    \_________
  /  .  .  .  .  .  .  . \_
 | ●  NISSAN  GT-R  R34  ● |>
  \___________________________/
     (●●)             (●●)
""",

"evo": r"""
     ___________
  __/    ⚡     \_________
 /  .  .  .  .  .  .  .  \_
| ●  MITSUBISHI  EVO  IX  ● |>
 \____________________________/
    (●●)              (●●)
""",

"nsx": r"""
       _______
    __/  ⚡  \_________
   / .  .  .  .  .  . \_
  | ●   HONDA  NSX   ● |>
   \______________________/
     (●●)         (●●)
""",

"mustang": r"""
       _____________
    __/      ⚡     \______
   /   .  .  .  .  .  .   \_
  | ●   FORD   MUSTANG  ●  |>
   \____________________________/
      (●●)             (●●)
""",

"camaro": r"""
      ______________
   __/      ⚡      \_____
  /   .  .  .  .  .  .   \_
 | ●  CHEVY  CAMARO  ZL1  ● |>
  \____________________________/
     (●●)              (●●)
""",

"challenger": r"""
        _______________
     __/       ⚡      \_____
    /   .  .  .  .  .  .    \_
   | ●  DODGE  CHALLENGER  ● |>
    \______________________________/
       (●●)               (●●)
""",

"corvette": r"""
       __________
    __/    ⚡    \_______
   /  .  .  .  .  .  .  \_
  | ●  CHEVY  C8  VETTE  ● |>
   \__________________________/
     (●●)            (●●)
""",

"hellcat": r"""
        _______________
     __/      ⚡       \____
    /   .  .  .  .  .  .   \_
   | ● DODGE CHARGER  HELL ● |>
    \______________________________/
      (●●)               (●●)
""",
}

# ══════════════════════════════════════════════════════════════
#  CAR DATABASE
# ══════════════════════════════════════════════════════════════
CARS = {
    # ── JDM ──────────────────────────────────────────────────
    "rx7": {
        "name":    "Mazda RX-7 FD",
        "type":    "JDM",
        "year":    1992,
        "hp":      276,
        "torque":  231,   # Nm
        "weight":  1270,  # kg
        "zto60":   5.3,   # 0-60 mph seconds
        "topspeed":250,   # km/h
        "engine":  "1.3L Twin-Turbo Rotary (13B-REW)",
        "drive":   "FR",
        "price":   35000,
        "cool":    98,    # factor de coolness lore
        "color":   C.RED,
        "ascii":   "rx7",
    },
    "supra": {
        "name":    "Toyota Supra MK4",
        "type":    "JDM",
        "year":    1993,
        "hp":      320,
        "torque":  441,
        "weight":  1570,
        "zto60":   4.6,
        "topspeed":285,
        "engine":  "3.0L Twin-Turbo I6 (2JZ-GTE)",
        "drive":   "FR",
        "price":   90000,
        "cool":    100,
        "color":   C.YLW,
        "ascii":   "supra",
    },
    "gtr": {
        "name":    "Nissan Skyline GT-R R34",
        "type":    "JDM",
        "year":    1999,
        "hp":      280,
        "torque":  392,
        "weight":  1560,
        "zto60":   4.7,
        "topspeed":250,
        "engine":  "2.6L Twin-Turbo I6 (RB26DETT)",
        "drive":   "AWD",
        "price":   120000,
        "cool":    99,
        "color":   C.BLU,
        "ascii":   "gtr",
    },
    "evo": {
        "name":    "Mitsubishi Lancer Evo IX",
        "type":    "JDM",
        "year":    2005,
        "hp":      286,
        "torque":  366,
        "weight":  1410,
        "zto60":   4.4,
        "topspeed":240,
        "engine":  "2.0L Turbo I4 (4G63T)",
        "drive":   "AWD",
        "price":   25000,
        "cool":    95,
        "color":   C.CYN,
        "ascii":   "evo",
    },
    "nsx": {
        "name":    "Honda NSX NA1",
        "type":    "JDM",
        "year":    1990,
        "hp":      270,
        "torque":  284,
        "weight":  1370,
        "zto60":   5.5,
        "topspeed":270,
        "engine":  "3.0L VTEC V6 (C30A)",
        "drive":   "RR",
        "price":   65000,
        "cool":    97,
        "color":   C.WHT,
        "ascii":   "nsx",
    },
    # ── MUSCLE ───────────────────────────────────────────────
    "mustang": {
        "name":    "Ford Mustang Shelby GT500",
        "type":    "MUSCLE",
        "year":    2020,
        "hp":      760,
        "torque":  847,
        "weight":  1920,
        "zto60":   3.3,
        "topspeed":290,
        "engine":  "5.2L Supercharged V8 (Predator)",
        "drive":   "FR",
        "price":   75000,
        "cool":    96,
        "color":   C.RED,
        "ascii":   "mustang",
    },
    "camaro": {
        "name":    "Chevrolet Camaro ZL1",
        "type":    "MUSCLE",
        "year":    2021,
        "hp":      650,
        "torque":  881,
        "weight":  1886,
        "zto60":   3.5,
        "topspeed":320,
        "engine":  "6.2L Supercharged V8 (LT4)",
        "drive":   "FR",
        "price":   68000,
        "cool":    94,
        "color":   C.YLW,
        "ascii":   "camaro",
    },
    "challenger": {
        "name":    "Dodge Challenger SRT Hellcat",
        "type":    "MUSCLE",
        "year":    2022,
        "hp":      717,
        "torque":  881,
        "weight":  2074,
        "zto60":   3.7,
        "topspeed":328,
        "engine":  "6.2L Supercharged HEMI V8",
        "drive":   "FR",
        "price":   62000,
        "cool":    95,
        "color":   C.MAG,
        "ascii":   "challenger",
    },
    "corvette": {
        "name":    "Chevrolet Corvette C8 Z06",
        "type":    "MUSCLE",
        "year":    2023,
        "hp":      670,
        "torque":  623,
        "weight":  1563,
        "zto60":   2.6,
        "topspeed":311,
        "engine":  "5.5L Flat-Plane V8 (LT6)",
        "drive":   "MR",
        "price":   110000,
        "cool":    97,
        "color":   C.YLW,
        "ascii":   "corvette",
    },
    "hellcat": {
        "name":    "Dodge Charger SRT Hellcat",
        "type":    "MUSCLE",
        "year":    2022,
        "hp":      717,
        "torque":  881,
        "weight":  1986,
        "zto60":   3.6,
        "topspeed":328,
        "engine":  "6.2L Supercharged HEMI V8",
        "drive":   "FR",
        "price":   72000,
        "cool":    93,
        "color":   C.RED,
        "ascii":   "hellcat",
    },
}

JDM    = {k:v for k,v in CARS.items() if v["type"]=="JDM"}
MUSCLE = {k:v for k,v in CARS.items() if v["type"]=="MUSCLE"}

# ══════════════════════════════════════════════════════════════
#  PANTALLA INTRO
# ══════════════════════════════════════════════════════════════
def intro():
    clr()
    title_lines = [
        "     ██████╗ ██████╗     ██╗   ██╗███████╗    ",
        "    ██╔════╝██╔════╝     ██║   ██║██╔════╝    ",
        "    ██║     ███████╗     ██║   ██║███████╗    ",
        "    ██║     ██╔═══██╗    ╚██╗ ██╔╝╚════██║    ",
        "    ╚██████╗╚██████╔╝     ╚████╔╝ ███████║    ",
        "     ╚═════╝ ╚═════╝       ╚═══╝  ╚══════╝    ",
    ]
    colors = [C.RED, C.YLW, C.WHT, C.CYN, C.BLU, C.MAG]
    p()
    for i, line in enumerate(title_lines):
        print(colors[i] + C.BOLD + line.center(W) + C.RST)
        sleep(0.07)

    p()
    sub = "  JDM  vs  MUSCLE  —  TERMINAL EDITION  "
    border = "═" * len(sub)
    print(C.BLK + C.BOLD + border.center(W) + C.RST)
    print(C.WHT + C.BOLD + sub.center(W) + C.RST)
    print(C.BLK + C.BOLD + border.center(W) + C.RST)
    p()

    taglines = [
        f"{C.RED}🔥 TURBO vs DISPLACEMENT{C.RST}",
        f"{C.CYN}⚡ PRECISION vs BRUTE FORCE{C.RST}",
        f"{C.YLW}🏁 WHICH LEGEND WINS?{C.RST}",
    ]
    for t in taglines:
        print(t.center(W + 30))
        sleep(0.3)
    p()
    sleep(0.5)
    input(C.BLK + "  [ PRESS ENTER TO START ]".center(W) + C.RST)

# ══════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════
def main_menu():
    while True:
        clr()
        hline("═", C.BLK)
        print(C.RED + C.BOLD + "  ⚡  GARAGE MENU".center(W) + C.RST)
        hline("═", C.BLK)
        p()
        opts = [
            ("1", "🏎️  Explorar todos los autos",         C.CYN),
            ("2", "⚔️  Batalla 1v1  (elige tus carros)",  C.YLW),
            ("3", "🏆  Top 3 por categoría",               C.GRN),
            ("4", "🎲  Batalla aleatoria épica",           C.MAG),
            ("5", "🚪  Salir",                             C.RED),
        ]
        for key, label, color in opts:
            print(f"  {color}{C.BOLD}[{key}]{C.RST}  {label}")
            sleep(0.05)
        p()
        hline("─", C.BLK)
        choice = input(f"\n  {C.WHT}Elige opción: {C.RST}").strip()
        if choice == "1": explore_all()
        elif choice == "2": battle_menu()
        elif choice == "3": top3_screen()
        elif choice == "4": random_battle()
        elif choice == "5":
            clr()
            typewrite("  See you on the streets... 🔥", 0.04, C.YLW)
            sleep(0.8)
            break

# ══════════════════════════════════════════════════════════════
#  FICHA DE AUTO
# ══════════════════════════════════════════════════════════════
def render_car_card(car, wide=False):
    c     = car["color"]
    badge = f"{C.RED}JDM{C.RST}" if car["type"]=="JDM" else f"{C.BLU}MUSCLE{C.RST}"
    ascii_art = ASCII_CARS.get(car["ascii"], "")

    lines = []
    lines.append(c + C.BOLD + f"  {'═'*50}" + C.RST)
    lines.append(c + C.BOLD + f"  {car['name']}  " + C.RST + f"[{badge}]  {C.BLK}{car['year']}{C.RST}")
    lines.append(c + C.BOLD + f"  {'═'*50}" + C.RST)

    # ASCII art coloreado
    for line in ascii_art.strip("\n").split("\n"):
        lines.append(c + C.BOLD + line + C.RST)
    lines.append("")

    # specs
    specs = [
        ("⚡ HP",        f"{car['hp']} hp",             car['hp'],  800, C.RED),
        ("💪 Torque",    f"{car['torque']} Nm",          car['torque'], 900, C.YLW),
        ("⚖️  Peso",     f"{car['weight']} kg",          2200-car['weight'], 1500, C.GRN),
        ("🚀 0-60 mph",  f"{car['zto60']} s",            10-car['zto60'], 8,    C.CYN),
        ("🏁 Top Speed", f"{car['topspeed']} km/h",      car['topspeed'], 350, C.MAG),
        ("😎 Coolness",  f"{car['cool']}/100",           car['cool'], 100, C.BLU),
    ]
    for label, val_str, val, maxv, bc in specs:
        b = bar(val, maxv, 22, bc)
        lines.append(f"  {C.WHT}{label:<16}{C.RST} {val_str:<12}  {b}")

    lines.append(f"\n  {C.BLK}Engine  :{C.RST} {car['engine']}")
    lines.append(f"  {C.BLK}Drive   :{C.RST} {car['drive']}")
    lines.append(f"  {C.BLK}Price   :{C.RST} ${car['price']:,}")
    lines.append(c + "  " + "─"*50 + C.RST)
    return lines

# ══════════════════════════════════════════════════════════════
#  EXPLORAR TODOS
# ══════════════════════════════════════════════════════════════
def explore_all():
    keys = list(CARS.keys())
    idx  = 0
    while True:
        clr()
        hline("═", C.BLK)
        car = CARS[keys[idx]]
        for line in render_car_card(car): print(line)
        p()
        nav = f"  {C.BLK}← A  {idx+1}/{len(keys)}  D →   [Q] volver{C.RST}"
        print(nav)
        ch = input("  ").strip().lower()
        if ch == "d": idx = (idx + 1) % len(keys)
        elif ch == "a": idx = (idx - 1) % len(keys)
        elif ch == "q": break

# ══════════════════════════════════════════════════════════════
#  SELECCIONAR AUTO
# ══════════════════════════════════════════════════════════════
def select_car(prompt, pool):
    keys = list(pool.keys())
    while True:
        clr()
        hline("═", C.BLK)
        print(C.YLW + C.BOLD + f"  {prompt}".center(W) + C.RST)
        hline("─", C.BLK)
        p()
        for i, k in enumerate(keys, 1):
            car = pool[k]
            badge = f"{C.RED}JDM   {C.RST}" if car["type"]=="JDM" else f"{C.BLU}MUSCLE{C.RST}"
            hp_b = bar(car["hp"], 800, 12, car["color"])
            print(f"  {car['color']}{C.BOLD}[{i:>2}]{C.RST}  [{badge}]  "
                  f"{car['name']:<35}  HP:{hp_b} {car['hp']}")
        p()
        hline("─", C.BLK)
        try:
            ch = int(input(f"\n  Elige (1-{len(keys)}): ").strip())
            if 1 <= ch <= len(keys):
                return CARS[keys[ch-1]]
        except ValueError:
            pass

# ══════════════════════════════════════════════════════════════
#  PANTALLA BATALLA  ⚔️
# ══════════════════════════════════════════════════════════════
STAT_KEYS = [
    ("⚡ HP",        "hp",       800,  True,  C.RED),
    ("💪 Torque",    "torque",   900,  True,  C.YLW),
    ("⚖️  Peso",     "weight",   2200, False, C.GRN),   # menos = mejor
    ("🚀 0-60 mph",  "zto60",    10,   False, C.CYN),   # menos = mejor
    ("🏁 Top Speed", "topspeed", 350,  True,  C.MAG),
    ("😎 Coolness",  "cool",     100,  True,  C.BLU),
]

def battle_screen(car_a, car_b):
    clr()
    hline("█", C.RED)
    vs_line = (
        car_a["color"] + C.BOLD + f"  {car_a['name']}" +
        C.RST + C.BOLD + "   ⚔️   VS   ⚔️   ".center(20) +
        car_b["color"] + C.BOLD + f"{car_b['name']}  " + C.RST
    )
    print(vs_line.center(W + 60))
    hline("█", C.RED)
    p()

    # ASCII arts lado a lado
    art_a = ASCII_CARS.get(car_a["ascii"], "").strip("\n").split("\n")
    art_b = ASCII_CARS.get(car_b["ascii"], "").strip("\n").split("\n")
    max_h = max(len(art_a), len(art_b))
    art_a += [""] * (max_h - len(art_a))
    art_b += [""] * (max_h - len(art_b))
    col_w = 50
    for la, lb in zip(art_a, art_b):
        left  = (car_a["color"] + C.BOLD + la + C.RST).ljust(col_w + 20)
        right = car_b["color"] + C.BOLD + lb + C.RST
        print(f"  {left}    {right}")
    p()

    # animación de carga
    animate_loading("Analizando specs...", 1.0)

    # tabla de batalla
    scores = {"a": 0, "b": 0}
    hline("─", C.BLK)
    header_row = (
        f"  {C.WHT}{C.BOLD}{'STAT':<16}{C.RST}"
        f"  {car_a['color']}{C.BOLD}{car_a['name'][:22]:<24}{C.RST}"
        f"  {'':^5}"
        f"  {car_b['color']}{C.BOLD}{car_b['name'][:22]}{C.RST}"
    )
    print(header_row)
    hline("─", C.BLK)

    round_results = []
    for label, key, maxv, higher_better, bc in STAT_KEYS:
        va = car_a[key]; vb = car_b[key]
        if higher_better:
            win_a = va > vb
        else:
            win_a = va < vb
        win_b = not win_a

        ba = bar(va, maxv, 14, car_a["color"] if win_a else C.BLK)
        bb = bar(vb, maxv, 14, car_b["color"] if win_b else C.BLK)

        icon_a = f"{C.GRN}✔{C.RST}" if win_a else f"{C.RED}✘{C.RST}"
        icon_b = f"{C.GRN}✔{C.RST}" if win_b else f"{C.RED}✘{C.RST}"

        unit = "s" if key == "zto60" else ("km/h" if key=="topspeed" else ("kg" if key=="weight" else ("Nm" if key=="torque" else ("hp" if key=="hp" else "/100"))))
        val_a = f"{va}{unit}"
        val_b = f"{vb}{unit}"

        row = (
            f"  {C.WHT}{label:<16}{C.RST}"
            f"  {icon_a} {ba} {car_a['color']}{val_a:<10}{C.RST}"
            f"  {C.BLK}│{C.RST}"
            f"  {icon_b} {bb} {car_b['color']}{val_b}{C.RST}"
        )
        print(row)
        sleep(0.12)

        if win_a: scores["a"] += 1
        else:     scores["b"] += 1

    hline("─", C.BLK)

    # RESULTADO FINAL
    p()
    animate_loading("Calculando ganador...", 0.8)

    if scores["a"] > scores["b"]:
        winner, loser = car_a, car_b
        w_score, l_score = scores["a"], scores["b"]
    elif scores["b"] > scores["a"]:
        winner, loser = car_b, car_a
        w_score, l_score = scores["b"], scores["a"]
    else:
        winner = None

    if winner:
        hline("█", winner["color"])
        flash_text(f"  🏆  GANADOR: {winner['name']}  ({w_score}-{l_score})  🏆", 4, winner["color"])
        hline("█", winner["color"])
        p()
        trophy_lines = [
            "         .  . * .",
            "       *  🏆  *  .",
            f"    {winner['color']}{C.BOLD}  ══ {winner['name']} ══{C.RST}",
            f"    {winner['color']}  {winner['engine']}{C.RST}",
            f"    {C.GRN}  Ganó {w_score}/6 categorías{C.RST}",
        ]
        for l in trophy_lines:
            print(l.center(W + 20))
            sleep(0.12)
    else:
        print(C.YLW + C.BOLD + "  🤝  EMPATE ÉPICO  3-3  🤝".center(W) + C.RST)

    p()
    # Power-to-weight bonus stat
    pw_a = round(car_a["hp"] / (car_a["weight"] / 1000), 1)
    pw_b = round(car_b["hp"] / (car_b["weight"] / 1000), 1)
    print(f"  {C.BLK}BONUS STAT — Relación Peso/Potencia:{C.RST}")
    print(f"  {car_a['color']}{car_a['name']:<30}{C.RST}  {pw_a} hp/ton  {bar(pw_a,600,18,car_a['color'])}")
    print(f"  {car_b['color']}{car_b['name']:<30}{C.RST}  {pw_b} hp/ton  {bar(pw_b,600,18,car_b['color'])}")
    p()
    input(C.BLK + "  [ ENTER para volver ]" + C.RST)

# ══════════════════════════════════════════════════════════════
#  BATTLE MENU
# ══════════════════════════════════════════════════════════════
def battle_menu():
    clr()
    hline("═", C.YLW)
    print(C.YLW + C.BOLD + "  SELECCIONA TUS COMBATIENTES".center(W) + C.RST)
    hline("═", C.YLW)
    p()
    modes = [
        ("1", "JDM  vs  JDM",     C.RED,  JDM,    JDM),
        ("2", "MUSCLE  vs  MUSCLE",C.BLU,  MUSCLE, MUSCLE),
        ("3", "JDM  vs  MUSCLE",   C.MAG,  JDM,    MUSCLE),
        ("4", "Libre (todos)",     C.GRN,  CARS,   CARS),
    ]
    for k, label, color, *_ in modes:
        print(f"  {color}{C.BOLD}[{k}]{C.RST}  {label}")
    p()
    ch = input("  Modo: ").strip()
    pools = {m[0]: (m[3], m[4]) for m in modes}
    if ch not in pools: return
    pool_a, pool_b = pools[ch]
    car_a = select_car("ELIGE PRIMER AUTO", pool_a)
    car_b = select_car("ELIGE SEGUNDO AUTO", pool_b)
    battle_screen(car_a, car_b)

# ══════════════════════════════════════════════════════════════
#  TOP 3 POR CATEGORÍA
# ══════════════════════════════════════════════════════════════
def top3_screen():
    categories = [
        ("⚡ Más HP",         "hp",       True,  "hp"),
        ("💪 Más Torque",     "torque",   True,  "Nm"),
        ("🚀 Más Rápido 0-60","zto60",    False, "s"),
        ("🏁 Mayor Top Speed","topspeed", True,  "km/h"),
        ("⚖️  Más Liviano",   "weight",   False, "kg"),
        ("😎 Más Cool",       "cool",     True,  "/100"),
    ]
    clr()
    hline("█", C.GRN)
    print(C.GRN + C.BOLD + "  🏆  TOP 3 POR CATEGORÍA  🏆".center(W) + C.RST)
    hline("█", C.GRN)
    p()
    medals = [f"{C.YLW}🥇{C.RST}", f"{C.BLK}{C.BOLD}🥈{C.RST}", f"{C.RED}🥉{C.RST}"]
    for cat_name, key, rev, unit in categories:
        sorted_cars = sorted(CARS.values(), key=lambda x: x[key], reverse=rev)[:3]
        thinline("─", C.BLK)
        print(f"  {C.WHT}{C.BOLD}{cat_name}{C.RST}")
        for i, car in enumerate(sorted_cars):
            val = car[key]
            b = bar(val if rev else (2200-val), 2200 if key=="weight" else val, 16, car["color"])
            badge = f"{C.RED}JDM{C.RST}" if car["type"]=="JDM" else f"{C.BLU}MUS{C.RST}"
            print(f"  {medals[i]}  [{badge}]  {car['color']}{car['name']:<33}{C.RST}  "
                  f"{C.WHT}{val}{unit}{C.RST}  {b}")
            sleep(0.04)
    thinline("─", C.BLK)
    p()
    input(C.BLK + "  [ ENTER para volver ]" + C.RST)

# ══════════════════════════════════════════════════════════════
#  BATALLA ALEATORIA
# ══════════════════════════════════════════════════════════════
def random_battle():
    keys = list(CARS.keys())
    a, b = random.sample(keys, 2)
    clr()
    animate_loading("Seleccionando combatientes aleatorios...", 1.2)
    battle_screen(CARS[a], CARS[b])

# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        intro()
        main_menu()
    except KeyboardInterrupt:
        clr()
        print(C.YLW + "\n  Hasta la próxima. 🏁\n" + C.RST)
        
        