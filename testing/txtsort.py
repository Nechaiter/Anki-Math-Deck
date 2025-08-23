from collections import defaultdict

# input_file = "testing/duplicates_by_name.txt"

input_file = "others/duplicated_exercises.txt"
output_file = "testing/duplicates_sorted.txt"


exercise_links = defaultdict(list)
current_title = None
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("https://"):
            if current_title:
                exercise_links[current_title].append(line)
        else:
            current_title = line


with open(output_file, "w", encoding="utf-8") as f:
    for title in sorted(exercise_links):
        if len(exercise_links[title])>1:
            f.write(f"{title}\n")
            for link in exercise_links[title]:
                f.write(f"{link}\n")