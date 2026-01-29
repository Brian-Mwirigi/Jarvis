from langchain.tools import tool
import subprocess
import platform

@tool("arp_scan_terminal", return_direct=True)
def arp_scan_terminal() -> str:
    """
    Runs 'arp -a' to show all devices on the local network.
    Works on Windows, macOS, and Linux.
    
    Example queries:
    - "Show me the ARP table"
    - "Run arp scan"
    - "Find all devices on my network"
    - "What devices are connected to my network?"
    """
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            apple_script = '''
            tell application "Terminal"
                activate
                do script "arp -a; echo ''; echo 'Press any key to close...'; read"
            end tell
            '''
            subprocess.Popen(["osascript", "-e", apple_script])
            return "Network devices are now displayed in Terminal. What else can I help with?"

        elif system == "Windows":
            # Run in new PowerShell window
            ps_script = '''
            arp -a
            Write-Host ""
            Write-Host "Press any key to close..." -NoNewline
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            '''
            subprocess.Popen([
                "powershell", 
                "-NoExit",
                "-Command", 
                ps_script
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return "Network devices are now displayed in a new window. What else can I help with?"

        elif system == "Linux":
            # Try different terminal emulators
            terminal_commands = [
                ["gnome-terminal", "--", "bash", "-c", "arp -a; echo ''; echo 'Press any key to close...'; read"],
                ["xterm", "-e", "bash", "-c", "arp -a; echo ''; echo 'Press any key to close...'; read"],
                ["konsole", "-e", "bash", "-c", "arp -a; echo ''; echo 'Press any key to close...'; read"],
            ]
            
            for cmd in terminal_commands:
                try:
                    subprocess.Popen(cmd)
                    return "Network devices are now displayed in Terminal. What else can I help with?"
                except FileNotFoundError:
                    continue
            
            # Fallback: return results directly
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return f"Network devices:\n\n{result.stdout}"
            else:
                return "Could not run ARP scan. Please ensure 'arp' command is available."

        else:
            return f"⚠️ ARP scan not supported on {system}."
            
    except Exception as e:
        return f"Failed to run ARP scan: {str(e)}"
