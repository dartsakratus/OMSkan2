import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from processing import process
from pypdf.errors import PdfReadError


# ----------------------------------------------------------------------
# WINDOW CODE
# ----------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OMSkan")
        self.geometry("560x300")
        self.minsize(480, 280)

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.stage_var = tk.StringVar(value="1")
        self.status_var = tk.StringVar(value="Wybierz plik ze skanami oraz folder w którym zostaną umieszczone podzielone prace.")
        self.messages: queue.Queue = queue.Queue()

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Plik ze skanami:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=self.input_var).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(frame, text="Przeglądaj...", command=self.pick_input).grid(row=0, column=2)

        ttk.Label(frame, text="Folder końcowy:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=self.output_var).grid(row=1, column=1, sticky="ew", padx=8)
        ttk.Button(frame, text="Przeglądaj...", command=self.pick_output).grid(row=1, column=2)

        ttk.Label(frame, text="Etap:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Spinbox(
            frame, from_=1, to=3, width=6, textvariable=self.stage_var
        ).grid(row=2, column=1, sticky="w", padx=8)

        self.run_btn = ttk.Button(frame, text="Podziel plik", command=self.start)
        self.run_btn.grid(row=3, column=0, columnspan=3, pady=(18, 8))

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky="ew")

        ttk.Label(frame, textvariable=self.status_var, wraplength=500).grid(
            row=5, column=0, columnspan=3, sticky="w", pady=(8, 0)
        )

    # ---- file pickers -------------------------------------------------
    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Wybierz plik ze skanami", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if path:
            self.input_var.set(path)
            # Convenience: default the output folder to the PDF's folder
            if not self.output_var.get():
                self.output_var.set(str(Path(path).parent))

    def pick_output(self):
        path = filedialog.askdirectory(title="Wybierz folder końcowy")
        if path:
            self.output_var.set(path)

    # ---- running the process -----------------------------------------
    def start(self):
        input_path = Path(self.input_var.get().strip())
        output_dir = Path(self.output_var.get().strip())

        if not self.input_var.get().strip() or not input_path.is_file():
            messagebox.showwarning("Brakujący plik", "Wybierz plik ze skanami.")
            return
        if input_path.suffix.lower() != ".pdf":
            messagebox.showwarning("Złe rozszerzenie pliku", "Wybrany plik nie jest w rozszerzeniu .pdf.")
            return
        if not self.output_var.get().strip():
            messagebox.showwarning("Brakujący folder", "Wybierz folder końcowy.")
            return

        stage_text = self.stage_var.get().strip()
        if not stage_text.isdigit() or int(stage_text) < 1 or int(stage_text) > 3:
            messagebox.showwarning("Nieprawidłowy etap", "Etap powinien być wartością całkowitą z przedziału [1,3].")
            return
        stage = int(stage_text)

        output_dir.mkdir(parents=True, exist_ok=True)

        self.run_btn.config(state="disabled")
        self.progress.start(12)
        self.status_var.set("Dzielenie pliku...")

        # Run in a background thread so the window doesn't freeze
        threading.Thread(
            target=self._worker, args=(input_path, output_dir, stage), daemon=True
        ).start()
        self.after(100, self._poll)

    def _worker(self, input_path: Path, output_dir: Path, stage: int):
        try:
            files = process(
                input_path,
                output_dir,
                stage,
                report=lambda m: self.messages.put(("status", m)),
            )
            self.messages.put(("done", files))
        except ValueError as e:
            self.messages.put(("error", str(e)))
        except PdfReadError:
            self.messages.put(("error", "Nie udało się otworzyć pliku."))
        except PermissionError:
            self.messages.put(("error", "Nie można zapisać plików do wybranego folderu. Wybierz inny folder końcowy."))
        except Exception as e:  # last resort: don't show a raw traceback to users
            self.messages.put(("error", f"Coś poszło nie tak: {e}"))

    def _poll(self):
        """Check for messages from the worker thread (runs on the UI thread)."""
        finished = False
        try:
            while True:
                kind, payload = self.messages.get_nowait()
                if kind == "status":
                    self.status_var.set(payload)
                elif kind == "done":
                    self._on_done(payload)
                    finished = True
                elif kind == "error":
                    self._on_error(payload)
                    finished = True
        except queue.Empty:
            pass

        if not finished:
            self.after(100, self._poll)

    def _on_done(self, files):
        self._reset_controls()
        self.status_var.set(f"Gotowe! Utworzono {len(files)} plików.")
        messagebox.showinfo("Gotowe", "Gotowe!")

    def _on_error(self, message):
        self._reset_controls()
        self.status_var.set("Błąd.")
        messagebox.showerror("Błąd", message)

    def _reset_controls(self):
        self.progress.stop()
        self.run_btn.config(state="normal")


if __name__ == "__main__":
    print("starting app")
    App().mainloop()