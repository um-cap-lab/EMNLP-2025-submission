import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the models and their performances on different constructions
models = [
    "GPT-2", "GPT-2-10M", "GPT-2-100M",
    "ConcreteGPT", "BabbleGPT"
]

constructions = [
    "Gap Distance\n(Obj)", "Gap Distance\n(PP)",
    "Double Gaps", "Wh-Islands", "Adjunct Islands"
]

# Binary matrix representing whether the model passed grammaticality test for each construction
# 1 = passed, 0 = failed
performance = [
    [1, 1, 1, 1, 1],      # GPT-2
    [0, 0, 1, 1, 0],      # GPT-2-10M
    [1, 0, 1, 1, 1],      # GPT-2-100M
    [0, 0, 1, 1, 1],      # ConcreteGPT
    [1, 0, 1, 1, 1]       # BabbleGPT
]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 5))
cmap = plt.cm.get_cmap('Greens')
ax.imshow(performance, cmap=cmap, vmin=0, vmax=1)

# Set axis labels
ax.set_xticks(range(len(constructions)))
ax.set_xticklabels(constructions, fontsize=10)
ax.set_yticks(range(len(models)))
ax.set_yticklabels(models, fontsize=10)

# Annotate cells with pass/fail text
for i in range(len(models)):
    for j in range(len(constructions)):
        text = "✓" if performance[i][j] == 1 else "✗"
        ax.text(j, i, text, ha='center', va='center', color='black', fontsize=12)

# Title and formatting
ax.set_title("Grammaticality Test Performance of BabyLM-Trained Models", fontsize=14)
plt.tight_layout()

plt.show()
