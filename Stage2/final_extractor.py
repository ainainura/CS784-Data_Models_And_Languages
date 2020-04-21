import codecs
brandNameSet = set()

#Precision = numCorrectBrand/numExtractedBrand
#Recall = numCorrectBrand/numWithBrand
numWithBrand = 0 #The number of products which have a brand - exclude those with "null".
numCorrectBrand = 0 #The number where the extracted brand matches the manually tagged brand.
numExtractedBrand = 0 #The number of products where we identified a brand name (includes false positives)


#Place the brand names in an unordered set for easy lookup
#Also returns the maximum number of words in a brand name for use in the
#brand extraction algorithm.
def buildBrandSet(filename):
	maxBrandWords = 0
	for line in open(filename, encoding="ISO-8859-1"):
    	brand=((str(line)).rstrip()).rstrip()   	 
    	brandNameSet.add(brand.lower())   	 
    	words = len(line.split())
    	if (words > maxBrandWords) :
        	maxBrandWords=words
	return maxBrandWords

#Get a substring of a product name consisting of a given number of words(numWords)
#delimited by spaces, beginning at word "index" (index = the 1st, 2nd, 3rd... word)
def getBrandCandidate(splitString,index,numWords):   	 
	returnStr=""
	for wordNum in range(index, index+numWords) :
    	returnStr+=(splitString[wordNum]+" ")
	return (returnStr.rstrip())

#Brand name extractor. Give it a file of the format matching our seti.txt / setj.txt
#(lines alternate between (product ID - product name) and (brand name), along
#with the maximum number of expected words in a brand name.
#If testMode is set to 1, the extractor will expect our "golden data" and evaluate whether the
#extractor got it correct. If it is not, it will expect a file of the form ID <tab> Product Name
#and will simply print the ID + extracted brand, if there is one.
def extractBrands(filename, maxWords,testMode):
	global numWithBrand
	global numCorrectBrand
	global numExtractedBrand
    
	#Write the results to outFile - start with a header.
	outFile = codecs.open('results.txt','w',"ISO-8859-1")
    
	#only include pass/fail info if running in test mode
	if (testMode):
    	outFile.write('{0} {1} {2} {3}\n' .format('ID','Extracted Brand','Brand','Fail?'))
	else :
    	outFile.write('{0} {1}\n' .format('ID','Extracted Brand'))
   	 
	#Since we may need to read two lines in for each product (for our test data), taking a less
	#elegant approach to reading the file in
	inputFile=open(filename, encoding="ISO-8859-1")
	inputLines=inputFile.readlines()
	lineIndex=0    
	while(lineIndex < len(inputLines)): 	 
    	line=inputLines[lineIndex]
    	lineIndex+=1
    	if (testMode) :
        	#get next line, which corresponds to manually extracted brand
        	correctBrand = (str(inputLines[lineIndex])).rstrip()
        	lineIndex+=1
    	#Reset these variables on for each product
    	wordsToTryMatching=maxWords
    	foundBrand=False
    	brand=""
   	 
    	#Get the product name attribute
    	#First, get the index at which the product name starts
    	productNameIndex=line.find("\'")
    	#Grab product ID - everything up to the first ' which indicates the start of the prod name
    	productID = line[0:productNameIndex-1]
    	#Grab the product name, without the trailing and leading 's
    	productName=line[(productNameIndex+1):(len(line) - 1)]
    	splitProdName=productName.split() #split the product name into its words
    	wordsInProdName=len(splitProdName)
   	 
    	#Try to find a brand name, starting with the largest-size to ensure most
    	#accurate matching   	 
    	while ((wordsToTryMatching > 0)): #& foundBrand==False):
        	#Iterate through the product name left to right,
        	#sliding a "window" to select substrings to try matching until we reach the
        	#point at which the brand names of size wordsToTryMatching would
        	#be too long to exist in the remainder of the product name string
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

    	#Track precision/recall and print a line in results.txt for this product.
    	if(testMode) :
        	if (correctBrand!='null') :
            	numWithBrand+=1
        	if (foundBrand==True): #Got a brand - is it correct, or false positive?
            	numExtractedBrand+=1
            	if (brand.lower()==correctBrand.lower()) :
                	outFile.write('{0} {1} {2} {3}\n' .format(productID,brand,correctBrand,'PASS'))
                	numCorrectBrand+=1
            	else :
                	outFile.write('{0} {1} {2} {3}\n' .format(productID,brand,correctBrand,'FAIL'))    
           	 
        	else : #didn't find a brand, is it a "true negative?"
            	if (correctBrand=='null') :
                	outFile.write('{0} {1} {2} {3}\n' .format(productID,'null','null','PASS'))
            	else :
                 	outFile.write('{0} {1} {2} {3}\n' .format(productID,'null',correctBrand,'FAIL'))
    	else :
        	outFile.write('{0} {1}\n' .format(productID,brand))
	#We're done! Write the precision/recall at the end of the file, and close it.
	outFile.write('\nTotal Products: ' + str(numWithBrand) + '\nCorrect brand extractions: ' + str(numCorrectBrand))
	outFile.write('\nPrecision: ' + str(float(numCorrectBrand)/float(numExtractedBrand)) + '\nRecall: ' + str(float(numCorrectBrand)/float(numWithBrand)))
	outFile.close()
    
#Main program
print('Starting brand dict build\n')
maxBrandWords=buildBrandSet('variation_brand_names.txt')
print('Starting brand extraction\n')
extractBrands('setj.txt', maxBrandWords, 1)

