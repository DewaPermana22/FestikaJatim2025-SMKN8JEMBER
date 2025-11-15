import msvcrt
import os
import sys
from utils.utils import Colors, colorize

MENU_OPTIONS = [
    "Backup Folder",
    "Sinkronisasi Folder",
    "Bersihkan Folder",
    "Rename File Massal",
    "Keluar",
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def hide_cursor():
    """Sembunyikan cursor untuk tampilan lebih bersih"""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    """Tampilkan kembali cursor"""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def move_cursor_up(lines):
    """Gerakkan cursor ke atas sebanyak n baris"""
    sys.stdout.write(f"\033[{lines}A")
    sys.stdout.flush()


def clear_line():
    """Bersihkan baris saat ini"""
    sys.stdout.write("\033[2K\r")
    sys.stdout.flush()


def print_menu_header():
    """Print header sekali saja di awal"""
    clear()
    print(f"\n{Colors.BOLD_CYAN}  AutoFile Manager{Colors.RESET}")
    print(f"{Colors.CYAN}  Alat untuk mempermudah manajemen file{Colors.RESET}\n")
    print(
        colorize("Gunakan ↑↓ untuk navigasi, ENTER untuk pilih tools\n", Colors.YELLOW)
    )


def print_menu_options(selected_index):
    """Print hanya menu options yang bisa di-update"""
    for index, option in enumerate(MENU_OPTIONS):
        clear_line()  # Bersihkan baris saat ini

        if index == selected_index:
            print(f"{Colors.GREEN}  > •  {option}{Colors.RESET}")
        else:
            print(f"{Colors.RESET}    •  {option}{Colors.RESET}")

    print()  # Extra line at bottom


def choose_menu():
    selected = 0

    # Print header sekali saja
    print_menu_header()

    # Print menu pertama kali
    print_menu_options(selected)

    hide_cursor()

    try:
        while True:
            key = msvcrt.getch()

            if key == b"\xe0":  # Tombol arrow
                key2 = msvcrt.getch()

                if key2 == b"H":  # Arrow up
                    new_selected = (selected - 1) % len(MENU_OPTIONS)

                    if new_selected != selected:
                        selected = new_selected
                        # Gerakkan cursor ke atas sejumlah menu + 1 baris extra
                        move_cursor_up(len(MENU_OPTIONS) + 1)
                        # Update hanya menu options
                        print_menu_options(selected)

                elif key2 == b"P":  # Arrow down
                    new_selected = (selected + 1) % len(MENU_OPTIONS)

                    if new_selected != selected:
                        selected = new_selected
                        # Gerakkan cursor ke atas sejumlah menu + 1 baris extra
                        move_cursor_up(len(MENU_OPTIONS) + 1)
                        # Update hanya menu options
                        print_menu_options(selected)

            elif key == b"\r":  # Enter
                return selected

    finally:
        show_cursor()


# Alternatif dengan library colorama (install: pip install colorama)
def choose_menu_colorama():
    """Versi menggunakan colorama untuk kompatibilitas lebih baik"""
    try:
        from colorama import init, AnsiToWin32
        import sys

        # Initialize colorama untuk Windows
        init()

        selected = 0
        print_menu_header()
        print_menu_options(selected)
        hide_cursor()

        try:
            while True:
                key = msvcrt.getch()

                if key == b"\xe0":
                    key2 = msvcrt.getch()

                    if key2 == b"H":  # Arrow up
                        new_selected = (selected - 1) % len(MENU_OPTIONS)

                        if new_selected != selected:
                            selected = new_selected
                            move_cursor_up(len(MENU_OPTIONS) + 1)
                            print_menu_options(selected)

                    elif key2 == b"P":  # Arrow down
                        new_selected = (selected + 1) % len(MENU_OPTIONS)

                        if new_selected != selected:
                            selected = new_selected
                            move_cursor_up(len(MENU_OPTIONS) + 1)
                            print_menu_options(selected)

                elif key == b"\r":
                    return selected

        finally:
            show_cursor()

    except ImportError:
        print("Install colorama untuk pengalaman lebih baik: pip install colorama")
        return choose_menu()
