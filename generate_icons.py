import os
import math
from PIL import Image, ImageDraw

def create_icon_folder():
    os.makedirs("icons", exist_ok=True)

def draw_rounded_rect(draw, coords, r, fill):
    x0, y0, x1, y1 = coords
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill)

# Drawing functions
def draw_basic(draw, bg_color):
    # Plus sign
    draw.line([(32, 38), (52, 38)], fill="white", width=8)
    draw.line([(42, 28), (42, 48)], fill="white", width=8)
    # Minus sign
    draw.line([(76, 38), (96, 38)], fill="white", width=8)
    # Multiplication sign
    draw.line([(32, 76), (52, 96)], fill="white", width=8)
    draw.line([(52, 76), (32, 96)], fill="white", width=8)
    # Equals sign
    draw.line([(76, 81), (96, 81)], fill="white", width=8)
    draw.line([(76, 91), (96, 91)], fill="white", width=8)

def draw_scientific(draw, bg_color):
    # Square root symbol
    draw.line([(22, 62), (36, 76)], fill="white", width=8, joint="round")
    draw.line([(36, 76), (56, 32)], fill="white", width=8, joint="round")
    draw.line([(56, 32), (95, 32)], fill="white", width=8, joint="round")
    # Draw x inside/below the root
    draw.line([(68, 56), (88, 76)], fill="white", width=8)
    draw.line([(88, 56), (68, 76)], fill="white", width=8)

def draw_finance(draw, bg_color):
    # Rupee symbol ₹
    draw.line([(38, 34), (90, 34)], fill="white", width=8)
    draw.line([(38, 48), (80, 48)], fill="white", width=8)
    draw.line([(48, 34), (48, 62)], fill="white", width=8)
    draw.arc([(48, 34), (84, 62)], start=-90, end=90, fill="white", width=8)
    draw.line([(56, 62), (85, 98)], fill="white", width=8)

def draw_statistical(draw, bg_color):
    # Bar chart
    draw.line([(25, 95), (103, 95)], fill="white", width=8)
    draw.rectangle([(35, 70), (50, 91)], fill="white")
    draw.rectangle([(56, 40), (71, 91)], fill="white")
    draw.rectangle([(77, 60), (92, 91)], fill="white")

def draw_retirement(draw, bg_color):
    # Shield shape for protection
    draw.line([(34, 30), (94, 30)], fill="white", width=8)
    draw.line([(34, 30), (34, 60)], fill="white", width=8)
    draw.line([(34, 60), (64, 98)], fill="white", width=8)
    draw.line([(94, 30), (94, 60)], fill="white", width=8)
    draw.line([(94, 60), (64, 98)], fill="white", width=8)
    # Inner checkmark
    draw.line([(52, 60), (60, 68)], fill="white", width=6)
    draw.line([(60, 68), (76, 52)], fill="white", width=6)

def draw_age(draw, bg_color):
    # Hourglass
    draw.line([(34, 30), (94, 30)], fill="white", width=8)
    draw.line([(34, 98), (94, 98)], fill="white", width=8)
    draw.line([(42, 30), (64, 64)], fill="white", width=8)
    draw.line([(86, 30), (64, 64)], fill="white", width=8)
    draw.line([(42, 98), (64, 64)], fill="white", width=8)
    draw.line([(86, 98), (64, 64)], fill="white", width=8)
    draw.polygon([(52, 40), (76, 40), (64, 58)], fill="white")
    draw.polygon([(48, 94), (80, 94), (64, 76)], fill="white")

def draw_converter(draw, bg_color):
    # Two arrows (Length/Unit Conversion)
    draw.line([(28, 48), (86, 48)], fill="white", width=8)
    draw.line([(86, 48), (72, 34)], fill="white", width=8)
    draw.line([(86, 48), (72, 62)], fill="white", width=8)
    draw.line([(100, 80), (42, 80)], fill="white", width=8)
    draw.line([(42, 80), (56, 66)], fill="white", width=8)
    draw.line([(42, 80), (56, 94)], fill="white", width=8)

def draw_health(draw, bg_color):
    # Heartbeat ECG pulse line
    draw.line([
        (18, 64), (45, 64), (52, 84), (64, 30), (76, 98), (84, 64), (110, 64)
    ], fill="white", width=8, joint="round")

def draw_history(draw, bg_color):
    # Clock
    draw.arc([(28, 28), (100, 100)], start=25, end=340, fill="white", width=8)
    draw.line([(64, 64), (64, 44)], fill="white", width=8)
    draw.line([(64, 64), (82, 64)], fill="white", width=8)
    draw.line([(96, 45), (108, 32)], fill="white", width=8)
    draw.line([(96, 45), (84, 38)], fill="white", width=8)

def draw_settings(draw, bg_color):
    # Gear
    for angle in [0, 45, 90, 135]:
        rad = math.radians(angle)
        dx = 46 * math.cos(rad)
        dy = 46 * math.sin(rad)
        draw.line([(64 - dx, 64 - dy), (64 + dx, 64 + dy)], fill="white", width=22)
    draw.ellipse([(28, 28), (100, 100)], fill="white")
    draw.ellipse([(38, 38), (90, 90)], fill=bg_color)
    draw.ellipse([(48, 48), (80, 80)], fill="white")
    draw.ellipse([(55, 55), (73, 73)], fill=bg_color)

def draw_audience(draw, bg_color):
    # Target
    draw.arc([(24, 24), (104, 104)], start=0, end=360, fill="white", width=8)
    draw.arc([(42, 42), (86, 86)], start=0, end=360, fill="white", width=8)
    draw.ellipse([(58, 58), (70, 70)], fill="white")
    draw.line([(105, 23), (72, 56)], fill="white", width=8)
    draw.line([(72, 56), (72, 70)], fill="white", width=8)
    draw.line([(72, 56), (86, 56)], fill="white", width=8)

def draw_theme(draw, bg_color):
    # Contrast split circle
    draw.ellipse([(28, 28), (100, 100)], outline="white", width=8)
    draw.chord([(28, 28), (100, 100)], start=90, end=270, fill="white")

def generate_all_icons():
    icons_def = {
        "basic": {"bg": "#10B981", "draw": draw_basic},
        "scientific": {"bg": "#06B6D4", "draw": draw_scientific},
        "finance": {"bg": "#F59E0B", "draw": draw_finance},
        "statistical": {"bg": "#3B82F6", "draw": draw_statistical},
        "retirement": {"bg": "#8B5CF6", "draw": draw_retirement},
        "age": {"bg": "#EC4899", "draw": draw_age},
        "converter": {"bg": "#6366F1", "draw": draw_converter},
        "health": {"bg": "#EF4444", "draw": draw_health},
        "history": {"bg": "#6B7280", "draw": draw_history},
        "settings": {"bg": "#4B5563", "draw": draw_settings},
        "audience": {"bg": "#D946EF", "draw": draw_audience},
        "theme": {"bg": "#F59E0B", "draw": draw_theme}
    }
    
    for name, info in icons_def.items():
        img = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw_rounded_rect(draw, (8, 8, 120, 120), r=28, fill=info["bg"])
        info["draw"](draw, info["bg"])
        
        # Resize to 32x32 for UI
        img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
        img_32.save(f"icons/{name}.png")
        print(f"Generated icons/{name}.png")

if __name__ == "__main__":
    create_icon_folder()
    generate_all_icons()
    print("All icons successfully generated!")
