from term_image.image import from_url
import subprocess
import os
import time

subprocess.run("clear")

#BRANDING
print("      __        __   ___     __       __  ___  ___        __ ")
print("|__/ |__) |  | |  \ |__     /__  \ / /__   |  |__   |\/| /__ ")
print("|  \ |  \ \__/ |__/ |___    .__/  |  .__/  |  |___  |  | .__/")
print("https://krude-systems.net/furr.html")
print("")
print("E621_CLI utility/interface [ctrl+z] to exit")
print("Dependencies: wget python3 term-image(python library)")

#==========API LOGIN==========
#check if file already exists
if os.path.isfile("prgmDir/lgn.txt"):
    #get login info proceed if correct, prompt overwrite if not
    with open("prgmDir/lgn.txt", 'r') as file:
        lgnFile = file.read()
    username = lgnFile[lgnFile.find('USR:') + 4:lgnFile.find('API:')]
    API_key = lgnFile[lgnFile.find('API:') + 4::]

else:
    #create file
    subprocess.run(["mkdir", "prgmDir"])
    print("The following is for API access/login")
    username = input("Enter Username: ")
    API_key = input("Enter API key: ")
    
    with open("prgmDir/lgn.txt", "w") as myfile:
	    myfile.write('USR:' + username + 'API:' + API_key)

print("Welcome: " + username + "!")
while True:
    tmp = input("Continue or Re-login [c/r]?: ")
    if tmp == "" or tmp == "c":
         break
    elif tmp == "r":
        print("The following is for API access/login")
        username = input("Enter Username: ")
        API_key = input("Enter API key: ")
        
        with open("prgmDir/lgn.txt", "w") as myfile:
            myfile.write('USR:' + username + 'API:' + API_key)
        print("Welcome: " + username + "!")
    else:
         print("Incorrect option selected.")


def downloadPageString(returnURL):
    #download and move file to prgmDir to be stored and read
    subprocess.run(["wget", returnURL, "--user-agent", "e621CLIInterface", "-O", "tmpFile.json"])
    subprocess.call("mv tmpFile.json prgmDir", shell=True)
    with open("prgmDir/tmpFile.json", 'r') as file:
        return file.read()

def getUserSearchArray(preDefTag = ["null"]):
    #auto enter predefined-tag if it exists
    #get tags
    if preDefTag[0] == "null":
        tagArray = []
    else:
        tagArray = preDefTag

    print("Enter search tags and terms for query.")
    print('Enter "c" to continue, "s" to show terms, and "r" to remove.')
    while True:
        tmp = input(" > ")
        if tmp == "c":
            #continue
            break
        elif tmp == "r":
            #removal menu
            removeArray = input("Enter index or tag to be removed: ")
            try:
                tagArray.pop(int(removeArray))
            except:
                try:
                    tagArray.remove(removeArray)
                except:
                    print("Invalid input error, try again")
        elif tmp == "s":
            #print current tag array
            print("Current tags:")
            print("[Index]: [Tag]")
            for i in range(len(tagArray)):
                print(str(i) + ": " + tagArray[i])
        else:
            tagArray.append(tmp)
    return tagArray


def generateSearchURL(tagArray, pageNumber):
    #generate url
    outputURL = "https://e621.net/posts.json?limit=10&page=" + str(pageNumber) + "&tags="
    
    #add tags
    for i in range(len(tagArray)):
        if i == len(tagArray) - 1:
            outputURL = outputURL + tagArray[i]
        else:
            outputURL = outputURL + tagArray[i] + "+"
    #add login
    outputURL = outputURL + '&login=' + username + '&api_key=' + API_key
    return outputURL

def buildPageArray(jsonString):
    fileArr = []
    while True:
        if (jsonString.find('{"id":') == -1):
            break

        indexStart = jsonString.find('{"id":')
        indexEnd = jsonString.find(',"duration":') + 17

        fileArr.append(jsonString[indexStart:indexEnd])

        #cut arrayed index range of string out
        jsonString = jsonString[(indexEnd+1):]

    return fileArr

def displayPost(postString):
    #display post number, post link, and immage or preview
    print("Entry POST ID: " + str(postString[6:postString.find(",")]))
    print("Link to post: https://e621.net/posts/" + str(postString[6:postString.find(",")]))

    urlTargetIndex1 = postString.find('"url":"') + 7
    urlTargetIndex2 = postString.find('"},"preview":')
    extractedUrl = postString[urlTargetIndex1:urlTargetIndex2]
    if (-1 == extractedUrl.find(".webm") and -1 == extractedUrl.find(".gif")):
        print("PostIMG:")
        print(from_url(extractedUrl))
    else:
        tmp = str(postString[postString.find('"preview":{') + 7::])
        urlTargetIndex1 = tmp.find('"url":"') + 7
        urlTargetIndex2 = tmp.find('"},"sample":')
        extractedUrl = tmp[urlTargetIndex1:urlTargetIndex2]
        print(from_url(extractedUrl))
        print("Preview is displayed because, original is animated.")



