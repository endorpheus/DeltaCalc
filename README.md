# Δ% Calculator

A simple utility for calculating percentage differences between two values, available in both GUI (Python/Qt) and CLI (C) versions. 

## What is Δ% (Delta Percentage)?

Delta can be used for a number of differnt types of mathematical expressions revolving around the differences between two points or numbers. For our purposes, Delta percentage (Δ%) represents how much two values differ, expressed as a percentage of the larger value. The calculation finds how much smaller one value is compared to the other.

### Formula

```
Δ% = (1 - smaller_value/larger_value) × 100
```

The result tells you what percentage smaller the smaller value is compared to the larger value.

### Simple Examples

1. Beer Ratings Example:
   ```
   Rater 1: 3.58
   Rater 2: 4.23
   
   Δ% = (1 - 3.58/4.23) × 100 = 15.37%
   
   This means:
   - 3.58 is 15.37% smaller than 4.23
   - 3.58 is 84.63% of 4.23
   ```

2. Price Comparison Example:
   ```
   Store A: $75
   Store B: $100
   
   Δ% = (1 - 75/100) × 100 = 25%
   
   This means:
   - Store A's price is 25% lower than Store B
   - Store A's price is 75% of Store B's price
   ```

## Python GUI Version

### Features
- Clean, modern interface
- Real-time calculations
- Copy results with a click
- Supports decimal precision
- Shows both percentage difference and proportion
- System theme integration

### Requirements
- Python 3.6+
- PyQt5

### Installation

1. Install dependencies:
```bash
pip install PyQt5
```

2. Clone the repository:
```bash
git clone https://github.com/endorpheus/DeltaCalc
cd DeltaCalc
```

3. Run the application:
```bash
python delta_calc.py
```

### Usage
1. Enter any two values in the input fields
2. Results update automatically showing:
   - The larger value
   - The smaller value
   - The percentage difference (Δ%)
   - The proportion of smaller to larger
3. Click on any result to copy it to clipboard
4. Use the Clear button to reset values

## C CLI Version

### Features
- Command-line interface
- Interactive and direct modes
- High precision calculations
- Clear, formatted output
- Simple, intuitive results

### Requirements
- C compiler (gcc, clang, etc.)
- Standard C library
- Math library

### Installation

1. Clone the repository:
```bash
git clone https://github.com/endorpheus/DeltaCalc
cd DeltaCalc
```

2. Compile the program:
```bash
gcc -o delta_calc delta_calc.c -lm
```

3. (Optional) Install system-wide:
```bash
sudo cp delta_calc /usr/local/bin/
```

### Usage

#### Command Line Mode
```bash
# Direct calculation
delta_calc 3.58 4.23

# Show help
delta_calc -h
```

#### Interactive Mode
```bash
# Start interactive session
delta_calc

# Then follow the prompts:
First value: 3.58
Second value: 4.23
```

### Command Reference
- `h` or `--help`: Show help message
- `q`: Quit (interactive mode)

## Common Use Cases

1. **Price Comparisons**
   ```
   Old price: $10
   New price: $12
   Δ% = 16.67%
   The old price is 83.33% of the new price
   ```

2. **Performance Metrics**
   ```
   Previous score: 85
   Current score: 100
   Δ% = 15%
   The previous score was 85% of the current score
   ```

3. **Ratings Analysis**
   ```
   Rating 1: 4.0
   Rating 2: 4.5
   Δ% = 11.11%
   The lower rating is 88.89% of the higher rating
   ```

## Special Cases

Both versions handle several special cases:
1. When both values are zero:
   - Reports "Both values are zero"
2. When one value is zero:
   - Reports "Cannot divide by zero"
3. Invalid inputs:
   - Shows appropriate error messages
   - Allows retry in interactive mode

## Benefits of This Approach

This calculator uses a straightforward percentage difference that:
1. Is intuitive to understand
2. Provides clear context for the difference
3. Shows both the difference and the proportion
4. Works well for comparing ratings, prices, measurements, or any numerical values

## Thanks for Looking!
