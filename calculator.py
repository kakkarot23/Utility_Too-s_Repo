import tkinter as tk
from tkinter import ttk
import math
import ast
import re

# Theme specifications
THEMES = {
    "Cyberpunk Neon": {
        "bg": "#120E2E",
        "display_bg": "#1B143F",
        "text": "#E0E0FF",
        "text_secondary": "#B388FF",
        "num_bg": "#261C5B",
        "num_fg": "#00FFFF",
        "num_hover": "#3D2B8C",
        "op_bg": "#3D1054",
        "op_fg": "#FF007F",
        "op_hover": "#5C1680",
        "spec_bg": "#FF007F",
        "spec_fg": "#FFFFFF",
        "spec_hover": "#FF3399",
        "accent": "#00FFFF",
        "sidebar_bg": "#151035",
        "grid_color": "#2A205A",
        "active_fg": "#FFFFFF"
    },
    "Deep Ocean": {
        "bg": "#0B132B",
        "display_bg": "#1C2541",
        "text": "#FFFFFF",
        "text_secondary": "#5BC0BE",
        "num_bg": "#1C2541",
        "num_fg": "#FFFFFF",
        "num_hover": "#2A375E",
        "op_bg": "#0B132B",
        "op_fg": "#5BC0BE",
        "op_hover": "#1C2541",
        "spec_bg": "#5BC0BE",
        "spec_fg": "#0B132B",
        "spec_hover": "#6FFFE9",
        "accent": "#6FFFE9",
        "sidebar_bg": "#0F1935",
        "grid_color": "#243763",
        "active_fg": "#0B132B"
    },
    "Sakura Blossom": {
        "bg": "#FFF0F5",
        "display_bg": "#FFE4E1",
        "text": "#4A2E35",
        "text_secondary": "#D06A80",
        "num_bg": "#FFE4E1",
        "num_fg": "#4A2E35",
        "num_hover": "#FFD1DC",
        "op_bg": "#FFF0F5",
        "op_fg": "#D06A80",
        "op_hover": "#FFE4E1",
        "spec_bg": "#FF82AB",
        "spec_fg": "#FFFFFF",
        "spec_hover": "#FFB7C5",
        "accent": "#D06A80",
        "sidebar_bg": "#FFF5F7",
        "grid_color": "#FFD1DC",
        "active_fg": "#FFFFFF"
    },
    "Retro Terminal": {
        "bg": "#0D1117",
        "display_bg": "#070A0E",
        "text": "#58A6FF",
        "text_secondary": "#8B949E",
        "num_bg": "#161B22",
        "num_fg": "#C9D1D9",
        "num_hover": "#21262D",
        "op_bg": "#161B22",
        "op_fg": "#58A6FF",
        "op_hover": "#21262D",
        "spec_bg": "#2EA043",
        "spec_fg": "#FFFFFF",
        "spec_hover": "#3FB950",
        "accent": "#58A6FF",
        "sidebar_bg": "#161B22",
        "grid_color": "#21262D",
        "active_fg": "#FFFFFF"
    }
}

