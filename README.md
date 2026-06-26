# Smart Multi-Purpose Calculator Suite

A modern, feature-rich, and professionally-designed desktop calculator application developed in Python using the **Tkinter** library and styled with premium Fluent Design aesthetics. 

The application is structured around a space-efficient navigation rail featuring colorful custom vector-like icons.

![Smart Multi-Purpose Calculator](screenshot.png)

## Key Highlights & Features

### 1. 🔢 Basic Calculator
* Full mathematical operations: addition, subtraction, multiplication, division.
* Parentheses support for operation hierarchy, square root, percent calculations, backspace, and clear operations.

### 2. 🧪 Scientific Calculator
* Core trigonometric functions: `sin`, `cos`, `tan`.
* Logarithmic calculations: `log10` (common log) and `ln` (natural log).
* Square roots (`√`), powers (`x²`, `x³`), factorials (`n!`), and constants like `π` and `e`.

### 3. 💵 Finance Suite
* **GST Calculator**: Quickly calculate Net Price, GST tax amount, and Total Price for 5%, 12%, 18%, or 28% tax slabs.
* **EMI Calculator**: Evaluate monthly loan repayments (EMIs), total interest payable, and total amount payable.
* **Compound Interest**: Compute compound returns with compounding frequency adjustments (Annual, Semi-Annual, Quarterly, Monthly).

### 4. 📊 Statistical Hub
* Input a comma-separated list of numbers to instantly compute: Mean, Median, Mode, Variance, and Standard Deviation.

### 5. 🏖️ Retirement Planner
* Plan your financial future by entering current age, planned retirement age, monthly savings, expected returns, and expected inflation to calculate estimated retirement corpus and real purchasing power.

### 6. 📅 Age Calculator
* Enter your birth year, month, and day to instantly calculate your precise age.

### 7. 🔄 Unit Converter
* Convert standard units dynamically across Length (meters, kilometers, miles, etc.), Weight (grams, kilograms, pounds, etc.), and Area.

### 8. ❤️ Health Hub
* **BMI Calculator**: Computes Body Mass Index (BMI) and provides weight category context.
* **Daily Calories**: Evaluates maintenance calories using age, gender, weight, height, and activity level.
* **Daily Water Intake**: Estimates daily hydration targets based on body weight and physical activity levels.

### 9. 📜 History Logs
* View a persistent history log of all calculations performed during the session. Double-click any log item to copy the result to your clipboard.

### 10. 👥 Target Audience Recommendation Engine
* Select a profile (Financial Planner, Student/Analyst, Health Enthusiast, Engineer/Scientist) to get personalized module recommendations.

### 11. ⚙️ Interface & Configurations
* Dynamic UI font scaling (100% to 160%) for high-DPI displays.
* Clean dark/light theme switching with instant layout adaptation.

---

## Technical Stack & Architecture
* **GUI Engine**: Tkinter
* **Layout Design**: Dual Sidebar Navigation Rail (75px width) displaying 32x32 custom PNG icons loaded dynamically.
* **Graphic Engine**: Pillow (PIL) for high-quality antialiased icons rendering.
* **Custom Widgets**: `RoundedButton` class built on `tk.Canvas` supporting custom hover transitions, selection states, custom fonts, and images.

---

## File Structure
```
d:\j_smar_calc/
│
├── calculator.py          # Main application entry point & GUI layout
├── generate_icons.py      # Python script utilizing Pillow to draw modern icons
├── README.md              # Project documentation
├── screenshot.png         # Main application visual screenshot
│
└── icons/                 # Folder containing custom generated PNG icons
    ├── basic.png
    ├── scientific.png
    ├── finance.png
    ├── statistical.png
    ├── retirement.png
    ├── age.png
    ├── converter.png
    ├── health.png
    ├── history.png
    ├── settings.png
    ├── audience.png
    └── theme.png
```

---

## Getting Started

### Prerequisites
Make sure Python 3.x and `Pillow` are installed:
```bash
pip install Pillow
```

### Running the Application
To launch the Smart Multi-Purpose Calculator:
```bash
python calculator.py
```

### Regenerating Icons
If you want to modify or regenerate the icon pack:
```bash
python generate_icons.py
```
