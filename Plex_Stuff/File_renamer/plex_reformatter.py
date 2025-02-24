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
    # New and reordered patterns for various naming formats:
    patterns = [
        # 1. Explicit "Season X Episode Y"
        re.compile(r"Season\s*(\d{1,4})\s*Episode\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 2. "sX Episode Y" (e.g., "s1 Episode 2")
        re.compile(r"[Ss](\d{1,4})\s+Episode\s+(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 3. SubsPlease format: "[SubsPlease] ... sX - e Y" 
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*E?\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 4. SubsPlease compact format: "[SubsPlease] ... SXXEYY"
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})E(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 5. General S/E format: "S2E5", "S2-E5", "S2 E5" (with potential decimals)
        re.compile(r"S?(\d{1,4})\s*[EeXx-]?\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 6. Alternative S - E format: "S2 - E08" or "S2-4"
        re.compile(r"\bS?(\d{1,4})\s*-\s*E?(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 7. Common "1x02" style (e.g., "1x02", "1x2", with optional decimal)
        re.compile(r"(\d{1,2})x(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        # 9. New pattern for bracketed prefix: e.g., "[AH] Bofuri - 01 (1080p)"
        re.compile(r"^\[[A-Za-z0-9]+\]\s*.+?\s*-\s*(\d{1,4})(?:\s*\(.*?\))", re.IGNORECASE),
        # 8. "Episode Y" only (no season info) – default season to 1
        re.compile(r"\bEpisode\s+(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)]

    current_folder = os.getcwd()
    total_files = len([f for f in os.listdir(current_folder)
                       if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))])
    
    files_to_rename = []
    skipped_files = []
    
    print(f"\nTotal files detected: {total_files}\n")

    for filename in os.listdir(current_folder):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):
            season, episode, part, language = None, None, "", "Subbed"

            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    # If this is the "Episode ..." only pattern (pattern 8), default season to "1"
                    if pattern.pattern.startswith(r"\bEpisode"):
                        season = "1"
                        episode = match.group(1)
                    # If this is our new bracketed pattern (pattern 9), also default season to "1"
                    elif pattern.pattern.startswith("^\\["):
                        season = "1"
                        episode = match.group(1)
                    else:
                        season, episode = match.group(1), match.group(2)
                    break  

            if "dub" in filename.lower():
                language = "Dubbed"
            elif "sub" in filename.lower():
                language = "Subbed"

            # Default to Season 1 if missing
            if not season:
                season = "1"
            if not episode:
                skipped_files.append(filename)
                continue

            # Format season and episode numbers in four digits
            season = f"s{int(season):04d}"
            # Handle decimal episode numbers (e.g., "7.5" becomes e0007 - pt5)
            if "." in episode:
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"
                part = f" - pt{part_num}"
            else:
                episode = f"e{int(episode):04d}"

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
