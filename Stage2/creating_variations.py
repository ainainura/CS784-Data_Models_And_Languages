brand_names = [line.rstrip('\n') for line in open("brand_names(3).txt", encoding="ISO-8859-1")]

# first run part for adding variations for AND;
# then run part for adding variations for inc and corp
"""
for brand in brand_names:
    posit = brand.find("&")
    if posit != -1:
        if posit-1 >=0:
            if brand[posit-1]==' ':
                print(brand.replace("&", "and"))
                print(brand.replace("&", "+"))
            else:
                print(brand.replace("&", " and "))
                print(brand.replace("&", " + "))
                print(brand.replace("&", "and"))
                print(brand.replace("&", "+"))

for brand in brand_names:
    posit = brand.find("+")
    if posit != -1:
        if posit-1>=0:
            if brand[posit-1]==' ':
                print(brand.replace("+", "and"))
                print(brand.replace("+", "&"))
            else:
                print(brand.replace("+", " and "))
                print(brand.replace("+", " & "))
                print(brand.replace("+", "and"))
                print(brand.replace("+", "&"))

for brand in brand_names:
    posit = brand.find(" and ")
    if posit != -1:
        print(brand.replace(" and ", " & "))
        print(brand.replace(" and ", " + "))
        print(brand.replace(" and ", "&"))
        print(brand.replace(" and ", "+"))
"""
# case with " inc"
for brand in brand_names:
    posit = brand.find(" inc")
    if posit != -1:
        print(brand.replace(" inc", ""))
        print(brand.replace(" inc", " incorporation"))
        print(brand.replace(" inc", " incorp"))
        print(brand.replace(" inc", " incorp."))
        print(brand.replace(" inc", ", incorp"))
        print(brand.replace(" inc", ", incorp."))
        print(brand.replace(" inc", ", corp."))
        print(brand.replace(" inc", ", corp"))
        print(brand.replace(" inc", ", corporation"))

# case with " Inc",  remove it
for brand in brand_names:
    posit = brand.find(" Inc") # cases with " Inc, Inc."
    # narrowing cases
    if posit != -1:
       # print(brand)
        if posit-1 >= 0:
            if brand[posit-1]==',':
                #print(brand)
                if posit+4<len(brand):
                    # case with ", Inc."
                    if brand[posit+4]=='.':
                       print(brand.replace(", Inc.", ""))
                       print(brand.replace(", Inc.", " incorporation"))
                       print(brand.replace(", Inc.", " incorp"))
                       print(brand.replace(", Inc.", " incorp."))
                       print(brand.replace(", Inc.", " corp."))
                       print(brand.replace(", Inc.", " corp"))
                       print(brand.replace(", Inc.", " corporation"))
                    else:
                        print(brand.replace(", Inc", ""))
                        print(brand.replace(", Inc", " incorporation"))
                        print(brand.replace(", Inc", " incorp"))
                        print(brand.replace(", Inc", " incorp."))
                        print(brand.replace(", Inc", " corp"))
                        print(brand.replace(", Inc", " corp."))
                        print(brand.replace(", Inc", " corporation"))
            elif brand[posit-1]=='-':
                if posit+4<len(brand):
                    if brand[posit+4]=='.':
                        print(brand.replace("- Inc.", ""))
                        print(brand.replace("- Inc.", " incorporation"))
                        print(brand.replace("- Inc.", " incorp"))
                        print(brand.replace("- Inc.", " incorp."))
                        print(brand.replace("- Inc.", " corp."))
                        print(brand.replace("- Inc.", " corp"))
                        print(brand.replace("- Inc.", " corporation"))
                    else:
                        print(brand.replace("- Inc", ""))
                        print(brand.replace("- Inc", " incorporation"))
                        print(brand.replace("- Inc", " incorp"))
                        print(brand.replace("- Inc", " incorp."))
                        print(brand.replace("- Inc", " corp."))
                        print(brand.replace("- Inc", " corp"))
                        print(brand.replace("- Inc", " corporation"))
            else:
                if posit+4<len(brand):
                    if brand[posit+4]=='.':
                        print(brand.replace(" Inc.", ""))
                        print(brand.replace(" Inc.", " incorporation"))
                        print(brand.replace(" Inc.", " incorp"))
                        print(brand.replace(" Inc.", " incorp."))
                        print(brand.replace(" Inc.", " corp."))
                        print(brand.replace(" Inc.", " corp"))
                        print(brand.replace(" Inc.", " corporation"))
                else:
                    print(brand.replace(" Inc", ""))
                    print(brand.replace(" Inc", " incorporation"))
                    print(brand.replace(" Inc", " incorp"))
                    print(brand.replace(" Inc", " incorp."))
                    print(brand.replace(" Inc", " corp."))
                    print(brand.replace(" Inc", " corp"))
                    print(brand.replace(" Inc", " corporation"))

