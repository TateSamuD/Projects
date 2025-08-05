import sys
import os


if (len.argv<3):
   print("""
         Usage: py video_metadata_updater.py <video_file_path/video_folder_path> <language [English, english, en, etc.]>\n
         video_file_path: Path to the video file.\n
         video_folder_path: Path to the folder containing video file(s).\n
         """
         )
   exit(1)
else:
   path = sys.argv[1]
   language = sys.argv[2]
   if not os.path.exists(path):
      print(f"Error: The path '{path}' does not exist.")
      exit(1)