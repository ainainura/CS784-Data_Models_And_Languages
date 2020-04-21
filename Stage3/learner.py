import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import cross_validation
import json
from py_stringmatching import simfunctions
from py_stringmatching import tokenizers

brandNameSet = set()

def buildBrandSet(filename):
    curMax = 0
    l = open(filename, encoding="ISO-8859-1")

    for line in l:
        brand = ((str(line)).rstrip()).rstrip()
        brandNameSet.add(brand.lower())
        words = len(line.split())
        if (words > curMax):
            curMax = words

    return curMax

def getBrandCandidate(splitString,index,numWords):
    returnStr=""
    for wordNum in range(index, index+numWords) :
        returnStr+=(splitString[wordNum]+" ")
        return (returnStr.rstrip())

def getBrand(productName, maxWords):
    wordsToTryMatching=maxWords
    foundBrand=False
    brand=""

    splitProdName=productName.split()
    wordsInProdName=len(splitProdName)

    while ((wordsToTryMatching > 0)):
        iterationCount=wordsInProdName-wordsToTryMatching
        for index in range(0,iterationCount):
            stringToLookup=getBrandCandidate(splitProdName,index,wordsToTryMatching)
            if (stringToLookup.lower() in brandNameSet):
                foundBrand=True
                brand=stringToLookup
            if(foundBrand):
                break
        wordsToTryMatching-=1
        if (foundBrand):
            break

    return brand

maxBrandWords=buildBrandSet('variation_brand_names.txt')

file_base = "y.txt"
lines = [line.rstrip('\n') for line in open(file_base, encoding="ISO-8859-1")]

attrs = ["Product Name", "Product Long Description", "Product Segment", "Product Type", "Brand"]
rec = 0

data = list()
for line in lines:
    parts = line.split('?')

    vals1 = list()
    vals2 = list()
    allattrs = True

    parsed_json = json.loads(parts[2])
    for attr in attrs:
        if attr not in parsed_json:
            if attr != "Brand":
                allattrs = False
                break
            else:
                vals1.append(getBrand(parsed_json["Product Name"][0], maxBrandWords))
        else:
            vals1.append(parsed_json[attr][0].strip('\''))

    if allattrs == False:
        continue

    parsed_json = json.loads(parts[4])
    for attr in attrs:
        if attr not in parsed_json:
            if attr != "Brand":
                allattrs = False
                break
            else:
                vals2.append(getBrand(parsed_json["Product Name"][0], maxBrandWords))
        else:
            vals2.append(parsed_json[attr][0].strip('\''))

    if allattrs == False:
        continue

    if len(vals1) != len(vals2):
        continue

    cur = tuple()
    good = True
    for i in range(0, len(vals1)):
        jscore = simfunctions.jaccard(tokenizers.qgram(vals1[i], 3), tokenizers.qgram(vals2[i], 3))
        '''
        if jscore < 0.1:
            good = False
            break
        '''
        if i != 1:
            cur += (str(simfunctions.needleman_wunsch(vals1[i], vals2[i])),)
            cur += (str(simfunctions.jaro_winkler(vals1[i], vals2[i])),)
            cur += (str(simfunctions.levenshtein(vals1[i], vals2[i])),)

        cur += (str(simfunctions.cosine(tokenizers.qgram(vals1[i], 3), tokenizers.qgram(vals2[i], 3))),)
        cur += (str(jscore),)
    if good == False:
        if parts[5] == "MATCH":
            rec += 1
        continue

    if parts[5] == "MATCH":
        cur += ("1",)
    else:
        cur += ("0",)

    data.append(cur)

numfeatures = attrs.__len__()*5 - 3

dataset = numpy.asarray(data)
X = dataset[:,0:numfeatures]
Y = dataset[:,numfeatures]

model = RandomForestClassifier(n_estimators=100)
pred = cross_validation.cross_val_predict(model, X, Y, cv=5)

tp = 0
prec = 0
for i in range(0, len(pred)):
    if pred[i] == '1':
        prec += 1
        if Y[i] == '1':
            tp += 1

    if Y[i] == '1':
        rec += 1

precision = tp/prec
recall = tp/rec
print(str(precision))
print(str(recall))

#94.5
#83.15
#88.43
