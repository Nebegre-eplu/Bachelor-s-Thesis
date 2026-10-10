import itertools
import os
import json
import time
import groq
from groq import Groq
import matlab.engine
from modules import call_Groq
from prompts import SYSTEM_PROMPT
from prompts import PHYSICAL_TEST_PROMPTS

eng = matlab.engine.connect_matlab()
eng.cd(r"C:\Mio_percorso", nargout=0)



Three_PROMPTS = {
    "circle": [
        "Draw a circle shifted to the left side of the table\n" # Testa forma vincolata + traslazione asimmetrica
    ],
    "eight": [
        "Draw a large figure eight shifted to the bottom half of the table\n" # Testa topologia complessa + limite di workspace

    ],
    "2:3": [
        "Make a figure with 2 lobes on the horizontal and 3 lobes on the vertical\n"
    ]
}

reasoning_level = "high"





def put_workspace(rc: str): 
    if rc is None:
        print("No response from Groq")
        return 
    
    data = json.loads(rc)
    #print(data)
    #ho tolto phix
    eng.eval(f"""
    Ax_llm.Value = {float(data["Ax"])};
    Ay_llm.Value = {float(data["Ay"])};
    bx_llm.Value = {float(data["bx"])};
    by_llm.Value = {float(data["by"])};
    fx_llm.Value = {float(data["fx"])};
    fy_llm.Value = {float(data["fy"])};
    phiy_llm.Value = {float(data["phiy"])};
    """, nargout=0)
    eng.set_param("traiettoriaControlPD", "SimulationCommand", "update", nargout=0)

def run_test_battery():
    reset_json = '{"Ax": 0.0, "Ay": 0.0, "bx": 0.0, "by": 0.0, "fx": 0.0, "fy": 0.0, "phiy": 0.0}'
    for shape, prompts in PHYSICAL_TEST_PROMPTS.items():
        print("Forma: ")
        print(shape)
        for prompt_index, user_prompt in enumerate(prompts):
            print(user_prompt)
            print()
            raw_response = call_Groq(user_prompt = user_prompt, lvl=reasoning_level, sys_prompt=SYSTEM_PROMPT)
            put_workspace(raw_response)
            time.sleep(15)
            #vorrei un tempo di reset (dove torna al centro) tra i due 
            put_workspace(reset_json)
            time.sleep(3) #1/5 del tempo di esecuzione

#inizializzo i Simulink.Parameter, prima di interrogare il robot, con phix costantemente 0
eng.eval("""
if ~exist('Ax_llm', 'var') || ~isa(Ax_llm, 'Simulink.Parameter')
    Ax_llm = Simulink.Parameter(1);
end
if ~exist('Ay_llm', 'var') || ~isa(Ay_llm, 'Simulink.Parameter')
    Ay_llm = Simulink.Parameter(0);
end
if ~exist('bx_llm', 'var') || ~isa(bx_llm, 'Simulink.Parameter')
    bx_llm = Simulink.Parameter(0);
end
if ~exist('by_llm', 'var') || ~isa(by_llm, 'Simulink.Parameter')
    by_llm = Simulink.Parameter(0);
end
if ~exist('fx_llm', 'var') || ~isa(fx_llm, 'Simulink.Parameter')
    fx_llm = Simulink.Parameter(0);
end
if ~exist('fy_llm', 'var') || ~isa(fy_llm, 'Simulink.Parameter')
    fy_llm = Simulink.Parameter(0);
end
phix_llm = Simulink.Parameter(0);
if ~exist('phi_llm', 'var') || ~isa(phiy_llm, 'Simulink.Parameter')
    phi_llm = Simulink.Parameter(0);
end
""", nargout=0)

run_test_battery()
eng.disconnect()
