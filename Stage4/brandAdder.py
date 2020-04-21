###
#This program will add brands from a file of product data to our brand dictionary file.
#First it reads in the existing dictionary into a list (to ensure we do not
#add a duplicate). Then it will parse each product in the product data file and append any brand
#not already included in the dictionary.
###
import json

#Read the existing brand dictionary into a list
def buildBrandDictionary(brandFilename, brandList):
    brands = [brand.rstrip('\n') for brand in open(brandFilename)]
    for brand in brands:
        brandList.append(brand)
    
#Read brands in from a product data file and write to the file if it's not already there.
def getBrandsFromFile(productFilename,brandFilename,brandList):
    brandFile=open(brandFilename,"a")
    lines = [line.rstrip('\n') for line in open(productFilename, encoding="ISO-8859-1")]
    for line in lines:
        jsonParts = line.split('?')
        productOne = json.loads(jsonParts[2])        
        if "Brand" in productOne:
            brand=productOne["Brand"][0].strip('\'')
            if brand not in brandList:                
                brandFile.write('\n' + str(brand))
                brandList.append(brand) #also add it to the list in case productTwo shares the brand

        productTwo = json.loads(jsonParts[4])
        if "Brand" in productTwo:
            brand=productTwo["Brand"][0].strip('\'')
            if brand not in brandList:
                brandFile.write('\n' + str(brand))
                brandList.append(brand)
        

#Run the program
brandList = list()
brandFilename="variation_brand_names.txt"
buildBrandDictionary(brandFilename, brandList)
getBrandsFromFile("elec_pairs_stage3_test1_20K_anon.txt",brandFilename,brandList)

    
