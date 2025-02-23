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
        re.compile(r"S?(\d{1,4})\s*[EeXx-]?\s*(\d{1,4})", re.IGNORECASE),  # S2E5, S2-E5, S2 E5
        re.compile(r"\bS?(\d{1,4})\s*-\s*E?(\d{1,4})", re.IGNORECASE),  # S2 - E08, S2-4
        re.compile(r"Season\s*(\d{1,4})\s*Episode\s*(\d{1,4}(\.\d)?)", re.IGNORECASE),  # Season 2 Episode 1
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*E?\s*(\d{1,4})", re.IGNORECASE),  # [SubsPlease] Solo Leveling s2 - e 8
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})E(\d{1,4})", re.IGNORECASE),  # [SubsPlease] Solo Leveling S02E03
        re.compile(r"Episode\s*(\d{1,4}(\.\d)?)", re.IGNORECASE)  # Episode 7.5 English Dubbed
    ]

    current_folder = os.getcwd()
    total_files = len([f for f in os.listdir(current_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))])
    
    files_to_rename = []
    skipped_files = []
    
    print(f"\nTotal files detected: {total_files}\n")

    for filename in os.listdir(current_folder):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):  
            season, episode, part, language = None, None, "", "Subbed"

            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    season, episode = match.group(1), match.group(2)
                    break  

            if "dub" in filename.lower():
                language = "Dubbed"
            elif "sub" in filename.lower():
                language = "Subbed"

            # **Default to Season 1 if missing**
            if not season:
                season = "1"

            if not episode:
                skipped_files.append(filename)
                continue

            season = f"s{int(season):04d}"  # **Ensures season is four digits (s0001, s0002, etc.)**
            if "." in episode:
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"  # **Ensures episode is four digits (e0001, e0002, etc.)**
                part = f" - pt{part_num}"
            else:
                episode = f"e{int(episode):04d}"  # **Ensures episode is four digits (e0001, e0002, etc.)**

            base_name, file_ext = os.path.splitext(filename)
            file_ext = file_ext.lower() if file_ext.lower() in ['.mp4', '.mkv', '.avi', '.mov'] else ".mp4"

            if year:
                new_filename = f"{show_name} ({year}) [edition-{language}] - {season}{episode}{part}{file_ext}"
            else:
                new_filename = f"{show_name} [edition-{language}] - {season}{episode}{part}{file_ext}"

            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(current_folder, new_filename)
            
            files_to_rename.append((old_path, new_path))

    print("\nPreview of File Renaming:\n")
    for old, new in files_to_rename:
        print(f"{os.path.basename(old)}  →  {os.path.basename(new)}")

    if skipped_files:
        print("\nFiles Skipped (No Episode Number Detected):")
        for skipped in skipped_files:
            print(f"{skipped}")

    confirm = input("\nProceed with renaming? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\nOperation canceled. No files were renamed.")
        return

    renamed_files = 0
    for old_path, new_path in files_to_rename:
        shutil.move(old_path, new_path)
        renamed_files += 1
        print(f"Renamed: {os.path.basename(old_path)} → {os.path.basename(new_path)}")

    print(f"\nRenaming complete! {renamed_files} files renamed.")

if len(sys.argv) < 2:
    print("Usage: python rename_plex_files.py '<Series Name>' [Year]")
else:
    series_name = sys.argv[1]  
    series_year = sys.argv[2] if len(sys.argv) > 2 else None  
    rename_tv_show_files(series_name, series_year)
