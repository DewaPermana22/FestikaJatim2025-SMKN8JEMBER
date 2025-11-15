import msvcrt
import os
from utils.utils import Colors, colorize

MENU_OPTIONS = [
    "Backup Folder",
    "Sinkronisasi Folder",
    "Bersihkan Folder",
    "Rename File Massal",
    "Keluar",
]

MENU_ICONS = ["💾", "🔄", "🧹", "📝", "🚪"]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_menu(selected_index):
    clear()

    # Header
    print(f"\n{Colors.BOLD_CYAN}  AutoFile Manager{Colors.RESET}")
    print(f"{Colors.CYAN}  Alat untuk mempermudah manajemen file{Colors.RESET}\n")

    # Instruksi
    print(colorize("Gunakan ↑↓ untuk navigasi, ENTER untuk pilih tools\n", Colors.YELLOW))

    # Menu options
    for index, option in enumerate(MENU_OPTIONS):
        icon = MENU_ICONS[index]

        if index == selected_index:
            # Selected item - Vite style dengan '>'
            print(f"{Colors.GREEN}  > {icon}  {option}{Colors.RESET}")
        else:
            # Unselected item
            print(f"{Colors.RESET}    {icon}  {option}{Colors.RESET}")

    print()  # Extra line at bottom


def choose_menu():
    selected = 0

    while True:
        print_menu(selected)
        key = msvcrt.getch()

        if key == b"\xe0":  # Tombol arrow
            key2 = msvcrt.getch()

            if key2 == b"H":  # Arrow up
                selected = (selected - 1) % len(MENU_OPTIONS)

            elif key2 == b"P":  # Arrow down
                selected = (selected + 1) % len(MENU_OPTIONS)

        elif key == b"\r":  # Enter
            return selected
