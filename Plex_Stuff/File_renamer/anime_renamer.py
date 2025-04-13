import os
import re
import shutil
import sys


def rename_tv_show_files(show_name, year=None):
    """
    Renames TV show files in the current directory to follow Plex's naming convention
    and moves them into a designated folder. The naming convention is:

        Show Name (Year) [language-Language] - sXXXXeYYYY [optional part] [ova].ext

    Files without an explicit season default to season 1. Files are moved into a target
    folder based on the show name, optional year, and detected language. OVA files (those
    with "OVA" in their name) are moved into a folder named "Special".

    Supported Naming Formats include:
        • "[AH] Dr. Stone S2 - 01 (1080p).mkv"
        • "[SubsPlease] Dr. Stone S4 - 03 (1080p) [691F8C8D].mkv"
        • "Dr Stone Season 2 Stone Wars Episode 9 English Dubbed ..."
        • "Hunter x Hunter (2011) ep 2.mp4"
        • "Hunter-x-Hunter-(2011)-Episode-118.mp4"
        • "My Bride is a Mermaid e01.mp4"  (new pattern added)

    Language Detection:
        - If the filename contains "subbed" (case-insensitive), it is marked as Japanese.
        - Otherwise, if it contains "dubbed" or "dub", it is marked as English.
        - Defaults to Japanese if neither is found.

    Args:
        show_name (str): The name of the TV show.
        year (str, optional): The release year (optional).
    """

    # Regex for OVA detection.
    ova_pattern = re.compile(r"\bOVA\b", re.IGNORECASE)

    # Define regex patterns for various naming conventions.
    bracketed_with_season = re.compile(
        r"^\[[A-Za-z0-9]+\]\s*.+?[Ss](\d{1,4})\s*-\s*(\d{1,4})", re.IGNORECASE
    )
    bracketed_without_season = re.compile(
        r"^\[[A-Za-z0-9]+\]\s*.+?\s*-\s*(\d{1,4})", re.IGNORECASE
    )
    explicit_season = re.compile(
        r"Season\s*(\d{1,4}).*?Episode\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    s_episode = re.compile(
        r"[Ss](\d{1,4})\s+Episode\s+(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    subsplease_format = re.compile(
        r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*E?\s*(\d{1,4}(?:\.\d)?)",
        re.IGNORECASE,
    )
    subsplease_compact = re.compile(
        r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})E(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    # "Episode Y" only (no season info) – default season to 1.
    episode_only = re.compile(r"\bEpisode\s+(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)
    ep_only = re.compile(r"\bep\s+(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)
    e_only = re.compile(r"\be(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)

    # "1x02" style (e.g., "1x02" or "1x2")
    one_x_two = re.compile(r"(\d{1,2})x(\d{1,4}(?:\.\d)?)", re.IGNORECASE)
    # General S/E format.
    general_se = re.compile(
        r"S?(\d{1,4})\s*[EeXx-]?\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    # Alternative S - E format.
    alt_se = re.compile(r"\bS?(\d{1,4})\s*-\s*E?(\d{1,4}(?:\.\d)?)", re.IGNORECASE)
    # HiAnime style.
    hianime = re.compile(r"s(\d{1,4}).*?ep(\d{1,4})", re.IGNORECASE)
    # Gogoanime style.
    gogoanime = re.compile(r"s(\d{1,4}).*?episode[-_\s]?(\d{1,4})", re.IGNORECASE)
    
    # Plex naming pattern - for renaming files in Plex.
	 # This pattern captures the show name, year, language, season, episode, and part.
    plex_pattern = re.compile(r"^(.+?)\s*\((\d{4})\)\s*\{language-(.+?)\}\s*-\s*s(\d{1,4})e(\d{1,4})\s*-\s*pt(\d{1,4})", re.IGNORECASE)

    # Order patterns: most specific first.
    patterns = [
        plex_pattern,
        bracketed_with_season,
        bracketed_without_season,
        explicit_season,
        s_episode,
        subsplease_format,
        subsplease_compact,
        episode_only,
        ep_only,
        e_only,
        one_x_two,
        general_se,
        alt_se,
        hianime,
        gogoanime,
    ]

    # Get current working directory and list video files.
    current_folder = os.getcwd()
    total_files = len(
        [
            f
            for f in os.listdir(current_folder)
            if f.endswith((".mp4", ".mkv", ".avi", ".mov"))
        ]
    )

    files_to_rename = []
    skipped_files = []

    print(f"\nTotal files detected: {total_files}\n")

    for filename in os.listdir(current_folder):
        if filename.endswith((".mp4", ".mkv", ".avi", ".mov")):
            season, episode, part, language = None, None, "", "Subbed"

            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    # For "Episode ..." or "ep ..." or "e..." only patterns, default season to "1".
                    if pattern in [episode_only, ep_only, e_only]:
                        season = "1"
                        episode = match.group(1)
                    # For bracketed without season pattern, default season to "1".
                    elif pattern == bracketed_without_season:
                        season = "1"
                        episode = match.group(1)
                    else:
                        season, episode = match.group(1), match.group(2)
                    break

            # Language detection: prioritize "subbed" over "dubbed".
            lower_name = filename.lower()
            if "subbed" in lower_name or "language-Japanese" in lower_name or "edition-Subbed" in lower_name:
                language = "Japanese"
            elif "dubbed" in lower_name or "dub" in lower_name or "language-English" in lower_name or "edition-Dubbed" in lower_name:
                language = "English"
            else:
                language = "Japanese"

            if not season:
                season = "1"
            if not episode:
                skipped_files.append(filename)
                continue

            # Format season and episode as four-digit strings.
            season = f"s{int(season):04d}"
            if "." in episode or "- pt" in episode:
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"
                part = f" - pt{int(part_num):04d}"
            else:
                episode = f"e{int(episode):04d}"

            # Check for OVA tag.
            ova_tag = ""
            if re.search(r"\bOVA\b", filename, re.IGNORECASE):
                ova_tag = " [ova]"

            # Extract file extension.
            base_name, file_ext = os.path.splitext(filename)
            file_ext = (
                file_ext.lower()
                if file_ext.lower() in [".mp4", ".mkv", ".avi", ".mov"]
                else ".mp4"
            )

            # Determine target folder.
            if ova_tag:
                target_folder = "Special"
            else:
                if year:
                    target_folder = f"{show_name} ({year}) {{language-{language}}}"
                else:
                    target_folder = f"{show_name} {{language-{language}}}"

            # Construct new filename.
            if year:
                new_filename = f"{show_name} ({year}) {{[language-{language}}} - {season}{episode}{part}{ova_tag}{file_ext}"
            else:
                new_filename = f"{show_name} {{language-{language}}} - {season}{episode}{part}{ova_tag}{file_ext}"

            # Create target folder if it doesn't exist.
            target_folder_path = os.path.join(current_folder, target_folder)
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path, exist_ok=True)

            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(target_folder_path, new_filename)
            files_to_rename.append((old_path, new_path))

    print("\nPreview of File Renaming:\n")
    for old, new in files_to_rename:
        print(f"{os.path.basename(old)}  →  {os.path.basename(new)}")

    if skipped_files:
        print("\nFiles Skipped (No Episode Number Detected):")
        for skipped in skipped_files:
            print(f"{skipped}")

    confirm = input("\nProceed with renaming? (y/n): ").strip().lower()
    if confirm != "y":
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
