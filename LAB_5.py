import subprocess, shlex, os
import datetime as dt

SIGROK = r"C:\Program Files\sigrok\sigrok-cli\sigrok-cli.exe"
DRIVER = "rigol-ds"

def run(cmd):
    print("[CMD]", " ".join(shlex.quote(str(c)) for c in cmd))
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if p.stdout.strip(): print(p.stdout)
    if p.stderr.strip(): print(p.stderr)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed (exit={p.returncode})")
    return p

def main():
    tag = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_csv = f"ch1_{tag}.csv"

    run([SIGROK, "-d", DRIVER, "--scan"])

    run([
        SIGROK,
        "-d", DRIVER,
        "-C", "CH1",
        "--config", "data_source=Live",
        "--config", "timebase=5 ms",
        "--config", "limit_frames=1",
        "-O", "csv:header=true",
        "-o", out_csv
    ])

    print("[DONE] Saved:", os.path.abspath(out_csv))

if __name__ == "__main__":
    main()
