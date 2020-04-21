###
#Description: This program will run the leaner in a debug mode, printing information regarding misclassified/unclassifiable examples
#This will generate 3 files: falsePositives.txt, falseNegatives.txt, and unknowns.txt. The names are self-explanatory :)
#The files will contain the attributes for these products. From this, we can look for ways to improve our matcher either by cleaning the
#data or adding hand-coded rules to the matcher.
###
import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import cross_validation
import json
import re
from py_stringmatching import simfunctions
from py_stringmatching import tokenizers

###Brand Extractor helper code###
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
###End Brand Extractor code###


###Debug Code###

#Files to write debug output to regarding product pairs our matcher did not classify correctly.
falsePosFile = open("falsePositives.txt", "w+")
falseNegFile = open("falseNegatives.txt", "w+")
truePosFile = open("truePositives.txt", "w")
unknownFile = open("unknowns.txt", "w+")

#Write a product pair to a given file
#Parameters: the json representation of the two products, the list of attributes,
###whether the pair was actually a match or mismatch, and the file to write to
def printPair(productOne, productTwo, attrs, actualMatch, file):
    file.write(str(actualMatch) + "\n")

    #additing additional color attribute to this list since we have a rule for color. We do NOT want this attribute to be in the global list though
    attrs.append("Color")

    for attr in attrs:
        file.write(str(attr) + ": \n")
        
        if attr not in productOne:
            prodOneVal=""
        else:
            prodOneVal=str(productOne[attr])
            
        if attr not in productTwo:
            prodTwoVal=""
        else:
            prodTwoVal=str(productTwo[attr])
            
        file.write('\t' + "Product 1 Value: " + prodOneVal + '\n')
        file.write('\t' + "Product 2 Value: " + prodTwoVal + '\n')
    file.write('\n')

    attrs.remove("Color")

###End Debug Code###


###Learner/Matcher Code###
    
file_base = "y.txt"
lines = [line.rstrip('\n') for line in open(file_base, encoding="ISO-8859-1")]

attrs = ["Product Name", "Product Long Description", "Product Segment", "Product Type", "Brand"]
wordstoremove = ["of", "and", "the", "at", "that", "for", "to", "as", "this", "you", "we", "too", "a", ","]
wordsremovalregex = re.compile('|'.join(map(re.escape, wordstoremove)))
rec = 0
tp = 0
prec = 0

data = list()
prodPairs=list()

def handleUnknown(prod1, prod2, label):
    global rec, tp, prec

    hasColor = False
    if "Color" in prod1 and "Color" in prod2:
        hasColor = True

    if (hasColor == False or (hasColor == True and prod1["Color"][0] == prod2["Color"][0])) and wordsremovalregex.sub("", prod1["Product Name"][0]) == wordsremovalregex.sub("", prod2["Product Name"][0]):
        if wordsremovalregex.sub("", prod1["Product Name"][0]) == wordsremovalregex.sub("", prod2["Product Name"][0]):
            prec += 1
            if parts[5] == "MATCH":
                tp += 1
                printPair(productOne, productTwo, attrs, parts[5],truePosFile)
            else:
                printPair(productOne, productTwo, attrs, parts[5],falsePosFile)
        else:
            printPair(productOne, productTwo, attrs, parts[5],unknownFile)
        if label == "MATCH":
            rec += 1

def handleColor(prod1, prod2):
    colorcheckattrs = ["Product Name", "Product Long Description", "Product Short Description"]
    colors = ["Red", "Green", "Black", "Blue", "Yellow", "White", "Maroon", "Purple", "Orange", "Lavender", "Multicolor", "Gray", "Ivory", "Silver", "Tan"]

    if "Color" in prod1 and "Color" in prod2 and (prod1["Color"][0] == prod2["Color"][0]):
        return 1
    elif "Color" in prod1:
        color = prod1["Color"][0].strip('\'')
        for attr in colorcheckattrs:
            if attr in prod2:
                attrval = re.sub(r"<[^>]+>", "", prod2[attr][0].strip('\''), count=0)
                if color in attrval:
                    return 1
        return -1
    elif "Color" in prod2:
        color = prod2["Color"][0].strip('\'')
        for attr in colorcheckattrs:
            if attr in prod1:
                attrval = re.sub(r"<[^>]+>", "", prod1[attr][0].strip('\''), count=0)
                if color in attrval:
                    return 1
        return -1
    else:
        colorsets = [set(), set()]
        prodstocheck = [prod1, prod2]

        for i in range(0, len(prodstocheck)):
            for attr in colorcheckattrs:
                if attr in prodstocheck[i]:
                    attrval = re.sub(r"<[^>]+>", "", prodstocheck[i][attr][0].strip('\''), count=0)
                    for color in colors:
                        if color in attrval:
                            colorsets[i].add(color)

        if len(colorsets[0]) > 0 and len(colorsets[1]) > 0:
            if len(colorsets[0].intersection(colorsets[1])) != 0:
                return 1
            else:
                return -1
        else:
            return -1

