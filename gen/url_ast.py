import os
import pprint

def generate(target : str = "./endpoints"):
    def single_file(file : str) -> dict:
        metadata = dict()
        tree = dict()
        with open(file, "r") as f:
            for line in f:
                if line[0] == "#":
                    try:
                        metadata = dict(line[1:])
                    except:
                        raise Exception("malformed metadata file:" + file)
                if "/" in line:
                    spaces = line.replace("\n", "").split(" ")
                    method = spaces[0]
                    deprecated = spaces[-1]
                    if "deprecated" in deprecated:
                        continue
                    endpoint = [x for x in line.replace("\n", "").split(" ")[1].split("/")[1:] if x != ""]
                    temp = tree
                    for i in range(len(endpoint)):
                        try:
                            if "methods" in temp[endpoint[i]].keys() and i == len(endpoint)-1:
                                temp[endpoint[i]]["methods"].append(method)
                        except (KeyError, AttributeError):
                            if i == len(endpoint)-1:
                                if endpoint[i] not in temp.keys():
                                    temp[endpoint[i]] = {"methods": [method]}
                                else:
                                    temp[endpoint[i]]["methods"].append(method)
                            else:
                                temp[endpoint[i]] = {}
                        temp = temp[endpoint[i]]
        return {"tree": tree, "metadata": metadata}

    results = []

    if os.path.isdir(target):
        for root,dirs,files in os.walk(target):
            for file in files:
                results.append(single_file(root + "/" + file))
    elif os.path.isfile(target):
        results.append(single_file(target))
    else:
        raise Exception("What did you pass in?")

    return results

if __name__ == "__main__":
    with open('output.txt', 'w') as out:
        pprint.pp(generate(), stream=out)