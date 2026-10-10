import matplotlib.pyplot as plt
import numpy as np
import math
import re


RAW_TEXT_you_can_do_it = """
=== point ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||

=== line ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||

=== circle ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||

=== ellipse ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||

=== eight ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||

=== parabola ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 19 Cost: (nan)ATC: 41.9 ||Successes: 7 Rejections: 11 Cost: (2257.7)ATC: 790.2 ||Successes: 10 Rejections: 10 Cost: (6950.0)ATC: 3475.0 ||
no_phase          Successes: 1 Rejections: 14 Cost: (1105.0)ATC: 55.2 ||Successes: 3 Rejections: 12 Cost: (4116.0)ATC: 617.4 ||Successes: 10 Rejections: 10 Cost: (6482.0)ATC: 3241.0 ||
no_op_instruction Successes: 0 Rejections: 17 Cost: (nan)ATC: 30.6 ||Successes: 2 Rejections: 13 Cost: (2001.5)ATC: 200.2 ||Successes: 5 Rejections: 14 Cost: (9685.6)ATC: 2421.4 ||
zero-shot         Successes: 0 Rejections: 20 Cost: (nan)ATC: 24.4 ||Successes: 8 Rejections: 11 Cost: (1567.1)ATC: 626.9 ||Successes: 9 Rejections: 11 Cost: (6758.9)ATC: 3041.5 ||

=== 3:1 ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||

=== 2:3 ===
                                       low                                                               medium                                                                 high              
complete          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_phase          Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
zero-shot         Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||Successes: 0 Rejections: 0 Cost: (nan)ATC: 0.0 ||
"""

