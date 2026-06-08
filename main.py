# -*- coding: utf-8 -*-
import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
HTML_FILE = PROJECT_ROOT / "web" / "cuaca.html"
SERVER_HOST = "127.0.0.1"

SCRIPTS = [
    "ambil_cuaca_bmkg.py",
    "convert_json_to_csv.py",
    "prediksi_tegangan.py",
]


def jalankan_script(script_name):
    script_path = SRC_DIR / script_name

    if not script_path.exists():
        print(f"[ERROR] File tidak ditemukan: {script_path}")
        return False

    try:
        print(f"\nMenjalankan {script_name}...")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            cwd=PROJECT_ROOT,
        )

        print(f"[BERHASIL] {script_name} selesai.")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        return True

    except subprocess.CalledProcessError as error:
        print(f"[GAGAL] {script_name} gagal dijalankan.")
        if error.stderr:
            print(f"Error:\n{error.stderr}")
        if error.stdout:
            print(f"Output:\n{error.stdout}")
        return False


def cari_port_kosong(mulai=8000, selesai=8100):
    for port in range(mulai, selesai):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((SERVER_HOST, port))
            except OSError:
                continue
            return port
    raise RuntimeError("Tidak ada port kosong untuk server lokal.")


def buka_halaman_html():
    if not HTML_FILE.exists():
        print(f"File HTML tidak ditemukan: {HTML_FILE}")
        return

    port = cari_port_kosong()
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(port),
            "--bind",
            SERVER_HOST,
            "--directory",
            str(PROJECT_ROOT),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    time.sleep(0.5)

    url = f"http://{SERVER_HOST}:{port}/web/cuaca.html"
    webbrowser.open(url)
    print(f"Membuka halaman HTML: {url}")


def main():
    for script in SCRIPTS:
        if not jalankan_script(script):
            print("\nProses dihentikan karena terjadi error.")
            print("Beberapa script gagal. Silakan periksa error di atas.")
            return 1

    print("\nSemua script berhasil dijalankan tanpa error.")
    buka_halaman_html()
    return 0


if __name__ == "__main__":
    sys.exit(main())
