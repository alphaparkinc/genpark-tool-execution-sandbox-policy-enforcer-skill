import sys
import json
from client import ToolSandboxPolicyEnforcer

enforcer = ToolSandboxPolicyEnforcer()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-tool-execution-sandbox-policy-enforcer-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "verify_sandbox_safety",
                        "description": "Check if file path or shell command conforms to sandbox policy",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "target_path": {"type": "string"},
                                "command": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        args = params.get("arguments", {})
        p = args.get("target_path")
        c = args.get("command")
        path_ok = enforcer.validate_path(p) if p else True
        cmd_ok = enforcer.validate_command(c) if c else True
        safe = path_ok and cmd_ok
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"allowed": safe, "path_valid": path_ok, "command_valid": cmd_ok})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
