import random
import time
import math
import os

# ─────────────────────────────────────────────
#  COLORES EN TERMINAL
# ─────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    MAGENTA= "\033[95m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"

def clr(): os.system("cls" if os.name == "nt" else "clear")

def header():
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════╗
║        ⚡  FÍSICA: QUIZ DE ENERGÍA  ⚡              ║
║          Serway Tomo 1 — Modo Examen                 ║
╚══════════════════════════════════════════════════════╝{C.RESET}
""")

def linea():
    print(f"{C.DIM}{'─'*56}{C.RESET}")

# ─────────────────────────────────────────────
#  GENERADORES DE PREGUNTAS (valores aleatorios)
# ─────────────────────────────────────────────
g = 9.8

def q_cinematica():
    m = round(random.uniform(0.5, 10.0), 1)
    v = round(random.uniform(2.0, 20.0), 1)
    K = round(0.5 * m * v**2, 2)
    opciones = sorted(set([
        round(K, 1),
        round(K * 1.5, 1),
        round(K * 0.6, 1),
        round(K * 2.0, 1)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  K = ½mv²\n"
        f"  K = ½ × {m} kg × ({v} m/s)²\n"
        f"  K = {C.GREEN}{K} J{C.RESET}"
    )
    return {
        "pregunta": f"Un objeto de {C.YELLOW}{m} kg{C.RESET} se mueve a {C.YELLOW}{v} m/s{C.RESET}.\n  ¿Cuál es su energía cinética?",
        "opciones": opciones,
        "respuesta": round(K, 1),
        "unidad": "J",
        "solucion": solucion,
        "tema": "Energía Cinética"
    }

def q_potencial_grav():
    m  = round(random.uniform(1.0, 15.0), 1)
    h  = round(random.uniform(2.0, 50.0), 1)
    U  = round(m * g * h, 2)
    opciones = sorted(set([
        round(U, 0),
        round(U * 1.3, 0),
        round(U * 0.7, 0),
        round(U * 1.8, 0)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  U = mgh\n"
        f"  U = {m} × 9.8 × {h}\n"
        f"  U = {C.GREEN}{round(U,1)} J{C.RESET}"
    )
    return {
        "pregunta": f"Un objeto de {C.YELLOW}{m} kg{C.RESET} está a {C.YELLOW}{h} m{C.RESET} de altura.\n  ¿Cuál es su energía potencial gravitacional?",
        "opciones": opciones,
        "respuesta": round(U, 0),
        "unidad": "J",
        "solucion": solucion,
        "tema": "Energía Potencial Gravitacional"
    }

def q_resorte():
    k = random.choice([100, 200, 500, 800, 1200, 2000])
    x = round(random.uniform(0.05, 0.30), 2)
    U = round(0.5 * k * x**2, 4)
    opciones = sorted(set([
        round(U, 3),
        round(U * 1.4, 3),
        round(U * 0.5, 3),
        round(U * 2.1, 3)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  U_e = ½kx²\n"
        f"  U_e = ½ × {k} N/m × ({x} m)²\n"
        f"  U_e = {C.GREEN}{round(U,3)} J{C.RESET}"
    )
    return {
        "pregunta": f"Un resorte con k = {C.YELLOW}{k} N/m{C.RESET} se comprime {C.YELLOW}{x} m{C.RESET}.\n  ¿Cuál es su energía potencial elástica?",
        "opciones": opciones,
        "respuesta": round(U, 3),
        "unidad": "J",
        "solucion": solucion,
        "tema": "Energía Potencial Elástica"
    }

def q_conservacion_v():
    m = round(random.uniform(0.5, 8.0), 1)
    h = round(random.uniform(3.0, 30.0), 1)
    v = round(math.sqrt(2 * g * h), 2)
    opciones = sorted(set([
        round(v, 1),
        round(v * 1.2, 1),
        round(v * 0.75, 1),
        round(v * 1.5, 1)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  mgh = ½mv²  →  las masas se cancelan\n"
        f"  v = √(2gh)\n"
        f"  v = √(2 × 9.8 × {h})\n"
        f"  v = {C.GREEN}{round(v,2)} m/s{C.RESET}"
    )
    return {
        "pregunta": f"Un objeto cae desde el reposo desde {C.YELLOW}{h} m{C.RESET} de altura (sin fricción).\n  ¿Cuál es su rapidez al llegar al suelo?",
        "opciones": opciones,
        "respuesta": round(v, 1),
        "unidad": "m/s",
        "solucion": solucion,
        "tema": "Conservación de Energía → velocidad"
    }

def q_conservacion_h():
    m = round(random.uniform(1.0, 10.0), 1)
    v = round(random.uniform(3.0, 15.0), 1)
    h = round(v**2 / (2 * g), 3)
    opciones = sorted(set([
        round(h, 2),
        round(h * 1.3, 2),
        round(h * 0.6, 2),
        round(h * 1.7, 2)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  ½mv² = mgh  →  masas se cancelan\n"
        f"  h = v²/(2g)\n"
        f"  h = ({v})²/(2×9.8)\n"
        f"  h = {C.GREEN}{round(h,2)} m{C.RESET}"
    )
    return {
        "pregunta": f"Un objeto se lanza verticalmente hacia arriba con {C.YELLOW}v = {v} m/s{C.RESET}.\n  ¿Cuál es la altura máxima que alcanza?",
        "opciones": opciones,
        "respuesta": round(h, 2),
        "unidad": "m",
        "solucion": solucion,
        "tema": "Conservación de Energía → altura"
    }

def q_friccion():
    m   = round(random.uniform(1.0, 8.0), 1)
    v0  = round(random.uniform(5.0, 15.0), 1)
    mu  = round(random.uniform(0.1, 0.4), 2)
    d   = round(random.uniform(2.0, 10.0), 1)
    fk  = round(mu * m * g, 3)
    Wf  = round(fk * d, 3)
    K0  = round(0.5 * m * v0**2, 3)
    Kf  = round(K0 - Wf, 3)
    if Kf < 0:
        Kf = 0.0
    vf  = round(math.sqrt(2 * Kf / m), 2) if Kf > 0 else 0.0
    opciones = sorted(set([
        round(vf, 1),
        round(vf + 1.5, 1),
        round(max(vf - 1.2, 0), 1),
        round(vf * 1.4, 1)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  f_k = μ·m·g = {mu}×{m}×9.8 = {fk} N\n"
        f"  W_f = f_k·d = {fk}×{d} = {Wf} J\n"
        f"  K_f = K_i − W_f = {K0} − {Wf} = {Kf} J\n"
        f"  v_f = √(2K_f/m) = {C.GREEN}{vf} m/s{C.RESET}"
    )
    return {
        "pregunta": (
            f"Un bloque de {C.YELLOW}{m} kg{C.RESET} se mueve a {C.YELLOW}{v0} m/s{C.RESET} sobre\n"
            f"  una superficie con μ_k = {C.YELLOW}{mu}{C.RESET}, recorriendo {C.YELLOW}{d} m{C.RESET}.\n"
            f"  ¿Cuál es su velocidad final?"
        ),
        "opciones": opciones,
        "respuesta": round(vf, 1),
        "unidad": "m/s",
        "solucion": solucion,
        "tema": "Fuerzas No Conservativas (Fricción)"
    }

def q_trabajo():
    F     = round(random.uniform(10, 100), 1)
    d     = round(random.uniform(1.0, 20.0), 1)
    theta = random.choice([0, 30, 45, 60])
    W     = round(F * d * math.cos(math.radians(theta)), 2)
    opciones = sorted(set([
        round(W, 1),
        round(W * 1.3, 1),
        round(W * 0.6, 1),
        round(W * 1.6, 1)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  W = F·d·cos θ\n"
        f"  W = {F} × {d} × cos({theta}°)\n"
        f"  W = {F} × {d} × {round(math.cos(math.radians(theta)),3)}\n"
        f"  W = {C.GREEN}{round(W,1)} J{C.RESET}"
    )
    return {
        "pregunta": (
            f"Una fuerza de {C.YELLOW}{F} N{C.RESET} actúa sobre un objeto desplazándolo\n"
            f"  {C.YELLOW}{d} m{C.RESET}, formando un ángulo de {C.YELLOW}{theta}°{C.RESET} con el movimiento.\n"
            f"  ¿Cuánto trabajo realiza?"
        ),
        "opciones": opciones,
        "respuesta": round(W, 1),
        "unidad": "J",
        "solucion": solucion,
        "tema": "Trabajo de una Fuerza"
    }

def q_resorte_velocidad():
    k  = random.choice([500, 800, 1000, 1500, 2000])
    x  = round(random.uniform(0.02, 0.15), 2)
    m  = round(random.uniform(0.01, 0.2), 3)
    v  = round(x * math.sqrt(k / m), 2)
    opciones = sorted(set([
        round(v, 1),
        round(v * 1.3, 1),
        round(v * 0.7, 1),
        round(v * 1.6, 1)
    ]))
    random.shuffle(opciones)
    solucion = (
        f"  ½kx² = ½mv²\n"
        f"  v = x·√(k/m)\n"
        f"  v = {x}·√({k}/{m})\n"
        f"  v = {C.GREEN}{v} m/s{C.RESET}"
    )
    return {
        "pregunta": (
            f"Un resorte (k = {C.YELLOW}{k} N/m{C.RESET}) comprimido {C.YELLOW}{x} m{C.RESET}\n"
            f"  lanza una bola de {C.YELLOW}{m} kg{C.RESET}. ¿Con qué rapidez sale la bola?"
        ),
        "opciones": opciones,
        "respuesta": round(v, 1),
        "unidad": "m/s",
        "solucion": solucion,
        "tema": "Resorte → Velocidad (Conservación)"
    }

# ─────────────────────────────────────────────
#  POOL DE PREGUNTAS
# ─────────────────────────────────────────────
GENERADORES = [
    q_cinematica,
    q_potencial_grav,
    q_resorte,
    q_conservacion_v,
    q_conservacion_h,
    q_friccion,
    q_trabajo,
    q_resorte_velocidad,
]

def generar_quiz(n=8):
    pool = GENERADORES * 2
    random.shuffle(pool)
    preguntas = []
    for gen in pool[:n]:
        try:
            preguntas.append(gen())
        except Exception:
            pass
    return preguntas

# ─────────────────────────────────────────────
#  MOSTRAR PREGUNTA
# ─────────────────────────────────────────────
def mostrar_pregunta(idx, total, q):
    linea()
    print(f"{C.MAGENTA}{C.BOLD}  Pregunta {idx}/{total}  |  {q['tema']}{C.RESET}")
    linea()
    print(f"\n  {q['pregunta']}\n")

    letras = ["A", "B", "C", "D"]
    for i, op in enumerate(q["opciones"][:4]):
        print(f"  {C.CYAN}[{letras[i]}]{C.RESET}  {op} {q['unidad']}")
    print()

def pedir_respuesta(q):
    letras = ["A", "B", "C", "D"]
    while True:
        ans = input(f"  {C.BOLD}Tu respuesta (A/B/C/D): {C.RESET}").strip().upper()
        if ans in letras[:len(q["opciones"])]:
            return q["opciones"][letras.index(ans)]
        print(f"  {C.RED}Ingresa A, B, C o D.{C.RESET}")

# ─────────────────────────────────────────────
#  PANTALLA DE RESULTADO FINAL
# ─────────────────────────────────────────────
def pantalla_final(score, total, tiempo, errores):
    clr()
    header()
    pct = score / total * 100
    if pct >= 80:
        emoji, color, msg = "🏆", C.GREEN,  "¡Excelente! Estás listo para el examen"
    elif pct >= 60:
        emoji, color, msg = "📚", C.YELLOW, "Bien, repasa los temas que fallaste"
    else:
        emoji, color, msg = "💪", C.RED,    "Necesitas repasar más — ¡tú puedes!"

    print(f"  {color}{C.BOLD}{emoji}  RESULTADO FINAL{C.RESET}\n")
    print(f"  Puntaje  : {color}{C.BOLD}{score}/{total}  ({pct:.0f}%){C.RESET}")
    print(f"  Tiempo   : {C.CYAN}{tiempo:.1f} segundos{C.RESET}")
    print(f"  Promedio : {C.CYAN}{tiempo/total:.1f} seg/pregunta{C.RESET}")
    print(f"\n  {color}{msg}{C.RESET}\n")

    if errores:
        linea()
        print(f"\n  {C.YELLOW}{C.BOLD}📋 TEMAS QUE FALLASTE:{C.RESET}\n")
        for e in errores:
            print(f"  {C.RED}✗ {e['tema']}{C.RESET}")
            print(f"    Pregunta  : {e['pregunta'].replace(chr(27)+'[93m','').replace(chr(27)+'[0m','')}")
            print(f"    Tu resp.  : {C.RED}{e['dada']} {e['unidad']}{C.RESET}")
            print(f"    Correcta  : {C.GREEN}{e['correcta']} {e['unidad']}{C.RESET}")
            print(f"\n    {C.CYAN}Solución paso a paso:{C.RESET}")
            print(f"{e['solucion']}\n")
            linea()

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    clr()
    header()
    print(f"  {C.WHITE}Bienvenido al Quiz de Energía — Serway Tomo 1{C.RESET}")
    print(f"  {C.DIM}Cada pregunta tiene valores aleatorios únicos.{C.RESET}")
    print(f"  {C.DIM}Se te mostrarán 8 preguntas de opción múltiple.{C.RESET}\n")
    input(f"  {C.BOLD}Presiona Enter para comenzar... {C.RESET}")

    preguntas = generar_quiz(8)
    total     = len(preguntas)
    score     = 0
    errores   = []
    t_inicio  = time.time()

    for i, q in enumerate(preguntas, 1):
        clr()
        header()
        mostrar_pregunta(i, total, q)
        t_p = time.time()
        respuesta = pedir_respuesta(q)
        t_elapsed = round(time.time() - t_p, 1)

        correcto = abs(float(respuesta) - float(q["respuesta"])) < 0.05

        if correcto:
            score += 1
            print(f"\n  {C.GREEN}{C.BOLD}✔  ¡Correcto!{C.RESET}  ({t_elapsed}s)\n")
        else:
            print(f"\n  {C.RED}{C.BOLD}✘  Incorrecto.{C.RESET}  Respuesta correcta: {C.GREEN}{q['respuesta']} {q['unidad']}{C.RESET}")
            print(f"\n  {C.CYAN}Solución:{C.RESET}")
            print(f"{q['solucion']}\n")
            errores.append({**q, "dada": respuesta})

        # barra de progreso
        barra = "█" * score + "░" * (i - score)
        print(f"  Progreso: [{C.GREEN}{barra}{C.RESET}] {score}/{i}\n")
        input(f"  {C.DIM}Enter para continuar...{C.RESET}")

    tiempo_total = time.time() - t_inicio
    clr()
    pantalla_final(score, total, tiempo_total, errores)

if __name__ == "__main__":
    main()
    