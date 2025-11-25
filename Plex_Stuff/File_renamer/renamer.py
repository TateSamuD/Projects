import os
import re
import shutil
from tqdm import tqdm


def rename_files(show_name):

    rip_pattern_0 = re.compile(
        r"(s\d{1,2}[\s._-]e\d{1,2})", re.IGNORECASE
    )  # Pattern to match S01_E01, S01-E01, S01.E01
    rip_pattern_1 = re.compile(
        r"(s\d{1,2}e\d{1,2})", re.IGNORECASE
    )  # Pattern to match S01E01
    rip_pattern_2 = re.compile(
        r"(\d{1,2}x\d{1,2})", re.IGNORECASE
    )  # Pattern to match 1x01
    rip_pattern_3 = re.compile(
        r"(season[\s._-]?(\d{1,4})[\s._-]?episode[\s._-]?(\d{1,4}))", re.IGNORECASE
    )  # Pattern to match season 01 episode 01
    rip_pattern_4 = re.compile(
        r"(season[\s._-]?(\d{1,4})[\s._-]?ep[\s._-]?(\d{1,4}))", re.IGNORECASE
    )  # Pattern to match season 01 ep 01
    rip_pattern_5 = re.compile(
        r"(ep[\s._-]?(\d{1,4}))", re.IGNORECASE
    )  # Pattern to match ep 01
    rip_pattern_6 = re.compile(
        r"(episode[\s._-]?(\d{1,4}))", re.IGNORECASE
    )  # Pattern to match episode 01
    rip_pattern_7 = re.compile(
        r"(e[\s._-]?(\d{1,4}))", re.IGNORECASE
    )  # Pattern to match e 01

    plex_pattern = re.compile(
        r"s(\d{1,4})e(\d{1,4})", re.IGNORECASE
    )  # Pattern to match - s0001e0001

    patterns = [
        plex_pattern,
        rip_pattern_0,
        rip_pattern_1,
        rip_pattern_2,
        rip_pattern_3,
        rip_pattern_4,
        rip_pattern_5,
        rip_pattern_6,
        rip_pattern_7,
    ]
    # Strip sanitise and organise video files
    current_folder = os.getcwd()
    total_files = len([f for f in os.listdir(current_folder) if f.endswith(("mp4"))])

    files_to_rename = []
    skipped_files = []

    video_files = [f for f in os.listdir(current_folder) if f.endswith(("mp4"))]

    for filename in tqdm(video_files, desc="Processing Files", unit="file"):
        if filename.endswith(("mp4")):
            season, episode = None, None

            season, episode = extract_season_episode(filename, patterns)
            # season = season_l[0]
            # episode = episode_l[0]
            ova_tag = ""
            if re.search(r"\bOVA\b", filename, re.IGNORECASE):
                ova_tag = "_[OVA]"

            if not season:
                season = "1"

            if not episode:
                skipped_files.append(filename)
                continue

            season = f"s{int(season):04d}"
            episode = f"e{int(episode):04d}"

            base_name, base_ext = os.path.splitext(filename)
            base_ext = (
                base_ext.lower()
                if base_ext.lower() in [".mp4", ".mkv", ".avi", ".mov"]
                else ".mp4"
            )

            if ova_tag:
                target_folder = "Special"
            else:
                target_folder = f"{show_name}"

            new_filename = f"{show_name}_-_{season}{episode}{ova_tag}{base_ext}"

            target_folder_path = os.path.join(current_folder, target_folder)
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path, exist_ok=True)

            # Move the file to the target folder
            old_file_path = os.path.join(current_folder, filename)
            new_file_path = os.path.join(target_folder_path, new_filename)
            files_to_rename.append((old_file_path, new_file_path))

    print(f"Total files to rename: {len(files_to_rename)}")
    print("\nPreview of Files to be Renamed:")
    for old_path, new_path in files_to_rename:
        print(f"<--{os.path.basename(old_path)}\n-->{os.path.basename(new_path)}")

    confirm = (
        input("\nDo you want to proceed with renaming? (yes/no): ").strip().lower()
    )
    if confirm != "yes":
        print("\n\nOperation cancelled. No files were renamed.")
        return

    renamed_files = 0
    for old_path, new_path in files_to_rename:
        shutil.move(old_path, new_path)
        renamed_files += 1
        # f"Renamed: {os.path.basename(old_path)} \n\t\t--> {os.path.basename(new_path)}")

    print(f"\nRenaming completed. {renamed_files} files were renamed.")
    # Input a folder with video files

    # Organise Files by episode number
    # Match episode patterns like S01E01, s01e01

    # Output a folder with a collection of renamed files


def extract_season_episode(filename, patterns):
    season, episode = None, None
    for pattern in patterns:
        match = pattern.search(filename)
        if match:
            if pattern.pattern == patterns[0].pattern:  # plex_pattern
                season = match.group(1)
                episode = match.group(2)
            elif pattern.pattern == patterns[1].pattern:  # rip_pattern_0
                season = re.search(r"s(\d{1,2})", match.group(0), re.IGNORECASE)
                season = re.sub(r"s", "", season.group(0), flags=re.IGNORECASE)
                episode = re.search(r"e(\d{1,2})", match.group(0), re.IGNORECASE)
                episode = re.sub(r"e", "", episode.group(0), flags=re.IGNORECASE)
            elif pattern.pattern == patterns[2].pattern:  # rip_pattern_1
                season = re.search(r"s(\d{1,2})", match.group(0), re.IGNORECASE)
                season = re.sub(r"s", "", season.group(0), flags=re.IGNORECASE)
                episode = re.search(r"e(\d{1,2})", match.group(0), re.IGNORECASE)
                episode = re.sub(r"e", "", episode.group(0), flags=re.IGNORECASE)
            elif pattern.pattern == patterns[3].pattern:  # rip_pattern_2
                season = re.search(r"(\d{1,2})x", match.group(0), re.IGNORECASE)
                episode = re.search(r"x(\d{1,2})", match.group(0), re.IGNORECASE)
                episode = re.sub(r"x", "", episode.group(0), flags=re.IGNORECASE)
            elif (
                pattern.pattern == patterns[4].pattern
                or pattern.pattern == patterns[5].pattern
            ):  # rip_pattern_3 or rip_pattern_4
                season = re.search(
                    r"season[\s._-]?(\d{1,4})", match.group(1), re.IGNORECASE
                )
                season = re.sub(
                    r"season[\s._-]?", "", season.group(0), flags=re.IGNORECASE
                )
                episode = re.search(
                    r"episode[\s._-]?(\d{1,4})", match.group(1), re.IGNORECASE
                )
                episode = re.sub(
                    r"episode[\s._-]?", "", episode.group(0), flags=re.IGNORECASE
                )
            elif (
                pattern.pattern == patterns[6].pattern
                or pattern.pattern == patterns[7].pattern
                or pattern.pattern == patterns[8].pattern
            ):  # rip_pattern_5 or rip_pattern_6 or rip_pattern_7
                season = "1"
                episode = re.search(
                    r"ep[\s._-]?(\d{1,4})", match.group(0), re.IGNORECASE
                )
            break
    return season, episode


if __name__ == "__main__":
    print(
        """

         Plex Tv-Show Renamer

         Expected file format examples:
         - ShowName_S01E01.mp4
         - Show.Name.S01.E01.mp4
         - Show-Name-1x01.mp4
         """
    )
    name = input("Enter the name of the show: ")
    rename_files(name)
