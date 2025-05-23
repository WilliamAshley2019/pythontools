import time
import datetime
from pynput import keyboard
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

log_file = "global_key_log.txt"

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Key Logger with Timestamps")

        self.text_area = ScrolledText(root, width=60, height=20, font=("Consolas", 12))
        self.text_area.pack(padx=10, pady=10)
        self.text_area.configure(state='disabled')

        self.start_time = time.perf_counter()

        # Start keyboard listener in a separate thread so GUI stays responsive
        listener_thread = threading.Thread(target=self.start_listener, daemon=True)
        listener_thread.start()

    def log_key(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)  # Special keys

        elapsed_ms = int((time.perf_counter() - self.start_time) * 1000)
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        log_entry = f"Key: {key_str}, Time(ms since start): {elapsed_ms}, Timestamp(UTC): {timestamp}"

        # Log to file
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

        # Update GUI text area safely from listener thread
        self.root.after(0, self.append_text, log_entry)

    def append_text(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)  # Scroll to end
        self.text_area.configure(state='disabled')

    def start_listener(self):
        with keyboard.Listener(on_press=self.log_key) as listener:
            listener.join()


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()

