import json
import csv
from django.template.defaultfilters import slugify

template = {
  "model": "api_v2.creatureset",
  "pk": "",
  "fields": {
    "name": "",
    "document": "srd",
    "type": "environment",
    "creatures": []
  }
}


temp_maps = []

with open("./scripts/env-map.csv", 'r') as envmap:
    envmap_obj = csv.reader(envmap)

    

    for row in envmap_obj:
        if row[0] not in ["","name"]:
            temp_map = {}
            temp_map["creature_key"] = creature_key = slugify(row[0])
            temp_map["envs"] = []
            for i in range(1,4):
                if row[i] not in ["","environments-1","environments-2","environments-3","environments-4"]:
                    temp_map["envs"].append(slugify(row[i]))
            # Problem 1: Plurals
            for i, env in enumerate(temp_map["envs"]):
                if env.endswith("s") and env not in ["abyss"]:
                    # It's a plural
                    env_fixed = env[:-1]
                    temp_map["envs"][i] = env_fixed
                # Problem 4 underdark
                if env == "underdark":
                    temp_map["envs"][i] = "underworld"
                    

            # Problem 2: "Any"
            for env in temp_map["envs"]:
                if env == "any":
                    temp_map["envs"].remove(env)

            # Problem 3: Duplicates
            temp_map["envs"] = list(set(temp_map["envs"]))

            temp_maps.append(temp_map)

environments = []

for temp_map in temp_maps:
    for map_env in temp_map["envs"]:
        if map_env not in environments:
            environments.append(map_env)

environment_sets = []

for env in environments:
    new_cs = {
  "model": "api_v2.creatureset",
  "pk": "",
  "fields": {
    "name": "",
    "document": "srd",
    "type": "environment",
    "creatures": []
  }
}
    new_cs["pk"] = env
    new_cs["fields"]["name"] = env.title()
    for temp_map in temp_maps:
        if env in temp_map["envs"]:
            new_cs["fields"]["creatures"].append(temp_map["creature_key"])
    
    environment_sets.append(new_cs)

    all_creature_pks = []
    with open("data/v2/wizards-of-the-coast/srd/Creature.json", "r") as cf:
        creatures = json.load(cf)
        for c in creatures:
            all_creature_pks.append(c["pk"])
        
    print(len(all_creature_pks))
    if temp_map["creature_key"] not in all_creature_pks:
        print(temp_map)

with open("test.json",'w', encoding='utf-8') as out:
    json.dump(environment_sets, out)