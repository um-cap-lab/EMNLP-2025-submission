import os

# imput(processed) file path
input_file = "Desktop/CHILDESdata/processed_childes_data_whole.txt"
child_output_file = "Desktop/CHILDESdata/child_only.txt"
non_child_output_file = "Desktop/CHILDESdata/non_child.txt"

# initialize lists to store sentences
child_sentences = []
non_child_sentences = []

# read the input file line by line
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("CHI:"):  # identify lines spoken by the child
            child_sentences.append(line.replace("CHI:", "").strip())
        elif ":" in line:  # other（MOT, FAT, INV .etc.） lines
            non_child_sentences.append(line.split(":", 1)[1].strip())

# save `child_only.txt`
with open(child_output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(child_sentences))

# save `non_child.txt`
with open(non_child_output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(non_child_sentences))

print(f"🎉 mission completed!")
print(f"👶 save child-only to: {child_output_file}")
print(f"👩🧑 save non-child to: {non_child_output_file}")