#==========MAIN MENU==========
#menu has search, favorites, latest, and popular option.
invalidInput = False
searchArray = []

while True:
    subprocess.run("clear")
    print("   ________ ___ ___  _______   ____")
    print("  / __/ __/|_  <  / / ___/ /  /  _/")
    print(" / _// _ \/ __// / / /__/ /___/ /  ")
    print("/___/\___/____/_/  \___/____/___/  ")
    print("Main Menu Options:")
    print("General Search [s]")
    print("Favorites [f]")
    print("Latest [l]")
    print("Popular [p]")
    print("ModifyCurrent [m]")
    print("Exit [exit]")
    if invalidInput:
        print("Input did not match selection, please try again.")
    menuSelectInput = input("Selection: ")
    if menuSelectInput == "s":
        #generalSearch
        searchTypeTag = ["null"]
        invalidInput = False
    elif menuSelectInput == "f":
        #favoritesSearch
        searchTypeTag = ["fav:" + username]
        invalidInput = False
    elif menuSelectInput == "l":
        #LatestSearch
        searchTypeTag = ["null"]
        invalidInput = False
    elif menuSelectInput == "p":
        #popular
        searchTypeTag=["order:rank"]
        invalidInput = False
    elif menuSelectInput == "m":
        #popular
        searchTypeTag=searchArray
        invalidInput = False
    elif menuSelectInput == "exit":
        invalidInput = False
        break
    else:
        invalidInput = True
    
    if not invalidInput:
        #ability to enter post number and jump to post in the page
        #ability to enter n or "" for next or p for previous
        #ability to enter s to save current JSON to a file.

        searchArray = getUserSearchArray(searchTypeTag) # add stuff for spicific searches
        #loop
        downloadNewPage = True
        pageNumber = 1 #query number
        while True:
            if(downloadNewPage):
                searchURL = generateSearchURL(searchArray, pageNumber)
                pageString = downloadPageString(searchURL)
                pageArray = buildPageArray(pageString)

                downloadNewPage = False
                postOnPageNumber = 0 #index
            #page loop
            displayPost(pageArray[postOnPageNumber])
            print("CURRENT:Page " + str(pageNumber) + " Post " + str(postOnPageNumber) + " of " + str(len(pageArray) - 1))  #OPTIONS: Save Current Post [s]   <<<< NOT CURRENTLY IMPLEMENTED
            print("Previous Page [q] Next Page [e] Spicific Page [PG<number>]")
            print("Previous Post [a] Next Post [d] Spicific Post [PN<number>]")

            startingPageNumber = pageNumber #used to tell if there is a difference in page numbers inorder to download a new one

            searchInput = input(" > ")
            if searchInput == "s":#save current post +++++++++++++++++++++++++++++++++++++++++++ AD STUFF THIS FUNCIONAL DOES NOT EXIST
                continue

            elif searchInput == "q":#previous page
                if pageNumber > 1:
                    pageNumber = pageNumber - 1
                else:
                    print("Page number is already at minimum.")

            elif searchInput == "e": #next page
                pageNumber = pageNumber + 1

            elif searchInput == "a":#previous post
                if postOnPageNumber > 0:
                    postOnPageNumber = postOnPageNumber - 1
                else:
                    print("Post number is already at minimum.")
            elif searchInput == "d" or searchInput == "":#next post (or "" is there for quickly going forward though posts)
                if postOnPageNumber < len(pageArray) - 1:
                    postOnPageNumber = postOnPageNumber + 1
                else:
                    print("Post number is already at maximum going to next page.")
                    pageNumber = pageNumber + 1

            elif searchInput.find("PG") == 0:#Spicific page
                try:
                    searchInput = int(searchInput[2::])
                    if searchInput >= 1:
                        pageNumber = searchInput
                    else:
                        print("Input out of range")
                except:
                    print("Datatype Error")

            elif searchInput.find("PN") == 0:#spicific post
                try:
                    searchInput = int(searchInput[2::])
                    if searchInput >= 0 and searchInput <= len(pageArray) - 1:
                        postOnPageNumber = searchInput
                    else:
                        print("Input out of range")
                except:
                    print("Datatype Error")
                
            elif searchInput == "exit":#exit
                break

            else:
                print("Invalid Input: " + searchInput)


            if not startingPageNumber == pageNumber:
                downloadNewPage = True
        