for line in lines:
    parts = line.split('?')

    vals1 = list()
    vals2 = list()
    allattrs = True

    productOne = json.loads(parts[2])
    productTwo = json.loads(parts[4])

    for attr in attrs:
        if attr not in productOne:
            if attr != "Brand":
                allattrs = False
                break
            else:
                vals1.append(getBrand(productOne["Product Name"][0], maxBrandWords))
        else:
            attrval = productOne[attr][0].strip('\'')
            if attr == "Product Long Description":
                if attrval.find("<") != -1:
                    attrval = re.sub(r"<[^>]+>", "", attrval, count=0)
            attrval = wordsremovalregex.sub("", attrval)
            vals1.append(attrval)
    
    if allattrs == False:
        handleUnknown(productOne, productTwo, parts[5])
        continue

    for attr in attrs:
        if attr not in productTwo:
            if attr != "Brand":
                allattrs = False
                break
            else:
                vals2.append(getBrand(productTwo["Product Name"][0], maxBrandWords))
        else:
            attrval = productTwo[attr][0].strip('\'')
            if attr == "Product Long Description":
                if attrval.find("<") != -1:
                    attrval = re.sub(r"<[^>]+>", "", attrval, count=0)
            attrval = wordsremovalregex.sub("", attrval)
            vals2.append(attrval)

    if allattrs == False:
        handleUnknown(productOne, productTwo, parts[5])
        continue

    if len(vals1) != len(vals2):
        handleUnknown(productOne, productTwo, parts[5])
        continue

    cur = tuple()
    for i in range(0, len(vals1)):
        jscore = simfunctions.jaccard(tokenizers.qgram(vals1[i], 3), tokenizers.qgram(vals2[i], 3))

        if i != 1:
            cur += (str(simfunctions.needleman_wunsch(vals1[i], vals2[i])),)
            cur += (str(simfunctions.jaro_winkler(vals1[i], vals2[i])),)
            cur += (str(simfunctions.levenshtein(vals1[i], vals2[i])),)

        cur += (str(simfunctions.cosine(tokenizers.qgram(vals1[i], 3), tokenizers.qgram(vals2[i], 3))),)
        cur += (str(jscore),)

    
    retVal = handleColor(productOne, productTwo)
    if retVal != -1:
        cur += (str(retVal),)
    else:
        handleUnknown(productOne, productTwo, parts[5])
        continue
    
    ##Test: refuse to make a prediction for anything with non-matching Product Type
    if vals1[3] != vals2[3]:
        if parts[5]== "MATCH":
            rec += 1
        continue
    
    pname1 = productOne["Product Name"][0]
    pname2 = productTwo["Product Name"][0]
    if "Refurbished" in pname1 or "refurbished" in pname2:
        if "Refurbished" not in pname1 and "refurbished" not in pname2:
            #cur+=("1",)
            #Flag as mismatch
            if parts[5] == "MATCH":
                rec += 1
            continue
        #else: #both have it
            #cur+=("0",)
    elif "Refurbished" in pname1 or "refurbished" in pname2:
        if "Refurbished" not in pname1 and "refurbished" not in pname2:
            #cur+=("1",)
            #Flag as mismatch
            if parts[5] == "MATCH":
                rec += 1
            continue
        #else: #both have it
            #cur+=("0",)
    #else: #neither have it
        #cur+=("0",)

    if parts[5] == "MATCH":
        cur += ("1",)
    else:
        cur += ("0",)

    data.append(cur)
    
    prodPair=list()
    prodPair.append(productOne)
    prodPair.append(productTwo)
    prodPairs.append(prodPair)
    
numfeatures = attrs.__len__()*5 - 3# + 1

dataset = numpy.asarray(data)
X = dataset[:,0:numfeatures]
Y = dataset[:,numfeatures]

model = RandomForestClassifier(n_estimators=100)
pred = cross_validation.cross_val_predict(model, X, Y, cv=5)

for i in range(0, len(pred)):
    
    if pred[i] == '1':
        prod1 = prodPairs[i][0]
        prod2 = prodPairs[i][1]

        if "Color" in prod1 and "Color" in prod2 and prod1["Color"][0] != prod2["Color"][0]:
            pred[i] = '0'
    

    if pred[i] == '1':
        prec += 1
        if Y[i] == '1':
            tp += 1
            printPair(prodPairs[i][0],prodPairs[i][1],attrs,"MATCH",truePosFile)
        else: #False Positive
            printPair(prodPairs[i][0],prodPairs[i][1],attrs,"MISMATCH",falsePosFile)

    if Y[i] == '1':
        rec += 1
        if pred[i] == '0': #False Negative
            printPair(prodPairs[i][0],prodPairs[i][1],attrs,"MATCH",falseNegFile)

precision = tp/prec
recall = tp/rec
print(str(precision))
print(str(recall))
