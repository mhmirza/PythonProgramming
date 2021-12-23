#90819 - Fall 2020 - Final Project

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import string
import re
import sys
import matplotlib.pyplot as plt

"""PART 0 - DEFINING FUNCTIONS AND SETTING CODES"""



def userInstr(): #simple function to give warning if users input an exception
    print("Please enter 'Y' to answer Yes, 'N' to answer No, or other information as instructed.")



# This function takes in 2 parameters: link and headers. link is just
# the weblink that you pass it which it uses to scrape information
# about related conditions and their descriptions. It also saves
# a csv file "top_results.csv" that contains this information.
# It also returns a dictionary of conditions (key) and a link (value)
# in case the user wants to get detailed information about a
# particular disease. **
def getTopDiagnoses(link, headers): 
    moreInfo = {}
    result_df = pd.DataFrame(columns=["Condition", "Description"])
    top_results = list()
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    related_conditions = soup.find(class_ = "related_conditions")
    results_list = related_conditions.find(class_ = "results_list")
    condition_links = results_list.find_all("li")
    count = 0
    for l in condition_links:
        tempDict = {}
        condition = l.find("a")
        desc = l.find("p").get_text()
        dataList = []
        dataList.append(condition.get_text())
        dataList.append(desc)
        result_df.loc[count] = dataList
        count += 1
        moreInfo[l.find("a").get_text()] = condition["href"]
    result_df = result_df.loc[:4] #return top 5 matches only
    result_df.to_csv("diagnosis_list.csv", index = False)
    return moreInfo, result_df


