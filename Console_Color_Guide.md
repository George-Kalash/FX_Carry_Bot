# Console Text Color in Python

This guide explains how to add colors to your console output in Python for better visualization and readability.

## Method 1: ANSI Escape Codes (Cross-platform)

The simplest way to add colors without external dependencies is using ANSI escape codes.

### Basic Usage

```python
# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'  # Reset to default color

# Print colored text
print(f"{RED}This is red text{RESET}")
print(f"{GREEN}This is green text{RESET}")
print(f"{YELLOW}This is yellow text{RESET}")
```

### Complete Color Reference

```python
# Text colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Bright/bold colors
BRIGHT_BLACK = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'

# Background colors
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'

# Text styles
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
REVERSE = '\033[7m'

# Reset
RESET = '\033[0m'
```

### Examples

```python
# Combining styles
print(f"{BOLD}{RED}Bold Red Text{RESET}")
print(f"{UNDERLINE}{BLUE}Underlined Blue Text{RESET}")
print(f"{BG_YELLOW}{BLACK}Black text on yellow background{RESET}")

# Multiple styles
print(f"{BOLD}{UNDERLINE}{GREEN}Bold, Underlined Green{RESET}")
```

## Method 2: Using Colorama (Recommended for Windows compatibility)

Colorama makes ANSI escape codes work on Windows and provides a cleaner API.

### Installation

```bash
pip install colorama
```

### Basic Usage

```python
from colorama import Fore, Back, Style, init

# Initialize colorama (optional on most systems, required on Windows)
init(autoreset=True)

# Print colored text
print(Fore.RED + 'This is red text')
print(Fore.GREEN + 'This is green text')
print(Fore.YELLOW + 'This is yellow text')

# With autoreset=True, you don't need to add Style.RESET_ALL
# Without autoreset:
print(Fore.RED + 'This is red' + Style.RESET_ALL)
```

### Complete Colorama Reference

```python
from colorama import Fore, Back, Style

# Foreground colors
Fore.BLACK
Fore.RED
Fore.GREEN
Fore.YELLOW
Fore.BLUE
Fore.MAGENTA
Fore.CYAN
Fore.WHITE
Fore.RESET

# Bright foreground colors
Fore.LIGHTBLACK_EX
Fore.LIGHTRED_EX
Fore.LIGHTGREEN_EX
Fore.LIGHTYELLOW_EX
Fore.LIGHTBLUE_EX
Fore.LIGHTMAGENTA_EX
Fore.LIGHTCYAN_EX
Fore.LIGHTWHITE_EX

# Background colors
Back.BLACK
Back.RED
Back.GREEN
Back.YELLOW
Back.BLUE
Back.MAGENTA
Back.CYAN
Back.WHITE
Back.RESET

# Styles
Style.DIM
Style.NORMAL
Style.BRIGHT
Style.RESET_ALL
```

### Colorama Examples

```python
from colorama import Fore, Back, Style, init

init(autoreset=True)

# Simple colors
print(Fore.GREEN + 'Success!')
print(Fore.RED + 'Error!')
print(Fore.YELLOW + 'Warning!')

# Combined styles
print(Fore.WHITE + Back.BLUE + Style.BRIGHT + 'Highlighted text')

# F-strings
status = "completed"
print(f"{Fore.GREEN}Task {status}{Style.RESET_ALL}")
```

## Method 3: Rich Library (Advanced)

For more advanced formatting, tables, progress bars, and syntax highlighting.

### Installation

```bash
pip install rich
```

### Basic Usage

```python
from rich import print
from rich.console import Console

console = Console()

# Simple colored print
print("[red]This is red[/red]")
print("[green]This is green[/green]")
print("[bold yellow]Bold yellow text[/bold yellow]")

# Using console
console.print("Hello", style="bold red")
console.print("Success!", style="green on black")
```

## Practical Examples for Trading Bot

### Example 1: Price Change Indicators

```python
# Using ANSI codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def print_price_change(price, previous_price):
    if price > previous_price:
        print(f"{GREEN}↑ ${price:.2f}{RESET}")
    elif price < previous_price:
        print(f"{RED}↓ ${price:.2f}{RESET}")
    else:
        print(f"${price:.2f}")
```

