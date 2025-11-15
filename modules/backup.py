import os
import shutil
from datetime import datetime
from pathlib import Path
from utils.utils import (
    log,
    ensure_folder,
    print_success,
    print_error,
    print_warning,
    print_info,
    Colors,
)


def run_backup(src, dst, incremental=False, timestamp=False):
    """
    Backup folder dari source ke destination

    Args:
        src: Folder sumber
        dst: Folder tujuan
        incremental: Jika True, hanya backup file yang berubah
        timestamp: Jika True, tambahkan timestamp ke nama folder backup
    """
    try:
        # Validasi folder sumber
        if not os.path.exists(src):
            print_error(f"❌ Folder sumber tidak ditemukan: {src}")
            return False

        if not os.path.isdir(src):
            print_error(f"❌ Path sumber bukan folder: {src}")
            return False

        # Buat folder tujuan jika belum ada
        ensure_folder(dst)

        # Tambahkan timestamp jika diminta
        if timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = os.path.basename(os.path.normpath(src))
            dst = os.path.join(dst, f"{folder_name}_backup_{ts}")
            ensure_folder(dst)

        log(f"🔄 Memulai backup dari '{src}' ke '{dst}'")

        if incremental:
            print_info("⚡ Mode: Incremental Backup (hanya file baru/berubah)")
        else:
            print_info("📦 Mode: Full Backup (semua file)")

        # Counter statistik
        stats = {"copied": 0, "skipped": 0, "failed": 0, "total_size": 0}

        # Scan semua file di folder sumber
        print_info("\n📊 Memindai file...")

        for root, dirs, files in os.walk(src):
            # Hitung relative path
            rel_path = os.path.relpath(root, src)
            dst_dir = os.path.join(dst, rel_path) if rel_path != "." else dst

            # Buat struktur folder di tujuan
            ensure_folder(dst_dir)

            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)

                try:
                    # Cek apakah perlu dicopy
                    should_copy = True

                    if incremental and os.path.exists(dst_file):
                        # Bandingkan waktu modifikasi dan ukuran
                        src_mtime = os.path.getmtime(src_file)
                        dst_mtime = os.path.getmtime(dst_file)
                        src_size = os.path.getsize(src_file)
                        dst_size = os.path.getsize(dst_file)

                        if src_mtime <= dst_mtime and src_size == dst_size:
                            should_copy = False
                            stats["skipped"] += 1

                    if should_copy:
                        # Copy file dengan metadata
                        shutil.copy2(src_file, dst_file)
                        file_size = os.path.getsize(src_file)
                        stats["copied"] += 1
                        stats["total_size"] += file_size

                        # Tampilkan progress untuk file besar (>1MB)
                        if file_size > 1024 * 1024:
                            size_mb = file_size / (1024 * 1024)
                            print(f"  ✓ {file} ({size_mb:.2f} MB)")

                except PermissionError:
                    print_warning(f"  ⚠️  Akses ditolak: {file}")
                    stats["failed"] += 1
                except Exception as e:
                    print_warning(f"  ⚠️  Gagal backup {file}: {str(e)}")
                    stats["failed"] += 1

        # Tampilkan hasil
        print()
        print_success("✅ Backup selesai!")
        print_info(f"\n📈 Statistik Backup:")
        print(
            f"  • File berhasil dicopy: {Colors.GREEN}{stats['copied']}{Colors.RESET}"
        )
        print(f"  • File dilewati: {Colors.YELLOW}{stats['skipped']}{Colors.RESET}")
        print(f"  • File gagal: {Colors.RED}{stats['failed']}{Colors.RESET}")

        if stats["total_size"] > 0:
            size_mb = stats["total_size"] / (1024 * 1024)
            if size_mb > 1024:
                size_gb = size_mb / 1024
                print(f"  • Total ukuran: {Colors.CYAN}{size_gb:.2f} GB{Colors.RESET}")
            else:
                print(f"  • Total ukuran: {Colors.CYAN}{size_mb:.2f} MB{Colors.RESET}")

        print(f"  • Lokasi backup: {Colors.BOLD_CYAN}{dst}{Colors.RESET}")

        return True

    except Exception as e:
        print_error(f"❌ Error saat backup: {str(e)}")
        return False
