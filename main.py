from menu import choose_menu
from modules.backup import run_backup
from modules.sync import run_sync
from modules.cleaner import run_clean
from modules.renamer import run_rename_custom_name, run_rename_with_pattern
from utils.utils import *
import os

def print_ascii(path="./utils/banner.txt"):
    with open(path, "r", encoding="utf-8") as f:
        art = f.read()
        print(colorize(art, Colors.BOLD_CYAN))
        
def show_welcome():
    print_ascii()
    print("\n")
    print(
        f"""{Colors.BOLD_CYAN}👋 Selamat datang di AutoFile Manager v1.0! 🗂️
{Colors.CYAN}Alat otomatisasi manajemen file sederhana untuk backup, sinkronisasi, pembersihan, dan rename massal{Colors.RESET}

{Colors.BOLD_YELLOW}⚠️  INFORMASI PENTING:{Colors.RESET}
{Colors.YELLOW}
  1. 📁 Gunakan PATH LENGKAP atau relative path (misal: ./folder)
  2. 🔒 Pastikan Anda punya akses READ/WRITE ke folder target
  3. 💾 BACKUP data penting sebelum menggunakan fitur Clean/Rename
  4. ⚡ Fitur Incremental Backup hanya copy file yang berubah
  5. ↔️  Two-way Sync akan saling menyinkronkan kedua folder
  6. 🧹 Fitur Clean akan MENGHAPUS file - gunakan dengan hati-hati!
  7. 📝 Rename File akan mengubah SEMUA nama file di folder
{Colors.RESET}

{Colors.BOLD_GREEN}💡 TIPS:{Colors.RESET}
{Colors.GREEN}
  • Tekan Ctrl+C kapan saja untuk keluar
  • Gunakan Tab untuk auto-complete path (jika terminal support)
  • Test dulu dengan folder dummy sebelum ke data real
  • Lihat contoh di dokumentasi: README.md
{Colors.RESET}
"""
    )
    input(f"{Colors.CYAN}Tekan ENTER untuk melanjutkan...{Colors.RESET}")
    print()


def validate_path(path, must_exist=True):
    """Validasi path yang diinput user"""
    if not path or path.strip() == "":
        return False, "Path tidak boleh kosong!"

    path = path.strip()

    if must_exist and not os.path.exists(path):
        return False, f"Path tidak ditemukan: {path}"

    return True, path


def interactive_backup():
    print_header("💾 Backup Folder")

    print(
        f"{Colors.CYAN}ℹ️  Info: Backup akan menyalin semua file dari folder sumber ke tujuan{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         Incremental: Hanya copy file baru/berubah (hemat waktu){Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         Timestamp: Tambah tanggal-waktu di nama folder backup{Colors.RESET}\n"
    )

    # Input dan validasi source
    while True:
        src = get_input("📂 Folder sumber: ")
        valid, result = validate_path(src, must_exist=True)
        if valid:
            src = result
            break
        else:
            print_error(f"❌ {result}")

    # Input destination (tidak perlu exist, akan dibuat otomatis)
    dst = get_input("📁 Folder tujuan: ")

    # Konfirmasi info
    print(f"\n{Colors.BOLD_CYAN}📋 Ringkasan:{Colors.RESET}")
    print(f"   Dari: {Colors.GREEN}{os.path.abspath(src)}{Colors.RESET}")
    print(f"   Ke:   {Colors.GREEN}{os.path.abspath(dst)}{Colors.RESET}\n")

    incremental = get_yes_no("⚡ Incremental backup?")
    timestamp = get_yes_no("🕐 Tambahkan timestamp?")

    # Konfirmasi final
    print()
    confirm = get_yes_no("✅ Lanjutkan backup?")
    if not confirm:
        print_warning("❌ Backup dibatalkan")
        input("\nTekan ENTER untuk kembali...")
        return

    print()
    run_backup(src, dst, incremental, timestamp)

    print_info("\nTekan ENTER untuk kembali ke menu...")
    input()


def interactive_sync():
    print_header("🔄 Sinkronisasi Folder")

    print(f"{Colors.CYAN}ℹ️  Info: Sync akan menyamakan isi kedua folder{Colors.RESET}")
    print(
        f"{Colors.YELLOW}         One-way: Folder 1 → Folder 2 (folder 2 jadi sama dengan folder 1){Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         Two-way: Folder 1 ↔️ Folder 2 (saling sinkron){Colors.RESET}\n"
    )

    # Input dan validasi folder1
    while True:
        folder1 = get_input("📂 Folder 1: ")
        valid, result = validate_path(folder1, must_exist=True)
        if valid:
            folder1 = result
            break
        else:
            print_error(f"❌ {result}")

    # Input folder2 (akan dibuat jika belum ada)
    folder2 = get_input("📂 Folder 2: ")

    # Konfirmasi info
    print(f"\n{Colors.BOLD_CYAN}📋 Ringkasan:{Colors.RESET}")
    print(f"   Folder 1: {Colors.GREEN}{os.path.abspath(folder1)}{Colors.RESET}")
    print(f"   Folder 2: {Colors.GREEN}{os.path.abspath(folder2)}{Colors.RESET}\n")

    twoway = get_yes_no("↔️  Two-way sync?")

    if twoway:
        print_warning("\n⚠️  Two-way sync akan mengubah KEDUA folder!")
    else:
        print_info("\n→  One-way sync: Folder 2 akan disamakan dengan Folder 1")

    # Konfirmasi final
    print()
    confirm = get_yes_no("✅ Lanjutkan sinkronisasi?")
    if not confirm:
        print_warning("❌ Sinkronisasi dibatalkan")
        input("\nTekan ENTER untuk kembali...")
        return

    print()
    run_sync(folder1, folder2, twoway)

    print_info("\nTekan ENTER untuk kembali ke menu...")
    input()


