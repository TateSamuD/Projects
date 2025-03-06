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

    Supported Naming Formats (examples):
        • "[AH] Dr. Stone S2 - 01 (1080p).mkv"
            → Dr. Stone [edition-Subbed] - s0002e0001.mp4
        • "[SubsPlease] Dr. Stone S4 - 03 (1080p) [691F8C8D].mkv"
            → Dr. Stone [edition-Subbed] - s0004e0003.mp4
        • "Dr Stone Season 2 Stone Wars Episode 9 English Dubbed ..."
            → Dr Stone [edition-Dubbed] - s0002e0009.mp4
        • "Dr Stone Season 3 New World Episode 9 English Dubbed ..."
            → Dr Stone [edition-Dubbed] - s0003e0009.mp4
        • "Akagami no Shirayuki-hime Season 2 Episode 2 English Subbed ..."
            → Snow White with the Red Hair [edition-Subbed] - s0002e0002.mp4

    Language Detection:
        - If the filename contains "subbed" (case-insensitive), it is marked as Subbed.
        - Otherwise, if it contains "dubbed" or "dub", it is marked as Dubbed.
        - If neither is found, it defaults to Subbed.

    Args:
        show_name (str): The name of the TV show.
        year (str, optional): The release year (optional).
    """

    # Patterns for detecting OVA episodes (case-insensitive).
    ova_pattern = re.compile(r"\bOVA\b", re.IGNORECASE)

    # Pattern for bracketed filenames with season info (e.g., "[AH] Dr. Stone S2 - 01 (1080p)")
    bracketed_with_season = re.compile(
        r"^\[[A-Za-z0-9]+\]\s*.+?[Ss](\d{1,4})\s*-\s*(\d{1,4})", re.IGNORECASE
    )
    # Pattern for bracketed filenames without explicit season info (defaults season to 1)
    bracketed_without_season = re.compile(
        r"^\[[A-Za-z0-9]+\]\s*.+?\s*-\s*(\d{1,4})", re.IGNORECASE
    )
    # Explicit season/episode pattern (allows extra text in between)
    explicit_season = re.compile(
        r"Season\s*(\d{1,4}).*?Episode\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    # "sX Episode Y" pattern (e.g., "s1 Episode 2")
    s_episode = re.compile(
        r"[Ss](\d{1,4})\s+Episode\s+(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    # SubsPlease formats
    subsplease_format = re.compile(
        r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})\s*-\s*E?\s*(\d{1,4}(?:\.\d)?)",
        re.IGNORECASE,
    )
    subsplease_compact = re.compile(
        r"\[SubsPlease\]\s*.+?\s*S?(\d{1,4})E(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    # "Episode Y" only (no season info) – default season to 1
    episode_only = re.compile(r"\bEpisode\s+(\d{1,4}(?:\.\d)?)\b", re.IGNORECASE)
    # "1x02" style (e.g., "1x02" or "1x2", with optional decimal)
    one_x_two = re.compile(r"(\d{1,2})x(\d{1,4}(?:\.\d)?)", re.IGNORECASE)
    # General S/E format (e.g., "S2E5", "S2-E5", "S2 E5")
    general_se = re.compile(
        r"S?(\d{1,4})\s*[EeXx-]?\s*(\d{1,4}(?:\.\d)?)", re.IGNORECASE
    )
    # Alternative S - E format (e.g., "S2 - E08" or "S2-4")
    alt_se = re.compile(r"\bS?(\d{1,4})\s*-\s*E?(\d{1,4}(?:\.\d)?)", re.IGNORECASE)
    # HiAnime style (if applicable), e.g., "s5_..._ep02"
    hianime = re.compile(r"s(\d{1,4}).*?ep(\d{1,4})", re.IGNORECASE)
    # Gogoanime style (if applicable), e.g., "s5-...episode-02"
    gogoanime = re.compile(r"s(\d{1,4}).*?episode[-_\s]?(\d{1,4})", re.IGNORECASE)

    # Order patterns: try more specific ones first.
    patterns = [
        bracketed_with_season,
        bracketed_without_season,
        explicit_season,
        s_episode,
        subsplease_format,
        subsplease_compact,
        episode_only,
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

            # Try to extract season/episode info using the defined patterns.
            for pattern in patterns:
                match = pattern.search(filename)
                if match:
                    # For the "Episode Y" only pattern, default season to "1".
                    if pattern == episode_only:
                        season = "1"
                        episode = match.group(1)
                    # For the bracketed without season pattern, default season to "1".
                    elif pattern == bracketed_without_season:
                        season = "1"
                        episode = match.group(1)
                    else:
                        season, episode = match.group(1), match.group(2)
                    break

            # Language Detection: Check for "subbed" first, then "dubbed" or "dub".
            lower_name = filename.lower()
            if "subbed" in lower_name:
                language = "Japanese"
            elif "dubbed" in lower_name or "dub" in lower_name:
                language = "English"
            else:
                language = "Japanese"

            # Default to season "1" if missing.
            if not season:
                season = "1"
            if not episode:
                skipped_files.append(filename)
                continue

            # Format season and episode as four-digit numbers.
            season = f"s{int(season):04d}"
            if "." in episode:
                episode_number, part_num = episode.split(".")
                episode = f"e{int(episode_number):04d}"
                part = f" - pt{part_num}"
            else:
                episode = f"e{int(episode):04d}"

            # Check if the episode is an OVA.
            ova_tag = ""
            if ova_pattern.search(filename):
                ova_tag = " [ova]"

            # Extract file extension.
            base_name, file_ext = os.path.splitext(filename)
            file_ext = (
                file_ext.lower()
                if file_ext.lower() in [".mp4", ".mkv", ".avi", ".mov"]
                else ".mp4"
            )

            # Construct folder name.
            if ova_tag:
                target_folder = f"Special"
            else:
                if year:
                    target_folder = f"{show_name} ({year}) [language-{language}]"
                else:
                    target_folder = f"{show_name} [language-{language}]"

            # Construct new filename.
            if year:
                new_filename = f"{show_name} ({year}) [language-{language}] - {season}{episode}{part}{file_ext}"
            else:
                new_filename = f"{show_name} [language-{language}] - {season}{episode}{part}{file_ext}"

            # Create target folder if it doesn't exist.
            target_folder_path = os.path.join(current_folder, target_folder)
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path, exist_ok=True)

            old_path = os.path.join(current_folder, filename)
            new_path = os.path.join(target_folder_path, new_filename)
            files_to_rename.append((old_path, new_path))

    # Display preview.
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
