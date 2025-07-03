from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("index.html", encoding="utf-8") as f:
        return f.read()

class ScriptRequest(BaseModel):
    script_name: str

@app.post("/run-script")
def run_script(req: ScriptRequest):
    script_map = {
        "script1": r"D:\Akshay\Work and Document\Work\LLM and Ai Agent\Zuora\Frontend_selnium\script\first.py",
        "script2": r"D:\Akshay\Work and Document\Work\LLM and Ai Agent\Zuora\Frontend_selnium\script\second.py"
    }
    print("req.script_name",req.script_name)
    print("script_map",script_map)
    script_path = script_map.get(req.script_name)
    print("script_path",script_path)
    if not script_path or not os.path.exists(script_path):
        return JSONResponse({"message": "Script not found."}, status_code=400)
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return {"message": f"Success! Output:\n{result.stdout}"}
        else:
            return {"message": f"Script failed. Error:\n{result.stderr}"}
    except Exception as e:
        return {"message": f"Error running script: {e}"}