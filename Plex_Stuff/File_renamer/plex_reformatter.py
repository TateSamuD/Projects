import os
import re
import shutil
import sys

def rename_tv_show_files(show_name, year=None):
    """
    Renames TV show files in the current directory to follow Plex's naming convention.  
    It first displays a preview of the changes before renaming the files.

    Plex Naming Format:
        Show Name (Year) - sXXXXeYYYY [edition-Language].ext

    Args:
        show_name (str): The name of the TV show.
        year (str, optional): The release year of the show (optional).

    Naming Pattern Examples:
        - "Show Name (2024) - s0001e0002 [edition-Subbed].mp4"
        - "Show Name [edition-Dubbed] - s0001e0010.mkv"

    The script detects different naming conventions and extracts season/episode numbers.

    Supported Naming Formats:
        1. "Season X Episode Y" -> Season and Episode extracted directly.
        2. "sX Episode Y" -> Recognizes season/episode formats.
        3. "[SubsPlease] ... sX - e Y" -> Matches fan-sub groups with season/episode.
        4. "[SubsPlease] ... SXXEYY" -> Compact format.
        5. "S2E5", "S2-E5", "S2 E5" -> Common season/episode formats.
        6. "S2 - E08" or "S2-4" -> Alternative S/E formats.
        7. "1x02", "1x2" -> Numbering with "x" separator.
        8. "Episode Y" (without season) -> Assumes Season 1 by default.
        9. "[AH] Show Name - 01 (1080p)" -> Extracts episode number and assumes Season 1.

    Example File Renaming:
        Before: "[SubsPlease] Anime Title - S1 - E05 (1080p).mp4"
        After:  "Anime Title [edition-Subbed] - s0001e0005.mp4"
    """

    # Regular expression patterns to match various file naming styles
    patterns = [
        re.compile(r"Season\s*(\d{1,4})\s*Episode\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"[Ss](\d{1,4})\s+Episode\s+(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*E?\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})E(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"S?(\d{1,4})\s*[EeXx-]?\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"\bS?(\d{1,4})\s*-\s*E?(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"(\d{1,2})x(\d{1,4}(?:\.\d)?)", re.IGNORECASE),
        re.compile(r"^\[[A-Za-z0-9]+\]\s*.+?\s*-\s*(\d{1,4})(?:\s*\(.*?\))", re.IGNORECASE),
        re.compile(r"\bEpisode\s+(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)
    ]

    # Get the current working directory
    current_folder = os.getcwd()
    total_files = len([f for f in os.listdir(current_folder)
                       if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))])

    files_to_rename = []
    skipped_files = []

    print(f"\nTotal files detected: {total_files}\n")

    for filename in os.listdir(current_folder):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):  # Only process video files
            season, episode, part, language = None, None, "", "Subbed"

            # Try to extract season/episode information using regex patterns
            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    if pattern.pattern.startswith(r"\bEpisode"):  # Episode-only format
                        season = "1"
                        episode = match.group(1)
                    elif pattern.pattern.startswith("^\\["):  # Bracketed format
                        season = "1"
                        episode = match.group(1)
                    else:
                        season, episode = match.group(1), match.group(2)
                    break  

            # Detect if the file contains "Dubbed" or "Subbed"
            if "dub" in filename.lower():
                language = "Dubbed"
            elif "sub" in filename.lower():
                language = "Subbed"

            # If season/episode is missing, skip the file
            if not season:
                season = "1"  # Default to season 1 if missing
            if not episode:
                skipped_files.append(filename)
                continue

            # Format season and episode numbers to 4 digits (e.g., s0001e0001)
            season = f"s{int(season):04d}"
            if "." in episode:  # Handle episodes with decimal parts
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"
                part = f" - pt{part_num}"
            else:
                episode = f"e{int(episode):04d}"

            # Extract file extension
            base_name, file_ext = os.path.splitext(filename)
            file_ext = file_ext.lower() if file_ext.lower() in ['.mp4', '.mkv', '.avi', '.mov'] else ".mp4"

            # Construct new filename based on show name, year, and detected info
            if year:
                new_filename = f"{show_name} ({year}) [edition-{language}] - {season}{episode}{part}{file_ext}"
            else:
                new_filename = f"{show_name} {{edition-{language}}} - {season}{episode}{part}{file_ext}"

            # Prepare for renaming
            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(current_folder, new_filename)
            
            files_to_rename.append((old_path, new_path))

    # Display a preview of file renaming
    print("\nPreview of File Renaming:\n")
    for old, new in files_to_rename:
        print(f"{os.path.basename(old)}  →  {os.path.basename(new)}")

    # Display skipped files
    if skipped_files:
        print("\nFiles Skipped (No Episode Number Detected):")
        for skipped in skipped_files:
            print(f"{skipped}")

    # Confirm with the user before proceeding with renaming
    confirm = input("\nProceed with renaming? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\nOperation canceled. No files were renamed.")
        return

    # Perform the renaming operation
    renamed_files = 0
    for old_path, new_path in files_to_rename:
        shutil.move(old_path, new_path)
        renamed_files += 1
        print(f"Renamed: {os.path.basename(old_path)} → {os.path.basename(new_path)}")

    print(f"\nRenaming complete! {renamed_files} files renamed.")

# Ensure the script runs with correct command-line arguments
if len(sys.argv) < 2:
    print("Usage: python rename_plex_files.py '<Series Name>' [Year]")
else:
    series_name = sys.argv[1]
    series_year = sys.argv[2] if len(sys.argv) > 2 else None
    rename_tv_show_files(series_name, series_year)
