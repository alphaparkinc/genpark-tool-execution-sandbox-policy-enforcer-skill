from client import ToolSandboxPolicyEnforcer

enforcer = ToolSandboxPolicyEnforcer(allowed_paths=["/workspace", "C:/Workspace"])
print("Path /workspace/src/app.py:", enforcer.validate_path("/workspace/src/app.py"))
print("Path /etc/passwd:", enforcer.validate_path("/etc/passwd"))
print("Command 'ls -la':", enforcer.validate_command("ls -la"))
print("Command 'rm -rf /':", enforcer.validate_command("rm -rf /"))
