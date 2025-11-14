from menu import choose_menu
from modules.backup import run_backup
from modules.sync import run_sync
from modules.cleaner import run_clean
from modules.renamer import run_rename_custom_name, run_rename_with_pattern
from utils.utils import *


def interactive_backup():
    print_header("💾 Backup Folder")
    
    src = get_input("📂 Folder sumber: ")
    dst = get_input("📁 Folder tujuan: ")
    incremental = get_yes_no("⚡ Incremental backup?")
    timestamp = get_yes_no("🕐 Tambahkan timestamp?")
    
    print()
    run_backup(src, dst, incremental, timestamp)
    
    print_info("Tekan ENTER untuk kembali ke menu...")
    input()


def interactive_sync():
    print_header("🔄 Sinkronisasi Folder")
    
    folder1 = get_input("📂 Folder 1: ")
    folder2 = get_input("📂 Folder 2: ")
    twoway = get_yes_no("↔️  Two-way sync?")
    
    print()
    run_sync(folder1, folder2, twoway)
    
    print_info("Tekan ENTER untuk kembali ke menu...")
    input()


def interactive_clean():
    print_header("🧹 Bersihkan Folder")
    
    folder = get_input("📂 Folder: ")
    days_input = get_input("📅 Hapus file lebih tua dari (hari) [default: 7]: ")
    days = int(days_input) if days_input else 7
    ext = get_input("🔍 Filter ekstensi (opsional, misal: .txt): ") or None
    
    print()
    run_clean(folder, days, ext)
    
    print_info("Tekan ENTER untuk kembali ke menu...")
    input()


def interactive_rename():
    print_header("📝 Rename File Massal")
    
    folder = get_input("📂 Folder: ")
    option_rename = get_yes_no("✏️  Ingin menambahkan prefix/suffix/ganti teks?")
    if not option_rename:
        replace_new_name = get_input("🔄 Masukkan Nama File Baru: ") or None
        start_input_custom = get_input("🔢 Nomor awal [default: 1]: ")
        start_custom = int(start_input_custom) if start_input_custom else 1
        print()
        run_rename_custom_name(folder, replace_new_name, start=start_custom)
        return
    
    # Penjelasan fitur
    print(f"\n{Colors.BOLD_CYAN}💡 Penjelasan Fitur:{Colors.RESET}")
    print(f"{Colors.YELLOW}  • Prefix: Tambah teks di DEPAN nama file{Colors.RESET}")
    print(f"{Colors.YELLOW}  • Suffix: Tambah teks di BELAKANG nama file (sebelum ekstensi){Colors.RESET}")
    print(f"{Colors.YELLOW}  • Ganti/Hapus teks: HAPUS teks tertentu dari nama file lama{Colors.RESET}")
    print(f"{Colors.YELLOW}  • Hapus timestamp dari file{Colors.RESET}")
    print(f"{Colors.YELLOW}  • Nomor: Semua file akan diberi nomor urut otomatis{Colors.RESET}\n")
    
    prefix = get_input("➕ Prefix - tambah di depan (opsional): ") or None
    suffix = get_input("➕ Suffix - tambah di belakang (opsional): ") or None
    
    print(f"\n{Colors.CYAN}Contoh: Jika file bernama 'foto_lama.jpg' dan Anda isi 'lama',")
    print(f"        maka 'lama' akan DIHAPUS menjadi 'foto_.jpg'{Colors.RESET}")
    replace = get_input("🔄 Hapus teks dari nama lama (opsional): ") or None
    delete_ts = get_yes_no("🕐 Hapus timestamp dari nama file?")
    start_input = get_input("🔢 Nomor awal [default: 1]: ")
    start = int(start_input) if start_input else 1
    
    print()
    run_rename_with_pattern(folder, prefix=prefix, suffix=suffix, replace=replace, start=start, remove_ts=delete_ts)
    
    print_info("Tekan ENTER untuk kembali ke menu...")
    input()


def main():
    while True:
        pilihan = choose_menu()

        if pilihan == 0:
            interactive_backup()
        elif pilihan == 1:
            interactive_sync()
        elif pilihan == 2:
            interactive_clean()
        elif pilihan == 3:
            interactive_rename()
        elif pilihan == 4:
            print_colored("\n👋 Terima kasih telah menggunakan AutoFile Manager!\n", Colors.BOLD_GREEN)
            break


if __name__ == "__main__":
    main()
