import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from utils.utils import (
    log,
    print_success,
    print_error,
    print_warning,
    print_info,
    Colors,
    get_yes_no,
)


def run_clean(folder, days, ext=None):
    """
    Membersihkan file lama dari folder

    Args:
        folder: Folder yang akan dibersihkan
        days: Hapus file yang lebih tua dari X hari
        ext: Filter ekstensi file (opsional), misal: '.txt' atau '.log'
    """
    try:
        # Validasi folder
        if not os.path.exists(folder):
            print_error(f"❌ Folder tidak ditemukan: {folder}")
            return False

        if not os.path.isdir(folder):
            print_error(f"❌ Path bukan folder: {folder}")
            return False

        log(f"🧹 Membersihkan folder: '{folder}'")
        print_info(f"🗑️  Menghapus file lebih tua dari {days} hari")

        if ext:
            print_info(f"🔍 Filter ekstensi: {ext}")

        # Hitung tanggal cutoff
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_date.timestamp()

        # Counter statistik
        stats = {"scanned": 0, "matched": 0, "deleted": 0, "failed": 0, "total_size": 0}

        files_to_delete = []

        print_info("\n📊 Memindai file...")

        # Scan semua file
        for root, dirs, files in os.walk(folder):
            for file in files:
                stats["scanned"] += 1
                file_path = os.path.join(root, file)

                try:
                    # Cek ekstensi jika ada filter
                    if ext and not file.lower().endswith(ext.lower()):
                        continue

                    # Cek waktu modifikasi
                    file_mtime = os.path.getmtime(file_path)

                    if file_mtime < cutoff_timestamp:
                        file_size = os.path.getsize(file_path)
                        file_age_days = (time.time() - file_mtime) / (60 * 60 * 24)

                        files_to_delete.append(
                            {
                                "path": file_path,
                                "name": file,
                                "size": file_size,
                                "age_days": file_age_days,
                                "modified": datetime.fromtimestamp(file_mtime),
                            }
                        )

                        stats["matched"] += 1
                        stats["total_size"] += file_size

                except PermissionError:
                    print_warning(f"  ⚠️  Akses ditolak: {file}")
                    stats["failed"] += 1
                except Exception as e:
                    print_warning(f"  ⚠️  Error scan {file}: {str(e)}")
                    stats["failed"] += 1

        # Tampilkan hasil scan
        print()
        print_info(f"📈 Hasil Pemindaian:")
        print(f"  • Total file dipindai: {Colors.CYAN}{stats['scanned']}{Colors.RESET}")
        print(f"  • File yang cocok: {Colors.YELLOW}{stats['matched']}{Colors.RESET}")

        if stats["matched"] == 0:
            print_success("\n✅ Tidak ada file yang perlu dihapus!")
            return True

        # Tampilkan ukuran total
        size_mb = stats["total_size"] / (1024 * 1024)
        if size_mb > 1024:
            size_gb = size_mb / 1024
            print(f"  • Total ukuran: {Colors.RED}{size_gb:.2f} GB{Colors.RESET}")
        else:
            print(f"  • Total ukuran: {Colors.RED}{size_mb:.2f} MB{Colors.RESET}")

        # Tampilkan beberapa contoh file
        print(f"\n{Colors.BOLD_YELLOW}📄 Contoh file yang akan dihapus:{Colors.RESET}")
        for i, file_info in enumerate(files_to_delete[:10]):
            size_kb = file_info["size"] / 1024
            age = int(file_info["age_days"])
            modified = file_info["modified"].strftime("%Y-%m-%d %H:%M")

            if size_kb > 1024:
                size_str = f"{size_kb/1024:.2f} MB"
            else:
                size_str = f"{size_kb:.2f} KB"

            print(f"  {i+1}. {file_info['name']}")
            print(f"     📅 {modified} ({age} hari) • 💾 {size_str}")

        if len(files_to_delete) > 10:
            print(f"  ... dan {len(files_to_delete) - 10} file lainnya")

        # Konfirmasi penghapusan
        print()
        confirm = get_yes_no(f"⚠️  Hapus {stats['matched']} file?", default=False)

        if not confirm:
            print_warning("\n❌ Pembersihan dibatalkan")
            return False

        # Hapus file
        print()
        print_info("🗑️  Menghapus file...")

        for file_info in files_to_delete:
            try:
                os.remove(file_info["path"])
                stats["deleted"] += 1

                # Tampilkan progress setiap 50 file
                if stats["deleted"] % 50 == 0:
                    print(f"  🗑️  Dihapus: {stats['deleted']}/{stats['matched']}")

            except PermissionError:
                print_warning(f"  ⚠️  Akses ditolak: {file_info['name']}")
                stats["failed"] += 1
            except Exception as e:
                print_warning(f"  ⚠️  Gagal hapus {file_info['name']}: {str(e)}")
                stats["failed"] += 1

        # Tampilkan hasil akhir
        print()
        print_success("✅ Pembersihan selesai!")
        print_info(f"\n📈 Statistik Pembersihan:")
        print(
            f"  • File berhasil dihapus: {Colors.GREEN}{stats['deleted']}{Colors.RESET}"
        )
        print(f"  • File gagal dihapus: {Colors.RED}{stats['failed']}{Colors.RESET}")

        if stats["deleted"] > 0:
            freed_mb = (stats["deleted"] / stats["matched"]) * (
                stats["total_size"] / (1024 * 1024)
            )
            if freed_mb > 1024:
                freed_gb = freed_mb / 1024
                print(
                    f"  • Ruang dibebaskan: {Colors.BOLD_GREEN}{freed_gb:.2f} GB{Colors.RESET}"
                )
            else:
                print(
                    f"  • Ruang dibebaskan: {Colors.BOLD_GREEN}{freed_mb:.2f} MB{Colors.RESET}"
                )

        return True

    except Exception as e:
        print_error(f"❌ Error saat pembersihan: {str(e)}")
        return False


def clean_empty_folders(folder):
    """
    Menghapus folder kosong (utility function)

    Args:
        folder: Root folder untuk memulai scan
    """
    try:
        deleted = 0

        # Walk bottom-up agar folder parent dicek setelah children
        for root, dirs, files in os.walk(folder, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    # Cek apakah folder kosong
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        deleted += 1
                        print(f"  🗑️  Folder kosong dihapus: {dir_name}")
                except Exception:
                    pass

        if deleted > 0:
            print_success(f"\n✅ {deleted} folder kosong berhasil dihapus")
        else:
            print_info("\n📂 Tidak ada folder kosong")

        return deleted

    except Exception as e:
        print_error(f"❌ Error menghapus folder kosong: {str(e)}")
        return 0
