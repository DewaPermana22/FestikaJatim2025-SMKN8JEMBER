"""
Script untuk testing semua fitur AutoFile Manager
Jalankan: python test_autofile.py
"""

import os
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path

# Import modules
from modules.backup import run_backup
from modules.sync import run_sync
from modules.cleaner import run_clean
from modules.renamer import run_rename_with_pattern, run_rename_custom_name
from utils.utils import print_header, print_success, print_info, print_warning, Colors

# Folder untuk testing
TEST_DIR = "test_autofile"
TEST_SRC = os.path.join(TEST_DIR, "source")
TEST_DST = os.path.join(TEST_DIR, "destination")
TEST_SYNC1 = os.path.join(TEST_DIR, "sync1")
TEST_SYNC2 = os.path.join(TEST_DIR, "sync2")
TEST_CLEAN = os.path.join(TEST_DIR, "clean")
TEST_RENAME = os.path.join(TEST_DIR, "rename")


def setup_test_environment():
    """Setup folder dan file untuk testing"""
    print_header("🔧 Setup Test Environment")

    # Hapus test folder jika sudah ada
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

    # Buat struktur folder
    os.makedirs(TEST_SRC)
    os.makedirs(TEST_DST)
    os.makedirs(TEST_SYNC1)
    os.makedirs(TEST_SYNC2)
    os.makedirs(TEST_CLEAN)
    os.makedirs(TEST_RENAME)

    # Buat subfolder
    os.makedirs(os.path.join(TEST_SRC, "subfolder1"))
    os.makedirs(os.path.join(TEST_SRC, "subfolder2", "nested"))

    print_info("📁 Membuat file test...")

    # Buat file untuk backup test
    files_to_create = [
        (TEST_SRC, "file1.txt", "Content file 1"),
        (TEST_SRC, "file2.log", "Log content"),
        (TEST_SRC, "document.pdf", "PDF content simulation"),
        (os.path.join(TEST_SRC, "subfolder1"), "nested1.txt", "Nested file 1"),
        (os.path.join(TEST_SRC, "subfolder2", "nested"), "deep.txt", "Deep nested"),
    ]

    for folder, filename, content in files_to_create:
        filepath = os.path.join(folder, filename)
        with open(filepath, "w") as f:
            f.write(content)

    # File untuk sync test
    sync_files = [
        (TEST_SYNC1, "shared.txt", "Shared file"),
        (TEST_SYNC1, "only_in_1.txt", "Only in folder 1"),
        (TEST_SYNC2, "only_in_2.txt", "Only in folder 2"),
    ]

    for folder, filename, content in sync_files:
        with open(os.path.join(folder, filename), "w") as f:
            f.write(content)

    # File untuk clean test (dengan timestamp berbeda)
    print_info("📅 Membuat file dengan berbagai umur...")

    clean_files = [
        ("old_file1.txt", 10),  # 10 hari lalu
        ("old_file2.log", 15),  # 15 hari lalu
        ("recent_file.txt", 2),  # 2 hari lalu
        ("today_file.txt", 0),  # Hari ini
        ("old_doc.pdf", 30),  # 30 hari lalu
    ]

    for filename, days_old in clean_files:
        filepath = os.path.join(TEST_CLEAN, filename)
        with open(filepath, "w") as f:
            f.write(f"File created {days_old} days ago")

        # Ubah timestamp file
        old_time = time.time() - (days_old * 24 * 60 * 60)
        os.utime(filepath, (old_time, old_time))

    # File untuk rename test
    rename_files = [
        "photo_001.jpg",
        "photo_002.jpg",
        "document_old_version.txt",
        "backup_20230115_file.pdf",
        "report_final.docx",
    ]

    for filename in rename_files:
        filepath = os.path.join(TEST_RENAME, filename)
        with open(filepath, "w") as f:
            f.write(f"Content of {filename}")

    print_success("✅ Test environment siap!\n")
    print_info(f"📂 Lokasi: {os.path.abspath(TEST_DIR)}\n")


def test_backup():
    """Test fitur backup"""
    print_header("🧪 TEST 1: Backup")

    print(f"\n{Colors.BOLD_CYAN}Test 1.1: Full Backup{Colors.RESET}")
    print_info(f"Source: {TEST_SRC}")
    print_info(f"Destination: {TEST_DST}/backup_full")
    input("Tekan ENTER untuk mulai...")
    run_backup(
        TEST_SRC,
        os.path.join(TEST_DST, "backup_full"),
        incremental=False,
        timestamp=False,
    )

    print(f"\n{Colors.BOLD_CYAN}Test 1.2: Incremental Backup{Colors.RESET}")
    print_info("Menambahkan file baru...")
    with open(os.path.join(TEST_SRC, "new_file.txt"), "w") as f:
        f.write("New content")

    input("Tekan ENTER untuk incremental backup...")
    run_backup(
        TEST_SRC,
        os.path.join(TEST_DST, "backup_full"),
        incremental=True,
        timestamp=False,
    )

    print(f"\n{Colors.BOLD_CYAN}Test 1.3: Backup dengan Timestamp{Colors.RESET}")
    input("Tekan ENTER untuk backup dengan timestamp...")
    run_backup(TEST_SRC, TEST_DST, incremental=False, timestamp=True)

    print_info("\n✅ Test Backup selesai!\n")
    input("Tekan ENTER untuk lanjut ke test berikutnya...")