RAW_TEXT = """
=== point ===
                                       low                                                               medium                                                                 high              
complete          Successes: 20 Rejections: 0 Cost: (86.5)ATC: 86.5 ||Successes: 20 Rejections: 0 Cost: (212.9)ATC: 212.9 ||Successes: 20 Rejections: 0 Cost: (871.4)ATC: 871.4 ||
no_phase          Successes: 20 Rejections: 0 Cost: (85.0)ATC: 85.0 ||Successes: 20 Rejections: 0 Cost: (214.8)ATC: 214.8 ||Successes: 20 Rejections: 0 Cost: (791.8)ATC: 791.8 ||
no_op_instruction Successes: 20 Rejections: 0 Cost: (72.1)ATC: 72.1 ||Successes: 20 Rejections: 0 Cost: (178.2)ATC: 178.2 ||Successes: 20 Rejections: 0 Cost: (713.0)ATC: 713.0 ||
zero-shot         Successes: 19 Rejections: 0 Cost: (97.5)ATC: 92.6 ||Successes: 20 Rejections: 0 Cost: (322.4)ATC: 322.4 ||Successes: 20 Rejections: 0 Cost: (1158.8)ATC: 1158.8 ||

=== line ===
                                       low                                                               medium                                                                 high              
complete          Successes: 18 Rejections: 2 Cost: (197.4)ATC: 177.7 ||Successes: 20 Rejections: 0 Cost: (475.6)ATC: 475.6 ||Successes: 20 Rejections: 0 Cost: (1927.5)ATC: 1927.5 ||
no_phase          Successes: 18 Rejections: 1 Cost: (183.7)ATC: 165.3 ||Successes: 19 Rejections: 1 Cost: (495.9)ATC: 471.1 ||Successes: 20 Rejections: 0 Cost: (1899.7)ATC: 1899.7 ||
no_op_instruction Successes: 18 Rejections: 1 Cost: (169.3)ATC: 152.3 ||Successes: 19 Rejections: 1 Cost: (391.4)ATC: 371.8 ||Successes: 20 Rejections: 0 Cost: (1493.5)ATC: 1493.5 ||
zero-shot         Successes: 18 Rejections: 2 Cost: (209.7)ATC: 188.7 ||Successes: 19 Rejections: 1 Cost: (597.7)ATC: 567.8 ||Successes: 20 Rejections: 0 Cost: (2835.5)ATC: 2835.5 ||

=== circle ===
                                       low                                                               medium                                                                 high              
complete          Successes: 7 Rejections: 0 Cost: (432.0)ATC: 151.2 ||Successes: 20 Rejections: 0 Cost: (438.4)ATC: 438.4 ||Successes: 20 Rejections: 0 Cost: (1919.5)ATC: 1919.5 ||
no_phase          Successes: 4 Rejections: 0 Cost: (720.0)ATC: 144.0 ||Successes: 15 Rejections: 0 Cost: (434.2)ATC: 325.6 ||Successes: 20 Rejections: 0 Cost: (1617.7)ATC: 1617.7 ||
no_op_instruction Successes: 0 Rejections: 0 Cost: (nan)ATC: 106.5 ||Successes: 9 Rejections: 0 Cost: (671.0)ATC: 301.9 ||Successes: 19 Rejections: 1 Cost: (1797.3)ATC: 1707.4 ||
zero-shot         Successes: 9 Rejections: 0 Cost: (378.4)ATC: 170.3 ||Successes: 20 Rejections: 0 Cost: (498.6)ATC: 498.6 ||Successes: 20 Rejections: 0 Cost: (1861.2)ATC: 1861.2 ||

=== ellipse ===
                                       low                                                               medium                                                                 high              
complete          Successes: 1 Rejections: 0 Cost: (2485.0)ATC: 124.2 ||Successes: 18 Rejections: 0 Cost: (535.7)ATC: 482.1 ||Successes: 20 Rejections: 0 Cost: (1925.7)ATC: 1925.7 ||
no_phase          Successes: 2 Rejections: 0 Cost: (1114.5)ATC: 111.5 ||Successes: 12 Rejections: 0 Cost: (563.2)ATC: 337.9 ||Successes: 18 Rejections: 0 Cost: (1701.1)ATC: 1531.0 ||
no_op_instruction Successes: 1 Rejections: 0 Cost: (2012.0)ATC: 100.6 ||Successes: 2 Rejections: 0 Cost: (2230.5)ATC: 223.1 ||Successes: 18 Rejections: 0 Cost: (1520.2)ATC: 1368.2 ||
zero-shot         Successes: 6 Rejections: 1 Cost: (471.0)ATC: 141.3 ||Successes: 16 Rejections: 0 Cost: (640.4)ATC: 512.3 ||Successes: 20 Rejections: 0 Cost: (2198.7)ATC: 2198.7 ||

=== eight ===
                                       low                                                               medium                                                                 high              
complete          Successes: 11 Rejections: 0 Cost: (344.2)ATC: 189.3 ||Successes: 7 Rejections: 0 Cost: (2511.0)ATC: 878.9 ||Successes: 9 Rejections: 0 Cost: (13354.4)ATC: 6009.5 ||
no_phase          Successes: 12 Rejections: 0 Cost: (324.8)ATC: 194.8 ||Successes: 19 Rejections: 0 Cost: (461.4)ATC: 438.4 ||Successes: 20 Rejections: 0 Cost: (3240.2)ATC: 3240.2 ||
no_op_instruction Successes: 10 Rejections: 0 Cost: (328.3)ATC: 164.2 ||Successes: 18 Rejections: 0 Cost: (442.0)ATC: 397.8 ||Successes: 18 Rejections: 0 Cost: (2234.2)ATC: 2010.8 ||
zero-shot         Successes: 10 Rejections: 0 Cost: (454.3)ATC: 227.2 ||Successes: 3 Rejections: 0 Cost: (5744.3)ATC: 861.6 ||Successes: 3 Rejections: 0 Cost: (40252.3)ATC: 6037.9 ||

=== parabola ===
                                       low                                                               medium                                                                 high
complete          Successes: 0 Rejections: 20 Cost: (nan)ATC: 22.9 ||Successes: 0 Rejections: 20 Cost: (nan)ATC: 128.6 ||Successes: 1 Rejections: 19 Cost: (19607.0)ATC: 980.4 ||
no_phase          Successes: 0 Rejections: 20 Cost: (nan)ATC: 21.4 ||Successes: 0 Rejections: 20 Cost: (nan)ATC: 157.1 ||Successes: 1 Rejections: 19 Cost: (16084.0)ATC: 804.2 ||
no_op_instruction Successes: 0 Rejections: 20 Cost: (nan)ATC: 17.4 ||Successes: 0 Rejections: 20 Cost: (nan)ATC: 118.2 ||Successes: 0 Rejections: 20 Cost: (nan)ATC: 356.6 ||
zero-shot         Successes: 0 Rejections: 20 Cost: (nan)ATC: 24.7 ||Successes: 0 Rejections: 20 Cost: (nan)ATC: 137.4 ||Successes: 0 Rejections: 20 Cost: (nan)ATC: 492.8 ||

=== 3:1 ===
                                       low                                                               medium                                                                 high
complete          Successes: 20 Rejections: 0 Cost: (279.0)ATC: 279.0 ||Successes: 20 Rejections: 0 Cost: (691.0)ATC: 691.0 ||Successes: 20 Rejections: 0 Cost: (2726.1)ATC: 2726.1 ||
no_phase          Successes: 4 Rejections: 0 Cost: (629.8)ATC: 126.0 ||Successes: 7 Rejections: 0 Cost: (1090.3)ATC: 381.6 ||Successes: 6 Rejections: 0 Cost: (6919.0)ATC: 2075.7 ||
no_op_instruction Successes: 4 Rejections: 0 Cost: (646.2)ATC: 129.2 ||Successes: 4 Rejections: 0 Cost: (1703.5)ATC: 340.7 ||Successes: 4 Rejections: 0 Cost: (8356.0)ATC: 1671.2 ||
zero-shot         Successes: 20 Rejections: 0 Cost: (296.2)ATC: 296.2 ||Successes: 20 Rejections: 0 Cost: (779.6)ATC: 779.6 ||Successes: 20 Rejections: 0 Cost: (2856.9)ATC: 2856.9 ||

=== 2:3 ===
                                       low                                                               medium                                                                 high
complete          Successes: 19 Rejections: 0 Cost: (297.4)ATC: 282.6 ||Successes: 20 Rejections: 0 Cost: (663.5)ATC: 663.5 ||Successes: 20 Rejections: 0 Cost: (3626.4)ATC: 3626.4 ||
no_phase          Successes: 15 Rejections: 0 Cost: (219.8)ATC: 164.8 ||Successes: 15 Rejections: 0 Cost: (503.5)ATC: 377.6 ||Successes: 15 Rejections: 0 Cost: (3265.8)ATC: 2449.3 ||
no_op_instruction Successes: 14 Rejections: 0 Cost: (216.1)ATC: 151.2 ||Successes: 15 Rejections: 0 Cost: (454.7)ATC: 341.0 ||Successes: 15 Rejections: 0 Cost: (2383.6)ATC: 1787.7 ||
zero-shot         Successes: 20 Rejections: 0 Cost: (271.8)ATC: 271.8 ||Successes: 20 Rejections: 0 Cost: (724.2)ATC: 724.2 ||Successes: 20 Rejections: 0 Cost: (3216.1)ATC: 3216.1 ||
"""


