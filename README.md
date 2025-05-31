# PGFPlots Generator

A Python script that generates TikZ/PGFPlots code for plotting mathematical functions or coordinates in LaTeX documents.

## Description

This tool helps you generate TikZ/PGFPlots code for:
- Plotting mathematical functions (e.g., y = x² + sin(x))
- Plotting coordinate points
- Customizing plot appearance (colors, labels, domain)

The generated code can be directly used in LaTeX documents with the TikZ and PGFPlots packages.

## Features

- Interactive command-line interface
- Support for mathematical functions using Python/sympy syntax
- Support for plotting coordinate points
- Customizable:
  - Plot domain
  - Axis labels
  - Plot color
  - Grid and axis settings
- Automatic conversion of mathematical expressions to PGFPlots syntax
- Generates complete, ready-to-use TikZ/PGFPlots code

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Pgfplots-Generator.git
cd Pgfplots-Generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python pgfplots_generator.py
```

The script will guide you through the following steps:

1. Choose input type:
   - Equation in x (e.g., y = x² + sin(x))
   - List of (x,y) coordinates

2. For equations:
   - Enter your equation
   - Specify the plotting domain
   - Customize axis labels
   - Choose plot color

3. For coordinates:
   - Enter coordinates as x,y pairs separated by semicolons
   - Customize axis labels
   - Choose plot color

4. Copy the generated TikZ/PGFPlots code into your LaTeX document

## Example

Input:
```
Choose input type:
  1) Equation in x (e.g. y = x**2 + sin(x))
  2) List of (x,y) coordinates
Enter 1 or 2: 1

Enter your equation: x^2 + sin(x)
```

Output will be TikZ/PGFPlots code that you can use in your LaTeX document.

## Requirements

- Python 3.x
- sympy
- LaTeX with TikZ and PGFPlots packages

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Author

Muneeb Azfar Nafees

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 