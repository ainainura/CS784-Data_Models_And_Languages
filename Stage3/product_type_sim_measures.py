from py_stringmatching import simfunctions, tokenizers
import json

attr_count_dict = dict()
attr_vals_dict = dict()
f = open('prod_type.txt','w')
lines = [line.rstrip('\n') for line in open('x.txt', encoding="ISO-8859-1")]
for line in lines:
    parts = line.split('?')
    str1 = ""
    str2 = ""
    i = 0
    for part in parts:
        i = i + 1
        if part.startswith('{') and part.endswith('}'):
            json_part = json.loads(part)
            for key, value in json_part.items():
                if key in attr_count_dict:
                    attr_count_dict[key] = attr_count_dict[key] + 1
                    attr_vals_dict[key].add(str(value))
                    if key == "Product Type" and i == 3:
                        str1 = str(value)
                    if key == "Product Type" and i == 5:
                        str2 = str(value)
                else:
                    attr_count_dict[key] = 1
                    attr_vals_dict[key] = set()
                    attr_vals_dict[key].add(str(value))
                    if key == "Product Type":
                        str1 = str(value)
    #l = simfunctions.levenshtein(str1, str2) ## integer values smaller than needleman
    #l = simfunctions.needleman_wunsch(str1, str2) # very large values
    l = simfunctions.jaro(str1, str2) # from 0 to 1
    #l = simfunctions.jaro_winkler(str1, str2) # from 0 to 1
    #l = simfunctions.smith_waterman(str1, str2) # i don't really want to use this
    #l = simfunctions.affine(str1, str2) # also large values
    #l = simfunctions.jaccard([str1], [str2]) # either 0 or 1
    f.write(str(l))
    f.write("\n")
    print(l)
f.close()
