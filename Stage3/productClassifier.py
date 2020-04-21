from py_stringmatching import simfunctions, tokenizers
import numpy
import json
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import cross_validation

featuresAll = [] #2D Array - each row contains the sim scores for a product pair.
classifications = [] #An entry for each product pair. 1 == match, 0 == mismatch

lines = [line.rstrip('\n') for line in open('x.txt', encoding="ISO-8859-1")]

#Evaluate each product pair, building the list of feature sets
for line in lines:
    parts = line.split('?')
    stringOne = ""
    stringTwo = ""
    foundFirst = False
    givenMatch = ""
    #simScores[0] = Jaro score for Segment
    simScores = []
    
    #Extract the json representation of each product.
    for part in parts:
        if part.startswith('{') and part.endswith('}') and foundFirst==False:
            foundFirst=True
            productOne = json.loads(part)
        elif part.startswith('{') and part.endswith('}'):
            productTwo = json.loads(part)
        if str(part)=="MATCH" or str(part)=="MISMATCH" :
            givenMatch = str(part)

    #Now that we have the two products, try to compare the desired attributes
    #Product Segment
    for key, value in productOne.items():
            if stringOne!="": break #quit once we have found the desired attr
            if key == "Product Segment":
                stringOne=str(value)
                for key, value in productTwo.items():
                    if stringTwo!="": break
                    if key == "Product Segment":
                        stringTwo=str(value)

    #Run desired similarity measures for Segment
    simScores.append(simfunctions.jaro(stringOne,stringTwo))    

    #Sim measures for Product Name
    stringOne=""
    stringTwo=""
    for key, value in productOne.items():
            if stringOne!="": break #quit once we have found the desired attr
            if key == "Product Name":
                stringOne=str(value)
                for key, value in productTwo.items():
                    if stringTwo!="": break
                    if key == "Product Name":
                        stringTwo=str(value)

    simScores.append(simfunctions.jaro(stringOne,stringTwo))
    simScores.append(simfunctions.jaro_winkler(stringOne,stringTwo))
    #Word-based set-based sim scores
    simScores.append(simfunctions.jaccard(stringOne.split(),stringTwo.split()))
    #3-gram based set-based sim scores
    simScores.append(simfunctions.jaccard(tokenizers.qgram
                                          (stringOne,3),(tokenizers.qgram
                                          (stringTwo,3))))
    simScores.append(simfunctions.overlap_coefficient(tokenizers.qgram
                                          (stringOne,3),(tokenizers.qgram
                                          (stringTwo,3))))
    simScores.append(simfunctions.cosine(tokenizers.qgram
                                          (stringOne,3),(tokenizers.qgram
                                          (stringTwo,3))))

    #Sim measures for Brand Name
    stringOne=""
    stringTwo=""
    for key, value in productOne.items():
            if stringOne!="": break #quit once we have found the desired attr
            if key == "Brand":
                stringOne=str(value)
                for key, value in productTwo.items():
                    if stringTwo!="": break
                    if key == "Brand":
                        stringTwo=str(value)
    simScores.append(simfunctions.jaro_winkler(stringOne,stringTwo))
    simScores.append(simfunctions.jaccard(stringOne.split(),stringTwo.split()))
    simScores.append(simfunctions.cosine(tokenizers.qgram
                                          (stringOne,3),(tokenizers.qgram
                                          (stringTwo,3))))
    simScores.append(simfunctions.jaccard(tokenizers.qgram
                                          (stringOne,3),(tokenizers.qgram
                                          (stringTwo,3))))

    #Sim measures for Product Type (to do...)
    
    #Add Match/Mismatch as the final feature
    if givenMatch=="MATCH":
        classifications.append(1)
    else:
        classifications.append(0)
    
    #Insert the sim scores into the list of product pair feature sets
    featuresAll.append(simScores)
    
    #print(simScores) #debug to verify that the scores are calculating as expected

#Now all features have been calculated. Build the learner. 
x = numpy.array(featuresAll)
y = numpy.array(classifications)
#model = GaussianNB()
model = RandomForestClassifier(n_estimators=100)
model.fit(x,y)
print(model)

predicted = model.predict(x)
print(metrics.classification_report(y, predicted))

scores = cross_validation.cross_val_score(model, x, y, cv=5, scoring='precision')
print(scores)
print(scores.mean())
