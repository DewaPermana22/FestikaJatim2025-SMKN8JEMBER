import msvcrt
import os
from colors import Colors, colorize, print_box

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


def print_banner():
    """Menampilkan banner aplikasi"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║         📁 AutoFile Manager 📁       ║
    ║    Kelola File dengan Mudah & Cepat   ║
    ╚═══════════════════════════════════════╝
    """
    print(colorize(banner, Colors.BOLD_CYAN))


def print_menu(selected_index):
    clear()
    print_banner()

    print(colorize("Gunakan ↑↓ untuk navigasi, ENTER untuk pilih\n", Colors.YELLOW))

    for index, option in enumerate(MENU_OPTIONS):
        icon = MENU_ICONS[index]
        if index == selected_index:
            # Highlight untuk pilihan yang dipilih
            print(
                f"{Colors.BG_CYAN}{Colors.BOLD_WHITE} ▶ {icon} {option} {Colors.RESET}"
            )
        else:
            print(f"{Colors.CYAN}   {icon} {option}{Colors.RESET}")

    print(f"\n{Colors.BOLD_YELLOW}{'─' * 43}{Colors.RESET}")


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
