from datasets import load_dataset, Dataset
import numpy as np

data = load_dataset("csv", data_files={'train':'./level-one-synth-data-with-action-seq.csv'})["train"]

S = {"square", "row", "rectangle", "tower", "diagonal", "diamond", "cube"}
C = {"orange", "red", "green", "blue", "purple", "yellow"}
cols_list = list(C)
block_placements = ["on top of", "to the side of", "touching", "not touching"]
block_removal = [None, "you just placed"]
d = {}
d["dial_with_actions"] = []
for i in range(len(data)):
    for s in S:
        if s in data["dial_with_actions"][i]:
            if s=="tower":
                block_removal_l = block_removal + ["top", "bottom"]
                if len(data["action_seq"][i])%2:
                    block_removal_l += ["centre"]
            elif s=="cube":
                block_removal_l = block_removal + ["corner"]
            elif s=="diamond" and "horizonal" in data["dial_with_actions"][i]:
                block_removal_l = block_removal + ["corner"]
            elif s=="square" and len(data["action_seq"][i])%2==1:
                block_removal_l = block_removal + ["centre"]
            elif s=="row" or s=="diagonal":
                block_removal_l = block_removal + ["end"]
            else:
                block_removal_l = block_removal
    #choose b/w place and removal
    if np.random.randint(2)==0:
        # go for place
        # chose a color
        col = np.random.permutation(cols_list)[0]
        place_loc = np.random.permutation(block_placements)[0]
        lvl2_inst = f"OK now place a {col} block {place_loc} that."
    else:
        # go for removal
        # chose removal location
        rem_loc = np.random.permutation(block_removal_l)[0]
        if rem_loc is None:
            lvl2_inst = f"OK now remove a block."
        elif rem_loc=="you just placed":
            lvl2_inst = f"OK now remove the block {rem_loc}."
        elif rem_loc in ["top","bottom","centre"]:
            lvl2_inst = f"OK now remove the {rem_loc} block."
        elif rem_loc=="corner":
            lvl2_inst = f"OK now remove a {rem_loc} block."
        elif rem_loc=="end":
            lvl2_inst = f"OK now remove an {rem_loc} block."
    print(lvl2_inst)
    d["dial_with_actions"].append(data["dial_with_actions"][i]+ " \n "+ data["action_seq"][i] + " \n " + "<Architect> "+lvl2_inst)

d = Dataset.from_dict(d)
#d.to_csv("./level-two-synth-data.csv")
