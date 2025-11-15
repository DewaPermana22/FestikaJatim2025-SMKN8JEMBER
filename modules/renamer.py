import os
import sys
import re
from utils.utils import print_error, print_warning, print_info, print_success

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from colors import *


def remove_timestamp(filename):
    """
    Menghapus pola timestamp umum dari nama file.
    Contoh:
    - IMG_20230115_123456.jpg → IMG.jpg
    - Foto_2023-01-15_12-34-56.jpg → Foto.jpg
    - 20230115_123456.jpg → .jpg (jika hanya timestamp)
    """
    # Pola timestamp yang umum ditemukan di foto
    patterns = [
        # Pattern 1: IMG_YYYYMMDD_HHMMSS
        r"_\d{8}_\d{6}",
        # Pattern 2: YYYYMMDD_HHMMSS
        r"\d{8}_\d{6}",
        # Pattern 3: YYYY-MM-DD_HH-MM-SS
        r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}",
        # Pattern 4: YYYYMMDD_HHMM
        r"\d{8}_\d{4}",
        # Pattern 5: YYYY-MM-DD HH.MM.SS
        r"\d{4}-\d{2}-\d{2} \d{2}\.\d{2}\.\d{2}",
    ]

    name, ext = os.path.splitext(filename)
    original_name = name

    for pattern in patterns:
        name = re.sub(pattern, "", name)

    # Jika setelah penghapusan nama menjadi kosong, gunakan nama default
    if not name.strip():
        name = "foto"

    return name + ext, original_name != name