def parse_raw_data(text):
    matrix = {}
    current_shape = ""
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("==="):
            current_shape = line.replace("=", "").strip()
            matrix[current_shape] = {}
        elif "Successes:" in line:
            parts = line.split("Successes:")
            prompt = parts[0].strip()
            matrix[current_shape][prompt] = {}
            
            blocks = line.split("||")
            efforts = ["low", "medium", "high"]
            
            for idx, effort in enumerate(efforts):
                if idx >= len(blocks) - 1: # L'ultimo blocco dopo || è vuoto
                    continue
                block = "Successes:" + blocks[idx]
                # Aggiornata la regex per catturare anche l'ATC finale
                m = re.search(r"Successes:\s*(\d+)\s*Rejections:\s*(\d+)\s*Cost:\s*\(([^)]+)\)ATC:\s*([0-9.]+)", block)
                if m:
                    cost_val = float(m.group(3)) if m.group(3) != "nan" else np.nan
                    atc_val = float(m.group(4)) if m.group(4) != "nan" else np.nan
                    matrix[current_shape][prompt][effort] = {
                        "successes": int(m.group(1)),
                        "rejections": int(m.group(2)),
                        "efficiency": cost_val,
                        "atc": atc_val # Nuova variabile M
                    }
    return matrix

def wilson_ci(successes, n=20, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = successes / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (max(0.0, center - half), min(1.0, center + half))



SHAPES = ["point", "line", "circle", "ellipse", "eight", "parabola", "3:1", "2:3"]
SYSTEM_PROMPTS = ["complete", "no_phase", "no_op_instruction", "zero-shot"]
EFFORTS = ["low", "medium", "high"]


METRICS = {
    "point": ["cost"],
    "line": ["cost"],
    "circle": ["success_rate", "cost", "atc"],
    "ellipse": ["success_rate", "cost", "atc"],
    "eight": ["success_rate", "cost", "atc"],
    "parabola": ["success_rate", "rejection_rate", "cost", "atc"],
    "3:1": ["success_rate", "cost", "atc"],
    "2:3": ["success_rate", "cost", "atc"],
}


def plot_shape(matrix, shape):
    metrics = METRICS[shape]
    n_metrics = len(metrics)

    fig, axes = plt.subplots(1, n_metrics, figsize=(6 * n_metrics, 5), squeeze=False, layout="constrained")
    axes = axes[0]

    for idx, (ax, metric) in enumerate(zip(axes, metrics)):
        values = np.full((len(SYSTEM_PROMPTS), len(EFFORTS)), np.nan)

        #gradient
        for i, prompt in enumerate(SYSTEM_PROMPTS):
            for j, effort in enumerate(EFFORTS):
                cell = matrix[shape][prompt][effort]
                
                if metric == "success_rate":
                    values[i, j] = (cell["successes"] / 20.0) * 100
                elif metric == "rejection_rate":
                    values[i, j] = (cell["rejections"] / 20.0) * 100
                elif metric == "cost":
                    values[i, j] = cell["efficiency"]
                elif metric == "atc":
                    values[i, j] = cell["atc"]

        #color map= (green = good, red = bad)
        if metric == "success_rate":
            cmap = "RdYlGn"
            vmin, vmax = 0, 100
            title = "Success Rate"
        elif metric == "rejection_rate":
            cmap = "RdYlGn_r"
            vmin, vmax = 0, 100
            title = "Rejection Rate"
        elif metric == "cost":
            cmap = "RdYlGn_r"
            vmin = np.nanmin(values) if not np.isnan(values).all() else 0
            vmax = np.nanmax(values) if not np.isnan(values).all() else 1
            title = "Success Cost (C)"
        elif metric == "atc":
            cmap = "RdYlGn_r"
            vmin = np.nanmin(values) if not np.isnan(values).all() else 0
            vmax = np.nanmax(values) if not np.isnan(values).all() else 1
            title = "Average Cost (M)"

        im = ax.imshow(values, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)

        #axis
        ax.set_xticks(np.arange(len(EFFORTS)))
        ax.set_xticklabels(EFFORTS)
        ax.set_yticks(np.arange(len(SYSTEM_PROMPTS)))
        ax.set_yticklabels(SYSTEM_PROMPTS)
        ax.set_xlabel("Effort")
        
        if idx == 0:
            ax.set_ylabel("System prompt")
        else:
            ax.set_yticklabels([]) 

        ax.set_title(title)

        #print texts
        for i in range(len(SYSTEM_PROMPTS)):
            for j in range(len(EFFORTS)):
                cell = matrix[shape][SYSTEM_PROMPTS[i]][EFFORTS[j]]
                
                if metric == "success_rate":
                    low_ci, high_ci = wilson_ci(cell["successes"], 20)
                    label = f"{low_ci*100:.0f}-{high_ci*100:.0f}%"
                elif metric == "rejection_rate":
                    low_ci, high_ci = wilson_ci(cell["rejections"], 20)
                    label = f"{low_ci*100:.0f}-{high_ci*100:.0f}%"
                elif metric == "cost":
                    cost_val = cell["efficiency"]
                    label = "N/A" if np.isnan(cost_val) else f"{cost_val:.0f}"
                elif metric == "atc":
                    atc_val = cell["atc"]
                    label = "N/A" if np.isnan(atc_val) else f"{atc_val:.0f}"
                
                
                ax.text(j, i, label, ha="center", va="center", color="black", weight="bold")

        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("Rate (%)" if metric in ["success_rate", "rejection_rate"] else "Reasoning tokens")


    display_names = {
        "success_rate": "Success Rate",
        "rejection_rate": "Rejection Rate",
        "cost": "Reasoning Cost",
        "atc": "Average Cost"
    }
    
    metric_labels = [display_names[m] for m in metrics]
    
    if len(metric_labels) == 1:
        metrics_str = metric_labels[0]
    elif len(metric_labels) == 2:
        metrics_str = f"{metric_labels[0]} and {metric_labels[1]}"
    else:
        metrics_str = ", ".join(metric_labels[:-1]) + f", and {metric_labels[-1]}"

    fig.suptitle(f"{shape.capitalize()} — {metrics_str}", fontsize=14)
    
    return fig



def plot_all_shapes(matrix):
    for shape in SHAPES:
        fig = plot_shape(matrix, shape)
        plt.show()
        plt.close(fig)


matrix = parse_raw_data(RAW_TEXT)
plot_all_shapes(matrix)