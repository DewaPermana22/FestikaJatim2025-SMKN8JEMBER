import os
import shutil
import filecmp
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


def run_sync(folder1, folder2, twoway=False):
    """
    Sinkronisasi dua folder

    Args:
        folder1: Folder pertama
        folder2: Folder kedua
        twoway: Jika True, sinkronisasi dua arah. Jika False, folder1 -> folder2
    """
    try:
        # Validasi folder
        if not os.path.exists(folder1):
            print_error(f"❌ Folder 1 tidak ditemukan: {folder1}")
            return False

        if not os.path.isdir(folder1):
            print_error(f"❌ Path 1 bukan folder: {folder1}")
            return False

        # Buat folder2 jika belum ada
        ensure_folder(folder2)

        if twoway:
            log(f"🔄 Sinkronisasi dua arah: '{folder1}' ↔️ '{folder2}'")
            print_info("↔️  Mode: Two-Way Sync (saling sinkronisasi)")
        else:
            log(f"🔄 Sinkronisasi satu arah: '{folder1}' → '{folder2}'")
            print_info("→  Mode: One-Way Sync (folder1 ke folder2)")

        stats = {
            "copied_to_2": 0,
            "copied_to_1": 0,
            "updated_in_2": 0,
            "updated_in_1": 0,
            "deleted_in_2": 0,
            "deleted_in_1": 0,
            "identical": 0,
        }

        print_info("\n📊 Menganalisis perbedaan...")

        # Sync dari folder1 ke folder2
        _sync_one_way(folder1, folder2, stats, "to_2")

        if twoway:
            # Sync dari folder2 ke folder1 (hanya file yang tidak ada di folder1)
            _sync_one_way(folder2, folder1, stats, "to_1")

        # Tampilkan hasil
        print()
        print_success("✅ Sinkronisasi selesai!")
        print_info(f"\n📈 Statistik Sinkronisasi:")

        if twoway:
            print(f"  📁 {Colors.BOLD_CYAN}Folder 1 → Folder 2:{Colors.RESET}")
            print(
                f"     • File baru dicopy: {Colors.GREEN}{stats['copied_to_2']}{Colors.RESET}"
            )
            print(
                f"     • File diperbarui: {Colors.YELLOW}{stats['updated_in_2']}{Colors.RESET}"
            )
            print()
            print(f"  📁 {Colors.BOLD_CYAN}Folder 2 → Folder 1:{Colors.RESET}")
            print(
                f"     • File baru dicopy: {Colors.GREEN}{stats['copied_to_1']}{Colors.RESET}"
            )
            print(
                f"     • File diperbarui: {Colors.YELLOW}{stats['updated_in_1']}{Colors.RESET}"
            )
        else:
            print(
                f"  • File baru dicopy: {Colors.GREEN}{stats['copied_to_2']}{Colors.RESET}"
            )
            print(
                f"  • File diperbarui: {Colors.YELLOW}{stats['updated_in_2']}{Colors.RESET}"
            )

        print(f"  • File identik: {Colors.CYAN}{stats['identical']}{Colors.RESET}")

        return True

    except Exception as e:
        print_error(f"❌ Error saat sinkronisasi: {str(e)}")
        return False


def _sync_one_way(src_folder, dst_folder, stats, direction):
    """
    Helper function untuk sinkronisasi satu arah

    Args:
        src_folder: Folder sumber
        dst_folder: Folder tujuan
        stats: Dictionary untuk menyimpan statistik
        direction: 'to_2' atau 'to_1' untuk tracking statistik
    """
    for root, dirs, files in os.walk(src_folder):
        # Hitung relative path
        rel_path = os.path.relpath(root, src_folder)
        dst_dir = os.path.join(dst_folder, rel_path) if rel_path != "." else dst_folder

        # Buat struktur folder di tujuan
        ensure_folder(dst_dir)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_dir, file)

            try:
                # Cek apakah file sudah ada di tujuan
                if os.path.exists(dst_file):
                    # Bandingkan file
                    if not filecmp.cmp(src_file, dst_file, shallow=False):
                        # File berbeda, cek mana yang lebih baru
                        src_mtime = os.path.getmtime(src_file)
                        dst_mtime = os.path.getmtime(dst_file)

                        if src_mtime > dst_mtime:
                            # File sumber lebih baru, update
                            shutil.copy2(src_file, dst_file)
                            if direction == "to_2":
                                stats["updated_in_2"] += 1
                            else:
                                stats["updated_in_1"] += 1
                            print(f"  🔄 Update: {file}")
                        else:
                            # File tujuan lebih baru atau sama, skip
                            stats["identical"] += 1
                    else:
                        # File identik
                        stats["identical"] += 1
                else:
                    # File baru, copy
                    shutil.copy2(src_file, dst_file)
                    if direction == "to_2":
                        stats["copied_to_2"] += 1
                    else:
                        stats["copied_to_1"] += 1
                    print(f"  ➕ Baru: {file}")

            except PermissionError:
                print_warning(f"  ⚠️  Akses ditolak: {file}")
            except Exception as e:
                print_warning(f"  ⚠️  Gagal sync {file}: {str(e)}")


def compare_folders(folder1, folder2):
    """
    Membandingkan dua folder dan menampilkan perbedaannya (utility function)
    """
    comparison = filecmp.dircmp(folder1, folder2)

    print_info("\n📊 Perbandingan Folder:")
    print(f"\n  📁 Hanya di Folder 1: {len(comparison.left_only)}")
    for item in comparison.left_only[:5]:  # Tampilkan 5 pertama
        print(f"     • {item}")
    if len(comparison.left_only) > 5:
        print(f"     ... dan {len(comparison.left_only) - 5} lainnya")

    print(f"\n  📁 Hanya di Folder 2: {len(comparison.right_only)}")
    for item in comparison.right_only[:5]:
        print(f"     • {item}")
    if len(comparison.right_only) > 5:
        print(f"     ... dan {len(comparison.right_only) - 5} lainnya")

    print(f"\n  🔄 File berbeda: {len(comparison.diff_files)}")
    for item in comparison.diff_files[:5]:
        print(f"     • {item}")
    if len(comparison.diff_files) > 5:
        print(f"     ... dan {len(comparison.diff_files) - 5} lainnya")

    print(f"\n  ✓ File identik: {len(comparison.same_files)}")

    return comparison
