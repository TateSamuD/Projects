import os
import re
import shutil
import sys

def rename_tv_show_files(show_name, year=None):
    """
    Renames TV show files in the current folder to match Plex's naming convention.

    Args:
        show_name (str): Name of the TV show.
        year (str, optional): Release year of the TV show. Defaults to None.
    """
    # List of regex patterns to match Season, Episode, and Language
    patterns = [
        re.compile(r"Episode\s*(\d{1,4}(\.\d)?)\s*(?:English\s*Dubbed|Dub|Sub)?", re.IGNORECASE),  # "Episode 7.5 English Dubbed"
        re.compile(r"\b(\d{1,4}(\.\d)?)\b.*?(?:Dub|Sub|1080p|720p|480p|544p)?", re.IGNORECASE),  # "Trigun - 19 (544p)"
        re.compile(r"S?(\d{1,4})[EX]?(\d{1,4}(\.\d)?)", re.IGNORECASE),  # "S01E19" or "1x19" or "S1 - 07.5"
        re.compile(r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*(\d{1,4}(\.\d)?)\s*\(.*?\)", re.IGNORECASE)  # "[SubsPlease] Solo Leveling S1 - 07.5 (1080p)"
    ]

    current_folder = os.getcwd()  # Get the current working directory
    total_files = len([f for f in os.listdir(current_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))])
    renamed_files = 0  # Counter for renamed files

    print(f"Total files to rename: {total_files}")

    for filename in os.listdir(current_folder):
        if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):  # Check for video files
            season, episode, part = "01", None, ""  # Default values

            # Try each pattern to extract Season and Episode number
            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    if match.lastindex and match.lastindex >= 2:  # If Season and Episode both found
                        season, episode = match.group(1), match.group(2)
                    else:  # If only Episode found
                        episode = match.group(1)
                    break  # Stop after first match

            # If episode is still not found, skip the file
            if not episode:
                print(f"Skipping: {filename} (No episode number detected)")
                continue

            # Format Season and Episode numbers in lowercase
            season = f"s{int(season):02d}"
            if "." in episode:
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):02d}"  # Format as "e01"
                part = f" - pt{part_num}"  # Format as " - pt1"
            else:
                episode = f"e{int(episode):02d}"

            # Fix double extensions (e.g., ".mkv.mp4" → ".mp4")
            base_name, file_ext = os.path.splitext(filename)
            if file_ext.lower() in ['.mp4', '.mkv', '.avi', '.mov']:  
                file_ext = file_ext.lower()  # Keep only the last valid extension
            else:  
                file_ext = ".mp4"  # Default to .mp4 if unknown

            # New filename format: "Show Name (Year) - sXXeYY - ptZ.ext"
            if year:
                new_filename = f"{show_name} ({year}) - {season}{episode}{part}{file_ext}"
            else:
                new_filename = f"{show_name} - {season}{episode}{part}{file_ext}"

            # Full file paths
            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(current_folder, new_filename)

            # Rename the file
            shutil.move(old_path, new_path)
            renamed_files += 1
            print(f"Renamed: {filename} → {new_filename} ({renamed_files}/{total_files})")

    print(f"Renaming complete! {renamed_files} files renamed.")

# Check if the user provided a series name (year is now optional)
if len(sys.argv) < 2:
    print("Usage: python rename_plex_files.py '<Series Name>' [Year]")
else:
    series_name = sys.argv[1]  # Get series name from command-line argument
    series_year = sys.argv[2] if len(sys.argv) > 2 else None  # Get year if provided
    rename_tv_show_files(series_name, series_year)
