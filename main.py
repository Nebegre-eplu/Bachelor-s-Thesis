import json 
from groq import Groq
import matlab.engine
import math
from validator import in_bounds
from prompts import SYSTEM_PROMPT #i need only the complete system prompt for the real pipeline
from modules import call_Groq

eng = matlab.engine.connect_matlab()
#eng = matlab.engine.start_matlab("-desktop")
#eng = matlab.engine.start_matlab("")
eng.cd(r"C:\Users\datoa\Desktop\Maschera", nargout=0)
#eng.open_system("traiettoriaControlPD", nargout=0)




#MODEL_NAME = "llama-3.3-70b-versatile" # deprecato mannaggia a Groq
MODEL_NAME = "openai/gpt-oss-120b"
#MODEL_NAME = "qwen/qwen3.6-27b" # alternativa a Openai/GTP-OSS-120B, non funziona bene





#estrai JSON dalla risposta di Groq
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

    
    #except json.JSONDecodeError as er:
    #    print("Error: not a valid JSON.")
    #    print(f"str{er}")




#def is_valid(rc):
#    p = json.loads(rc)
#    return (
#        abs(p["Ax"]) + abs(p["bx"]) <= MAX_X and
#        abs(p["Ay"]) + abs(p["by"]) <= MAX_Y and
#        0 <= p["fx"] <= MAX_FREQ and
#        0 <= p["fy"] <= MAX_FREQ and
#        -PI <= p["phiy"] <= PI
#    )

#inizializzo i Simulink.Parameter, con phix costantemente 0
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
if ~exist('phiy_llm', 'var') || ~isa(phiy_llm, 'Simulink.Parameter')
    phiy_llm = Simulink.Parameter(0);
end
""", nargout=0)

while True:
    user_prompt = input("Insert ball instruction: ")
    if user_prompt.lower() == "exit":
        break
    user_prompt = user_prompt


    rawr_content, temp = call_Groq(user_prompt=user_prompt, lvl="high", sys_prompt=SYSTEM_PROMPT, model_name=MODEL_NAME)
    print(rawr_content)
    #MINI VALIDATORE
    p = json.loads(rawr_content)
    if not in_bounds(p): #validità solo fisica, non check sulla topologia
        print("Warning, the model has generated a non valid output")
        break
    put_workspace(rawr_content) #parsing e invio al workspace

    #debug print for the MATLAB workspace values
    #eng.eval("""
    #disp('--- VALORI MATLAB ---')
    #disp(['Ax_llm   = ', num2str(Ax_llm.Value)])
    #disp(['Ay_llm   = ', num2str(Ay_llm.Value)])
    #disp(['bx_llm   = ', num2str(bx_llm.Value)])
    #disp(['by_llm   = ', num2str(by_llm.Value)])
    #disp(['fx_llm   = ', num2str(fx_llm.Value)])
    #disp(['fy_llm   = ', num2str(fy_llm.Value)])
    #disp(['phix_llm = ', num2str(phix_llm.Value)])
    #disp(['phiy_llm = ', num2str(phiy_llm.Value)])
    #""", nargout=0)


#eng.close_system("traiettoriaControlPD", 0, nargout=0) #anche senza quit sembra chiudersi lo stesso
#eng.quit()
eng.disconnect()