### Example 2: Bar Status Display

```python
from colorama import Fore, Style, init

init(autoreset=True)

def print_bar(bar):
    bucket_time = datetime.fromtimestamp(bar["bucket"], tz=timezone.utc)
    
    # Color based on bar direction (close vs open)
    if bar["close"] > bar["open"]:
        color = Fore.GREEN
        symbol = "▲"
    else:
        color = Fore.RED
        symbol = "▼"
    
    print(f"{color}[{bucket_time}] {symbol} "
          f"O:{bar['open']:.2f} "
          f"H:{bar['high']:.2f} "
          f"L:{bar['low']:.2f} "
          f"C:{bar['close']:.2f}")
```

### Example 3: OHLC Bar with Colors

```python
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_ohlc_bar(bar):
    bucket_time = datetime.fromtimestamp(bar["bucket"], tz=timezone.utc)
    
    # Determine if bullish or bearish
    if bar["close"] >= bar["open"]:
        direction_color = GREEN
        direction = "BULL"
    else:
        direction_color = RED
        direction = "BEAR"
    
    print(f"[{CYAN}{bucket_time}{RESET}] {direction_color}{direction}{RESET} "
          f"O:{YELLOW}{bar['open']:.2f}{RESET} "
          f"H:{GREEN}{bar['high']:.2f}{RESET} "
          f"L:{RED}{bar['low']:.2f}{RESET} "
          f"C:{direction_color}{bar['close']:.2f}{RESET}")
```

### Example 4: Trading Signals

```python
from colorama import Fore, Back, Style, init

init(autoreset=True)

def print_signal(signal_type, price, reason):
    if signal_type == "BUY":
        print(f"{Back.GREEN}{Fore.BLACK} BUY {Style.RESET_ALL} "
              f"@ ${price:.2f} - {reason}")
    elif signal_type == "SELL":
        print(f"{Back.RED}{Fore.WHITE} SELL {Style.RESET_ALL} "
              f"@ ${price:.2f} - {reason}")
    else:
        print(f"{Fore.YELLOW}HOLD{Style.RESET_ALL} @ ${price:.2f}")

# Usage
print_signal("BUY", 150.25, "MACD crossover")
print_signal("SELL", 152.80, "Take profit hit")
print_signal("HOLD", 151.50, "Waiting for signal")
```

## Helper Function for Easy Use

```python
class Colors:
    """Helper class for console colors"""
    
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def red(text):
        return f"{Colors.RED}{text}{Colors.RESET}"
    
    @staticmethod
    def green(text):
        return f"{Colors.GREEN}{text}{Colors.RESET}"
    
    @staticmethod
    def yellow(text):
        return f"{Colors.YELLOW}{text}{Colors.RESET}"
    
    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.RESET}"
    
    @staticmethod
    def bold(text):
        return f"{Colors.BOLD}{text}{Colors.RESET}"

# Usage
print(Colors.green("Success!"))
print(Colors.red("Error!"))
print(Colors.yellow("Warning!"))
print(Colors.bold(Colors.blue("Important message")))
```

## Platform Compatibility

- **macOS/Linux**: ANSI codes work natively in Terminal
- **Windows**: 
  - Windows 10+ supports ANSI codes in Command Prompt and PowerShell
  - For older Windows, use `colorama` library
- **VS Code Terminal**: Full ANSI support on all platforms

## Tips

1. **Always reset colors**: Use `RESET` or `Style.RESET_ALL` to avoid color bleeding
2. **Use autoreset**: With colorama, `init(autoreset=True)` automatically resets after each print
3. **Test compatibility**: If targeting multiple platforms, use `colorama`
4. **Don't overuse**: Too many colors can be distracting
5. **Accessibility**: Consider users who may have color blindness; use symbols too (▲, ▼, ✓, ✗)

## Disabling Colors

For logging to files or when colors aren't supported:

```python
import sys

USE_COLORS = sys.stdout.isatty()  # Only use colors if output is a terminal

def colored_text(text, color_code):
    if USE_COLORS:
        return f"{color_code}{text}{RESET}"
    return text
```
