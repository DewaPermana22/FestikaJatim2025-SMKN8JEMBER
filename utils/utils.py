import os
from datetime import datetime
from colors import Colors

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(timestamp, msg)

def get_input(prompt, color=Colors.BOLD_YELLOW):
    """Helper untuk input dengan warna"""
    return input(f"{color}{prompt}{Colors.RESET}")


def get_yes_no(prompt):
    """Helper untuk input yes/no"""
    response = get_input(f"{prompt} (y/n): ", Colors.BOLD_YELLOW).lower()
    return response == "y"


def colorize(text, color):
    """Menambahkan warna pada teks"""
    return f"{color}{text}{Colors.RESET}"


def print_colored(text, color):
    """Print teks dengan warna"""
    print(colorize(text, color))


def print_success(text):
    """Print pesan sukses (hijau dengan ✓)"""
    print(f"{Colors.BOLD_GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Print pesan error (merah dengan ✗)"""
    print(f"{Colors.BOLD_RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    """Print pesan warning (kuning dengan ⚠)"""
    print(f"{Colors.BOLD_YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text):
    """Print pesan info (biru dengan ℹ)"""
    print(f"{Colors.BOLD_CYAN}ℹ {text}{Colors.RESET}")


def print_header(text):
    """Print header dengan garis"""
    width = len(text) + 4
    print(f"\n{Colors.BOLD_CYAN}{'═' * width}")
    print(f"  {text}  ")
    print(f"{'═' * width}{Colors.RESET}\n")


def print_box(text, color=Colors.BOLD_CYAN):
    """Print teks dalam box"""
    lines = text.split("\n")
    max_len = max(len(line) for line in lines)

    print(f"{color}╔{'═' * (max_len + 2)}╗")
    for line in lines:
        padding = max_len - len(line)
        print(f"║ {line}{' ' * padding} ║")
    print(f"╚{'═' * (max_len + 2)}╝{Colors.RESET}")