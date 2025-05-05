"""
pgfplots_generator.py

Author:            Muneeb Azfar Nafees
Last Updated:      02-May-2024
Description:       This script generates TikZ/PGFPlots code for plotting mathematical functions or coordinates.
Licensed under Apache-2.0 (see LICENSE file for details).
"""

# Import necessary libraries
import sympy as sp
import re

# Preamble for TikZ/PGFPlots
PREAMBLE = (
    "Preamble to copy-paste:\n"
    "\\usepackage{tikz}\n"
    "\\usepackage{pgfplots}\n"
    "\\pgfplotsset{compat=1.18,width=\\linewidth,"
    "height=0.5\\textheight,tick align=outside,"
    "grid=major,trig format plots=rad}\n"
)


def prompt_choice() -> str:
    """ Prompt the user to choose between entering an equation or coordinates.
    1) Equation in x (e.g. y = x**2 + sin(x))
    2) List of (x,y) coordinates

    Returns:
        (str): The user's choice, either "1" or "2".
    """

    while True:
        choice = input("Choose input type:\n"
                       "  1) Equation in x (e.g. y = x**2 + sin(x))\n"
                       "  2) List of (x,y) coordinates\n"
                       "Enter 1 or 2: ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Invalid choice. Please enter 1 or 2.")

def prompt_equation() -> sp.Basic:
    """ Prompt the user for a mathematical equation and parse it using sympy.
    The equation can be in the form of y = f(x) or just f(x).

    Returns:
        (sympy expression): The parsed sympy expression.
    """

    x = sp.symbols('x')
    while True:
        eq_str = input("Enter your equation (e.g. y = x**2 + sin(x) or x**2 + sin(x)): ").strip()
        eq_str = re.sub(r'^\s*[a-zA-Z]\s*=\s*', '', eq_str)
        # allow caret (^) for exponentiation, convert to **
        eq_str = eq_str.replace('^', '**')
        # insert explicit multiplication between number and variable/parenthesis
        eq_str = re.sub(r'(\d)(?=[A-Za-z\(])', r'\1*', eq_str)
        try:
            expr = sp.sympify(eq_str, evaluate=True)
            return sp.simplify(expr)
        except Exception:
            print("Could not parse the equation. Please use valid Python/math syntax.")

def prompt_domain() -> tuple:
    """ Prompt the user for the plotting domain for x.
    The default domain is (-5, 5). The user can enter a custom domain.

    Returns:
        (tuple): A tuple containing the minimum and maximum values for x.
    """

    default = (-5, 5)
    print(f"Enter the plotting domain for x (default {default}):")
    try:
        xmin = float(input(f"  x-min [{default[0]}]: ").strip() or default[0])
        xmax = float(input(f"  x-max [{default[1]}]: ").strip() or default[1])
        if xmin >= xmax:
            print("x-min must be less than x-max. Using default domain.")
            return default
        return (xmin, xmax)
    except ValueError:
        print("Invalid number. Using default domain.")
        return default

def prompt_coordinates() -> list:
    """ Prompt the user for a list of coordinates in the format x,y; x,y; ...
    The coordinates are parsed and returned as a list of tuples.

    Returns:
        (list): A list of tuples containing the coordinates.
    """

    print("Enter your coordinates as x,y pairs separated by semicolons\n"
          "(e.g. 0,0; 1,2; 2,1):")
    while True:
        data = input().strip()
        try:
            pts = []
            for pair in data.split(";"):
                x_str, y_str = pair.split(",")
                x_val = float(x_str)
                y_val = float(y_str)
                pts.append((x_val, y_val))
            if len(pts) < 2:
                print("Need at least two points. Please enter again.")
                continue
            return pts
        except Exception:
            print("Invalid format. Please follow x,y; x,y; ...")

def generate_pgfplots_equation(expr, x_domain) -> str:
    """ Generate TikZ/PGFPlots code for a given equation.
    The equation is converted to a string format suitable for PGFPlots.

    Args:
        expr (sympy expression): The sympy expression to plot.
        x_domain (tuple): The domain for x as a tuple (xmin, xmax).

    Returns:
        (str): The TikZ/PGFPlots code for the equation.
    """

    xmin, xmax = x_domain
    raw = str(expr)
    # then convert ** to ^
    raw = raw.replace('**', '^')
    # replace standalone x with \x, but not inside words like 'exp'
    raw = re.sub(r'(?<![A-Za-z])x(?![A-Za-z])', r'\\x', raw)
    # convert log(...) to ln(...) for PGFPlots
    raw = raw.replace('log(', 'ln(')
    return (
        PREAMBLE + "\n"
        "\\begin{tikzpicture}  % start TikZ environment\n"
        "  \\begin{axis}[  % configure axis settings\n"
        f"    domain={xmin}:{xmax}, samples=200,  % set domain & sampling\n"
        "     axis lines=middle,  % draw axes through origin\n"
        "     xlabel={$x$}, ylabel={$y$},  % label axes\n"
        "     grid=major,  % add major grid lines\n"
        "     enlargelimits=true  % add padding around plot\n"
        "   ]\n"
        f"    \\addplot [smooth, thick] {{ {raw} }};  % draw the curve\n"
        "  \\end{axis}  % end axis environment\n"
        "\\end{tikzpicture}  % end TikZ environment\n"
    )

def generate_tikz_coordinates(points) -> str:
    """ Generate TikZ code for a list of coordinates.
    The coordinates are formatted as a string suitable for PGFPlots.

    Args:
        points (list): A list of tuples containing the coordinates.

    Returns:
        (str): The TikZ code for the coordinates.
    """

    coords_str = " ".join(f"({x},{y})" for x, y in points)
    return (
        PREAMBLE + "\n"
        "\\begin{tikzpicture}  % start TikZ environment\n"
        "  \\begin{axis}[  % configure axis for coordinate plot\n"
        "    axis lines=middle,  % draw axes through origin\n"
        "    grid=major,  % add grid\n"
        "    enlargelimits=true  % add padding around plot\n"
        "  ]\n"
        f"    \\addplot [thick] coordinates {{{coords_str}}};  % plot given coordinates\n"
        "  \\end{axis}  % end axis environment\n"
        "\\end{tikzpicture}  % end TikZ environment\n"
    )

def main():
    """ Main function to run the script.
    """

    choice = prompt_choice()
    if choice == "1":
        expr = prompt_equation()
        x_domain = prompt_domain()
        tikz_code = generate_pgfplots_equation(expr, x_domain)
    else:
        points = prompt_coordinates()
        tikz_code = generate_tikz_coordinates(points)

    print("\nCopy the following TikZ/PGFPlots code:\n")
    print(tikz_code)

if __name__ == "__main__":
    main()