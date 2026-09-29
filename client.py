"""Tool Execution Sandbox Policy Enforcer.
100% Python Standard Library.
"""

class ToolSandboxPolicyEnforcer:
    """Validates filesystem paths and shell commands against sandbox containment policies."""
    def __init__(self, allowed_paths=None, blocked_commands=None):
        self.allowed_paths = [p.replace("\\", "/").lower() for p in (allowed_paths or ["/workspace", "c:/workspace"])]
        self.blocked_commands = set(blocked_commands or ["rm -rf", "format", "shutdown", "drop database"])

    def validate_path(self, target_path):
        norm = target_path.replace("\\", "/").lower()
        if any(norm.startswith(p) for p in self.allowed_paths):
            return True
        return False

    def validate_command(self, cmd):
        cmd_lower = cmd.lower()
        if any(blocked in cmd_lower for blocked in self.blocked_commands):
            return False
        return True
