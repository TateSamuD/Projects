import os
import re
import shutil
import sys

def rename_tv_show_files(show_name, year=None):
    """
    Renames TV show files in the current directory to follow Plex's naming convention.
    
    Plex Naming Format:
        Show Name (Year) - sXXXXeYYYY [edition-Language].ext
    
    This script first displays a preview of the changes before renaming the files.

    Supported Naming Formats (examples):
        1. "Season 2 Episode 1 ..."            -> s0002e0001
        2. "s1 Episode 2 ..."                  -> s0001e0002
        3. "[SubsPlease] ... s2 - e 8 ..."      -> s0002e0008
        4. "[SubsPlease] ... S02E03"            -> s0002e0003
        5. "S2E5", "S2-E5", "S2 E5"             -> s0002e0005
        6. "S2 - E08" or "S2-4"                -> s0002e0008 or s0002e0004
        7. "1x02" style                        -> s0001e0002
        8. "Episode 10 ..." (no season info)   -> defaults to season 1: s0001e0010
        9. "[AH] Bofuri - 01 (1080p)"          -> defaults to season 1: s0001e0001
       10. Gogoanime style with resolution info:
           "(1280x720-gogoanime)dungeon-ni-deai-wo-motomeru-no-wa-machigatteiru-darou-ka-s2-dub-episode-03"
           -> s0002e0003

    Language Detection:
        - If "dub" is found in the filename, it is marked as Dubbed.
        - Otherwise, it defaults to Subbed.
    
    Args:
        show_name (str): The name of the TV show.
        year (str, optional): The release year (optional).
    """

    # New pattern for gogoanime style with resolution prefix.
    # This pattern matches filenames that begin with a resolution block like "(1280x720-gogoanime)"
    # and then later contain "s<season>" and "episode<episode>".
    gogoanime_pattern = re.compile(
        r"^\(\d+x\d+-gogoanime\).*?s(\d{1,4}).*?episode[-_\s]*(\d{1,4})",
        re.IGNORECASE
    )

    # Other patterns to cover a variety of naming formats:
    patterns = [
        gogoanime_pattern,
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
        # 8. Bracketed format: "[AH] Bofuri - 01 (1080p)"
        re.compile(r"^\[[A-Za-z0-9]+\]\s*.+?\s*-\s*(\d{1,4})(?:\s*\(.*?\))", re.IGNORECASE),
        # 9. "Episode Y" only (no season info) – default season to 1
        re.compile(r"\bEpisode\s+(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)
    ]

    # Get current working directory and list video files.
    current_folder = os.getcwd()
    total_files = len([f for f in os.listdir(current_folder)
                       if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))])
    
    files_to_rename = []
    skipped_files = []

    print(f"\nTotal files detected: {total_files}\n")

    # Process each video file.
    for filename in os.listdir(current_folder):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):
            season, episode, part, language = None, None, "", "Subbed"

            # Iterate over regex patterns until one matches.
            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    # For "Episode Y" only pattern (pattern 9), default season to "1".
                    if pattern.pattern.startswith(r"\bEpisode"):
                        season = "1"
                        episode = match.group(1)
                    # For the bracketed format (pattern 8), also default season to "1".
                    elif pattern.pattern.startswith(r"^\[[A-Za-z0-9]+\]"):
                        season = "1"
                        episode = match.group(1)
                    else:
                        season, episode = match.group(1), match.group(2)
                    break  

            # Detect language: if "dub" is found, mark as Dubbed; otherwise, default to Subbed.
            if "dub" in filename.lower():
                language = "Dubbed"
            else:
                language = "Subbed"

            # If season or episode info is missing, skip the file.
            if not season:
                season = "1"
            if not episode:
                skipped_files.append(filename)
                continue

            # Format season and episode numbers to four digits.
            season = f"s{int(season):04d}"
            if "." in episode:  # Handle decimal parts (e.g., "7.5" → e0007 - pt5)
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"
                part = f" - pt{part_num}"
            else:
                episode = f"e{int(episode):04d}"

            # Get file extension.
            base_name, file_ext = os.path.splitext(filename)
            file_ext = file_ext.lower() if file_ext.lower() in ['.mp4', '.mkv', '.avi', '.mov'] else ".mp4"

            # Construct the new filename.
            if year:
                new_filename = f"{show_name} ({year}) [edition-{language}] - {season}{episode}{part}{file_ext}"
            else:
                new_filename = f"{show_name} [edition-{language}] - {season}{episode}{part}{file_ext}"

            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(current_folder, new_filename)
            files_to_rename.append((old_path, new_path))

    # Display a preview of the file renaming.
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
