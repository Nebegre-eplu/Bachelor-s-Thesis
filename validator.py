import json
import math
from collections import defaultdict
 
#INPUT_FILE = "output_clean.jsonl"
INPUT_FILE = "with_Lissajous_you_can_do_it.jsonl"

PI = math.pi
N = 20 #numero di test per terna (Shape, Sys_prompt, Effort_lvl)
PHASE_3_1_DEGENERATE_1 = 0
PHASE_3_1_DEGENERATE_2 = PI / 3 #però lo è anche per 0 e per 2 PI / 3
PHASE_3_1_DEGENERATE_3 = (2*PI) / 3 #però lo è anche per 0 e per 2 PI / 3
PHASE_2_3_DEGENERATE_1 = (3*PI)/ 4 #però lo è anche PI / 4
PHASE_2_3_DEGENERATE_2 = PI / 4

 
TOL = {
    "amp_zero": 0.0003,  #praticamente inutile perchè il modello restituisce SEMPRE 0.0 e MAI infinitesimi maggiori
    "amp_equal": 0.0005, 
    "freq_zero": 0.0005, #praticamente inutile perchè il modello restituisce SEMPRE 0.0 e MAI infinitesimi maggiori
    "ratio": 0.08,
    "phase": 0.3, #partivo da 0.3 ma il cerchio aveva troppi errori
}

BOUNDS = {"x": 0.084, "y": 0.067, "f": 0.6, "phi": 2 * PI} #metà dimensione del tavolo lungo x, che è lungo 0.168 e y che è 0.134
                                                            #la frequenza è stata scelta tramite piccoli test su figure semplici, convalidata dal Professore
                                                            #la fase è scelta così solo per comodità di generazione e verifica
                                                
SYSTEM_PROMPTS = ["complete", "no_phase", "no_op_instruction", "zero-shot"]
EFFORTS = ["low", "medium", "high"]
SHAPES = ["point", "line", "circle", "ellipse", "eight", "parabola", "3:1", "2:3"]
REQUIRED_FIELDS = ("Ax", "Ay", "bx", "by", "fx", "fy", "phiy")
 
 
def ratio_is(fx, fy, p, q):
    #se è vicina alla frequenza p,q
    if fx < TOL["freq_zero"] or fy < TOL["freq_zero"]:
        return False
    target = p / q
    return abs(fx / fy - target) <= TOL["ratio"] * target 

 
def phase_is(phiy, target):
    d = abs(phiy - target) % PI #mi interessa MOD PI
    return min(d, PI - d) <= TOL["phase"]
 
 
def in_bounds(p):
    return (
        abs(p["Ax"]) + abs(p["bx"]) <= BOUNDS["x"] + 1e-6 and
        abs(p["Ay"]) + abs(p["by"]) <= BOUNDS["y"] + 1e-6 and
        0 <= p["fx"] <= BOUNDS["f"] + 1e-6 and
        0 <= p["fy"] <= BOUNDS["f"] + 1e-6 and
        -BOUNDS["phi"] <= p["phiy"] <= BOUNDS["phi"] + 1e-6
    )
 

def is_point(p):
    return (p["Ax"] <= TOL["amp_zero"] and p["Ay"] <= TOL["amp_zero"])
 
def is_line(p):
    # Orizzontale
    if p["Ay"] <= TOL["amp_zero"]:
        return True

    # Verticale
    if p["Ax"] <= TOL["amp_zero"]:
        return True

    # Obliqua (può essere qualsiasi in base alle ampiezze relative Ax e Ay, default 45°)
    return (
        ratio_is(p["fx"], p["fy"], 1, 1)
        and phase_is(p["phiy"], 0)
    )
 
 
def is_circle(p):
    return (
        ratio_is(p["fx"], p["fy"], 1, 1)
        and abs(p["Ax"] - p["Ay"]) <= TOL["amp_equal"]
        and phase_is(p["phiy"], PI / 2)
    )
 
 
def is_ellipse(p):
    # amplitudes are allowed to differ, phase CANT BE 0 (degenerates in a line)
    return ratio_is(p["fx"], p["fy"], 1, 1) and not phase_is(p["phiy"], 0)
 

def is_eight(p):

    # fx:fy = 1:2
    # parabola verticale: phase = pi/2
    if ratio_is(p["fx"], p["fy"], 1, 2):
        return not phase_is(p["phiy"], PI / 2)

    # fx:fy = 2:1
    # parabola orizzontale: phase = pi/4 oppure 3*pi/4
    if ratio_is(p["fx"], p["fy"], 2, 1):
        
        return (
            not phase_is(p["phiy"], PI / 4)
            and not phase_is(p["phiy"], 3 * PI / 4)
        )

    return False
 
 
def is_parabola(p):
    # 1:2 ratio -> vertical parabola (opens up/down): phase pi/2 covers both directions (mod pi)
    if ratio_is(p["fx"], p["fy"], 1, 2):
        return phase_is(p["phiy"], PI / 2)
    # 2:1 ratio -> horizontal parabola (opens left/right): pi/4 and 3*pi/4 are NOT
    # mod-pi equivalent here, so both must be checked explicitly to cover both directions
    if ratio_is(p["fx"], p["fy"], 2, 1):
        return phase_is(p["phiy"], PI / 4) or phase_is(p["phiy"], (3*PI) / 4)
    return False
 

#per 3:1 e 2:3, if DEGENERATE deve avere una fase specifica, se no va bene TUTTO ciò che è DIVERSO dalla fase degenere