def test_sync():
    """Test fitur sync"""
    print_header("🧪 TEST 2: Sync")

    print(f"\n{Colors.BOLD_CYAN}Test 2.1: One-Way Sync{Colors.RESET}")
    print_info(f"Sync dari: {TEST_SYNC1}")
    print_info(f"Ke: {TEST_SYNC2}")
    input("Tekan ENTER untuk mulai...")
    run_sync(TEST_SYNC1, TEST_SYNC2, twoway=False)

    print(f"\n{Colors.BOLD_CYAN}Test 2.2: Two-Way Sync{Colors.RESET}")
    print_info("Menambahkan file baru di kedua folder...")
    with open(os.path.join(TEST_SYNC1, "new_in_1.txt"), "w") as f:
        f.write("New in folder 1")
    with open(os.path.join(TEST_SYNC2, "new_in_2.txt"), "w") as f:
        f.write("New in folder 2")

    input("Tekan ENTER untuk two-way sync...")
    run_sync(TEST_SYNC1, TEST_SYNC2, twoway=True)

    print_info("\n✅ Test Sync selesai!\n")
    input("Tekan ENTER untuk lanjut ke test berikutnya...")


def test_clean():
    """Test fitur clean"""
    print_header("🧪 TEST 3: Clean")

    print(f"\n{Colors.BOLD_CYAN}Test 3.1: Clean file > 7 hari{Colors.RESET}")
    print_info(f"Folder: {TEST_CLEAN}")
    print_info("Hapus file lebih tua dari 7 hari")
    input("Tekan ENTER untuk mulai...")
    run_clean(TEST_CLEAN, days=7)

    print(f"\n{Colors.BOLD_CYAN}Test 3.2: Clean dengan filter ekstensi{Colors.RESET}")
    print_info("Filter: hanya file .txt")

    # Buat file baru untuk test kedua
    old_time = time.time() - (20 * 24 * 60 * 60)
    for i in range(3):
        filepath = os.path.join(TEST_CLEAN, f"old_test_{i}.txt")
        with open(filepath, "w") as f:
            f.write(f"Old test file {i}")
        os.utime(filepath, (old_time, old_time))

    input("Tekan ENTER untuk clean dengan filter...")
    run_clean(TEST_CLEAN, days=7, ext=".txt")

    print_info("\n✅ Test Clean selesai!\n")
    input("Tekan ENTER untuk lanjut ke test berikutnya...")


def test_rename():
    """Test fitur rename"""
    print_header("🧪 TEST 4: Rename")

    print(f"\n{Colors.BOLD_CYAN}Test 4.1: Rename dengan Pattern{Colors.RESET}")
    print_info(f"Folder: {TEST_RENAME}")
    print_info("Pattern: prefix='NEW_', suffix='_v2', replace='old'")
    input("Tekan ENTER untuk mulai...")

    # Perlu import dulu jika belum
    try:
        run_rename_with_pattern(
            TEST_RENAME,
            prefix="NEW_",
            suffix="_v2",
            replace="old",
            start=1,
            remove_ts=False,
        )
    except Exception as e:
        print_warning(f"⚠️  Error: {e}")
        print_info("Pastikan modul renamer sudah ada")

    print(f"\n{Colors.BOLD_CYAN}Test 4.2: Rename dengan Custom Name{Colors.RESET}")

    # Buat file baru untuk test
    test_custom_dir = os.path.join(TEST_DIR, "rename_custom")
    os.makedirs(test_custom_dir, exist_ok=True)

    for i in range(5):
        with open(os.path.join(test_custom_dir, f"random_name_{i}.txt"), "w") as f:
            f.write(f"File {i}")

    print_info(f"Folder: {test_custom_dir}")
    print_info("Custom name: 'MyFile'")
    input("Tekan ENTER untuk rename...")

    try:
        run_rename_custom_name(test_custom_dir, "MyFile", start=1)
    except Exception as e:
        print_warning(f"⚠️  Error: {e}")

    print_info("\n✅ Test Rename selesai!\n")


def cleanup_test_environment():
    """Hapus folder test"""
    print_header("🧹 Cleanup")
    print_info(f"Hapus folder test: {TEST_DIR}")

    response = input("Hapus folder test? (y/n): ").lower()
    if response == "y":
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
            print_success("✅ Folder test berhasil dihapus!")
    else:
        print_info(f"📂 Folder test tetap ada di: {os.path.abspath(TEST_DIR)}")


def main():
    """Main test runner"""
    print(
        f"""
{Colors.BOLD_CYAN}
╔═══════════════════════════════════════════╗
║     AutoFile Manager - Test Suite        ║
║         Automated Testing Script         ║
╚═══════════════════════════════════════════╝
{Colors.RESET}
"""
    )

    print_info("Script ini akan menguji semua fitur AutoFile Manager")
    print_warning("⚠️  Akan membuat folder 'test_autofile' untuk testing\n")

    input("Tekan ENTER untuk mulai setup...")

    try:
        # Setup
        setup_test_environment()

        # Run tests
        test_backup()
        test_sync()
        test_clean()
        test_rename()

        # Summary
        print_header("📊 Test Summary")
        print_success("✅ Semua test selesai!")
        print_info("\nReview hasil test di folder: " + os.path.abspath(TEST_DIR))

        print(f"\n{Colors.BOLD_CYAN}Folder Structure:{Colors.RESET}")
        print(f"  📁 {TEST_DIR}/")
        print(f"     ├── source/          (file untuk backup)")
        print(f"     ├── destination/     (hasil backup)")
        print(f"     ├── sync1/           (folder sync 1)")
        print(f"     ├── sync2/           (folder sync 2)")
        print(f"     ├── clean/           (folder untuk clean test)")
        print(f"     └── rename/          (folder untuk rename test)")

        print()
        cleanup_test_environment()

    except KeyboardInterrupt:
        print_warning("\n\n⚠️  Test dibatalkan oleh user")
    except Exception as e:
        print_warning(f"\n\n❌ Error saat testing: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