def interactive_clean():
    print_header("🧹 Bersihkan Folder")

    print(
        f"{Colors.BOLD_RED}⚠️  PERINGATAN: Fitur ini akan MENGHAPUS file!{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}    File yang dihapus TIDAK bisa dikembalikan!{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}    Gunakan dengan hati-hati pada data penting!{Colors.RESET}\n"
    )

    print(
        f"{Colors.CYAN}ℹ️  Info: Clean akan menghapus file lama berdasarkan tanggal modifikasi{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         Contoh: Input '7' = hapus file lebih dari 7 hari{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         Filter ekstensi: '.txt' atau '.log' (opsional){Colors.RESET}\n"
    )

    # Input dan validasi folder
    while True:
        folder = get_input("📂 Folder: ")
        valid, result = validate_path(folder, must_exist=True)
        if valid:
            folder = result
            break
        else:
            print_error(f"❌ {result}")

    # Input hari
    while True:
        days_input = get_input("📅 Hapus file lebih tua dari (hari) [default: 7]: ")
        if days_input == "":
            days = 7
            break
        try:
            days = int(days_input)
            if days <= 0:
                print_error("❌ Jumlah hari harus lebih dari 0!")
                continue
            break
        except ValueError:
            print_error("❌ Input harus berupa angka!")

    ext = get_input("🔍 Filter ekstensi (opsional, misal: .txt): ") or None

    # Konfirmasi info
    print(f"\n{Colors.BOLD_CYAN}📋 Ringkasan:{Colors.RESET}")
    print(f"   Folder: {Colors.GREEN}{os.path.abspath(folder)}{Colors.RESET}")
    print(f"   Hapus file lebih tua dari: {Colors.YELLOW}{days} hari{Colors.RESET}")
    if ext:
        print(f"   Filter ekstensi: {Colors.YELLOW}{ext}{Colors.RESET}")
    else:
        print(f"   Filter ekstensi: {Colors.YELLOW}Semua file{Colors.RESET}")

    print(
        f"\n{Colors.BOLD_RED}⚠️  File akan dipindai dulu, Anda bisa review sebelum hapus{Colors.RESET}\n"
    )

    print()
    run_clean(folder, days, ext)

    print_info("\nTekan ENTER untuk kembali ke menu...")
    input()


