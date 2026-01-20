import tkinter as tk
from tkinter import ttk, messagebox


class ElectronicsToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geminiano's Electroliter")
        self.root.geometry("650x750")

        style = ttk.Style()
        style.theme_use("default")

        # --- Notebook Tabs ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Circuit Calculator")
        self.notebook.add(self.tab2, text="Resistor Color Code")
        self.notebook.add(self.tab3, text="Ohm's & Kirchhoff's Laws")

        # --- Setup Tabs ---
        self.setup_circuit_tab()
        self.setup_color_tab()
        self.setup_laws_tab()

    # =====================================================
    # TAB 1: SERIES / PARALLEL CALCULATOR
    # =====================================================
    def setup_circuit_tab(self):
        frame = self.tab1

        # Component Type
        type_frame = ttk.LabelFrame(frame, text="Component Type")
        type_frame.pack(fill="x", padx=10, pady=5)

        self.comp_type_var = tk.StringVar(value="R")
        ttk.Radiobutton(type_frame, text="Resistors (Ω)",
                        variable=self.comp_type_var, value="R").pack(anchor="w")
        ttk.Radiobutton(type_frame, text="Capacitors (F / µF)",
                        variable=self.comp_type_var, value="C").pack(anchor="w")

        # Configuration
        config_frame = ttk.LabelFrame(frame, text="Configuration")
        config_frame.pack(fill="x", padx=10, pady=5)

        self.config_var = tk.StringVar(value="Series")
        ttk.Radiobutton(config_frame, text="Series",
                        variable=self.config_var, value="Series").pack(anchor="w")
        ttk.Radiobutton(config_frame, text="Parallel",
                        variable=self.config_var, value="Parallel").pack(anchor="w")

        # Add Values
        val_frame = ttk.LabelFrame(frame, text="Add Values")
        val_frame.pack(fill="both", expand=True, padx=10, pady=5)

        row = ttk.Frame(val_frame)
        row.pack(fill="x", pady=5)

        ttk.Label(row, text="Value:").pack(side="left")
        self.val_entry = ttk.Entry(row, width=15)
        self.val_entry.pack(side="left", padx=5)
        self.val_entry.bind("<Return>", lambda e: self.add_value())

        ttk.Button(row, text="Add", command=self.add_value).pack(side="left")
        ttk.Button(row, text="Clear", command=self.clear_list).pack(side="right")

        self.val_listbox = tk.Listbox(val_frame, height=6)
        self.val_listbox.pack(fill="x", padx=5, pady=5)

        ttk.Button(frame, text="CALCULATE", command=self.calculate_circuit).pack(pady=10)

        self.lbl_circuit_result = ttk.Label(frame, text="Equivalent Value: ---",
                                            font=("Arial", 12, "bold"))
        self.lbl_circuit_result.pack()

    def add_value(self):
        try:
            val = float(self.val_entry.get())
            self.val_listbox.insert(tk.END, val)
            self.val_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid number")

    def clear_list(self):
        self.val_listbox.delete(0, tk.END)
        self.lbl_circuit_result.config(text="Equivalent Value: ---")

    def calculate_circuit(self):
        values = list(self.val_listbox.get(0, tk.END))
        if not values:
            messagebox.showwarning("No Values", "Add values first")
            return

        comp = self.comp_type_var.get()
        cfg = self.config_var.get()
        use_recip = (comp == "R" and cfg == "Parallel") or (comp == "C" and cfg == "Series")

        try:
            if use_recip:
                result = 1 / sum(1 / v for v in values)
            else:
                result = sum(values)

            unit = "Ω" if comp == "R" else "F / µF"
            self.lbl_circuit_result.config(text=f"Equivalent Value: {result:.4f} {unit}")
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero")

    # =====================================================
    # TAB 2: RESISTOR COLOR CODE
    # =====================================================
    def setup_color_tab(self):
        frame = self.tab2

        # Data
        self.colors = ["Black", "Brown", "Red", "Orange", "Yellow",
                       "Green", "Blue", "Violet", "Gray", "White"]
        self.color_map = {c: i for i, c in enumerate(self.colors)}
        self.multiplier_map = {c: 10 ** i for i, c in enumerate(self.colors)}
        self.multiplier_map.update({"Gold": 0.1, "Silver": 0.01})
        self.tolerance_map = {
            "Brown": 1, "Red": 2, "Green": 0.5,
            "Blue": 0.25, "Violet": 0.1, "Gray": 0.05,
            "Gold": 5, "Silver": 10
        }

        # Mode Selector
        mode_frame = ttk.LabelFrame(frame, text="Resistor Bands")
        mode_frame.pack(fill="x", padx=10, pady=5)
        self.band_mode = tk.IntVar(value=4)
        ttk.Radiobutton(mode_frame, text="4-Band", variable=self.band_mode, value=4,
                        command=self.toggle_band_mode).pack(side="left", padx=10)
        ttk.Radiobutton(mode_frame, text="5-Band", variable=self.band_mode, value=5,
                        command=self.toggle_band_mode).pack(side="left", padx=10)

        # Input Grid
        grid = ttk.Frame(frame)
        grid.pack(padx=10, pady=5)
        self.band1 = tk.StringVar()
        self.band2 = tk.StringVar()
        self.band3 = tk.StringVar()
        self.mult = tk.StringVar()
        self.tol = tk.StringVar()

        def add_row(row, text, options, var):
            ttk.Label(grid, text=text).grid(row=row, column=0, sticky="w", pady=4)
            cb = ttk.Combobox(grid, values=options, state="readonly", textvariable=var)
            cb.grid(row=row, column=1, padx=10)
            cb.current(0)
            return cb

        self.cb_b1 = add_row(0, "1st Band (Digit)", self.colors, self.band1)
        self.cb_b2 = add_row(1, "2nd Band (Digit)", self.colors, self.band2)
        self.cb_b3 = add_row(2, "3rd Band (Digit)", self.colors, self.band3)
        self.cb_mult = add_row(3, "Multiplier", list(self.multiplier_map.keys()), self.mult)
        self.cb_tol = add_row(4, "Tolerance", list(self.tolerance_map.keys()), self.tol)

        ttk.Button(frame, text="CALCULATE RESISTANCE", command=self.calculate_resistor).pack(pady=8)

        self.lbl_res = ttk.Label(frame, text="Resistance: ---", font=("Arial", 12, "bold"),
                                 foreground="darkgreen")
        self.lbl_res.pack()

        # Cheat Sheet
        cheat = ttk.LabelFrame(frame, text="Resistor Color Code Cheat Sheet")
        cheat.pack(fill="both", expand=True, padx=10, pady=8)

        columns = ("Color", "Digit", "Multiplier", "Tolerance")
        tree = ttk.Treeview(cheat, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
        tree.pack(fill="both", expand=True)

        for c in self.colors:
            tree.insert("", "end", values=(c, self.color_map[c], f"x10^{self.color_map[c]}", self.tolerance_map.get(c, "—")))
        tree.insert("", "end", values=("Gold", "—", "x0.1", "5"))
        tree.insert("", "end", values=("Silver", "—", "x0.01", "10"))

        self.toggle_band_mode()  # initial setup

    def toggle_band_mode(self):
        if self.band_mode.get() == 4:
            self.cb_b3.grid_remove()
        else:
            self.cb_b3.grid()

    def calculate_resistor(self):
        try:
            d1 = self.color_map[self.band1.get()]
            d2 = self.color_map[self.band2.get()]
            if self.band_mode.get() == 5:
                d3 = self.color_map[self.band3.get()]
                base = d1 * 100 + d2 * 10 + d3
            else:
                base = d1 * 10 + d2

            value = base * self.multiplier_map[self.mult.get()]
            tol = self.tolerance_map[self.tol.get()]

            if value >= 1_000_000:
                disp = f"{value / 1_000_000:.2f} MΩ"
            elif value >= 1_000:
                disp = f"{value / 1_000:.2f} kΩ"
            else:
                disp = f"{value:.2f} Ω"

            self.lbl_res.config(text=f"Resistance: {disp} ±{tol}%")
        except Exception:
            messagebox.showerror("Error", "Invalid band selection")

    # =====================================================
    # TAB 3: OHM'S & KIRCHHOFF'S LAWS
    # =====================================================
    def setup_laws_tab(self):
        frame = self.tab3

        ttk.Label(frame, text="Ohm's Law", font=("Arial", 13, "bold")).pack(pady=5)
        form = ttk.Frame(frame)
        form.pack()

        self.v = ttk.Entry(form, width=10)
        self.i = ttk.Entry(form, width=10)
        self.r = ttk.Entry(form, width=10)

        ttk.Label(form, text="Voltage (V)").grid(row=0, column=0)
        ttk.Label(form, text="Current (A)").grid(row=1, column=0)
        ttk.Label(form, text="Resistance (Ω)").grid(row=2, column=0)

        self.v.grid(row=0, column=1)
        self.i.grid(row=1, column=1)
        self.r.grid(row=2, column=1)

        self.lbl_ohm = ttk.Label(frame, text="Result: ---")
        self.lbl_ohm.pack(pady=5)

        def calc_ohm():
            try:
                v = float(self.v.get()) if self.v.get() else None
                i = float(self.i.get()) if self.i.get() else None
                r = float(self.r.get()) if self.r.get() else None

                if [v, i, r].count(None) != 1:
                    raise ValueError

                if v is None:
                    self.lbl_ohm.config(text=f"Voltage = {i * r:.4f} V")
                elif i is None:
                    self.lbl_ohm.config(text=f"Current = {v / r:.4f} A")
                else:
                    self.lbl_ohm.config(text=f"Resistance = {v / i:.4f} Ω")
            except Exception:
                messagebox.showerror("Error", "Enter exactly two values")

        ttk.Button(frame, text="CALCULATE", command=calc_ohm).pack()

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(frame, text="Kirchhoff's Laws", font=("Arial", 13, "bold")).pack()

        self.kvl = ttk.Entry(frame)
        self.kvl.pack(fill="x", padx=20)
        ttk.Button(frame, text="Check KVL",
                   command=lambda: self.check_sum(self.kvl, "V")).pack()

        self.kcl = ttk.Entry(frame)
        self.kcl.pack(fill="x", padx=20)
        ttk.Button(frame, text="Check KCL",
                   command=lambda: self.check_sum(self.kcl, "A")).pack()

        self.lbl_k = ttk.Label(frame, text="Result: ---")
        self.lbl_k.pack(pady=5)

    def check_sum(self, entry, unit):
        try:
            total = sum(float(v.strip()) for v in entry.get().split(","))
            if abs(total) < 1e-6:
                self.lbl_k.config(text=f"✔ Law satisfied (Σ = 0 {unit})")
            else:
                self.lbl_k.config(text=f"✖ Σ = {total:.4f} {unit}")
        except Exception:
            messagebox.showerror("Error", "Invalid input")


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectronicsToolApp(root)
    root.mainloop()
