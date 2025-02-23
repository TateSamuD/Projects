import os
import re
import shutil
import sys

def rename_tv_show_files(show_name, year=None):
    """
    Renames TV show files in the current folder to match Plex's naming convention,
    but first, it shows a preview for confirmation.

    Args:
        show_name (str): Name of the TV show.
        year (str, optional): Release year of the TV show. Defaults to None.
    """
    patterns = [
        re.compile(r"Season\s*(\d{1,4})\s*Episode\s*(\d{1,4}(\.\d)?)", re.IGNORECASE),  # "Season 2 Episode 1"
        re.compile(r"Episode\s*(\d{1,4}(\.\d)?)\s*(?:English\s*Dubbed|Dub|Sub)?", re.IGNORECASE),  # "Episode 7.5 English Dubbed"
        re.compile(r"\b(\d{1,4}(\.\d)?)\b.*?(?:Dub|Sub|1080p|720p|480p|544p)?", re.IGNORECASE),  # "Trigun - 19 (544p)"
        re.compile(r"S?(\d{1,4})[EX]?(\d{1,4}(\.\d)?)", re.IGNORECASE),  # "S01E19" or "1x19" or "S1 - 07.5"
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*(\d{1,4}(\.\d)?)\s*\(.*?\)", re.IGNORECASE)  # "[SubsPlease] Solo Leveling S1 - 07.5 (1080p)"
    ]

    current_folder = os.getcwd()
    total_files = len([f for f in os.listdir(current_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))])

    files_to_rename = []  # Store preview of renaming changes
    skipped_files = []  # Store skipped files

    print(f"\nTotal files detected: {total_files}\n")

    for filename in os.listdir(current_folder):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):
            season, episode, part, language = "0001", None, "", "Subbed"

            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    if match.lastindex and match.lastindex >= 2:
                        season, episode = match.group(1), match.group(2)
                    else:
                        episode = match.group(1)
                    break

            if "dub" in filename.lower():
                language = "Dubbed"
            elif "sub" in filename.lower():
                language = "Subbed"

            if not episode:
                skipped_files.append(filename)
                continue

            season = f"s{int(season):04d}"
            if "." in episode:
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"
                part = f" - pt{part_num}"
            else:
                episode = f"e{int(episode):04d}"

            base_name, file_ext = os.path.splitext(filename)
            if file_ext.lower() in ['.mp4', '.mkv', '.avi', '.mov']:
                file_ext = file_ext.lower()
            else:
                file_ext = ".mp4"

            if year:
                new_filename = f"{show_name} ({year}) [edition-{language}] - {season}{episode}{part}{file_ext}"
            else:
                new_filename = f"{show_name} [edition-{language}] - {season}{episode}{part}{file_ext}"

            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(current_folder, new_filename)

            files_to_rename.append((old_path, new_path))

    # Preview before renaming
    print("\n🔍 **Preview of File Renaming:**\n")
    for old, new in files_to_rename:
        print(f"📂 {os.path.basename(old)}  →  📂 {os.path.basename(new)}")

    if skipped_files:
        print("\n⚠ **Files Skipped (No Episode Number Detected):**")
        for skipped in skipped_files:
            print(f"❌ {skipped}")

    # Ask for user confirmation
    confirm = input("\nProceed with renaming? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Operation canceled. No files were renamed.")
        return

    # Perform the actual renaming
    renamed_files = 0
    for old_path, new_path in files_to_rename:
        shutil.move(old_path, new_path)
        renamed_files += 1
        print(f"✅ Renamed: {os.path.basename(old_path)} → {os.path.basename(new_path)}")

    print(f"\n🎉 Renaming complete! {renamed_files} files renamed.")

if len(sys.argv) < 2:
    print("Usage: python rename_plex_files.py '<Series Name>' [Year]")
else:
    series_name = sys.argv[1]  
    series_year = sys.argv[2] if len(sys.argv) > 2 else None  
    rename_tv_show_files(series_name, series_year)