def is_3_1(p, prompt):
    if not ratio_is(p["fx"], p["fy"], 3, 1):
        return False
    is_degenerate = "degenerate" in prompt.lower() 
    if is_degenerate:
        return phase_is(p["phiy"], PHASE_3_1_DEGENERATE_1) or phase_is(p["phiy"], PHASE_3_1_DEGENERATE_2) or phase_is(p["phiy"], PHASE_3_1_DEGENERATE_3)
    else:
        return not phase_is(p["phiy"], PHASE_3_1_DEGENERATE_1) and not phase_is(p["phiy"], PHASE_3_1_DEGENERATE_2) and not phase_is(p["phiy"], PHASE_3_1_DEGENERATE_3)

     

def is_2_3(p, prompt):
    if not ratio_is(p["fx"], p["fy"], 2, 3):
        return False
    degenerate = "degenerate" in prompt.lower()
    if degenerate:
        return phase_is(p["phiy"], PHASE_2_3_DEGENERATE_1) or phase_is(p["phiy"], PHASE_2_3_DEGENERATE_2)
    else:
        return not phase_is(p["phiy"], PHASE_2_3_DEGENERATE_1) and not phase_is(p["phiy"], PHASE_2_3_DEGENERATE_2)
 
def validate_record(record):
    try:
        data = json.loads(record["response"])
        p = {k: float(data[k]) for k in REQUIRED_FIELDS}
        uprompt = record["user_prompt"]
        shape = record["shape"]
    except Exception:
        return False  # malformed JSON / missing or non-numeric field = fail
        #aggiungi rifiuto
    
    if not in_bounds(p):
        return False

    #aggiungo il controllo sul RIFIUTO
    rifiutato = True
    for k in REQUIRED_FIELDS:
        if(p[k] != 0.0): 
            rifiutato = False
            break

    if shape != "point" and rifiutato: #nuovo controllo sul rifiuto
        return "rejected"
    
    if shape == "point":
        return is_point(p)
    elif shape == "line":
        return is_line(p)
    elif shape == "circle":
        return is_circle(p)
    elif shape == "ellipse":
        return is_ellipse(p)
    elif shape == "parabola":
        return is_parabola(p)
    elif shape == "eight":
        return is_eight(p)
    elif shape == "3:1":
        return is_3_1(p, uprompt)
    elif shape == "2:3":
        return is_2_3(p, uprompt)
    else:
        return False
 
 
#assumo di star lavorando con l'output ripulito
#         if r.get("status") != "success":
#            continue
def build_matrix(records):
    matrix = {
        shape: {
            prompt: {
                effort: {
                    "successes": 0, #calcolo chiamando validate_record
                    "rejections": 0, #quante volte non sbaglio MA reputo la figura NON ottenibile (parabola penso a te)
                    "tokens": 0, #calcolo a prescindere dal successo
                    "success_rate": 0.0,
                    "rejection_rate": 0.0, 
                    "efficiency": 0.0, #è un costo
                    "average_token_cost": 0.0 #simile al costo, ma per tutti  itentativi e non per solo quelli successi
                }
                for effort in EFFORTS
            }
            for prompt in SYSTEM_PROMPTS
        }
        for shape in SHAPES
    }
    
    #valori intermedi
    for r in records: #devo scorrere tutti i record per forza
        cell = matrix[r["shape"]][r["system_prompt"]][r["effort"]] #è collegata allo stesso puntatore e quindi modificando cell
                                                                    #modifico anche matrix originale!!
                                                                    #sto imparando python mo
        cell["tokens"] += r["reasoning_token"]
        validity = validate_record(r)
        



        if validity == True:
            cell["successes"] += 1
        elif validity == "rejected":
            cell["rejections"] += 1

    #valori finali, ciò che mi interessa
    for s in SHAPES: #devo scorrere nella matrice
        for p in SYSTEM_PROMPTS:
            for e in EFFORTS:
                cell = matrix[s][p][e]

                cell["success_rate"] = cell["successes"] / N
                cell["rejection_rate"] = cell["rejections"] / N #con la parabola sarà molto alto, altrove sarà quasi nullo
                cell["average_token_cost"] = cell["tokens"] / N
                if (cell["successes"] > 0): #non succederà mai che avrò 0 successi? PARABOLA 
                    cell["efficiency"] = cell["tokens"] / cell["successes"]
                    #print(cell["efficiency"])
                else:
                    cell["efficiency"] = float('nan')


    return matrix

                 
def print_matrices(matrix):
    for s in SHAPES:
        print(f"\n=== {s} ===")
        print(f"{'':<18}" + "".join(f"{e:>24}                                             " for e in EFFORTS)) #includendo anche reject rate la colonna deve essere più chiatta

        for p in SYSTEM_PROMPTS:
            row = f"{p:<18}"

            for eff in EFFORTS:
                cell = matrix[s][p][eff]

                text = (
                    f"Successes: {cell['successes']} "
                    #f"Success rate: {cell['success_rate'] * 100:5.1f}% "
                    f"Rejections: {cell['rejections']} "
                    #f"Rejection rate: {cell['rejection_rate'] * 100:5.1f}% "
                    f"Cost: ({cell['efficiency']:.1f})"
                    f"ATC: {cell['average_token_cost']:.1f} ||"
                )

                row += f"{text:>24}"

            print(row)

 
 
if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    matrix = build_matrix(records)
    print_matrices(matrix)