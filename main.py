from merge_files_fct import merge_files


file_paths = ["SH_20_21.json", "SH_21_22.json", "SH_22_23.json", "SH_23_24.json"]
file = "full_spotify_streaming_history_samvilla.json"
merge_files(file_paths, file)
print(f"Merged data written to '{file}")

