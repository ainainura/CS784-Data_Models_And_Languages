from py_stringmatching import simfunctions, tokenizers
import numpy
import json
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import cross_validation
from sklearn.svm import SVC

featuresAll = [] #2D Array - each row contains the sim scores for a product pair.
classifications = [] #An entry for each product pair. 1 == match, 0 == mismatch

lines = [line.rstrip('\n') for line in open('y.txt', encoding="ISO-8859-1")]

#Evaluate each product pair, building the list of feature sets
for line in lines:    
    parts = line.split('?')
    stringOne = ""
    stringTwo = ""
    foundFirst = False
    givenMatch = ""
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
    #Discard any pair missing attributes (implicitly labelling them "Unknown")
    if (stringOne=="" or stringTwo==""): continue
        
    #Run desired similarity measures for Segment
    score = simfunctions.jaro(stringOne,stringTwo)
    simScores.append(score)

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
    #Discard any pair missing attributes (implicitly labelling them "Unknown")
    if (stringOne=="" or stringTwo==""): continue
    #Discard pairs with sim scores in a range that we are not confident in predicting a match.
    score = simfunctions.jaro(stringOne,stringTwo)
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
    
    score = simfunctions.jaro_winkler(stringOne,stringTwo)
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
    
    score = simfunctions.jaccard(stringOne.split(),stringTwo.split())
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
    
    score = simfunctions.jaccard(tokenizers.qgram(stringOne,3),(tokenizers.qgram
                                                      (stringTwo,3)))
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)

    score = simfunctions.overlap_coefficient(tokenizers.qgram
                                              (stringOne,3),(tokenizers.qgram
                                              (stringTwo,3)))
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
    
    score = simfunctions.cosine(tokenizers.qgram
                                              (stringOne,3),(tokenizers.qgram
                                              (stringTwo,3)))
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)

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
    #Discard any pair missing attributes (implicitly labelling them "Unknown")
    #if (stringOne=="" or stringTwo==""): continue    
        
    score = simfunctions.jaro_winkler(stringOne,stringTwo)
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
          
    score = simfunctions.jaccard(stringOne.split(),stringTwo.split())
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
    
    score = simfunctions.cosine(tokenizers.qgram
                                                  (stringOne,3),(tokenizers.qgram
                                                  (stringTwo,3)))
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)
    
    score = simfunctions.jaccard(tokenizers.qgram
                                                  (stringOne,3),(tokenizers.qgram
                                                  (stringTwo,3)))
    if ((score > 0.3) and (score < 0.7)): continue
    else: simScores.append(score)

    #Sim measures for Product Type
    stringOne=""
    stringTwo=""
    for key, value in productOne.items():
            if stringOne!="": break #quit once we have found the desired attr
            if key == "Product Type":
                stringOne=str(value)
                for key, value in productTwo.items():
                    if stringTwo!="": break
                    if key == "Product Type":
                        stringTwo=str(value)
    #Discard any pair missing attributes (implicitly labelling them "Unknown")
    if (stringOne=="" or stringTwo==""): continue
    
    score = simfunctions.jaro(stringOne,stringTwo)
    simScores.append(score)
    
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
#model = SVC(C=1.0)
model.fit(x,y)
print(model)

predicted = model.predict(x)
print(metrics.classification_report(y, predicted))

scores = cross_validation.cross_val_score(model, x, y, cv=5, scoring='precision')
print(scores)
print(scores.mean())
