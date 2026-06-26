import tkinter as tk
from tkinter import ttk
import math
import re
from datetime import datetime

class RoundedButton(tk.Canvas):
    """Custom flat button with rounded corners and smooth color transitions on hover."""
    def __init__(self, master, text, radius=8, normal_bg="", hover_bg="", active_bg="", normal_fg="", hover_fg="", active_fg="", command=None, font=("Segoe UI", 10, "bold"), is_selected=False, image=None, *args, **kwargs):
        super().__init__(master, bd=0, highlightthickness=0, cursor="hand2", *args, **kwargs)
        self.text = text
        self.radius = radius
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.normal_fg = normal_fg
        self.hover_fg = hover_fg
        self.active_fg = active_fg
        self.command = command
        self.font = font
        self.is_selected = is_selected
        self.image = image
        
        # Configure self background to match parent
        self.configure(bg=master.cget("bg"))
        
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def set_selected(self, selected):
        """Toggle button selection highlight."""
        self.is_selected = selected
        bg = self.active_bg if self.is_selected else self.normal_bg
        fg = self.active_fg if self.is_selected else self.normal_fg
        self.draw_button(bg, fg)
        
    def on_resize(self, event):
        bg = self.active_bg if self.is_selected else self.normal_bg
        fg = self.active_fg if self.is_selected else self.normal_fg
        self.draw_button(bg, fg)
        
    def draw_button(self, bg, fg):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
            
        r = min(self.radius, w//2, h//2)
        
        # Draw rounded rectangle parts
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, style="pieslice", fill=bg, outline=bg)
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, style="pieslice", fill=bg, outline=bg)
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, style="pieslice", fill=bg, outline=bg)
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, style="pieslice", fill=bg, outline=bg)
        self.create_rectangle(r, 0, w-r, h, fill=bg, outline=bg)
        self.create_rectangle(0, r, w, h-r, fill=bg, outline=bg)
        
        # Draw text and image centered
        if self.image:
            self.create_image(w/2, h/2 - 10, image=self.image)
            self.create_text(w/2, h/2 + 16, text=self.text, fill=fg, font=self.font, justify="center")
        else:
            self.create_text(w/2, h/2, text=self.text, fill=fg, font=self.font, justify="center")
        
    def on_press(self, event):
        self.draw_button(self.active_bg, self.active_fg)
        if self.command:
            self.command()
            
    def on_release(self, event):
        bg = self.hover_bg if self.winfo_containing(event.x_root, event.y_root) == self else self.normal_bg
        fg = self.hover_fg if self.winfo_containing(event.x_root, event.y_root) == self else self.normal_fg
        if self.is_selected:
            bg, fg = self.active_bg, self.active_fg
        self.draw_button(bg, fg)
        
    def on_enter(self, event):
        if not self.is_selected:
            self.draw_button(self.hover_bg, self.hover_fg)
            
    def on_leave(self, event):
        if not self.is_selected:
            self.draw_button(self.normal_bg, self.normal_fg)
            
    def update_colors(self, normal_bg, hover_bg, active_bg, normal_fg, hover_fg, active_fg):
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.normal_fg = normal_fg
        self.hover_fg = hover_fg
        self.active_fg = active_fg
        self.configure(bg=self.master.cget("bg"))
        bg = self.active_bg if self.is_selected else self.normal_bg
        fg = self.active_fg if self.is_selected else self.normal_fg
        self.draw_button(bg, fg)


class SmartMultiCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Multi-Purpose Calculator")
        self.root.geometry("1024x640")
        self.root.resizable(False, False)
        
        self.center_window()
        
        self.current_theme = "dark"
        self.active_module = "Scientific Calculator"
        self.expression = ""
        self.font_scale = 1.0
        self.history_log = []
        
        self.load_themes()
        self.load_icons()
        self.setup_ui_layout()
        self.configure_combo_styles()
        self.rebuild_center()

    def center_window(self):
        self.root.update_idletasks()
        width = 1024
        height = 640
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_themes(self):
        self.themes = {
            "dark": {
                "bg": "#0B0F19",
                "sidebar_bg": "#0F172A",
                "display_bg": "#1E293B",
                "display_fg": "#FFFFFF",
                "btn_num_bg": "#1E293B",
                "btn_num_fg": "#FFFFFF",
                "btn_num_hover": "#334155",
                "btn_num_active": "#475569",
                "btn_op_bg": "#0EA5E9",
                "btn_op_fg": "#FFFFFF",
                "btn_op_hover": "#38BDF8",
                "btn_op_active": "#0284C7",
                "btn_spec_bg": "#475569",
                "btn_spec_fg": "#FFFFFF",
                "btn_spec_hover": "#64748B",
                "btn_spec_active": "#334155",
                "btn_eq_bg": "#10B981",
                "btn_eq_fg": "#FFFFFF",
                "btn_eq_hover": "#34D399",
                "btn_eq_active": "#059669",
            },
            "light": {
                "bg": "#F1F5F9",
                "sidebar_bg": "#E2E8F0",
                "display_bg": "#FFFFFF",
                "display_fg": "#0F172A",
                "btn_num_bg": "#E2E8F0",
                "btn_num_fg": "#0F172A",
                "btn_num_hover": "#CBD5E1",
                "btn_num_active": "#94A3B8",
                "btn_op_bg": "#3B82F6",
                "btn_op_fg": "#FFFFFF",
                "btn_op_hover": "#60A5FA",
                "btn_op_active": "#2563EB",
                "btn_spec_bg": "#CBD5E1",
                "btn_spec_fg": "#0F172A",
                "btn_spec_hover": "#94A3B8",
                "btn_spec_active": "#64748B",
                "btn_eq_bg": "#10B981",
                "btn_eq_fg": "#FFFFFF",
                "btn_eq_hover": "#34D399",
                "btn_eq_active": "#059669",
            }
        }

    def load_icons(self):
        self.icons = {}
        icon_names = [
            "basic", "scientific", "finance", "statistical", "retirement",
            "age", "converter", "health", "history", "settings", "audience", "theme"
        ]
        import os
        icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
        for name in icon_names:
            path = os.path.join(icon_dir, f"{name}.png")
            if os.path.exists(path):
                self.icons[name] = tk.PhotoImage(file=path)
            else:
                self.icons[name] = None

    def setup_ui_layout(self):
        theme = self.themes[self.current_theme]
        
        self.left_sidebar = tk.Frame(self.root, bg=theme["sidebar_bg"], width=75)
        self.left_sidebar.pack(side="left", fill="y")
        self.left_sidebar.pack_propagate(False)
        
        self.right_sidebar = tk.Frame(self.root, bg=theme["sidebar_bg"], width=75)
        self.right_sidebar.pack(side="right", fill="y")
        self.right_sidebar.pack_propagate(False)
        
        self.center_pane = tk.Frame(self.root, bg=theme["bg"])
        self.center_pane.pack(side="left", fill="both", expand=True)
        
        # Stylized Logo Headers (Icons only for narrow layout)
        logo_frame = tk.Frame(self.left_sidebar, bg=theme["sidebar_bg"])
        logo_frame.pack(fill="x", pady=(15, 5))
        tk.Label(logo_frame, text="⚡", font=self.scale_font("Segoe UI", 18, "bold"), bg=theme["sidebar_bg"], fg=theme["btn_op_bg"]).pack()
        
        logo_frame_r = tk.Frame(self.right_sidebar, bg=theme["sidebar_bg"])
        logo_frame_r.pack(fill="x", pady=(15, 5))
        tk.Label(logo_frame_r, text="🌐", font=self.scale_font("Segoe UI", 18, "bold"), bg=theme["sidebar_bg"], fg=theme["btn_op_bg"]).pack()
        
        self.sidebar_buttons = {}
        
        left_btns = [
            ("Basic", "Basic Calculator", self.icons.get("basic")),
            ("Scientific", "Scientific Calculator", self.icons.get("scientific")),
            ("Finance", "Finance", self.icons.get("finance")),
            ("Stats", "Statistical", self.icons.get("statistical")),
            ("Retire", "Retirement Planning", self.icons.get("retirement")),
            ("Age", "Age Calculator", self.icons.get("age"))
        ]
        
        right_btns = [
            ("Units", "Unit Converter", self.icons.get("converter")),
            ("Health", "Health Calculator", self.icons.get("health")),
            ("History", "History", self.icons.get("history")),
            ("Settings", "Settings", self.icons.get("settings")),
            ("Audience", "Target Audience", self.icons.get("audience")),
            ("Theme", "Toggle Theme", self.icons.get("theme"))
        ]
        
        if self.current_theme == "dark":
            sidebar_color_theme = {
                "normal_bg": theme["sidebar_bg"],
                "hover_bg": "#1E293B",
                "active_bg": "#334155",
                "normal_fg": "#94A3B8",
                "hover_fg": "#FFFFFF",
                "active_fg": "#FFFFFF"
            }
        else:
            sidebar_color_theme = {
                "normal_bg": theme["sidebar_bg"],
                "hover_bg": "#CBD5E1",
                "active_bg": "#94A3B8",
                "normal_fg": "#475569",
                "hover_fg": "#0F172A",
                "active_fg": "#0F172A"
            }
        
        for disp, internal, icon in left_btns:
            btn = RoundedButton(
                self.left_sidebar,
                text=disp,
                radius=10,
                font=self.scale_font("Segoe UI", 8, "bold"),
                normal_bg=sidebar_color_theme["normal_bg"],
                hover_bg=sidebar_color_theme["hover_bg"],
                active_bg=sidebar_color_theme["active_bg"],
                normal_fg=sidebar_color_theme["normal_fg"],
                hover_fg=sidebar_color_theme["hover_fg"],
                active_fg=sidebar_color_theme["active_fg"],
                image=icon,
                command=lambda val=internal: self.navigation_click(val),
                height=60
            )
            btn.pack(fill="x", padx=6, pady=4)
            self.sidebar_buttons[internal] = btn
            
        for disp, internal, icon in right_btns:
            btn = RoundedButton(
                self.right_sidebar,
                text=disp,
                radius=10,
                font=self.scale_font("Segoe UI", 8, "bold"),
                normal_bg=sidebar_color_theme["normal_bg"],
                hover_bg=sidebar_color_theme["hover_bg"],
                active_bg=sidebar_color_theme["active_bg"],
                normal_fg=sidebar_color_theme["normal_fg"],
                hover_fg=sidebar_color_theme["hover_fg"],
                active_fg=sidebar_color_theme["active_fg"],
                image=icon,
                command=lambda val=internal: self.navigation_click(val),
                height=60
            )
            btn.pack(fill="x", padx=6, pady=4)
            self.sidebar_buttons[internal] = btn

    def configure_combo_styles(self):
        theme = self.themes[self.current_theme]
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure(
            "TCombobox",
            fieldbackground=theme["display_bg"],
            background=theme["btn_num_bg"],
            foreground=theme["display_fg"],
            arrowcolor=theme["display_fg"],
            bordercolor=theme["bg"],
            lightcolor=theme["bg"],
            darkcolor=theme["bg"]
        )
        
        self.root.option_add("*TCombobox*Listbox.background", theme["display_bg"])
        self.root.option_add("*TCombobox*Listbox.foreground", theme["display_fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", theme["btn_op_bg"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", theme["btn_op_fg"])

    def navigation_click(self, target):
        if target == "Toggle Theme":
            self.toggle_theme()
            return
        
        self.active_module = target
        self.rebuild_center()

    def update_sidebar_highlights(self):
        for name, btn in self.sidebar_buttons.items():
            btn.set_selected(name == self.active_module)

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        theme = self.themes[self.current_theme]
        
        self.left_sidebar.configure(bg=theme["sidebar_bg"])
        self.right_sidebar.configure(bg=theme["sidebar_bg"])
        
        self.left_sidebar.destroy()
        self.right_sidebar.destroy()
        self.center_pane.destroy()
        
        self.setup_ui_layout()
        self.configure_combo_styles()
        self.rebuild_center()

    def get_category_colors(self, category, theme):
        if category == "num":
            return {
                "normal_bg": theme["btn_num_bg"],
                "hover_bg": theme["btn_num_hover"],
                "active_bg": theme["btn_num_active"],
                "normal_fg": theme["btn_num_fg"],
                "hover_fg": theme["btn_num_fg"],
                "active_fg": theme["btn_num_fg"]
            }
        elif category == "op":
            return {
                "normal_bg": theme["btn_op_bg"],
                "hover_bg": theme["btn_op_hover"],
                "active_bg": theme["btn_op_active"],
                "normal_fg": theme["btn_op_fg"],
                "hover_fg": theme["btn_op_fg"],
                "active_fg": theme["btn_op_fg"]
            }
        elif category == "eq":
            return {
                "normal_bg": theme["btn_eq_bg"],
                "hover_bg": theme["btn_eq_hover"],
                "active_bg": theme["btn_eq_active"],
                "normal_fg": theme["btn_eq_fg"],
                "hover_fg": theme["btn_eq_fg"],
                "active_fg": theme["btn_eq_fg"]
            }
        else:  # spec
            return {
                "normal_bg": theme["btn_spec_bg"],
                "hover_bg": theme["btn_spec_hover"],
                "active_bg": theme["btn_spec_active"],
                "normal_fg": theme["btn_spec_fg"],
                "hover_fg": theme["btn_spec_fg"],
                "active_fg": theme["btn_spec_fg"]
            }

    def scale_font(self, font_name, size, weight="normal"):
        return (font_name, int(size * self.font_scale), weight)

    def add_history(self, expression, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_log.append({
            "time": timestamp,
            "expr": expression,
            "res": result
        })

    def draw_center_header(self, title):
        theme = self.themes[self.current_theme]
        lbl = tk.Label(self.center_pane, text=title, font=self.scale_font("Segoe UI", 18, "bold"), bg=theme["bg"], fg=theme["btn_op_bg"])
        lbl.pack(pady=(12, 4))
        divider = tk.Frame(self.center_pane, height=1, bg=theme["btn_num_bg"] if self.current_theme == "dark" else "#CBD5E1")
        divider.pack(fill="x", padx=45, pady=(2, 10))

    def rebuild_center(self):
        for widget in self.center_pane.winfo_children():
            widget.destroy()
            
        theme = self.themes[self.current_theme]
        self.center_pane.configure(bg=theme["bg"])
        
        if self.active_module == "Basic Calculator":
            self.build_basic_calc()
        elif self.active_module == "Scientific Calculator":
            self.build_scientific_calc()
        elif self.active_module == "Finance":
            self.build_finance()
        elif self.active_module == "Statistical":
            self.build_statistical()
        elif self.active_module == "Retirement Planning":
            self.build_retirement()
        elif self.active_module == "Age Calculator":
            self.build_age_calc()
        elif self.active_module == "Unit Converter":
            self.build_unit_conv()
        elif self.active_module == "Health Calculator":
            self.build_health()
        elif self.active_module == "History":
            self.build_history()
        elif self.active_module == "Settings":
            self.build_settings()
        elif self.active_module == "Target Audience":
            self.build_target_audience()
            
        self.update_sidebar_highlights()

    # --- Module: Basic Calculator ---
    def build_basic_calc(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Basic Calculator")
        
        disp_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], height=80, bd=0, relief="flat", highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        disp_frame.pack(fill="x", padx=40, pady=5)
        disp_frame.pack_propagate(False)
        
        self.basic_display = tk.Entry(
            disp_frame,
            font=self.scale_font("Segoe UI", 24, "bold"),
            bg=theme["display_bg"],
            fg=theme["display_fg"],
            bd=0,
            justify="right",
            insertbackground=theme["display_fg"],
            state="readonly"
        )
        self.basic_display.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.expression = ""
        self.update_basic_display("0")
        
        keypad_frame = tk.Frame(self.center_pane, bg=theme["bg"])
        keypad_frame.pack(fill="both", expand=True, padx=40, pady=(5, 20))
        
        buttons_def = [
            ("C", 0, 0, "spec"), ("⌫", 0, 1, "spec"), ("^", 0, 2, "spec"), ("÷", 0, 3, "op"),
            ("7", 1, 0, "num"),  ("8", 1, 1, "num"),  ("9", 1, 2, "num"),  ("×", 1, 3, "op"),
            ("4", 2, 0, "num"),  ("5", 2, 1, "num"),  ("6", 2, 2, "num"),  ("-", 2, 3, "op"),
            ("1", 3, 0, "num"),  ("2", 3, 1, "num"),  ("3", 3, 2, "num"),  ("+", 3, 3, "op"),
            ("√", 4, 0, "spec"), ("0", 4, 1, "num"),  (".", 4, 2, "num"),  ("%", 4, 3, "spec"),
            ("(", 5, 0, "spec"), (")", 5, 1, "spec"), ("=", 5, 2, "eq")
        ]
        
        for i in range(4):
            keypad_frame.columnconfigure(i, weight=1)
        for i in range(6):
            keypad_frame.rowconfigure(i, weight=1)
            
        for text, row, col, category in buttons_def:
            colors = self.get_category_colors(category, theme)
            
            if text == "C":
                cmd = self.clear_basic
            elif text == "⌫":
                cmd = self.backspace_basic
            elif text == "=":
                cmd = self.calculate_basic
            else:
                cmd = lambda val=text: self.basic_click(val)
                
            btn = RoundedButton(
                keypad_frame,
                text=text,
                radius=12,
                font=self.scale_font("Segoe UI", 12, "bold"),
                normal_bg=colors["normal_bg"],
                hover_bg=colors["hover_bg"],
                active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"],
                hover_fg=colors["hover_fg"],
                active_fg=colors["active_fg"],
                command=cmd
            )
            
            if text == "=":
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=3, pady=3)
            else:
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    def basic_click(self, value):
        if self.expression == "Error":
            self.expression = ""
        self.expression += str(value)
        self.update_basic_display(self.expression)

    def clear_basic(self):
        self.expression = ""
        self.update_basic_display("0")

    def backspace_basic(self):
        if self.expression == "Error":
            self.expression = ""
        elif len(self.expression) > 0:
            self.expression = self.expression[:-1]
        self.update_basic_display(self.expression if self.expression else "0")

    def calculate_basic(self):
        if not self.expression or self.expression == "Error":
            return
        orig_expr = self.expression
        try:
            expr = self.expression
            expr = expr.replace("√(", "sqrt(")
            expr = re.sub(r'√([0-9.]+)', r'sqrt(\1)', expr)
            expr = expr.replace("×", "*")
            expr = expr.replace("÷", "/")
            expr = expr.replace("^", "**")
            expr = expr.replace("%", "/100")
            
            check_str = expr.replace("sqrt", "")
            allowed = set("0123456789+-*/.() ")
            for char in check_str:
                if char not in allowed:
                    raise ValueError
                    
            result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt})
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            self.expression = str(result)
            self.update_basic_display(self.expression)
            self.add_history(orig_expr, self.expression)
        except Exception:
            self.expression = "Error"
            self.update_basic_display(self.expression)

    def update_basic_display(self, text):
        self.basic_display.configure(state="normal")
        self.basic_display.delete(0, tk.END)
        self.basic_display.insert(0, text)
        self.basic_display.configure(state="readonly")

    # --- Module: Scientific Calculator ---
    def build_scientific_calc(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Scientific Calculator")
        
        disp_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], height=80, bd=0, relief="flat", highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        disp_frame.pack(fill="x", padx=55, pady=5)
        disp_frame.pack_propagate(False)
        
        self.display_var = tk.StringVar(value="30")
        self.scientific_display = tk.Entry(
            disp_frame,
            textvariable=self.display_var,
            font=self.scale_font("Segoe UI", 24, "bold"),
            bg=theme["display_bg"],
            fg=theme["display_fg"],
            bd=0,
            justify="left"
        )
        self.scientific_display.pack(fill="both", expand=True, padx=15, pady=(10, 2))
        
        self.preview_var = tk.StringVar(value="sin(30)")
        preview_lbl = tk.Label(
            self.center_pane,
            textvariable=self.preview_var,
            font=self.scale_font("Segoe UI", 12),
            bg=theme["bg"],
            fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8"
        )
        preview_lbl.pack(pady=(2, 8))
        
        key_frame = tk.Frame(self.center_pane, bg=theme["bg"])
        key_frame.pack(fill="both", expand=True, padx=55, pady=(5, 25))
        
        for i in range(3):
            key_frame.columnconfigure(i, weight=1)
        for i in range(4):
            key_frame.rowconfigure(i, weight=1)
            
        sci_buttons = [
            ("sin", 0, 0), ("cos", 0, 1), ("tan", 0, 2),
            ("log", 1, 0), ("ln", 1, 1),  ("√", 1, 2),
            ("x²", 2, 0),  ("x³", 2, 1),  ("n!", 2, 2),
            ("π", 3, 0),   ("e", 3, 1),   ("=", 3, 2)
        ]
        
        teal_theme = {
            "normal_bg": "#14B8A6",
            "hover_bg": "#2DD4BF",
            "active_bg": "#0F766E",
            "normal_fg": "#FFFFFF",
            "hover_fg": "#FFFFFF",
            "active_fg": "#FFFFFF"
        }
        
        eq_colors = self.get_category_colors("eq", theme)
        
        for text, row, col in sci_buttons:
            colors = eq_colors if text == "=" else teal_theme
            
            btn = RoundedButton(
                key_frame,
                text=text,
                radius=12,
                font=self.scale_font("Segoe UI", 12, "bold"),
                normal_bg=colors["normal_bg"],
                hover_bg=colors["hover_bg"],
                active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"],
                hover_fg=colors["hover_fg"],
                active_fg=colors["active_fg"],
                command=lambda val=text: self.scientific_click(val)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

    def scientific_click(self, op):
        current = self.display_var.get().strip()
        
        if op == "=":
            self.calculate_scientific()
            return
            
        if self.display_var.get() == "Error":
            current = ""
            
        if op == "π":
            self.display_var.set(current + str(round(math.pi, 8)))
            return
        elif op == "e":
            self.display_var.set(current + str(round(math.e, 8)))
            return
            
        if op in ["sin", "cos", "tan", "log", "ln", "√"]:
            if current == "" or current == "0":
                self.display_var.set(f"{op}(")
            else:
                self.display_var.set(f"{op}({current})")
                self.preview_var.set(f"{op}({current})")
                self.calculate_scientific()
            return
            
        if op == "x²":
            if current != "":
                self.display_var.set(f"({current})^2")
                self.preview_var.set(f"({current})²")
                self.calculate_scientific()
            return
        elif op == "x³":
            if current != "":
                self.display_var.set(f"({current})^3")
                self.preview_var.set(f"({current})³")
                self.calculate_scientific()
            return
        elif op == "n!":
            if current != "":
                self.display_var.set(f"fact({current})")
                self.preview_var.set(f"({current})!")
                self.calculate_scientific()
            return

    def calculate_scientific(self):
        expr = self.display_var.get().strip()
        if not expr or expr == "Error":
            return
            
        try:
            def sin_deg(x): return math.sin(math.radians(x))
            def cos_deg(x): return math.cos(math.radians(x))
            def tan_deg(x):
                if math.isclose(math.cos(math.radians(x)), 0, abs_tol=1e-9):
                    raise ValueError
                return math.tan(math.radians(x))
                
            def log_10(x):
                if x <= 0: raise ValueError
                return math.log10(x)
                
            def ln_e(x):
                if x <= 0: raise ValueError
                return math.log(x)
                
            def sqrt_op(x):
                if x < 0: raise ValueError
                return math.sqrt(x)
                
            def fact_op(x):
                if x < 0 or not float(x).is_integer():
                    raise ValueError
                return math.factorial(int(x))
                
            cleaned = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
            
            eval_namespace = {
                "sin": sin_deg,
                "cos": cos_deg,
                "tan": tan_deg,
                "log": log_10,
                "ln": ln_e,
                "sqrt": sqrt_op,
                "fact": fact_op,
                "pi": math.pi,
                "e": math.e
            }
            
            check_str = cleaned
            for key in eval_namespace.keys():
                check_str = check_str.replace(key, "")
            allowed = set("0123456789+-*/.() %*")
            for char in check_str:
                if char not in allowed:
                    raise ValueError
                    
            result = eval(cleaned, {"__builtins__": {}}, eval_namespace)
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)
            self.display_var.set(str(result))
            self.add_history(expr, str(result))
        except Exception:
            self.display_var.set("Error")

    # --- Module: Finance ---
    def build_finance(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Finance Hub")
        
        selector_frame = tk.Frame(self.center_pane, bg=theme["bg"])
        selector_frame.pack(fill="x", padx=40, pady=5)
        
        tk.Label(selector_frame, text="Select Tool:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["bg"], fg=theme["display_fg"]).pack(side="left")
        self.finance_tool_var = tk.StringVar(value="GST Calculator")
        finance_combo = ttk.Combobox(selector_frame, textvariable=self.finance_tool_var, values=["GST Calculator", "EMI Calculator", "Compound Interest"], state="readonly", font=self.scale_font("Segoe UI", 10))
        finance_combo.pack(side="left", padx=10)
        finance_combo.bind("<<ComboboxSelected>>", lambda e: self.rebuild_finance_form())
        
        self.finance_content = tk.Frame(self.center_pane, bg=theme["bg"])
        self.finance_content.pack(fill="both", expand=True, padx=40, pady=5)
        
        self.rebuild_finance_form()

    def rebuild_finance_form(self):
        for w in self.finance_content.winfo_children():
            w.destroy()
            
        theme = self.themes[self.current_theme]
        tool = self.finance_tool_var.get()
        
        form_frame = tk.Frame(self.finance_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        form_frame.pack(fill="x", pady=10)
        form_frame.columnconfigure(1, weight=1)
        
        colors = self.get_category_colors("op", theme)
        
        if tool == "GST Calculator":
            tk.Label(form_frame, text="Original Amount (₹):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=5)
            self.gst_amount_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid", highlightthickness=0)
            self.gst_amount_entry.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
            self.gst_amount_entry.insert(0, "1000")
            
            tk.Label(form_frame, text="GST Rate (%):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=5)
            self.gst_rate_var = tk.StringVar(value="18")
            gst_rate_combo = ttk.Combobox(form_frame, textvariable=self.gst_rate_var, values=["5", "12", "18", "28"], state="readonly", font=self.scale_font("Segoe UI", 10))
            gst_rate_combo.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
            
            calc_btn = RoundedButton(
                self.finance_content, text="Calculate GST", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
                normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
                command=self.calculate_gst, height=35
            )
            calc_btn.pack(pady=10, fill="x")
            
            self.fin_results_frame = tk.Frame(self.finance_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
            self.fin_results_frame.pack(fill="x", pady=5)
            
            row1 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row1.pack(fill="x", pady=3)
            tk.Label(row1, text="Net Price (Excl. GST):", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl1 = tk.Label(row1, text="₹1,000.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"])
            self.fin_lbl1.pack(side="right")
            
            row2 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row2.pack(fill="x", pady=3)
            tk.Label(row2, text="GST Tax Amount (18%):", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl2 = tk.Label(row2, text="₹180.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
            self.fin_lbl2.pack(side="right")
            
            row3 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row3.pack(fill="x", pady=3)
            tk.Label(row3, text="Total Price (Incl. GST):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl3 = tk.Label(row3, text="₹1,180.00", font=self.scale_font("Segoe UI", 13, "bold"), bg=theme["display_bg"], fg=theme["btn_eq_bg"])
            self.fin_lbl3.pack(side="right")
            
        elif tool == "EMI Calculator":
            tk.Label(form_frame, text="Loan Amount (Principal ₹):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=4)
            self.emi_p_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.emi_p_entry.grid(row=0, column=1, pady=4, padx=10, sticky="ew")
            self.emi_p_entry.insert(0, "100000")
            
            tk.Label(form_frame, text="Annual Interest Rate (%):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=4)
            self.emi_r_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.emi_r_entry.grid(row=1, column=1, pady=4, padx=10, sticky="ew")
            self.emi_r_entry.insert(0, "8.5")
            
            tk.Label(form_frame, text="Tenure (Months):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=2, column=0, sticky="w", pady=4)
            self.emi_n_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.emi_n_entry.grid(row=2, column=1, pady=4, padx=10, sticky="ew")
            self.emi_n_entry.insert(0, "24")
            
            calc_btn = RoundedButton(
                self.finance_content, text="Calculate EMI", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
                normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
                command=self.calculate_emi, height=35
            )
            calc_btn.pack(pady=10, fill="x")
            
            self.fin_results_frame = tk.Frame(self.finance_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
            self.fin_results_frame.pack(fill="x", pady=5)
            
            row1 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row1.pack(fill="x", pady=3)
            tk.Label(row1, text="Monthly EMI:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl1 = tk.Label(row1, text="₹0.00", font=self.scale_font("Segoe UI", 13, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
            self.fin_lbl1.pack(side="right")
            
            row2 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row2.pack(fill="x", pady=3)
            tk.Label(row2, text="Total Interest Payable:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl2 = tk.Label(row2, text="₹0.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"])
            self.fin_lbl2.pack(side="right")
            
            row3 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row3.pack(fill="x", pady=3)
            tk.Label(row3, text="Total Amount Payable:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl3 = tk.Label(row3, text="₹0.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["btn_eq_bg"])
            self.fin_lbl3.pack(side="right")
            
        else:  # Compound Interest
            tk.Label(form_frame, text="Principal Amount (₹):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=4)
            self.ci_p_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.ci_p_entry.grid(row=0, column=1, pady=4, padx=10, sticky="ew")
            self.ci_p_entry.insert(0, "10000")
            
            tk.Label(form_frame, text="Interest Rate (% per year):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=4)
            self.ci_r_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.ci_r_entry.grid(row=1, column=1, pady=4, padx=10, sticky="ew")
            self.ci_r_entry.insert(0, "5")
            
            tk.Label(form_frame, text="Tenure (Years):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=2, column=0, sticky="w", pady=4)
            self.ci_t_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.ci_t_entry.grid(row=2, column=1, pady=4, padx=10, sticky="ew")
            self.ci_t_entry.insert(0, "5")
            
            tk.Label(form_frame, text="Compounding:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=3, column=0, sticky="w", pady=4)
            self.ci_freq_var = tk.StringVar(value="Annual")
            ci_combo = ttk.Combobox(form_frame, textvariable=self.ci_freq_var, values=["Annual", "Semi-Annual", "Quarterly", "Monthly"], state="readonly", font=self.scale_font("Segoe UI", 10))
            ci_combo.grid(row=3, column=1, pady=4, padx=10, sticky="ew")
            
            calc_btn = RoundedButton(
                self.finance_content, text="Calculate Interest", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
                normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
                command=self.calculate_compound_interest, height=35
            )
            calc_btn.pack(pady=10, fill="x")
            
            self.fin_results_frame = tk.Frame(self.finance_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
            self.fin_results_frame.pack(fill="x", pady=5)
            
            row1 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row1.pack(fill="x", pady=3)
            tk.Label(row1, text="Future Value (Total):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl1 = tk.Label(row1, text="₹0.00", font=self.scale_font("Segoe UI", 13, "bold"), bg=theme["display_bg"], fg=theme["btn_eq_bg"])
            self.fin_lbl1.pack(side="right")
            
            row2 = tk.Frame(self.fin_results_frame, bg=theme["display_bg"])
            row2.pack(fill="x", pady=3)
            tk.Label(row2, text="Interest Earned:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
            self.fin_lbl2 = tk.Label(row2, text="₹0.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
            self.fin_lbl2.pack(side="right")

    # --- Module: Statistical ---
    def build_statistical(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Statistical Calculator")
        
        form_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=20, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        form_frame.pack(padx=50, pady=10, fill="x")
        
        tk.Label(form_frame, text="Enter Numbers (separated by commas):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).pack(anchor="w")
        self.stat_input_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.stat_input_entry.pack(fill="x", pady=10)
        self.stat_input_entry.insert(0, "10, 20, 30, 40, 50")
        
        colors = self.get_category_colors("op", theme)
        calc_btn = RoundedButton(
            self.center_pane, text="Compute Statistics", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
            normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
            normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
            command=self.calculate_statistical, height=35
        )
        calc_btn.pack(pady=15, padx=50, fill="x")
        
        self.stat_results_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        self.stat_results_frame.pack(padx=50, pady=10, fill="x")
        
        s1 = tk.Frame(self.stat_results_frame, bg=theme["display_bg"])
        s1.pack(fill="x", pady=3)
        tk.Label(s1, text="Mean | Median | Mode:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
        self.stat_res_lbl1 = tk.Label(s1, text="Mean: 30 | Median: 30 | Mode: 10", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
        self.stat_res_lbl1.pack(side="right")
        
        s2 = tk.Frame(self.stat_results_frame, bg=theme["display_bg"])
        s2.pack(fill="x", pady=3)
        tk.Label(s2, text="Variance | Std Dev:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
        self.stat_res_lbl2 = tk.Label(s2, text="Var: 250 | Std Dev: 15.81", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["btn_eq_bg"])
        self.stat_res_lbl2.pack(side="right")

    # --- Module: Retirement Planning ---
    def build_retirement(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Retirement Planner")
        
        form_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        form_frame.pack(padx=50, pady=10, fill="x")
        
        tk.Label(form_frame, text="Current Age:", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=4)
        self.ret_age_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.ret_age_entry.grid(row=0, column=1, pady=4, padx=10, sticky="ew")
        self.ret_age_entry.insert(0, "30")
        
        tk.Label(form_frame, text="Planned Retirement Age:", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=4)
        self.ret_target_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.ret_target_entry.grid(row=1, column=1, pady=4, padx=10, sticky="ew")
        self.ret_target_entry.insert(0, "60")
        
        tk.Label(form_frame, text="Monthly Savings (₹):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=2, column=0, sticky="w", pady=4)
        self.ret_savings_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.ret_savings_entry.grid(row=2, column=1, pady=4, padx=10, sticky="ew")
        self.ret_savings_entry.insert(0, "5000")
        
        tk.Label(form_frame, text="Expected Return (% / yr):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=3, column=0, sticky="w", pady=4)
        self.ret_return_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.ret_return_entry.grid(row=3, column=1, pady=4, padx=10, sticky="ew")
        self.ret_return_entry.insert(0, "10")
        
        tk.Label(form_frame, text="Expected Inflation (% / yr):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=4, column=0, sticky="w", pady=4)
        self.ret_inf_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.ret_inf_entry.grid(row=4, column=1, pady=4, padx=10, sticky="ew")
        self.ret_inf_entry.insert(0, "6")
        
        form_frame.columnconfigure(1, weight=1)
        
        colors = self.get_category_colors("op", theme)
        calc_btn = RoundedButton(
            self.center_pane, text="Calculate Corpus", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
            normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
            normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
            command=self.calculate_retirement, height=35
        )
        calc_btn.pack(pady=10, padx=50, fill="x")
        
        self.ret_results_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        self.ret_results_frame.pack(padx=50, pady=5, fill="x")
        
        t1 = tk.Frame(self.ret_results_frame, bg=theme["display_bg"])
        t1.pack(fill="x", pady=3)
        tk.Label(t1, text="Invested Years & Principal:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
        self.ret_res_lbl1 = tk.Label(t1, text="Invested Years: 30 | Total Principal: ₹1,800,000.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"])
        self.ret_res_lbl1.pack(side="right")
        
        t2 = tk.Frame(self.ret_results_frame, bg=theme["display_bg"])
        t2.pack(fill="x", pady=3)
        tk.Label(t2, text="Estimated Nominal Value:", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
        self.ret_res_lbl2 = tk.Label(t2, text="₹11,396,627.00", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
        self.ret_res_lbl2.pack(side="right")
        
        t3 = tk.Frame(self.ret_results_frame, bg=theme["display_bg"])
        t3.pack(fill="x", pady=3)
        tk.Label(t3, text="Real Purchasing Power:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"] if self.current_theme == "light" else "#94A3B8").pack(side="left")
        self.ret_res_lbl3 = tk.Label(t3, text="₹1,984,277.00", font=self.scale_font("Segoe UI", 13, "bold"), bg=theme["display_bg"], fg=theme["btn_eq_bg"])
        self.ret_res_lbl3.pack(side="right")

    # --- Module: Age Calculator ---
    def build_age_calc(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Age Calculator")
        
        form_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=20, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        form_frame.pack(padx=50, pady=10, fill="x")
        
        tk.Label(form_frame, text="Birth Year (YYYY):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=6)
        self.age_year_sb = tk.Spinbox(form_frame, from_=1900, to=2026, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.age_year_sb.grid(row=0, column=1, pady=6, padx=10, sticky="ew")
        self.age_year_sb.delete(0, "end")
        self.age_year_sb.insert(0, "1995")
        
        tk.Label(form_frame, text="Birth Month (1-12):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=6)
        self.age_month_sb = tk.Spinbox(form_frame, from_=1, to=12, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.age_month_sb.grid(row=1, column=1, pady=6, padx=10, sticky="ew")
        self.age_month_sb.delete(0, "end")
        self.age_month_sb.insert(0, "10")
        
        tk.Label(form_frame, text="Birth Day (1-31):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=2, column=0, sticky="w", pady=6)
        self.age_day_sb = tk.Spinbox(form_frame, from_=1, to=31, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.age_day_sb.grid(row=2, column=1, pady=6, padx=10, sticky="ew")
        self.age_day_sb.delete(0, "end")
        self.age_day_sb.insert(0, "15")
        
        form_frame.columnconfigure(1, weight=1)
        
        colors = self.get_category_colors("op", theme)
        calc_btn = RoundedButton(
            self.center_pane, text="Calculate Age", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
            normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
            normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
            command=self.calculate_age, height=35
        )
        calc_btn.pack(pady=15, padx=50, fill="x")
        
        self.age_results_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        self.age_results_frame.pack(padx=50, pady=10, fill="x")
        
        self.age_result_lbl = tk.Label(self.age_results_frame, text="Result: Click Calculate", font=self.scale_font("Segoe UI", 14, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
        self.age_result_lbl.pack(pady=5)

    # --- Module: Unit Converter ---
    def build_unit_conv(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Unit Converter")
        
        form_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        form_frame.pack(padx=50, pady=10, fill="x")
        
        tk.Label(form_frame, text="Category:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=5)
        self.unit_cat_var = tk.StringVar(value="Length")
        unit_cat_combo = ttk.Combobox(form_frame, textvariable=self.unit_cat_var, values=["Length", "Weight", "Area"], state="readonly", font=self.scale_font("Segoe UI", 11))
        unit_cat_combo.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        unit_cat_combo.bind("<<ComboboxSelected>>", self.on_unit_category_change)
        
        tk.Label(form_frame, text="Value:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=5)
        self.unit_val_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
        self.unit_val_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        self.unit_val_entry.insert(0, "1")
        
        tk.Label(form_frame, text="From Unit:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=2, column=0, sticky="w", pady=5)
        self.unit_from_var = tk.StringVar()
        self.unit_from_combo = ttk.Combobox(form_frame, textvariable=self.unit_from_var, state="readonly", font=self.scale_font("Segoe UI", 11))
        self.unit_from_combo.grid(row=2, column=1, pady=5, padx=10, sticky="ew")
        
        tk.Label(form_frame, text="To Unit:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=3, column=0, sticky="w", pady=5)
        self.unit_to_var = tk.StringVar()
        self.unit_to_combo = ttk.Combobox(form_frame, textvariable=self.unit_to_var, state="readonly", font=self.scale_font("Segoe UI", 11))
        self.unit_to_combo.grid(row=3, column=1, pady=5, padx=10, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        self.update_unit_combos()
        
        colors = self.get_category_colors("op", theme)
        calc_btn = RoundedButton(
            self.center_pane, text="Convert Unit", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
            normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
            normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
            command=self.convert_unit, height=35
        )
        calc_btn.pack(pady=10, padx=50, fill="x")
        
        self.unit_results_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        self.unit_results_frame.pack(padx=50, pady=10, fill="x")
        self.unit_result_lbl = tk.Label(self.unit_results_frame, text="Result: 1.00 m", font=self.scale_font("Segoe UI", 14, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
        self.unit_result_lbl.pack(pady=5)

    # --- Module: Health Calculator ---
    def build_health(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Health Hub")
        
        selector_frame = tk.Frame(self.center_pane, bg=theme["bg"])
        selector_frame.pack(fill="x", padx=40, pady=5)
        
        tk.Label(selector_frame, text="Select Tool:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["bg"], fg=theme["display_fg"]).pack(side="left")
        self.health_tool_var = tk.StringVar(value="BMI Calculator")
        health_combo = ttk.Combobox(selector_frame, textvariable=self.health_tool_var, values=["BMI Calculator", "Daily Calories", "Daily Water Intake"], state="readonly", font=self.scale_font("Segoe UI", 10))
        health_combo.pack(side="left", padx=10)
        health_combo.bind("<<ComboboxSelected>>", lambda e: self.rebuild_health_form())
        
        self.health_content = tk.Frame(self.center_pane, bg=theme["bg"])
        self.health_content.pack(fill="both", expand=True, padx=40, pady=5)
        self.rebuild_health_form()

    def rebuild_health_form(self):
        for w in self.health_content.winfo_children():
            w.destroy()
            
        theme = self.themes[self.current_theme]
        tool = self.health_tool_var.get()
        
        form_frame = tk.Frame(self.health_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        form_frame.pack(fill="x", pady=10)
        form_frame.columnconfigure(1, weight=1)
        
        colors = self.get_category_colors("op", theme)
        
        if tool == "BMI Calculator":
            tk.Label(form_frame, text="Weight (kg):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=6)
            self.bmi_w_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.bmi_w_entry.grid(row=0, column=1, pady=6, padx=10, sticky="ew")
            self.bmi_w_entry.insert(0, "70")
            
            tk.Label(form_frame, text="Height (cm):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=6)
            self.bmi_h_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.bmi_h_entry.grid(row=1, column=1, pady=6, padx=10, sticky="ew")
            self.bmi_h_entry.insert(0, "175")
            
            calc_btn = RoundedButton(
                self.health_content, text="Calculate BMI", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
                normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
                command=self.calculate_bmi, height=35
            )
            calc_btn.pack(pady=10, fill="x")
            
            self.health_results_frame = tk.Frame(self.health_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
            self.health_results_frame.pack(fill="x", pady=5)
            self.health_res_lbl = tk.Label(self.health_results_frame, text="BMI: 22.86 (Normal weight)", font=self.scale_font("Segoe UI", 14, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
            self.health_res_lbl.pack(pady=5)
            
        elif tool == "Daily Calories":
            tk.Label(form_frame, text="Gender:", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=4)
            self.cal_gender_var = tk.StringVar(value="Male")
            cal_gender_combo = ttk.Combobox(form_frame, textvariable=self.cal_gender_var, values=["Male", "Female"], state="readonly", font=self.scale_font("Segoe UI", 10))
            cal_gender_combo.grid(row=0, column=1, pady=4, padx=10, sticky="ew")
            
            tk.Label(form_frame, text="Age (Years):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=4)
            self.cal_age_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.cal_age_entry.grid(row=1, column=1, pady=4, padx=10, sticky="ew")
            self.cal_age_entry.insert(0, "30")
            
            tk.Label(form_frame, text="Weight (kg):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=2, column=0, sticky="w", pady=4)
            self.cal_weight_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.cal_weight_entry.grid(row=2, column=1, pady=4, padx=10, sticky="ew")
            self.cal_weight_entry.insert(0, "70")
            
            tk.Label(form_frame, text="Height (cm):", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=3, column=0, sticky="w", pady=4)
            self.cal_height_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.cal_height_entry.grid(row=3, column=1, pady=4, padx=10, sticky="ew")
            self.cal_height_entry.insert(0, "175")
            
            tk.Label(form_frame, text="Activity:", font=self.scale_font("Segoe UI", 10, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=4, column=0, sticky="w", pady=4)
            self.cal_act_var = tk.StringVar(value="Moderate")
            cal_act_combo = ttk.Combobox(form_frame, textvariable=self.cal_act_var, values=["Sedentary", "Light", "Moderate", "Active"], state="readonly", font=self.scale_font("Segoe UI", 10))
            cal_act_combo.grid(row=4, column=1, pady=4, padx=10, sticky="ew")
            
            calc_btn = RoundedButton(
                self.health_content, text="Calculate Calories", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
                normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
                command=self.calculate_calories, height=35
            )
            calc_btn.pack(pady=10, fill="x")
            
            self.health_results_frame = tk.Frame(self.health_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
            self.health_results_frame.pack(fill="x", pady=5)
            self.health_res_lbl = tk.Label(self.health_results_frame, text="Maintenance Calories: 2,230 kcal / day", font=self.scale_font("Segoe UI", 12, "bold"), bg=theme["display_bg"], fg=theme["display_fg"])
            self.health_res_lbl.pack(pady=5)
            
        else:  # Daily Water Intake
            tk.Label(form_frame, text="Weight (kg):", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=6)
            self.water_w_entry = tk.Entry(form_frame, font=self.scale_font("Segoe UI", 11), bg=theme["bg"], fg=theme["display_fg"], bd=1, relief="solid")
            self.water_w_entry.grid(row=0, column=1, pady=6, padx=10, sticky="ew")
            self.water_w_entry.insert(0, "70")
            
            tk.Label(form_frame, text="Daily Activity:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=1, column=0, sticky="w", pady=6)
            self.water_act_var = tk.StringVar(value="Moderate")
            water_act_combo = ttk.Combobox(form_frame, textvariable=self.water_act_var, values=["Low", "Moderate", "High"], state="readonly", font=self.scale_font("Segoe UI", 11))
            water_act_combo.grid(row=1, column=1, pady=6, padx=10, sticky="ew")
            
            calc_btn = RoundedButton(
                self.health_content, text="Calculate Water Target", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
                normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
                command=self.calculate_water, height=35
            )
            calc_btn.pack(pady=10, fill="x")
            
            self.health_results_frame = tk.Frame(self.health_content, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
            self.health_results_frame.pack(fill="x", pady=5)
            self.health_res_lbl = tk.Label(self.health_results_frame, text="Water Target: 2.95 Liters / day", font=self.scale_font("Segoe UI", 14, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"])
            self.health_res_lbl.pack(pady=5)

    # --- Module: History ---
    def build_history(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Calculation History")
        
        history_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=20, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        history_frame.pack(padx=50, pady=10, fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            font=self.scale_font("Consolas", 11),
            bg=theme["bg"],
            fg=theme["display_fg"],
            bd=0,
            highlightthickness=0,
            selectbackground=theme["btn_op_bg"],
            selectforeground=theme["btn_op_fg"]
        )
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
        if not self.history_log:
            self.history_listbox.insert(tk.END, "No recent calculations found.")
        else:
            for item in reversed(self.history_log):
                line = f"[{item['time']}] {item['expr']} = {item['res']}"
                self.history_listbox.insert(tk.END, line)
                
        self.history_listbox.bind("<Double-Button-1>", self.on_history_double_click)
        
        btn_frame = tk.Frame(self.center_pane, bg=theme["bg"])
        btn_frame.pack(pady=15)
        
        colors = self.get_category_colors("spec", theme)
        clear_btn = RoundedButton(
            btn_frame, text="Clear Logs", radius=8, font=self.scale_font("Segoe UI", 11, "bold"),
            normal_bg=colors["normal_bg"], hover_bg=colors["hover_bg"], active_bg=colors["active_bg"],
            normal_fg=colors["normal_fg"], hover_fg=colors["hover_fg"], active_fg=colors["active_fg"],
            command=self.clear_history, width=120, height=35
        )
        clear_btn.pack()

    def on_history_double_click(self, event):
        try:
            sel_idx = self.history_listbox.curselection()[0]
            sel_text = self.history_listbox.get(sel_idx)
            if "=" in sel_text:
                result_part = sel_text.split("=")[1].strip()
                self.root.clipboard_clear()
                self.root.clipboard_append(result_part)
        except IndexError:
            pass

    def clear_history(self):
        self.history_log.clear()
        self.rebuild_center()

    # --- Module: Settings ---
    def build_settings(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Settings & Config")
        
        card = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=20, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        card.pack(padx=50, pady=10, fill="x")
        
        tk.Label(card, text="Interface Font Scaling:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).grid(row=0, column=0, sticky="w", pady=10)
        
        scales = {"Standard (100%)": 1.0, "Medium (120%)": 1.2, "Large (140%)": 1.4, "Extra Large (160%)": 1.6}
        current_scale_lbl = [k for k, v in scales.items() if v == self.font_scale][0]
        
        self.settings_scale_var = tk.StringVar(value=current_scale_lbl)
        scale_combo = ttk.Combobox(card, textvariable=self.settings_scale_var, values=list(scales.keys()), state="readonly", font=self.scale_font("Segoe UI", 10))
        scale_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        scale_combo.bind("<<ComboboxSelected>>", self.on_scale_selected)
        
        card.columnconfigure(1, weight=1)
        
        credit_card = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=20, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        credit_card.pack(padx=50, pady=10, fill="x")
        
        tk.Label(credit_card, text="Credits & Build Version", font=self.scale_font("Segoe UI", 12, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"]).pack(anchor="w", pady=(0, 5))
        tk.Label(credit_card, text="Smart Multi-Purpose Calculator Suite v2.1.0\nCreated using Python and Tkinter UI Engine.\nFully optimized for high-density Windows screens.", font=self.scale_font("Segoe UI", 10), bg=theme["display_bg"], fg=theme["display_fg"], justify="left").pack(anchor="w")

    def on_scale_selected(self, event):
        scales = {"Standard (100%)": 1.0, "Medium (120%)": 1.2, "Large (140%)": 1.4, "Extra Large (160%)": 1.6}
        self.font_scale = scales[self.settings_scale_var.get()]
        
        self.left_sidebar.destroy()
        self.right_sidebar.destroy()
        self.center_pane.destroy()
        
        self.setup_ui_layout()
        self.configure_combo_styles()
        self.rebuild_center()

    # --- Module: Target Audience ---
    def build_target_audience(self):
        theme = self.themes[self.current_theme]
        self.draw_center_header("Target Audience Profiles")
        
        card = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=15, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        card.pack(padx=40, pady=5, fill="x")
        
        tk.Label(card, text="Select Your Profile:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).pack(side="left")
        self.audience_profile_var = tk.StringVar(value="Financial Planner")
        profile_combo = ttk.Combobox(card, textvariable=self.audience_profile_var, values=["Financial Planner", "Student / Analyst", "Health Enthusiast", "Engineer / Scientist"], state="readonly", font=self.scale_font("Segoe UI", 10))
        profile_combo.pack(side="left", padx=10)
        profile_combo.bind("<<ComboboxSelected>>", lambda e: self.rebuild_audience_details())
        
        self.audience_detail_frame = tk.Frame(self.center_pane, bg=theme["display_bg"], padx=20, pady=20, bd=0, highlightthickness=1, highlightbackground=theme["btn_num_bg"])
        self.audience_detail_frame.pack(padx=40, pady=15, fill="both", expand=True)
        
        self.rebuild_audience_details()

    def rebuild_audience_details(self):
        for w in self.audience_detail_frame.winfo_children():
            w.destroy()
            
        theme = self.themes[self.current_theme]
        profile = self.audience_profile_var.get()
        colors = self.get_category_colors("op", theme)
        
        desc = ""
        recs = []
        
        if profile == "Financial Planner":
            desc = "Designed to assist in budgeting, tax forecasting, loan EMI evaluation, and compound interest calculations for rapid investment projections."
            recs = [("Finance Suite", "Finance"), ("Retirement Planner", "Retirement Planning"), ("Basic Calculator", "Basic Calculator")]
        elif profile == "Student / Analyst":
            desc = "Optimized for algebra, statistical processing, basic math homework, list evaluations (mean/median/std dev), and standard calculation steps."
            recs = [("Statistical Hub", "Statistical"), ("Basic Calculator", "Basic Calculator"), ("Unit Converter", "Unit Converter")]
        elif profile == "Health Enthusiast":
            desc = "Tailored to calculate healthy metrics, including Body Mass Index (BMI), daily calorie maintenance numbers, and hydration intake estimates."
            recs = [("Health Hub", "Health Calculator"), ("Age Calculator", "Age Calculator")]
        else:  # Engineer / Scientist
            desc = "Built for handling complex math, trigs, logs, factorials, scientific constants (e, pi), and advanced physical unit conversions."
            recs = [("Scientific Hub", "Scientific Calculator"), ("Unit Converter", "Unit Converter"), ("Statistical Calculator", "Statistical")]
            
        tk.Label(self.audience_detail_frame, text=f"Profile: {profile}", font=self.scale_font("Segoe UI", 14, "bold"), bg=theme["display_bg"], fg=theme["btn_op_bg"]).pack(anchor="w", pady=(0, 5))
        tk.Label(self.audience_detail_frame, text=desc, font=self.scale_font("Segoe UI", 11), bg=theme["display_bg"], fg=theme["display_fg"], justify="left", wraplength=450).pack(anchor="w", pady=5)
        
        tk.Label(self.audience_detail_frame, text="Recommended Utilities for You:", font=self.scale_font("Segoe UI", 11, "bold"), bg=theme["display_bg"], fg=theme["display_fg"]).pack(anchor="w", pady=(15, 8))
        
        for display_name, internal_name in recs:
            btn = RoundedButton(
                self.audience_detail_frame,
                text=f"👉 Open {display_name}",
                radius=8,
                font=self.scale_font("Segoe UI", 10, "bold"),
                normal_bg=colors["normal_bg"],
                hover_bg=colors["hover_bg"],
                active_bg=colors["active_bg"],
                normal_fg=colors["normal_fg"],
                hover_fg=colors["hover_fg"],
                active_fg=colors["active_fg"],
                command=lambda dest=internal_name: self.navigation_click(dest),
                height=32
            )
            btn.pack(anchor="w", pady=4, padx=10, fill="x", ipady=2)


if __name__ == "__main__":
    print("Initializing Smart Multi-Purpose Calculator...")
    root = tk.Tk()
    app = SmartMultiCalculator(root)
    print("Application successfully initialized and running.")
    root.mainloop()