#function to loop through webmd database and return matching symptoms' 
#permutations based on initial symptom input by the user
def loadFurtherSymptomsAndCounts(symptoms_links, headers):
    furtherSymptoms = {}
    symptom_counts = {}
    for (key, value) in symptoms_links.items():
        page = requests.get(value, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        related_symptoms = soup.find(class_ = "related_symptoms")
        related_symptoms_table = related_symptoms.find("table")
        table_rows = related_symptoms_table.find_all("tr")
        for row in table_rows:
            cols = row.find_all("td")
            for col in cols:
                info = col.find("a")
                if(info != None):
                    tempDict = {}
                    tempLink = "https://symptomchecker.webmd.com/" + info["href"]
                    furtherSymptoms[tempLink] = info.get_text().split(",")
                    
                    for s in furtherSymptoms[tempLink]:
                        if(s in symptom_counts):
                            symptom_counts[s] += 1
                        else:
                            symptom_counts[s] = 1
    return (furtherSymptoms, symptom_counts)

#takes diagnosis selected by the user, searches for the disease information
#on Google and returns the result from multiple sources, whichever matches and 
#provides best displayabale result. 
def fetchGoogleResults(toSearch, headers):
    allSymptoms = "+".join(toSearch)
    linkDict = {}
    healthLineLinks = list()
    livehealthily = list()
    wikiResults = list()
    
    googleLink = "https://www.google.com/search?q=" + allSymptoms
    page = requests.get(googleLink, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.findAll("a")
    for link in links:
        hrefLink = str(link["href"])
        if("/url?q=" in hrefLink and "&sa=" in hrefLink):
            hrefLink = hrefLink[hrefLink.index("/url?q=") + len("/url?q="):hrefLink.index("&sa=")] # to get the appropriate link string,  need to double check
            if(re.search(r'healthline', hrefLink) != None):
                healthLineLinks.append(hrefLink)
            if(re.search(r'livehealthily', hrefLink) != None):
                livehealthily.append(hrefLink)
            if(re.search(r'wikipedia', hrefLink) != None):
                wikiResults.append(hrefLink)
        linkDict["healthline"] = healthLineLinks
        linkDict["livehealthily"] = livehealthily
        linkDict["wikipedia"] = wikiResults
        
    return linkDict


# This function takes in a parameter symptom_counts which
# is a dictionary containing symptoms as keys and their
# relevant counts as values. It then goes on to plot a bar graph for users
# to show the most common symptoms associated with their input as a guide
def showBarChart(symptom_counts):
    fig = plt.figure(figsize=(10.0, 10.0))
    plt.xticks(rotation = 60)
    plt.title("RELATED SYMPTOMS FREQUENCY")
    plt.ylabel("Ocurrence")
    plt.bar(list(symptom_counts.keys())[:10], list(symptom_counts.values())[:10])
    plt.show()
    


#primary function to match and display information related to symptoms from
#WebMD symptoms database. Further comments are inline

def loadAllSymptoms_webmd(headers):
    symptoms_links = {}
    furtherSymptoms = {}
    symptom_counts = {}
    page = requests.get("https://symptomchecker.webmd.com/symptoms-a-z", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    found = False
    while(not found):
        symp = input("Please enter most prominent symptom you're experiencing right now: ").capitalize().strip()
        firstLetter = symp[0]
        alphabet = [firstLetter] #first letter retrieved to scrape Alphabetic Index of symptoms
        symptoms_links = {} # comment to store each letter's symptoms together
        for letter in alphabet:
            list_az = soup.find(id="list_az")
            if(list_az != None):
                listA = list_az.find(id="list_" + letter)
                if(listA != None):
                    bullets = listA.find_all("li")
                    for bullet in bullets:
                        links = bullet.find_all("a")
                        for link in links:
                            webLink = "https://symptomchecker.webmd.com/" + link["href"]
                            symptoms_links[link.get_text()] = webLink.replace("amp;", "")
                    
                    copy = list(symptoms_links.keys()).copy()
                    
                    for sm in [i.lower().capitalize() for i in copy]:
                        if(symp == sm):
                            found = True
                    if(not found):
                        if(len(list(symptoms_links.keys())) > 0):
                            print("\nEntered symptom cannot be found. Please ensure there are no typos!")
                            print("Choose from the symptoms below (case sensitive): ")
                            for s in symptoms_links.keys():
                                print(s)
                        else:
                            print("Your search did not return any results!") #exceptions if user inputs invalid symptoms 
                else:
                    print("No results could be loaded for the mentioned symptom.\nSymptom should not contain numbers. ")
            else:
                print("No results could be loaded for the mentioned symptom. \nSymptom should not contain numbers. ")
    updatedSymptomLinks = {}
    updatedSymptomLinks[symp] = symptoms_links[symp]
    furtherSymptoms, symptom_counts = loadFurtherSymptomsAndCounts(updatedSymptomLinks, headers=headers)
    showBarChart(symptom_counts) #show user barchart of how their symptoms match with combinations of other symptoms 
    index = 0
    for (key, value) in furtherSymptoms.items():
        print("\n\nDo you experience the following symptoms: ")
        for val in value:
            print(val.lstrip())
        ans = input("Enter 'Y' to confirm, 'N' to get list of more symptoms: ").upper().strip() 
        #testing whther user experiences the combination of symptoms in displayed list
        while ans not in ['Y', 'N']:
            userInstr()
            ans = input("Enter 'Y' to confirm, 'N' to get list of more symptoms: ").upper().strip()
        if ans == "Y":
            print('Fetching results, please wait.')
            moreInfo, res_df = getTopDiagnoses(key, headers)
            res_df.index += 1
            wantsMoreInfo = True       
            print('(CSV file of your top matched diagnosis downloaded for your reference)')
            while(wantsMoreInfo):
                print('\nYour top matched results are: ')
                print(res_df)
                res = input("\nPlease type the relevant number to retrieve information related to disease\
                            \n(or 'Q' to quit and move to the next part): ").upper().strip()
                if res not in ['1', '2', '3', '4', '5', 'Q']:
                    print()
                    print("Entered number or letter not found! ")
                    userInstr()
                    
                elif (res != "Q"):
                    res = int(res) - 1
                    print('\nPlease wait while we fetch your results.')
                    condition_desc = printDescription(res_df.iloc[res]["Condition"], headers)
                    if(condition_desc != ""):
                        print(condition_desc)
                    else:
                        print(res_df.iloc[res]["Description"])
                elif(res == 'Q'):
                    break
                
            break #break the while loop with wantsMoreInfor = True


#function to print limited textual information on diagnosis results matched for user
# in the console for their perusal
def printDescription(condition, headers):
    cond_det = fetchGoogleResults([condition, "treatment"], headers)
    all_cont = ""
    if(len(cond_det["healthline"]) != 0):
        link_h = cond_det["healthline"]
        page = requests.get(link_h[0], headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_Paragraphs = soup.find_all("p")
        count = 0
                        
        if(len(all_Paragraphs) <= 3):
            for p in all_Paragraphs:
                all_cont += p.get_text()
                all_cont += '\n'
        else:
            for p in all_Paragraphs:
                if(count <= 3):
                    all_cont += p.get_text()
                    all_cont += '\n'
                count += 1
    return(all_cont)

#Function uses Google Maps Geocode API to return latitude and longitude for any address
#this is required for retrieving facilities in user's vicinity
def Coordinates(address_or_zipcode):
    latitude, longitude = '',''
    api_key = 'AIzaSyC7kYdgm4ucwVlt7dgn6L6VjcPOeuk6Brw'
    headers = {'Content-Type': 'application/xml'}
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    final_search = f'{base_url}?address={address_or_zipcode}&key={api_key}'
    response = requests.get(final_search, headers = headers)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        results = dict(data['results'][0])
        latitude = results ['geometry']['location']['lat']
        longitude = results ['geometry']['location']['lng']
    return latitude, longitude


#Function uses Google Maps Place Search API to return a list of pharmacies 
# (name,address), along with place_id
def typeSearch():
    address = input ('Enter valid address/neighborhood/zip-code: ').strip() #user input for address/zip
    premises = int(input ('Enter 1 for Pharmacy or 2 for Hospital: ').strip()) #user input for address/zip
    keyword = list() 
    if premises not in [1, 2]:
        userInstr()
        premises = int(input ('Enter 1 for Pharmacy or 2 for Hospital: '))
    elif premises == 1:
        keyword = ['pharmacy']
    elif premises == 2:
        keyword = ['hospital']
    radius = '1600'#fixed to within 1 mile radius
    latitude = str(Coordinates(address)[0])    #nested call for the Coordinates Function
    longitude = str(Coordinates(address)[1])
    api_key = 'AIzaSyC7kYdgm4ucwVlt7dgn6L6VjcPOeuk6Brw' 
    #API key above generated by registering GoogleMaps, limited to $200 per user free usage!
    headers = {'Content-Type': 'application/json'}
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    final_search = f'{base_url}{latitude},{longitude}&radius={radius}&keyword={keyword}&key={api_key}'
    response = requests.get(final_search, headers = headers)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        results = pd.json_normalize (data['results'])
        subset_results = results [['name', 'vicinity']].copy()
        subset_results.rename (columns = {"name": "NAME", "vicinity": "ADDRESS"}, inplace = True)
        place_id = results ['place_id'].copy()
    return subset_results, place_id, keyword


#Function uses Google Maps Place Details API to return a CSV containing the list of pharmacies (with phone numbers included)
# this uses previous 2 functions to provide coordinates and specific information (phone etc)
# for the type of facility selected.
def toCSV():
    subset_results, place_id, keyword = typeSearch() #nested call for the Search Function 
    phone_numbers = []
    print('\nPlease wait while we fetch your results.')
    for i in place_id:
        api_key = 'AIzaSyC7kYdgm4ucwVlt7dgn6L6VjcPOeuk6Brw'
        headers = {'Content-Type': 'application/json'}
        base_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='
        final_search = f'{base_url}{i}&key={api_key}'
        response = requests.get(final_search, headers = headers)
        print('\n...almost there...')
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            result = pd.json_normalize (data ['result'])
        if 'formatted_phone_number' in result:
            phone_numbers.append(str (result ['formatted_phone_number'].iloc[0]))
        else:
            phone_numbers.append(' Not Available')
    print('\n...almost there...')
    subset_results ['CONTACT DETAILS'] = phone_numbers
    if keyword == ['pharmacy']:
        subset_results.to_csv('Pharmacy.csv', index = False)
    elif keyword == ['hospital']:
        subset_results.to_csv('Hospitals.csv', index = False)


#Function uses webscraping to retrieve a list of doctors based on speciality and state input by the user
# for online/tele-medicine appointment
def Doctors():
    page = requests.get('https://www.healthgrades.com/specialty-directory')
    soup = BeautifulSoup(page.content, 'html.parser')
    details = soup.find(id = "root")
    specialities = details.find_all(class_= "listArray__name")
    spec = []
    for i in range (len (specialities)):
        spec.append(specialities [i].get_text().upper())
    speciality = input ('Enter the speciality you want to search e.g. neurology: ').upper().strip()   #USER INPUT 1                                                                              #USER INPUT 1
    while speciality not in spec:
        first = speciality[0].upper()
        options = {}
        for i in range (len (spec)):
            if re.search('^' + first, spec [i]) != None:
                options [i] = spec [i]
        # print (options)
        for oKey, oVal in options.items():
            print("Code: %s, Description: %s" % (oKey, oVal))
        code = input ('Specialty Misspelled! Enter the speciality code from above instead: ')
        speciality = options [int (code)]
    state_abbrv = input ('Enter your State (e.g. PA): ').upper()
    states = {'AL': 'Alabama','AK': 'Alaska',
 'AS': 'American-Samoa','AZ': 'Arizona', 'AR': 'Arkansas','CA': 'California',
 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District-of-Columbia',
 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
 'ME': 'Maine', 'MD': 'Maryland','MA': 'Massachusetts','MI': 'Michigan', 'MN': 'Minnesota',
 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
 'NH': 'New-Hampshire', 'NJ': 'New-Jersey', 'NM': 'New-Mexico', 'NY': 'New-York', 'NC': 'North-Carolina',
 'ND': 'North-Dakota', 'MP': 'Northern-Mariana-Islands', 'OH': 'Ohio', 'OK': 'Oklahoma',
 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto-Rico', 'RI': 'Rhode-Island', 'SC': 'South-Carolina',
 'SD': 'South-Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
 'VI': 'Virgin-Islands', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West-Virginia', 'WI': 'Wisconsin',
 'WY': 'Wyoming'}
    while state_abbrv not in states.keys():
        userInstr()
        state_abbrv = input ('Enter your State (e.g. PA): ').upper()
        
    if state_abbrv in states.keys():
        state = states[state_abbrv]
    print('\nPlease wait while we fetch your results.')
    httpString = f'https://www.healthgrades.com/{speciality}-directory/{state_abbrv}-{state}'
    page = requests.get(httpString)
    soup = BeautifulSoup(page.content, 'html.parser')
    details = soup.find(id = "root")
    summary_updated = pd.DataFrame(columns=["Phone", "Names", "Speciality", "Address"])
    print('...almost there...\n')
    if(details != None):
        doctors = details.find_all(class_= "sd-provider-card")
        name = []
        speciality = []
        address = []
        phone = []
        for i in range (len (doctors)):
            a = doctors[i]
            speciality.append (a.find(class_="provider-details__subtitle").get_text())
            address.append (a.find(class_="directory-card-body__directory-card-location").get_text().split(',')[0])
            name.append (a.find(class_= "card-summary__provider-details").get_text().split(',')[0])
            phone.append (a.find(class_= "provider-view-profile-card__phone-lnk").get_text())
        summary = pd.DataFrame ()
        summary['Phone'] = phone
        summary['Names'] = name
        summary['Speciality'] = speciality
        summary['Address'] = address
        row_constraint = summary ["Phone"] != ''
        summary_updated = summary.loc [row_constraint, ]
        print('List of available doctors for online consultation downloaded!')
        summary_updated.to_csv('Doctors.csv', index = False)
    else:
        print("No such doctors found on the website!")


#Function to control Part 1 (Input) of the application, giving users instructions and
# asking if they want  to proceed further. After user completes one cycle through
# the application, they return here in case they want to start all over again.
def part1():
    """PART 1 - WELCOME MENU AND INSTRUCTIONS"""
    
    print("\nWelcome! This checker provides you with a quick assessment of your symptoms, "
                    "so you don't have to go a hospital or clinic in times of social distancing!"
                    "\nIt's easy! Simply:"
                    "\nStep 1. Answer a preliminary question."
                    "\nStep 2. Enter your major symptom."
                    "\nStep 3. Select possible related symptoms from a list"
                    "\nStep 4. View top matched results with your symptoms." 
                    "\nStep 5. Download:"
                    "\n\t\t - List of possible diseases matching your symptoms for future reference;"
                    "\n\t\t - List of pharmacies/hospitals near your zipcode;"
                    "\n\t\t - List of Doctors for tele-medicine appointment.")
    userInstr()
    
    
    start = input("\nDo you wish to continue? (Y/N): ").upper().strip()
    if start not in ['Y', 'N']:
            userInstr()
            start = input("\nDo you wish to continue? (Y/N): ").upper().strip()
    return start

#Function to control Part 2 (Processing) of the user's information, by calling
# the  webscrapping and symptom checking functions

def part2(start):
    """PART 2 - SCRAPING AND DISPLAY RESULTS"""
    
    print("\nGreat! let's get started.")
    loop = 0
    while loop == 0:
        check = input("Are you currently bleeding, experiencing blackouts, or difficulty moving? (Y/N): ").upper().strip()
        if check not in ['Y', 'N']:
            userInstr()
            loop = 0
        elif check == 'Y':
            print("Please call 911 or visit your nearest hospital immediately!")
            loop = 1
        elif check == 'N': 
            headers = {}
            loadAllSymptoms_webmd(headers) 
            loop = 1


# Function to process Part 3 (Output) for the application, allowing users to select 
#type of infromation they want to download as CSV
def part3():
    """PART 3 - DOWNLOAD CSV"""
    end = 0
    toExit = 0
    proceed = input ('\nWould you like information about Pharmacies/Hopitals in your vicinity or Doctors online? (Y/N): ').upper().strip()
    while end == 0:
        if proceed not in ['Y','N']:
            userInstr()
            proceed = input ('Would you like to get information about Pharmacies or Doctors? (Y/N): ').upper().strip()
        elif proceed == 'N': 
            print('\nThank you for your time! Have a nice day!\n')
            end = 1
            toExit = 1
        else:
            print("What would you like? \n\t1. Get List of Pharmacies or Hospital Near Me."
              "\n\t2. Get list of Doctors for virtual consultation."
              "\n\t3. Quit")    
            selection = input ('Select one number from above: ').upper().strip()
            if selection not in ['1','2', '3']:
                userInstr()
            elif selection == '1':
                toCSV()
                print('CSV of Facilities near you successfully downloaded!')
                end = 1
            elif selection == '2':
                Doctors()
                end = 1
            elif selection == '3':
                print('\nThank you for your time! Have a nice day!\n')
                end = 1
                toExit = 1
    return(toExit)


#Main function, which starts the application when code is executed

def main():
    
    end = 1
    while(end != 0):
        start = part1()
        if(start == 'Y'):
            part2(start)
            toExit = part3()
            if(toExit == 1):
                end = 0
        else:
            end = 0
            print("\nThank you for your time! Have a nice day!\n")
        
                
if __name__ == "__main__":
    main()
