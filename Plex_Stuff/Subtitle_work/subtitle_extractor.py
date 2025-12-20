import subprocess
import os
import sys

SUBTITLE_EDIT_PATH = r"C:\Program Files\Subtitle Edit\SubtitleEdit.exe"

def check_tools():
	if not os.path.exists(SUBTITLE_EDIT_PATH):
		print("Subtitle Edit executable not found.")
		print("To install Subtitle Edit, visit: https://www.nikse.dk/SubtitleEdit")
		return False

	try:
		subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except FileNotFoundError:
		print("FFmpeg not found. Please install FFmpeg and ensure it's in your system PATH.")
		print("To download FFmpeg, visit: https://ffmpeg.org/download.html")
		return False
	return True

def extract_pgs(file):
	sup_file = os.path.splitext(file)[0] + ".sup"
	print(f"Extracting PGS subtitles from {file} to {sup_file}...")

	# Command: ffmpeg -i input.mkv -map 0:s:0 -c copy output.sup
	cmd = [
		"ffmpeg", "-y",
		"-i", file,
		"-map", "0:s:0",
		"-c", "copy",
		sup_file
	]

	try:
		subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		if os.path.exists(sup_file):
			print(f"PGS subtitles extracted to {sup_file}.")
			return sup_file
		else:
			print("Failed to extract PGS subtitles.")
			return None
	except subprocess.CalledProcessError:
		print("Error during PGS subtitle extraction.")
		return None

def convert_to_srt(sup_file):
	srt_file = os.path.splitext(sup_file)[0] + ".srt"
	print(f"Converting {sup_file} to {srt_file} using Subtitle Edit...")
	cmd = [
		SUBTITLE_EDIT_PATH,
		"/convert",
		sup_file,
		"srt"
	]

	try:
		subprocess.run(cmd, check=True)

		if os.path.exists(srt_file):
			print(f"Converted to SRT: {srt_file}")
			return srt_file
		else:
			print("Failed to convert to SRT.")
			return None
	except subprocess.CalledProcessError:
		print("Error during subtitle conversion.")
		return None


def main():


if __name__ == "__main__":	 main()
