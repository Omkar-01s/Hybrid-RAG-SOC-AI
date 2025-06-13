from core.engine import generate_playbook
import sys

# 🏁 Entry point for CLI-based execution
if __name__ == '__main__':
    alert_file_path = sys.argv[1] if len(sys.argv) > 1 else "data/alerts/suspicious_login.json"
    report = generate_playbook(alert_file_path)
    print(f"✅ Playbook report generated: {report}")