# case with " Corp"/ " Corporation" / " Corp." / " Corporat" 
for brand in brand_names:
    posit = brand.find(" Corp")
    if posit != -1:
        if posit+5 < len(brand):
            if brand[posit+5]=='.':
                print(brand.replace(" Corp.", ""))
                print(brand.replace(" Corp.", " corporation"))
                print(brand.replace(" Corp.", " incorporation"))
                print(brand.replace(" Corp.", " inc"))
                print(brand.replace(" Corp.", " incorp"))
                print(brand.replace(" Corp.", " inc."))
                print(brand.replace(" Corp.", " incorp."))
            elif " Corporation" in brand:
                print(brand.replace(" Corporation", ""))
                print(brand.replace(" Corporation", " corp"))
                print(brand.replace(" Corporation", " corp."))
                print(brand.replace(" Corporation", " inc."))
                print(brand.replace(" Corporation", " incorp."))
                print(brand.replace(" Corporation", " incorp"))
                print(brand.replace(" Corporation", " inc"))
                print(brand.replace(" Corporation", " incorporation"))
            elif " Corporat" in brand:
                print(brand.replace(" Corporat", ""))
                print(brand.replace(" Corporat", " corporation"))
                print(brand.replace(" Corporat", " corp."))
                print(brand.replace(" Corporat", " corp"))
                print(brand.replace(" Corporat", " incorp."))
                print(brand.replace(" Corporat", " inc."))
                print(brand.replace(" Corporat", " incorp"))
                print(brand.replace(" Corporat", " inc"))
                print(brand.replace(" Corporat", " incorporation"))
        else:
            print(brand.replace(" Corp", ""))
            print(brand.replace(" Corp", " corporation"))
            print(brand.replace(" Corp", " corp."))
            print(brand.replace(" Corp", " incorp"))
            print(brand.replace(" Corp", " incorp."))
            print(brand.replace(" Corp", " inc."))
            print(brand.replace(" Corp", " inc"))
            print(brand.replace(" Corp", " incorporation"))

# ", INC." / " INC" / " INC." / ", INC"
for brand in brand_names:
    posit = brand.find(" INC")
    if posit != -1:
        if posit-1 >=0:
            if brand[posit-1]==',':
                if posit+4 < len(brand):
                    if brand[posit+4]=='.':
                        print(brand.replace(", INC.", ""))
                        print(brand.replace(", INC.", " incorporation"))
                        print(brand.replace(", INC.", " incorp"))
                        print(brand.replace(", INC.", " incorp."))
                        print(brand.replace(", INC.", " corp."))
                        print(brand.replace(", INC.", " corp"))
                        print(brand.replace(", INC.", " corporation"))
                    else:
                        print(brand.replace(", INC", ""))
                        print(brand.replace(", INC", " incorporation"))
                        print(brand.replace(", INC", " incorp"))
                        print(brand.replace(", INC", " incorp."))
                        print(brand.replace(", INC", " corp."))
                        print(brand.replace(", INC", " corp"))
                        print(brand.replace(", INC", " corporation"))
            else:
                if posit+4 < len(brand):
                    if brand[posit+4]=='.':
                        print(brand.replace(" INC.", ""))
                        print(brand.replace(" INC.", " incorporation"))
                        print(brand.replace(" INC.", " incorp"))
                        print(brand.replace(" INC.", " incorp."))
                        print(brand.replace(" INC.", " corp"))
                        print(brand.replace(" INC.", " corp."))
                        print(brand.replace(" INC.", " corporation"))
                    else:
                        print(brand.replace(" INC", ""))
                        print(brand.replace(" INC", " incorporation"))
                        print(brand.replace(" INC", " incorp"))
                        print(brand.replace(" INC", " incorp."))
                        print(brand.replace(" INC", " corp"))
                        print(brand.replace(" INC", " corp."))
                        print(brand.replace(" INC", " corporation"))


