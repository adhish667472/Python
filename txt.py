# import os

# current_directory = os.getcwd()
# high_score_file_path = os.path.join(current_directory, "high_score.txt")

# print("Current directory:", current_directory)
# print("High score file path:", high_score_file_path)
high_score=50
with open("high_score.txt", "w") as file:
        file.write(str(high_score))