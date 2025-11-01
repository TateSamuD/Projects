import os
import re
import shutil
from tqdm import tqdm

def rename_files(show_name):

	rip_pattern_0 = re.compile(r'(s\d{1,2}[\s._-]e\d{1,2})', re.IGNORECASE) # Pattern to match S01_E01, S01-E01, S01.E01
	rip_pattern_1 = re.compile(r'(s\d{1,2}e\d{1,2})', re.IGNORECASE) # Pattern to match S01E01
	rip_pattern_2 = re.compile(r'(\d{1,2}x\d{1,2})', re.IGNORECASE) # Pattern to match 1x01

	plex_pattern = re.compile(r'(s\d{1,4}[-]e\d{1,4})', re.IGNORECASE) # Pattern to match S01-E01 with 4 digit support

	patterns = [rip_pattern_0, rip_pattern_1, rip_pattern_2, plex_pattern]
	# Strip sanitise and organise video files
	current_folder = os.getcwd()
	total_files = len(
		[
			f
			for f in os.listdir(current_folder)
			if f.endswith(('mp4'))
		]
	)

	files_to_rename = []
	skipped_files = []

	video_files = [
		f
		for f in os.listdir(current_folder)
		if f.endswith(('mp4'))
	]

	for filename in tqdm(video_files, desc="Processing Files", unit="file"):
		if filename.endswith(('mp4')):
			season, episode = None, None

			season, episode = extract_season_episode(filename, patterns)

			ova_tag = ""
			if re.search(r'\bOVA\b', filename, re.IGNORECASE):
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
				if base_ext.lower() in ['.mp4', '.mkv', '.avi', '.mov']
				else '.mp4'
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
		print(f"{os.path.basename(old_path)}  \n\t\t-->  {os.path.basename(new_path)}")

	confirm = input("\nDo you want to proceed with renaming? (yes/no): ").strip().lower()
	if confirm != 'yes':
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
			season = re.search(r's(\d{1,2})', match.group(0), re.IGNORECASE)
			if season:
				season = season.group(1)
			episode = re.search(r'e(\d{1,2})', match.group(0), re.IGNORECASE)
			if episode:
				episode = episode.group(1)
		break
	return season, episode

if __name__ == "__main__":
	print("""

			Plex Tv-Show Renamer

			Expected file format examples:
			- ShowName_S01E01.mp4
			- Show.Name.S01.E01.mp4
			- Show-Name-1x01.mp4
			""")
	name = input("Enter the name of the show: ")
	rename_files(name)