def interactive_rename():
    print_header("📝 Rename File Massal")

    print(
        f"{Colors.CYAN}ℹ️  Info: Rename akan mengubah nama SEMUA file di folder{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         Backup folder dulu jika data penting!{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}         File akan diberi nomor urut otomatis{Colors.RESET}\n"
    )

    # Input dan validasi folder
    while True:
        folder = get_input("📂 Folder: ")
        valid, result = validate_path(folder, must_exist=True)
        if valid:
            folder = result
            break
        else:
            print_error(f"❌ {result}")

    # Hitung jumlah file
    try:
        files_count = len(
            [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        )
        print(
            f"\n{Colors.CYAN}📊 Ditemukan {Colors.BOLD_CYAN}{files_count}{Colors.CYAN} file di folder ini{Colors.RESET}\n"
        )
    except Exception:
        pass

    option_rename = get_yes_no("✏️  Ingin menambahkan prefix/suffix/ganti teks?")

    if not option_rename:
        # Mode: Custom Name (ganti semua nama)
        print(f"\n{Colors.BOLD_YELLOW}📝 Mode: Custom Name{Colors.RESET}")
        print(
            f"{Colors.YELLOW}   Semua file akan dinamai: [NamaBaru]_001, [NamaBaru]_002, ...{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}   Contoh: Input 'Photo' → Photo_001.jpg, Photo_002.jpg{Colors.RESET}\n"
        )

        replace_new_name = get_input("🔄 Masukkan Nama File Baru: ") or None
        if not replace_new_name:
            print_error("❌ Nama file tidak boleh kosong!")
            input("\nTekan ENTER untuk kembali...")
            return

        start_input_custom = get_input("🔢 Nomor awal [default: 1]: ")
        start_custom = int(start_input_custom) if start_input_custom else 1

        # Konfirmasi
        print(f"\n{Colors.BOLD_CYAN}📋 Ringkasan:{Colors.RESET}")
        print(f"   {files_count} file akan direname menjadi:")
        print(
            f"   {Colors.GREEN}{replace_new_name}_{start_custom:03d}.[ext]{Colors.RESET}"
        )
        print(
            f"   {Colors.GREEN}{replace_new_name}_{start_custom+1:03d}.[ext]{Colors.RESET}"
        )
        print(f"   {Colors.GREEN}...{Colors.RESET}\n")

        confirm = get_yes_no("✅ Lanjutkan rename?")
        if not confirm:
            print_warning("❌ Rename dibatalkan")
            input("\nTekan ENTER untuk kembali...")
            return

        print()
        run_rename_custom_name(folder, replace_new_name, start=start_custom)

    else:
        # Mode: Pattern (prefix/suffix/replace)
        print(f"\n{Colors.BOLD_YELLOW}📝 Mode: Pattern{Colors.RESET}")
        print(f"\n{Colors.BOLD_CYAN}💡 Penjelasan Fitur:{Colors.RESET}")
        print(
            f"{Colors.YELLOW}  • Prefix: Tambah teks di DEPAN nama file{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}    Contoh: file.txt → PREFIX_file_001.txt{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}  • Suffix: Tambah teks di BELAKANG nama file (sebelum ekstensi){Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}    Contoh: file.txt → file_SUFFIX_001.txt{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}  • Ganti/Hapus teks: HAPUS teks tertentu dari nama file lama{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}    Contoh: old_file.txt (hapus 'old') → _file_001.txt{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}  • Hapus timestamp: Hapus pola tanggal seperti 20231215, 2023-12-15{Colors.RESET}"
        )
        print(
            f"{Colors.YELLOW}  • Nomor: Semua file akan diberi nomor urut otomatis (_001, _002, ...){Colors.RESET}\n"
        )

        prefix = get_input("➕ Prefix - tambah di depan (opsional): ") or None
        suffix = get_input("➕ Suffix - tambah di belakang (opsional): ") or None

        print(
            f"\n{Colors.CYAN}💡 Tips: Jika file bernama 'foto_lama.jpg' dan Anda isi 'lama',"
        )
        print(f"        maka 'lama' akan DIHAPUS menjadi 'foto__001.jpg'{Colors.RESET}")
        replace = get_input("🔄 Hapus teks dari nama lama (opsional): ") or None

        delete_ts = get_yes_no("🕐 Hapus timestamp dari nama file?")

        start_input = get_input("🔢 Nomor awal [default: 1]: ")
        start = int(start_input) if start_input else 1

        # Konfirmasi
        print(f"\n{Colors.BOLD_CYAN}📋 Ringkasan:{Colors.RESET}")
        print(f"   Folder: {Colors.GREEN}{os.path.abspath(folder)}{Colors.RESET}")
        print(f"   Jumlah file: {Colors.YELLOW}{files_count}{Colors.RESET}")
        if prefix:
            print(f"   Prefix: {Colors.GREEN}{prefix}{Colors.RESET}")
        if suffix:
            print(f"   Suffix: {Colors.GREEN}{suffix}{Colors.RESET}")
        if replace:
            print(f"   Hapus teks: {Colors.RED}{replace}{Colors.RESET}")
        if delete_ts:
            print(f"   Hapus timestamp: {Colors.YELLOW}Ya{Colors.RESET}")
        print(f"   Nomor mulai dari: {Colors.CYAN}{start}{Colors.RESET}\n")

        confirm = get_yes_no("✅ Lanjutkan rename?")
        if not confirm:
            print_warning("❌ Rename dibatalkan")
            input("\nTekan ENTER untuk kembali...")
            return

        print()
        run_rename_with_pattern(
            folder,
            prefix=prefix,
            suffix=suffix,
            replace=replace,
            start=start,
            remove_ts=delete_ts,
        )

    print_info("\nTekan ENTER untuk kembali ke menu...")
    input()


def main():
    """Main function"""
    try:
        show_welcome()

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
                print(
                    f"\n{Colors.BOLD_GREEN}╔══════════════════════════════════════════╗{Colors.RESET}"
                )
                print(
                    f"{Colors.BOLD_GREEN}║   👋 Terima kasih telah menggunakan     ║{Colors.RESET}"
                )
                print(
                    f"{Colors.BOLD_GREEN}║       AutoFile Manager v1.0! 🗂️         ║{Colors.RESET}"
                )
                print(
                    f"{Colors.BOLD_GREEN}╚══════════════════════════════════════════╝{Colors.RESET}\n"
                )
                print(
                    f"{Colors.CYAN}💡 Tips: Jalankan 'python test_autofile.py' untuk testing{Colors.RESET}"
                )
                print(
                    f"{Colors.CYAN}🐛 Bug report: Hubungi developer atau buat issue{Colors.RESET}\n"
                )
                break

    except KeyboardInterrupt:
        print(
            f"\n\n{Colors.YELLOW}⚠️  Program dihentikan oleh user (Ctrl+C){Colors.RESET}"
        )
        print(f"{Colors.CYAN}👋 Sampai jumpa!{Colors.RESET}\n")
    except Exception as e:
        print_error(f"\n❌ Terjadi error tidak terduga: {str(e)}")
        print(f"{Colors.YELLOW}💡 Silakan restart aplikasi{Colors.RESET}\n")


if __name__ == "__main__":
    main()