class HoverButton(tk.Button):
    """Custom flat button with smooth color transition on hover."""
    def __init__(self, master, normal_bg, hover_bg, active_bg, normal_fg, hover_fg, active_fg, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.normal_fg = normal_fg
        self.hover_fg = hover_fg
        self.active_fg = active_fg
        
        self.configure(
            bg=self.normal_bg,
            fg=self.normal_fg,
            activebackground=self.active_bg,
            activeforeground=self.active_fg,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.fade_job = None
        
    def on_enter(self, event):
        self.configure(fg=self.hover_fg)
        self.animate_bg(self.hover_bg)
        
    def on_leave(self, event):
        self.configure(fg=self.normal_fg)
        self.animate_bg(self.normal_bg)

    def animate_bg(self, target_color):
        if self.fade_job:
            self.after_cancel(self.fade_job)
            self.fade_job = None
        self.fade_step(self.cget("bg"), target_color, 0, 6)

    def fade_step(self, current_hex, target_hex, step, total_steps):
        if step > total_steps:
            self.configure(bg=target_hex)
            return
        
        try:
            r1, g1, b1 = self.master.winfo_rgb(current_hex)
            r2, g2, b2 = self.master.winfo_rgb(target_hex)
            
            # Map 16-bit to 8-bit color space
            r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
            r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256
            
            r = int(r1 + (r2 - r1) * (step / total_steps))
            g = int(g1 + (g2 - g1) * (step / total_steps))
            b = int(b1 + (b2 - b1) * (step / total_steps))
            
            next_color = f"#{r:02x}{g:02x}{b:02x}"
            self.configure(bg=next_color)
            
            self.fade_job = self.after(15, lambda: self.fade_step(next_color, target_hex, step + 1, total_steps))
        except Exception:
            self.configure(bg=target_hex)

    def update_colors(self, normal_bg, hover_bg, active_bg, normal_fg, hover_fg, active_fg):
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.normal_fg = normal_fg
        self.hover_fg = hover_fg
        self.active_fg = active_fg
        self.configure(
            bg=self.normal_bg,
            fg=self.normal_fg,
            activebackground=self.active_bg,
            activeforeground=self.active_fg
        )


def make_eval_namespace(deg_mode=True):
    """Create custom math namespace resolving DEG/RAD appropriately."""
    import math
    
    def sin_val(x):
        return math.sin(math.radians(x) if deg_mode else x)
        
    def cos_val(x):
        return math.cos(math.radians(x) if deg_mode else x)
        
    def tan_val(x):
        rad = math.radians(x) if deg_mode else x
        # Handle undefined asymptotes (tan of 90 deg / pi/2 rad)
        if math.isclose(math.cos(rad), 0, abs_tol=1e-9):
            raise ValueError("Undefined Tangent")
        return math.tan(rad)
        
    def asin_val(x):
        val = math.asin(x)
        return math.degrees(val) if deg_mode else val
        
    def acos_val(x):
        val = math.acos(x)
        return math.degrees(val) if deg_mode else val
        
    def atan_val(x):
        val = math.atan(x)
        return math.degrees(val) if deg_mode else val

    def log_val(x):
        if x <= 0:
            raise ValueError("Log domain error")
        return math.log10(x)

    def ln_val(x):
        if x <= 0:
            raise ValueError("Ln domain error")
        return math.log(x)

    def sqrt_val(x):
        if x < 0:
            raise ValueError("Sqrt domain error")
        return math.sqrt(x)

    def factorial_val(x):
        if x < 0 or not float(x).is_integer():
            raise ValueError("Factorial domain error")
        return math.factorial(int(x))

    return {
        'sin': sin_val,
        'cos': cos_val,
        'tan': tan_val,
        'asin': asin_val,
        'acos': acos_val,
        'atan': atan_val,
        'log': log_val,
        'ln': ln_val,
        'sqrt': sqrt_val,
        'fact': factorial_val,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'round': round,
        'math': math
    }


class SafeEvaluator:
    """AST-based mathematical expression parser to avoid arbitrary code execution."""
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,
        ast.Name,
        ast.Call,
        ast.Load,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.USub, ast.UAdd
    }
    
    # Dynamically support legacy ast.Num if present in current python version
    if hasattr(ast, "Num"):
        ALLOWED_NODES.add(ast.Num)
    
    def __init__(self, namespace):
        self.namespace = namespace
        
    def evaluate(self, expr_str):
        # Human math translation replacements
        expr_str = expr_str.replace('^', '**')
        expr_str = expr_str.replace('×', '*')
        expr_str = expr_str.replace('÷', '/')
        expr_str = expr_str.replace('π', 'pi')
        
        # Parse expression to AST
        tree = ast.parse(expr_str, mode='eval')
        
        # Verify node security
        for node in ast.walk(tree):
            if type(node) not in self.ALLOWED_NODES:
                raise TypeError(f"Operation {type(node).__name__} is restricted")
            if isinstance(node, ast.Name):
                if node.id not in self.namespace:
                    raise NameError(f"Undefined identifier: {node.id}")
                    
        code = compile(tree, '<string>', 'eval')
        return eval(code, {"__builtins__": {}}, self.namespace)


class SmarCalcApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmarCalc — Captivating Scientific Calculator")
        self.geometry("450x640")
        self.resizable(False, False)
        
        self.current_theme_name = "Cyberpunk Neon"
        self.theme = THEMES[self.current_theme_name]
        
        self.deg_mode = True
        self.history = []
        
        # Sidebar state (collapsed initially)
        self.sidebar_open = False
        self.current_sidebar_tab = "Graph"
        
        # Constants database
        self.constants = [
            {"name": "Speed of Light", "symbol": "c", "value": "299792458", "unit": "m/s"},
            {"name": "Planck Constant", "symbol": "h", "value": "6.62607015e-34", "unit": "J·s"},
            {"name": "Gravitational Const", "symbol": "G", "value": "6.67430e-11", "unit": "m³/kg·s²"},
            {"name": "Avogadro Number", "symbol": "N_A", "value": "6.02214076e23", "unit": "mol⁻¹"},
            {"name": "Boltzmann Constant", "symbol": "k_B", "value": "1.380649e-23", "unit": "J/K"},
            {"name": "Electron Charge", "symbol": "e_q", "value": "1.602176634e-19", "unit": "C"},
            {"name": "Electron Mass", "symbol": "m_e", "value": "9.1093837e-31", "unit": "kg"},
            {"name": "Gas Constant", "symbol": "R", "value": "8.314462618", "unit": "J/mol·K"}
        ]
        
        # Graph bounds
        self.xmin, self.xmax = -10.0, 10.0
        self.ymin, self.ymax = -10.0, 10.0
        self.canvas_w, self.canvas_h = 330, 360
        
        # Setup modern ttk styles for combos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Layout container
        self.main_container = tk.Frame(self, bg=self.theme["bg"])
        self.main_container.pack(fill="both", expand=True)
        
        # Left Panel (Calculator Pane)
        self.calc_pane = tk.Frame(self.main_container, bg=self.theme["bg"], width=450)
        self.calc_pane.pack(side="left", fill="both")
        
        # Right Panel (Sidebar Pane)
        self.sidebar_pane = tk.Frame(self.main_container, bg=self.theme["sidebar_bg"], width=350)
        # Packed dynamically when sidebar toggles
        
        self.build_calc_ui()
        self.build_sidebar_ui()
        self.apply_theme()
        
        # Bind keyboard shortcuts
        self.bind_keys()
        
    def build_calc_ui(self):
        # Header Controls
        header = tk.Frame(self.calc_pane, bg=self.theme["bg"], height=40)
        header.pack(fill="x", padx=15, pady=(15, 5))
        header.pack_propagate(False)
        
        self.app_title = tk.Label(
            header, text="SmarCalc", font=("Segoe UI", 16, "bold"),
            bg=self.theme["bg"], fg=self.theme["accent"]
        )
        self.app_title.pack(side="left")
        
        # Theme dropdown
        self.theme_var = tk.StringVar(value=self.current_theme_name)
        theme_combo = ttk.Combobox(
            header, textvariable=self.theme_var, values=list(THEMES.keys()),
            state="readonly", width=14
        )
        theme_combo.pack(side="right", padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_select)
        
        # Sidebar togglers
        self.toggle_btn = HoverButton(
            header, text="☰ Tools", font=("Segoe UI", 9, "bold"),
            normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
            normal_fg=self.theme["accent"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=self.toggle_sidebar, width=8, height=1
        )
        self.toggle_btn.pack(side="right", padx=5)
        
        # Displays Frame
        displays = tk.Frame(self.calc_pane, bg=self.theme["display_bg"], relief="flat", bd=0)
        displays.pack(fill="x", padx=15, pady=10)
        
        # Expression formula bar
        self.expr_var = tk.StringVar()
        self.expr_entry = tk.Entry(
            displays, textvariable=self.expr_var, font=("Consolas", 14),
            bg=self.theme["display_bg"], fg=self.theme["text_secondary"],
            bd=0, highlightthickness=0, insertbackground=self.theme["text"]
        )
        self.expr_entry.pack(fill="x", padx=15, pady=(15, 2))
        self.expr_entry.focus()
        
        # Large results label
        self.result_var = tk.StringVar(value="0")
        self.result_label = tk.Label(
            displays, textvariable=self.result_var, font=("Segoe UI", 28, "bold"),
            bg=self.theme["display_bg"], fg=self.theme["text"], anchor="e"
        )
        self.result_label.pack(fill="x", padx=15, pady=(2, 15))
        
        # Status Bar (Deg/Rad)
        self.status_frame = tk.Frame(self.calc_pane, bg=self.theme["bg"])
        self.status_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        self.mode_label = tk.Label(
            self.status_frame, text="DEG", font=("Segoe UI", 8, "bold"),
            bg=self.theme["num_bg"], fg=self.theme["accent"], padx=6, pady=2
        )
        self.mode_label.pack(side="left")
        
        # Keypad Layout
        # Buttons are defined as (text, row, col, type, [action])
        # Types: 'num' (numbers, variables), 'op' (standard operations), 'spec' (eval, backspace, clear)
        buttons_def = [
            # Row 0
            ("DEG/RAD", 0, 0, "op", self.toggle_deg_rad),
            ("C", 0, 1, "spec", self.clear_expr),
            ("⌫", 0, 2, "spec", self.backspace_expr),
            ("(", 0, 3, "op", lambda: self.insert_text("(")),
            (")", 0, 4, "op", lambda: self.insert_text(")")),
            ("^", 0, 5, "op", lambda: self.insert_text("^")),
            
            # Row 1
            ("sin", 1, 0, "op", lambda: self.insert_text("sin(")),
            ("cos", 1, 1, "op", lambda: self.insert_text("cos(")),
            ("tan", 1, 2, "op", lambda: self.insert_text("tan(")),
            ("7", 1, 3, "num", lambda: self.insert_text("7")),
            ("8", 1, 4, "num", lambda: self.insert_text("8")),
            ("9", 1, 5, "num", lambda: self.insert_text("9")),
            
            # Row 2
            ("asin", 2, 0, "op", lambda: self.insert_text("asin(")),
            ("acos", 2, 1, "op", lambda: self.insert_text("acos(")),
            ("atan", 2, 2, "op", lambda: self.insert_text("atan(")),
            ("4", 2, 3, "num", lambda: self.insert_text("4")),
            ("5", 2, 4, "num", lambda: self.insert_text("5")),
            ("6", 2, 5, "num", lambda: self.insert_text("6")),
            
            # Row 3
            ("log", 3, 0, "op", lambda: self.insert_text("log(")),
            ("ln", 3, 1, "op", lambda: self.insert_text("ln(")),
            ("sqrt", 3, 2, "op", lambda: self.insert_text("sqrt(")),
            ("1", 3, 3, "num", lambda: self.insert_text("1")),
            ("2", 3, 4, "num", lambda: self.insert_text("2")),
            ("3", 3, 5, "num", lambda: self.insert_text("3")),
            
            # Row 4
            ("π", 4, 0, "num", lambda: self.insert_text("π")),
            ("e", 4, 1, "num", lambda: self.insert_text("e")),
            ("!", 4, 2, "op", lambda: self.insert_text("fact(")),
            ("0", 4, 3, "num", lambda: self.insert_text("0")),
            (".", 4, 4, "num", lambda: self.insert_text(".")),
            ("=", 4, 5, "spec", self.evaluate_expr),
            
            # Row 5
            ("÷", 5, 0, "op", lambda: self.insert_text("÷")),
            ("×", 5, 1, "op", lambda: self.insert_text("×")),
            ("-", 5, 2, "op", lambda: self.insert_text("-")),
            ("+", 5, 3, "op", lambda: self.insert_text("+")),
            ("%", 5, 4, "op", lambda: self.insert_text("%")),
            ("mod", 5, 5, "op", lambda: self.insert_text(" % "))
        ]
        
        self.keypad_frame = tk.Frame(self.calc_pane, bg=self.theme["bg"])
        self.keypad_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Configure columns/rows weight
        for i in range(6):
            self.keypad_frame.columnconfigure(i, weight=1)
        for i in range(6):
            self.keypad_frame.rowconfigure(i, weight=1)
            
        self.buttons = {}
        for btn_def in buttons_def:
            text, r, c, b_type, action = btn_def
            
            # Determine color set based on type
            if b_type == "num":
                nbg, hbg, abg = self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"]
                nfg, hfg, afg = self.theme["num_fg"], self.theme["active_fg"], self.theme["active_fg"]
            elif b_type == "op":
                nbg, hbg, abg = self.theme["op_bg"], self.theme["op_hover"], self.theme["num_hover"]
                nfg, hfg, afg = self.theme["op_fg"], self.theme["active_fg"], self.theme["active_fg"]
            else:  # spec
                nbg, hbg, abg = self.theme["spec_bg"], self.theme["spec_hover"], self.theme["num_hover"]
                nfg, hfg, afg = self.theme["spec_fg"], self.theme["active_fg"], self.theme["active_fg"]
                
            btn = HoverButton(
                self.keypad_frame, text=text, font=("Segoe UI", 12, "bold"),
                normal_bg=nbg, hover_bg=hbg, active_bg=abg,
                normal_fg=nfg, hover_fg=hfg, active_fg=afg,
                command=action
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
            self.buttons[text] = btn

    def build_sidebar_ui(self):
        # Sidebar tabs switcher
        self.sidebar_header = tk.Frame(self.sidebar_pane, bg=self.theme["sidebar_bg"], height=40)
        self.sidebar_header.pack(fill="x", padx=10, pady=(15, 5))
        self.sidebar_header.pack_propagate(False)
        
        tabs = [("Graph", "📈"), ("Convert", "🔄"), ("Const", "⚛"), ("History", "📜")]
        self.tab_buttons = {}
        
        for name, icon in tabs:
            btn = HoverButton(
                self.sidebar_header, text=f"{icon} {name}", font=("Segoe UI", 8, "bold"),
                normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
                normal_fg=self.theme["text_secondary"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
                command=lambda n=name: self.switch_sidebar_tab(n)
            )
            btn.pack(side="left", fill="both", expand=True, padx=1)
            self.tab_buttons[name] = btn
            
        # Display Panel Container
        self.sidebar_content = tk.Frame(self.sidebar_pane, bg=self.theme["sidebar_bg"])
        self.sidebar_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Build individual tabs
        self.build_graph_tab()
        self.build_convert_tab()
        self.build_constants_tab()
        self.build_history_tab()
        
    def build_graph_tab(self):
        self.graph_tab_frame = tk.Frame(self.sidebar_content, bg=self.theme["sidebar_bg"])
        
        # Instructions/Controls frame
        ctrl_frame = tk.Frame(self.graph_tab_frame, bg=self.theme["sidebar_bg"])
        ctrl_frame.pack(fill="x", pady=5)
        
        tk.Label(ctrl_frame, text="y = ", font=("Consolas", 12, "bold"), bg=self.theme["sidebar_bg"], fg=self.theme["text"]).pack(side="left")
        
        self.graph_expr_entry = tk.Entry(
            ctrl_frame, font=("Consolas", 12), bg=self.theme["display_bg"], fg=self.theme["text"],
            bd=0, highlightthickness=0, insertbackground=self.theme["text"]
        )
        self.graph_expr_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.graph_expr_entry.insert(0, "sin(x)")
        
        self.plot_btn = HoverButton(
            ctrl_frame, text="Plot", font=("Segoe UI", 9, "bold"),
            normal_bg=self.theme["spec_bg"], hover_bg=self.theme["spec_hover"], active_bg=self.theme["num_bg"],
            normal_fg=self.theme["spec_fg"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=self.draw_graph, width=6
        )
        self.plot_btn.pack(side="right")
        
        # Canvas representation of cartesian plane
        self.graph_canvas = tk.Canvas(
            self.graph_tab_frame, bg=self.theme["display_bg"], width=self.canvas_w, height=self.canvas_h,
            bd=0, highlightthickness=0
        )
        self.graph_canvas.pack(fill="both", expand=True, pady=5)
        
        # Zoom & Reset Controls at the bottom
        btns_frame = tk.Frame(self.graph_tab_frame, bg=self.theme["sidebar_bg"])
        btns_frame.pack(fill="x", pady=(2, 10))
        
        self.zoom_in_btn = HoverButton(
            btns_frame, text="🔍 +", font=("Segoe UI", 9, "bold"),
            normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
            normal_fg=self.theme["text"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=lambda: self.zoom_at(self.canvas_w/2, self.canvas_h/2, 0.7), width=6
        )
        self.zoom_in_btn.pack(side="left", padx=2, expand=True, fill="x")
        
        self.zoom_out_btn = HoverButton(
            btns_frame, text="🔍 -", font=("Segoe UI", 9, "bold"),
            normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
            normal_fg=self.theme["text"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=lambda: self.zoom_at(self.canvas_w/2, self.canvas_h/2, 1.4), width=6
        )
        self.zoom_out_btn.pack(side="left", padx=2, expand=True, fill="x")
        
        self.reset_graph_btn = HoverButton(
            btns_frame, text="Reset", font=("Segoe UI", 9, "bold"),
            normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
            normal_fg=self.theme["text"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=self.reset_graph, width=6
        )
        self.reset_graph_btn.pack(side="left", padx=2, expand=True, fill="x")
        
        # Bind Drag-to-Pan and Scroll-to-Zoom
        self.graph_canvas.bind("<Button-1>", self.start_pan)
        self.graph_canvas.bind("<B1-Motion>", self.drag_pan)
        self.graph_canvas.bind("<MouseWheel>", self.zoom_wheel)
        
        # Error Label
        self.graph_error_lbl = tk.Label(self.graph_tab_frame, text="", font=("Segoe UI", 9, "italic"), bg=self.theme["sidebar_bg"], fg="#FF3333")
        self.graph_error_lbl.pack(fill="x")
        
        # Display by default inside container
        self.graph_tab_frame.pack(fill="both", expand=True)

    def build_convert_tab(self):
        self.convert_tab_frame = tk.Frame(self.sidebar_content, bg=self.theme["sidebar_bg"])
        
        # Unit Categories
        cat_frame = tk.Frame(self.convert_tab_frame, bg=self.theme["sidebar_bg"])
        cat_frame.pack(fill="x", pady=10)
        
        tk.Label(cat_frame, text="Category:", font=("Segoe UI", 10, "bold"), bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"]).pack(anchor="w")
        
        self.conv_categories = {
            "Length": ["Meter (m)", "Kilometer (km)", "Mile (mi)", "Foot (ft)", "Inch (in)"],
            "Mass": ["Kilogram (kg)", "Gram (g)", "Pound (lb)", "Ounce (oz)"],
            "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
            "Angle": ["Degree (°)", "Radian (rad)"]
        }
        
        self.conv_cat_var = tk.StringVar(value="Length")
        self.conv_cat_combo = ttk.Combobox(
            cat_frame, textvariable=self.conv_cat_var, values=list(self.conv_categories.keys()),
            state="readonly"
        )
        self.conv_cat_combo.pack(fill="x", pady=2)
        self.conv_cat_combo.bind("<<ComboboxSelected>>", self.on_conv_cat_change)
        
        # From Frame
        from_frame = tk.Frame(self.convert_tab_frame, bg=self.theme["sidebar_bg"])
        from_frame.pack(fill="x", pady=10)
        
        tk.Label(from_frame, text="From:", font=("Segoe UI", 9, "bold"), bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"]).pack(anchor="w")
        self.conv_from_var = tk.StringVar()
        self.conv_from_combo = ttk.Combobox(from_frame, textvariable=self.conv_from_var, state="readonly")
        self.conv_from_combo.pack(fill="x", pady=2)
        self.conv_from_combo.bind("<<ComboboxSelected>>", lambda e: self.perform_conversion())
        
        self.conv_input_var = tk.StringVar(value="1")
        self.conv_input_entry = tk.Entry(
            from_frame, textvariable=self.conv_input_var, font=("Consolas", 14),
            bg=self.theme["display_bg"], fg=self.theme["text"], bd=0, highlightthickness=0, insertbackground=self.theme["text"]
        )
        self.conv_input_entry.pack(fill="x", pady=5, ipady=5)
        self.conv_input_var.trace_add("write", lambda *args: self.perform_conversion())
        
        # Swap Button
        swap_frame = tk.Frame(self.convert_tab_frame, bg=self.theme["sidebar_bg"])
        swap_frame.pack(fill="x")
        self.swap_units_btn = HoverButton(
            swap_frame, text="⇅ Swap", font=("Segoe UI", 9, "bold"),
            normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
            normal_fg=self.theme["accent"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=self.swap_units, width=10
        )
        self.swap_units_btn.pack(anchor="center")
        
        # To Frame
        to_frame = tk.Frame(self.convert_tab_frame, bg=self.theme["sidebar_bg"])
        to_frame.pack(fill="x", pady=10)
        
        tk.Label(to_frame, text="To:", font=("Segoe UI", 9, "bold"), bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"]).pack(anchor="w")
        self.conv_to_var = tk.StringVar()
        self.conv_to_combo = ttk.Combobox(to_frame, textvariable=self.conv_to_var, state="readonly")
        self.conv_to_combo.pack(fill="x", pady=2)
        self.conv_to_combo.bind("<<ComboboxSelected>>", lambda e: self.perform_conversion())
        
        self.conv_result_var = tk.StringVar(value="1")
        self.conv_result_lbl = tk.Label(
            to_frame, textvariable=self.conv_result_var, font=("Segoe UI", 16, "bold"),
            bg=self.theme["display_bg"], fg=self.theme["accent"], anchor="w"
        )
        self.conv_result_lbl.pack(fill="x", pady=5, ipady=5, padx=5)
        
        # Set initial drop items
        self.on_conv_cat_change(None)

    def build_constants_tab(self):
        self.constants_tab_frame = tk.Frame(self.sidebar_content, bg=self.theme["sidebar_bg"])
        
        # Title
        tk.Label(
            self.constants_tab_frame, text="Physical & Math Constants", font=("Segoe UI", 10, "bold"),
            bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"]
        ).pack(anchor="w", pady=(5, 10))
        
        # Scrollable Canvas
        const_canvas = tk.Canvas(self.constants_tab_frame, bg=self.theme["sidebar_bg"], bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.constants_tab_frame, orient="vertical", command=const_canvas.yview)
        
        self.const_scroll_frame = tk.Frame(const_canvas, bg=self.theme["sidebar_bg"])
        self.const_scroll_frame.bind(
            "<Configure>",
            lambda e: const_canvas.configure(scrollregion=const_canvas.bbox("all"))
        )
        
        const_canvas.create_window((0, 0), window=self.const_scroll_frame, anchor="nw", width=310)
        const_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        const_canvas.pack(side="left", fill="both", expand=True)
        
        # Bind scrolling on mouse hover
        def _on_mousewheel(event):
            const_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        const_canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e) if self.current_sidebar_tab == "Const" else None)
        
        # Populate Constants cards
        for c in self.constants:
            card = tk.Frame(self.const_scroll_frame, bg=self.theme["display_bg"], padx=10, pady=8)
            card.pack(fill="x", pady=4)
            
            lbl_title = tk.Label(card, text=c["name"], font=("Segoe UI", 9, "bold"), bg=self.theme["display_bg"], fg=self.theme["text"])
            lbl_title.pack(anchor="nw")
            
            det_frame = tk.Frame(card, bg=self.theme["display_bg"])
            det_frame.pack(fill="x", pady=(2, 0))
            
            lbl_val = tk.Label(
                det_frame, text=f"{c['symbol']} = {c['value']} {c['unit']}",
                font=("Consolas", 8), bg=self.theme["display_bg"], fg=self.theme["text_secondary"]
            )
            lbl_val.pack(side="left")
            
            btn_ins = HoverButton(
                det_frame, text="Insert", font=("Segoe UI", 7, "bold"),
                normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
                normal_fg=self.theme["accent"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
                command=lambda v=c['value']: self.insert_constant(v), width=6
            )
            btn_ins.pack(side="right")

    def build_history_tab(self):
        self.history_tab_frame = tk.Frame(self.sidebar_content, bg=self.theme["sidebar_bg"])
        
        # Header / Clear Controls
        header = tk.Frame(self.history_tab_frame, bg=self.theme["sidebar_bg"])
        header.pack(fill="x", pady=5)
        
        tk.Label(
            header, text="Calculation History", font=("Segoe UI", 10, "bold"),
            bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"]
        ).pack(side="left", anchor="w")
        
        self.clear_hist_btn = HoverButton(
            header, text="Clear", font=("Segoe UI", 8, "bold"),
            normal_bg=self.theme["num_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
            normal_fg=self.theme["accent"], hover_fg=self.theme["active_fg"], active_fg=self.theme["active_fg"],
            command=self.clear_history, width=6
        )
        self.clear_hist_btn.pack(side="right")
        
        # Scrollable Canvas for History Logs
        self.hist_canvas = tk.Canvas(self.history_tab_frame, bg=self.theme["sidebar_bg"], bd=0, highlightthickness=0)
        hist_scrollbar = ttk.Scrollbar(self.history_tab_frame, orient="vertical", command=self.hist_canvas.yview)
        
        self.hist_scroll_frame = tk.Frame(self.hist_canvas, bg=self.theme["sidebar_bg"])
        self.hist_scroll_frame.bind(
            "<Configure>",
            lambda e: self.hist_canvas.configure(scrollregion=self.hist_canvas.bbox("all"))
        )
        
        self.hist_canvas.create_window((0, 0), window=self.hist_scroll_frame, anchor="nw", width=310)
        self.hist_canvas.configure(yscrollcommand=hist_scrollbar.set)
        
        hist_scrollbar.pack(side="right", fill="y")
        self.hist_canvas.pack(side="left", fill="both", expand=True)
        
        self.update_history_display()

    # --- UI Logic / Tab Switcher ---
    def switch_sidebar_tab(self, tab_name):
        self.current_sidebar_tab = tab_name
        
        # Pack-forget all frames
        self.graph_tab_frame.pack_forget()
        self.convert_tab_frame.pack_forget()
        self.constants_tab_frame.pack_forget()
        self.history_tab_frame.pack_forget()
        
        # Restore desired tab
        if tab_name == "Graph":
            self.graph_tab_frame.pack(fill="both", expand=True)
            self.draw_graph()
        elif tab_name == "Convert":
            self.convert_tab_frame.pack(fill="both", expand=True)
        elif tab_name == "Const":
            self.constants_tab_frame.pack(fill="both", expand=True)
        elif tab_name == "History":
            self.history_tab_frame.pack(fill="both", expand=True)
            self.update_history_display()
            
        # Visual tab highlights
        for name, btn in self.tab_buttons.items():
            if name == tab_name:
                btn.configure(bg=self.theme["accent"], fg=self.theme["active_fg"])
                btn.update_colors(
                    self.theme["accent"], self.theme["accent"], self.theme["op_hover"],
                    self.theme["active_fg"], self.theme["active_fg"], self.theme["active_fg"]
                )
            else:
                btn.configure(bg=self.theme["num_bg"], fg=self.theme["text_secondary"])
                btn.update_colors(
                    self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
                    self.theme["text_secondary"], self.theme["active_fg"], self.theme["active_fg"]
                )

    def toggle_sidebar(self):
        if self.sidebar_open:
            # Collapse
            self.sidebar_pane.pack_forget()
            self.geometry("450x640")
            self.sidebar_open = False
        else:
            # Expand
            self.sidebar_pane.pack(side="right", fill="both", expand=True)
            self.geometry("800x640")
            self.sidebar_open = True
            self.switch_sidebar_tab(self.current_sidebar_tab)

    # --- Calculations Engine ---
    def insert_text(self, text):
        # If display says "Error", clear it first
        if self.result_var.get().startswith("Error"):
            self.result_var.set("0")
            
        curr_pos = self.expr_entry.index(tk.INSERT)
        self.expr_entry.insert(curr_pos, text)
        self.expr_entry.focus()
        
    def clear_expr(self):
        self.expr_var.set("")
        self.result_var.set("0")
        
    def backspace_expr(self):
        if self.result_var.get().startswith("Error"):
            self.result_var.set("0")
            
        curr_pos = self.expr_entry.index(tk.INSERT)
        if curr_pos > 0:
            self.expr_entry.delete(curr_pos - 1, curr_pos)
            
    def toggle_deg_rad(self):
        self.deg_mode = not self.deg_mode
        self.mode_label.configure(text="DEG" if self.deg_mode else "RAD")
        # Recalculate current expression if exists
        if self.expr_var.get():
            self.evaluate_expr()

    def evaluate_expr(self):
        expr = self.expr_var.get().strip()
        if not expr:
            return
            
        # Standard balance validation for parentheses
        open_b = expr.count('(')
        close_b = expr.count(')')
        if open_b > close_b:
            expr += ')' * (open_b - close_b)
            self.expr_var.set(expr)
            
        try:
            ns = make_eval_namespace(deg_mode=self.deg_mode)
            evaluator = SafeEvaluator(ns)
            res = evaluator.evaluate(expr)
            
            # Format float decimals beautifully
            if isinstance(res, float):
                if res.is_integer():
                    res = int(res)
                else:
                    # Truncate to maximum 8 decimals for presentation precision
                    res = round(res, 8)
                    
            res_str = str(res)
            self.result_var.set(res_str)
            
            # Add to history log list
            self.add_history(expr, res_str)
            
        except ZeroDivisionError:
            self.result_var.set("Error: Division by zero")
        except ValueError as ve:
            self.result_var.set(f"Error: {str(ve)}")
        except Exception:
            self.result_var.set("Error: Invalid Syntax")

    def insert_constant(self, val):
        self.insert_text(val)
        
    # --- History Handling ---
    def add_history(self, expr, result):
        # Deduplicate sequential identical entries
        if self.history and self.history[-1] == (expr, result):
            return
        self.history.append((expr, result))
        if len(self.history) > 30: # Limit size
            self.history.pop(0)
        self.update_history_display()
        
    def clear_history(self):
        self.history.clear()
        self.update_history_display()
        
    def update_history_display(self):
        # Clear old rows in canvas frame
        for widget in self.hist_scroll_frame.winfo_children():
            widget.destroy()
            
        if not self.history:
            lbl = tk.Label(
                self.hist_scroll_frame, text="No previous calculations", font=("Segoe UI", 9, "italic"),
                bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"]
            )
            lbl.pack(pady=20)
            return
            
        # Reverse history to show newest on top
        for expr, result in reversed(self.history):
            card = tk.Frame(self.hist_scroll_frame, bg=self.theme["display_bg"], padx=10, pady=8)
            card.pack(fill="x", pady=3)
            
            btn_expr = HoverButton(
                card, text=expr, font=("Consolas", 9), anchor="w",
                normal_bg=self.theme["display_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
                normal_fg=self.theme["text_secondary"], hover_fg=self.theme["accent"], active_fg=self.theme["active_fg"],
                command=lambda e=expr: self.expr_var.set(e)
            )
            btn_expr.pack(fill="x", anchor="w")
            
            btn_res = HoverButton(
                card, text=f"= {result}", font=("Segoe UI", 10, "bold"), anchor="w",
                normal_bg=self.theme["display_bg"], hover_bg=self.theme["num_hover"], active_bg=self.theme["op_hover"],
                normal_fg=self.theme["text"], hover_fg=self.theme["accent"], active_fg=self.theme["active_fg"],
                command=lambda r=result: self.insert_text(r)
            )
            btn_res.pack(fill="x", anchor="w", pady=(2, 0))

    # --- 2D Interactive Function Grapher Engine ---
    def reset_graph(self):
        self.xmin, self.xmax = -10.0, 10.0
        self.ymin, self.ymax = -10.0, 10.0
        self.draw_graph()
        
    def to_screen(self, x, y):
        sx = self.canvas_w * (x - self.xmin) / (self.xmax - self.xmin)
        sy = self.canvas_h * (self.ymax - y) / (self.ymax - self.ymin)
        return sx, sy
        
    def to_math(self, sx, sy):
        mx = self.xmin + (sx / self.canvas_w) * (self.xmax - self.xmin)
        my = self.ymax - (sy / self.canvas_h) * (self.ymax - self.ymin)
        return mx, my

    def draw_graph(self):
        self.graph_canvas.delete("all")
        self.graph_error_lbl.configure(text="")
        
        # Grid steps logic based on bounds size
        span_x = self.xmax - self.xmin
        if span_x <= 0:
            return
            
        # Determine grid step magnitude
        order = math.floor(math.log10(span_x))
        grid_step = 10**order
        if span_x / grid_step < 3:
            grid_step /= 5
        elif span_x / grid_step < 6:
            grid_step /= 2
            
        # Draw dynamic horizontal & vertical grids
        start_x = math.floor(self.xmin / grid_step) * grid_step
        while start_x <= self.xmax:
            sx, _ = self.to_screen(start_x, 0)
            self.graph_canvas.create_line(sx, 0, sx, self.canvas_h, fill=self.theme["grid_color"], width=1)
            # Label
            if not math.isclose(start_x, 0, abs_tol=1e-10):
                self.graph_canvas.create_text(
                    sx, self.canvas_h - 10, text=f"{round(start_x, 4):g}",
                    fill=self.theme["text_secondary"], font=("Segoe UI", 7)
                )
            start_x += grid_step
            
        start_y = math.floor(self.ymin / grid_step) * grid_step
        while start_y <= self.ymax:
            _, sy = self.to_screen(0, start_y)
            self.graph_canvas.create_line(0, sy, self.canvas_w, sy, fill=self.theme["grid_color"], width=1)
            # Label
            if not math.isclose(start_y, 0, abs_tol=1e-10):
                self.graph_canvas.create_text(
                    12, sy, text=f"{round(start_y, 4):g}",
                    fill=self.theme["text_secondary"], font=("Segoe UI", 7), anchor="w"
                )
            start_y += grid_step

        # Draw main axis lines
        sx_axis, sy_axis = self.to_screen(0, 0)
        # Vertical axis line
        if 0 <= sx_axis <= self.canvas_w:
            self.graph_canvas.create_line(sx_axis, 0, sx_axis, self.canvas_h, fill=self.theme["accent"], width=1.5)
        # Horizontal axis line
        if 0 <= sy_axis <= self.canvas_h:
            self.graph_canvas.create_line(0, sy_axis, self.canvas_w, sy_axis, fill=self.theme["accent"], width=1.5)
            
        # Plot equation points
        self.draw_function()
        
    def draw_function(self):
        expr = self.graph_expr_entry.get().strip()
        if not expr:
            return
            
        # Pre-compile variables
        ns = make_eval_namespace(deg_mode=False) # Graphing plotted standard in radians
        
        points = []
        steps = 400
        
        # Parse expressions safely
        for i in range(steps + 1):
            sx = (i / steps) * self.canvas_w
            x_math, _ = self.to_math(sx, 0)
            
            ns['x'] = x_math
            try:
                evaluator = SafeEvaluator(ns)
                y_math = evaluator.evaluate(expr)
                
                if isinstance(y_math, complex):
                    y_math = y_math.real
                if math.isnan(y_math) or math.isinf(y_math):
                    raise ValueError()
                    
                _, sy = self.to_screen(x_math, y_math)
                
                # Check for canvas clipping limits
                if -200 <= sy <= self.canvas_h + 200:
                    points.append((sx, sy))
                else:
                    if len(points) > 1:
                        self.graph_canvas.create_line(points, fill=self.theme["spec_bg"], width=2.5, tags="function")
                    points = []
            except Exception:
                if len(points) > 1:
                    self.graph_canvas.create_line(points, fill=self.theme["spec_bg"], width=2.5, tags="function")
                points = []
                
        if len(points) > 1:
            self.graph_canvas.create_line(points, fill=self.theme["spec_bg"], width=2.5, tags="function")
            
        # Display validation notice
        # Test math parsing once to catch typing errors
        ns['x'] = 1.0
        try:
            evaluator = SafeEvaluator(ns)
            evaluator.evaluate(expr)
        except Exception as ex:
            self.graph_error_lbl.configure(text=f"Formula error: {str(ex)}")

    def start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        
    def drag_pan(self, event):
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        
        math_dx = (dx / self.canvas_w) * (self.xmax - self.xmin)
        math_dy = (dy / self.canvas_h) * (self.ymax - self.ymin)
        
        self.xmin -= math_dx
        self.xmax -= math_dx
        self.ymin += math_dy
        self.ymax += math_dy
        
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.draw_graph()
        
    def zoom_wheel(self, event):
        factor = 0.85 if event.delta > 0 else 1.15
        self.zoom_at(event.x, event.y, factor)
        
    def zoom_at(self, sx, sy, factor):
        # Adjust dimensions focused on current cursor math translation
        mx, my = self.to_math(sx, sy)
        
        self.xmin = mx - (mx - self.xmin) * factor
        self.xmax = mx + (self.xmax - mx) * factor
        self.ymin = my - (my - self.ymin) * factor
        self.ymax = my + (self.ymax - my) * factor
        
        self.draw_graph()

    # --- Unit Converter Logic ---
    def on_conv_cat_change(self, event):
        cat = self.conv_cat_var.get()
        units = self.conv_categories[cat]
        
        self.conv_from_combo.configure(values=units)
        self.conv_to_combo.configure(values=units)
        
        self.conv_from_var.set(units[0])
        self.conv_to_var.set(units[1] if len(units) > 1 else units[0])
        
        self.perform_conversion()
        
    def swap_units(self):
        f = self.conv_from_var.get()
        t = self.conv_to_var.get()
        self.conv_from_var.set(t)
        self.conv_to_var.set(f)
        self.perform_conversion()
        
    def perform_conversion(self):
        cat = self.conv_cat_var.get()
        val_str = self.conv_input_var.get().strip()
        
        if not val_str:
            self.conv_result_var.set("")
            return
            
        try:
            val = float(val_str)
        except ValueError:
            self.conv_result_var.set("Error: Enter numeric input")
            return
            
        from_unit = self.conv_from_var.get()
        to_unit = self.conv_to_var.get()
        
        if from_unit == to_unit:
            self.conv_result_var.set(f"{val_str}")
            return
            
        # Core standard unit mappings
        res = 0.0
        if cat == "Length":
            # Map factors to Meters (base)
            factors = {"Meter (m)": 1.0, "Kilometer (km)": 1000.0, "Mile (mi)": 1609.344, "Foot (ft)": 0.3048, "Inch (in)": 0.0254}
            val_m = val * factors[from_unit]
            res = val_m / factors[to_unit]
            
        elif cat == "Mass":
            # Map factors to Kilograms (base)
            factors = {"Kilogram (kg)": 1.0, "Gram (g)": 0.001, "Pound (lb)": 0.45359237, "Ounce (oz)": 0.028349523}
            val_kg = val * factors[from_unit]
            res = val_kg / factors[to_unit]
            
        elif cat == "Angle":
            # Map to Radians
            if from_unit == "Degree (°)":
                val_rad = math.radians(val)
            else:
                val_rad = val
                
            if to_unit == "Degree (°)":
                res = math.degrees(val_rad)
            else:
                res = val_rad
                
        elif cat == "Temperature":
            # Conversions
            if from_unit == "Celsius (°C)":
                if to_unit == "Fahrenheit (°F)":
                    res = (val * 9/5) + 32
                elif to_unit == "Kelvin (K)":
                    res = val + 273.15
            elif from_unit == "Fahrenheit (°F)":
                if to_unit == "Celsius (°C)":
                    res = (val - 32) * 5/9
                elif to_unit == "Kelvin (K)":
                    res = (val - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin (K)":
                if to_unit == "Celsius (°C)":
                    res = val - 273.15
                elif to_unit == "Fahrenheit (°F)":
                    res = (val - 273.15) * 9/5 + 32
                    
        # Presentation format rounding
        self.conv_result_var.set(f"{round(res, 8):g}")

    # --- Theme Switching Engine ---
    def on_theme_select(self, event):
        self.current_theme_name = self.theme_var.get()
        self.theme = THEMES[self.current_theme_name]
        self.apply_theme()
        
    def apply_theme(self):
        # Update colors on base configurations
        self.main_container.configure(bg=self.theme["bg"])
        self.calc_pane.configure(bg=self.theme["bg"])
        self.sidebar_pane.configure(bg=self.theme["sidebar_bg"])
        
        self.app_title.configure(bg=self.theme["bg"], fg=self.theme["accent"])
        self.expr_entry.configure(bg=self.theme["display_bg"], fg=self.theme["text_secondary"], insertbackground=self.theme["text"])
        self.result_label.configure(bg=self.theme["display_bg"], fg=self.theme["text"])
        self.expr_entry.master.configure(bg=self.theme["display_bg"])
        
        self.status_frame.configure(bg=self.theme["bg"])
        self.mode_label.configure(bg=self.theme["num_bg"], fg=self.theme["accent"])
        self.keypad_frame.configure(bg=self.theme["bg"])
        
        self.sidebar_header.configure(bg=self.theme["sidebar_bg"])
        self.sidebar_content.configure(bg=self.theme["sidebar_bg"])
        
        # Tabs frame
        self.graph_tab_frame.configure(bg=self.theme["sidebar_bg"])
        self.graph_tab_frame.winfo_children()[0].configure(bg=self.theme["sidebar_bg"])  # ctrl_frame
        self.graph_tab_frame.winfo_children()[0].winfo_children()[0].configure(bg=self.theme["sidebar_bg"], fg=self.theme["text"])  # label
        self.graph_expr_entry.configure(bg=self.theme["display_bg"], fg=self.theme["text"], insertbackground=self.theme["text"])
        self.graph_canvas.configure(bg=self.theme["display_bg"])
        self.graph_tab_frame.winfo_children()[2].configure(bg=self.theme["sidebar_bg"])  # btns_frame
        self.graph_error_lbl.configure(bg=self.theme["sidebar_bg"])
        
        self.convert_tab_frame.configure(bg=self.theme["sidebar_bg"])
        for child in self.convert_tab_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self.theme["sidebar_bg"])
                for label in child.winfo_children():
                    if isinstance(label, tk.Label):
                        if label == self.conv_result_lbl:
                            label.configure(bg=self.theme["display_bg"], fg=self.theme["accent"])
                        else:
                            label.configure(bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"])
            
        self.conv_input_entry.configure(bg=self.theme["display_bg"], fg=self.theme["text"], insertbackground=self.theme["text"])
        
        self.constants_tab_frame.configure(bg=self.theme["sidebar_bg"])
        self.constants_tab_frame.winfo_children()[0].configure(bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"])
        const_canvas = self.constants_tab_frame.winfo_children()[1]
        const_canvas.configure(bg=self.theme["sidebar_bg"])
        self.const_scroll_frame.configure(bg=self.theme["sidebar_bg"])
        
        # Re-theme individual cards in scroll frame
        for card in self.const_scroll_frame.winfo_children():
            card.configure(bg=self.theme["display_bg"])
            card.winfo_children()[0].configure(bg=self.theme["display_bg"], fg=self.theme["text"])  # Title
            card.winfo_children()[1].configure(bg=self.theme["display_bg"])  # det_frame
            card.winfo_children()[1].winfo_children()[0].configure(bg=self.theme["display_bg"], fg=self.theme["text_secondary"])  # Label
            card.winfo_children()[1].winfo_children()[1].update_colors(
                self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
                self.theme["accent"], self.theme["active_fg"], self.theme["active_fg"]
            )
            
        # History frame
        self.history_tab_frame.configure(bg=self.theme["sidebar_bg"])
        self.history_tab_frame.winfo_children()[0].configure(bg=self.theme["sidebar_bg"])  # header
        self.history_tab_frame.winfo_children()[0].winfo_children()[0].configure(bg=self.theme["sidebar_bg"], fg=self.theme["text_secondary"])
        self.clear_hist_btn.update_colors(
            self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
            self.theme["accent"], self.theme["active_fg"], self.theme["active_fg"]
        )
        self.hist_canvas.configure(bg=self.theme["sidebar_bg"])
        self.hist_scroll_frame.configure(bg=self.theme["sidebar_bg"])
        self.update_history_display()
        
        # Update tab switcher buttons colors
        for name, btn in self.tab_buttons.items():
            if name == self.current_sidebar_tab:
                btn.update_colors(
                    self.theme["accent"], self.theme["accent"], self.theme["op_hover"],
                    self.theme["active_fg"], self.theme["active_fg"], self.theme["active_fg"]
                )
            else:
                btn.update_colors(
                    self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
                    self.theme["text_secondary"], self.theme["active_fg"], self.theme["active_fg"]
                )
                
        # Main UI Buttons colors
        buttons_defs = {
            "num": ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", ".", "π", "e"],
            "spec": ["C", "⌫", "="],
            # All other buttons are 'op'
        }
        
        for text, btn in self.buttons.items():
            if text in buttons_defs["num"]:
                nbg, hbg, abg = self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"]
                nfg, hfg, afg = self.theme["num_fg"], self.theme["active_fg"], self.theme["active_fg"]
            elif text in buttons_defs["spec"]:
                nbg, hbg, abg = self.theme["spec_bg"], self.theme["spec_hover"], self.theme["num_hover"]
                nfg, hfg, afg = self.theme["spec_fg"], self.theme["active_fg"], self.theme["active_fg"]
            else:
                nbg, hbg, abg = self.theme["op_bg"], self.theme["op_hover"], self.theme["num_hover"]
                nfg, hfg, afg = self.theme["op_fg"], self.theme["active_fg"], self.theme["active_fg"]
            btn.update_colors(nbg, hbg, abg, nfg, hfg, afg)
            
        # Top toggle button update
        self.toggle_btn.update_colors(
            self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
            self.theme["accent"], self.theme["active_fg"], self.theme["active_fg"]
        )
        
        # Plot button update
        self.plot_btn.update_colors(
            self.theme["spec_bg"], self.theme["spec_hover"], self.theme["num_hover"],
            self.theme["spec_fg"], self.theme["active_fg"], self.theme["active_fg"]
        )
        
        # Zoom in/out update
        self.zoom_in_btn.update_colors(
            self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
            self.theme["text"], self.theme["active_fg"], self.theme["active_fg"]
        )
        self.zoom_out_btn.update_colors(
            self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
            self.theme["text"], self.theme["active_fg"], self.theme["active_fg"]
        )
        self.reset_graph_btn.update_colors(
            self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
            self.theme["text"], self.theme["active_fg"], self.theme["active_fg"]
        )
        
        # Swap converter update
        self.swap_units_btn.update_colors(
            self.theme["num_bg"], self.theme["num_hover"], self.theme["op_hover"],
            self.theme["accent"], self.theme["active_fg"], self.theme["active_fg"]
        )

        # Style Comboboxes dropdown lists using themed elements
        self.style.configure(
            "TCombobox", fieldbackground=self.theme["display_bg"], background=self.theme["num_bg"],
            foreground=self.theme["text"], bordercolor=self.theme["grid_color"],
            arrowcolor=self.theme["accent"]
        )
        # Apply dark themes to TCombobox selection lists too
        self.option_add("*TCombobox*Listbox.background", self.theme["display_bg"])
        self.option_add("*TCombobox*Listbox.foreground", self.theme["text"])
        self.option_add("*TCombobox*Listbox.selectBackground", self.theme["accent"])
        self.option_add("*TCombobox*Listbox.selectForeground", self.theme["active_fg"])
        
        # Redraw graph (will apply new colors)
        if self.sidebar_open and self.current_sidebar_tab == "Graph":
            self.draw_graph()

    # --- Keyboard Key Bindings Engine ---
    def bind_keys(self):
        # Digital buttons triggers
        for char in "0123456789.()":
            self.bind(char, lambda e, c=char: self.insert_text(c))
            
        # Operator conversions
        self.bind("+", lambda e: self.insert_text("+"))
        self.bind("-", lambda e: self.insert_text("-"))
        self.bind("*", lambda e: self.insert_text("×"))
        self.bind("/", lambda e: self.insert_text("÷"))
        self.bind("^", lambda e: self.insert_text("^"))
        self.bind("%", lambda e: self.insert_text("%"))
        
        # Functional evaluations
        self.bind("<Return>", lambda e: self.evaluate_expr())
        self.bind("<KP_Enter>", lambda e: self.evaluate_expr())
        self.bind("<BackSpace>", lambda e: self.backspace_expr())
        self.bind("<Escape>", lambda e: self.clear_expr())
        self.bind("<Delete>", lambda e: self.clear_expr())


if __name__ == "__main__":
    # Standard high-DPI scaling check for beautiful crisp fonts on modern Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
        
    app = SmarCalcApp()
    app.mainloop()