def run_rename_with_pattern(folder, prefix=None, suffix=None, replace=None, start=1, remove_ts=False):
    """
    Melakukan rename massal dengan PATTERN - menambahkan prefix/suffix ke nama file yang sudah ada.

    Parameters:
        folder  : folder target berisi file yang akan di-rename
        prefix  : teks di depan nama baru (opsional)
        suffix  : teks di belakang nama baru sebelum ekstensi (opsional)
        replace : HAPUS teks tertentu pada nama file lama (opsional)
        start   : nomor awal jika menggunakan penomoran otomatis
        remove_ts : hapus timestamp dari nama file (opsional)

    Contoh penggunaan:
        File awal: "foto_lama_001.jpg"
        - prefix = "liburan_"
        - suffix = "_edited"
        - replace = "lama_"
        - remove_ts = True
        - start = 1
        Hasil: "liburan_foto_001_edited_1.jpg"
    """

    # --- CEK FOLDER ---
    if not os.path.isdir(folder):
        print_error(f"Folder tidak ditemukan: {folder}")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    files.sort()  # Supaya urut dan konsisten

    if not files:
        print_warning("Tidak ada file dalam folder.")
        return

    print_info(f"Total file ditemukan: {len(files)}")

    # Preview 5 file pertama
    print(f"\n{Colors.BOLD_MAGENTA}📋 File yang Akan Direname:{Colors.RESET}")
    for i, f in enumerate(files[:5], 1):
        print(f"{Colors.CYAN}  {i}. {f}{Colors.RESET}")
    if len(files) > 5:
        print(f"{Colors.CYAN}  ... dan {len(files) - 5} file lainnya{Colors.RESET}")

    # Tampilkan aturan yang akan diterapkan
    print(f"\n{Colors.BOLD_YELLOW}⚙️  Aturan Rename (PATTERN):{Colors.RESET}")
    if prefix:
        print(f"{Colors.GREEN}  ✓ Prefix: '{prefix}' (ditambah di depan){Colors.RESET}")
    if suffix:
        print(f"{Colors.GREEN}  ✓ Suffix: '{suffix}' (ditambah di belakang){Colors.RESET}")
    if replace:
        print(f"{Colors.GREEN}  ✓ Hapus teks: '{replace}' (dihapus dari nama lama){Colors.RESET}")
    if remove_ts:
        print(f"{Colors.GREEN}  ✓ Hapus timestamp: YA{Colors.RESET}")
    print(f"{Colors.GREEN}  ✓ Penomoran: dimulai dari {start}{Colors.RESET}")

    if not prefix and not suffix and not replace and not remove_ts:
        print(f"{Colors.YELLOW}  ⚠ Tidak ada perubahan, hanya penomoran yang ditambahkan{Colors.RESET}")

    # Preview hasil rename
    print(f"\n{Colors.BOLD_MAGENTA}👀 Preview Hasil Rename:{Colors.RESET}")
    counter = start
    for filename in files[:3]:
        name, ext = os.path.splitext(filename)
        new_name = name

        # Tunjukkan step by step
        steps = [f"Nama awal: '{name}'"]

        # 1. HAPUS TIMESTAMP
        if remove_ts:
            name_after_ts, ts_removed = remove_timestamp(filename)
            new_name = os.path.splitext(name_after_ts)[0]
            if ts_removed:
                steps.append(f"Setelah hapus timestamp: '{new_name}'")
            else:
                steps.append(f"Tidak ada timestamp yang dihapus: '{new_name}'")

        # 2. Hapus text
        if replace:
            new_name = new_name.replace(replace, "")
        # 3. tambah prefix
        if prefix:
            new_name = f"{prefix}{new_name}"
        # 4. tambah suffix
        if suffix:
            new_name = f"{new_name}{suffix}"
        # 5. auto numbering
        new_name = f"{new_name}_{counter}"
        new_filename = new_name + ext

        print(f"\n{Colors.CYAN}  File: {filename}{Colors.RESET}")
        for step in steps:
            print(f"{Colors.YELLOW}    → {step}{Colors.RESET}")
        print(f"{Colors.RED}  Hasil: {filename}{Colors.RESET} {Colors.YELLOW}→{Colors.RESET} {Colors.GREEN}{new_filename}{Colors.RESET}")
        counter += 1

    if len(files) > 3:
        print(f"\n{Colors.CYAN}  ... dan {len(files) - 3} file lainnya dengan pola yang sama{Colors.RESET}")

    # Konfirmasi
    print()
    confirm = input(f"{Colors.BOLD_YELLOW}Apakah preview sudah sesuai? Lanjutkan? (y/n): {Colors.RESET}").lower()
    if confirm != "y":
        print_warning("Proses dibatalkan.")
        return

    print(f"\n{Colors.BOLD_CYAN}🚀 Memulai proses rename...{Colors.RESET}\n")

    counter = start
    success = 0
    errors = []

    for filename in files:
        try:
            old_path = os.path.join(folder, filename)

            # Pisahkan nama & ekstensi
            name, ext = os.path.splitext(filename)
            new_name = name

            # 1. hapus TIMESTAMP
            if remove_ts:
                name_after_ts, _ = remove_timestamp(filename)
                new_name = os.path.splitext(name_after_ts)[0]
            # 2. HAPUS TEKS
            if replace:
                new_name = new_name.replace(replace, "")
            # 3. TAMBAH PREFIX
            if prefix:
                new_name = f"{prefix}{new_name}"
            # 4. TAMBAH SUFFIX
            if suffix:
                new_name = f"{new_name}{suffix}"
            # 5. AUTO NUMBERING
            new_name = f"{new_name}_{counter}"
            # 6. GABUNGKAN EKSTENSI
            new_filename = new_name + ext
            new_path = os.path.join(folder, new_filename)
            # Rename file
            os.rename(old_path, new_path)

            print(f"{Colors.GREEN}✓{Colors.RESET} {filename} {Colors.YELLOW}→{Colors.RESET} {Colors.GREEN}{new_filename}{Colors.RESET}")

            success += 1
            counter += 1

        except Exception as e:
            errors.append((filename, str(e)))
            print_error(f"Gagal rename {filename}: {str(e)}")

    # Summary
    print(f"\n{Colors.BOLD_CYAN}{'═' * 50}{Colors.RESET}")
    print_success(f"Berhasil rename {success} file!")

    if errors:
        print_error(f"Gagal rename {len(errors)} file")
        for fname, err in errors:
            print(f"{Colors.RED}  • {fname}: {err}{Colors.RESET}")

    print(f"{Colors.BOLD_CYAN}{'═' * 50}{Colors.RESET}\n")


def run_rename_custom_name(folder, custom_name, start=1):
    """
    Melakukan rename massal dengan CUSTOM NAME - mengganti nama file sepenuhnya.

    Parameters:
        folder      : folder target berisi file yang akan di-rename
        custom_name : nama baru untuk semua file (tanpa ekstensi)
        start       : nomor awal untuk penomoran otomatis

    Contoh penggunaan:
        File awal: "foto_lama_001.jpg", "document.pdf", "data.xlsx"
        - custom_name = "laporan"
        - start = 1
        Hasil: "laporan_1.jpg", "laporan_2.pdf", "laporan_3.xlsx"
    """

    # --- CEK FOLDER ---
    if not os.path.isdir(folder):
        print_error(f"Folder tidak ditemukan: {folder}")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    files.sort()  # Supaya urut dan konsisten

    if not files:
        print_warning("Tidak ada file dalam folder.")
        return

    print_info(f"Total file ditemukan: {len(files)}")

    # Preview 5 file pertama
    print(f"\n{Colors.BOLD_MAGENTA}📋 File yang Akan Direname:{Colors.RESET}")
    for i, f in enumerate(files[:5], 1):
        print(f"{Colors.CYAN}  {i}. {f}{Colors.RESET}")
    if len(files) > 5:
        print(f"{Colors.CYAN}  ... dan {len(files) - 5} file lainnya{Colors.RESET}")

    # Tampilkan aturan yang akan diterapkan
    print(f"\n{Colors.BOLD_YELLOW}⚙️  Aturan Rename (CUSTOM NAME):{Colors.RESET}")
    print(f"{Colors.GREEN}  ✓ Nama baru: '{custom_name}'{Colors.RESET}")
    print(f"{Colors.GREEN}  ✓ Penomoran: dimulai dari {start}{Colors.RESET}")
    print(f"{Colors.YELLOW}  ⚠ Semua nama file lama akan diganti sepenuhnya!{Colors.RESET}")

    # Preview hasil rename
    print(f"\n{Colors.BOLD_MAGENTA}👀 Preview Hasil Rename:{Colors.RESET}")
    counter = start
    for filename in files[:3]:
        _, ext = os.path.splitext(filename)
        new_filename = f"{custom_name}_{counter}{ext}"

        print(f"{Colors.CYAN}  File: {filename}{Colors.RESET}")
        print(f"{Colors.YELLOW}    → Nama awal: '{filename}'{Colors.RESET}")
        print(f"{Colors.YELLOW}    → Setelah custom name + nomor: '{new_filename}'{Colors.RESET}")
        print(f"{Colors.RED}  Hasil: {filename}{Colors.RESET} {Colors.YELLOW}→{Colors.RESET} {Colors.GREEN}{new_filename}{Colors.RESET}")
        counter += 1

    if len(files) > 3:
        print(f"\n{Colors.CYAN}  ... dan {len(files) - 3} file lainnya dengan pola yang sama{Colors.RESET}")

    # Konfirmasi
    print()
    confirm = input(f"{Colors.BOLD_YELLOW}Apakah preview sudah sesuai? Lanjutkan? (y/n): {Colors.RESET}").lower()
    if confirm != "y":
        print_warning("Proses dibatalkan.")
        return

    print(f"\n{Colors.BOLD_CYAN}🚀 Memulai proses rename...{Colors.RESET}\n")

    counter = start
    success = 0
    errors = []

    for filename in files:
        try:
            old_path = os.path.join(folder, filename)

            # Pisahkan ekstensi
            _, ext = os.path.splitext(filename)

            # Buat nama baru dengan custom name + nomor
            new_filename = f"{custom_name}_{counter}{ext}"
            new_path = os.path.join(folder, new_filename)

            # Rename file
            os.rename(old_path, new_path)

            print(f"{Colors.GREEN}✓{Colors.RESET} {filename} {Colors.YELLOW}→{Colors.RESET} {Colors.GREEN}{new_filename}{Colors.RESET}")

            success += 1
            counter += 1

        except Exception as e:
            errors.append((filename, str(e)))
            print_error(f"Gagal rename {filename}: {str(e)}")

    # Summary
    print(f"\n{Colors.BOLD_CYAN}{'═' * 50}{Colors.RESET}")
    print_success(f"Berhasil rename {success} file!")

    if errors:
        print_error(f"Gagal rename {len(errors)} file")
        for fname, err in errors:
            print(f"{Colors.RED}  • {fname}: {err}{Colors.RESET}")

    print(f"{Colors.BOLD_CYAN}{'═' * 50}{Colors.RESET}\n")