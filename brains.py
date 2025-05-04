
from pyscript import document
from pyodide.ffi import create_proxy #Proxy tells python not to destroy any event listeners
from pyodide.http import open_url
import pandas as pd #Data manipulation
import math
import json
from js import document
from io import StringIO
import random
from js import localStorage
from difflib import get_close_matches

#Getting the selectors
inputText = document.querySelector(".inputText") #inputText is the text that is displayed on the screen that the user asks the AI
responseText = document.querySelector(".responseText")#responseText is the text that the AI gives
textQuery = document.querySelector("#textQuery") #textQuery is the input tag that the user inputs into the AI
paperPlaneIcon = document.querySelector("#paperPlaneIcon") #This is responsible for submitting the textQuery into the AI
queryAndResponse = document.querySelector(".queryAndResponse")

#URL to the hosted CSV file
url = "https://raw.githubusercontent.com/JonasTheW/Tourism-AI-Chatbot/main/Tourism%20Dataset%20Updated%202.csv"


#Import the dataset into df
response = open_url(url).getvalue()

df = pd.read_csv(StringIO(response), encoding='utf-8-sig')
df["alt_country_name"] = df["alt_country_name"].fillna("-")



def normalized_data(val, min_value, max_value):
    return (val-min_value)/(max_value-min_value)

#Convert each data frame columns to an array
country_name_arr = df["country_name"].tolist()
alt_country_name_arr = df["alt_country_name"].tolist()
capital_arr = df["capital"].tolist()
alt_location_arr = df["alt_location"].tolist()
place_to_visit_arr = df["place_to_visit"].tolist()
place_to_eat_arr = df["place_to_eat"].tolist()
place_to_stay_arr = df["place_to_stay"].tolist()
country_pop_arr = df["country_pop(m)"].tolist()
category_arr = df["category(s)"].tolist()
crime_rate_arr = df["crime_rate"].tolist()
safety_index_arr = df["safety_index"].tolist()
ttdi_arr = df["tourist_development_index"].tolist()

    
normalized_crime_arr = []
normalized_safety_index_arr = []
normalized_population_arr = []
normalized_ttdi_arr = []
touriticity_score_arr = []
log_pop = []

min_crime = min(crime_rate_arr)
max_crime = max(crime_rate_arr)

min_safety_index = min(safety_index_arr)
max_safety_index = max(safety_index_arr)

min_ttdi = min(ttdi_arr)
max_ttdi = max(ttdi_arr)

min_population = min(country_pop_arr)
max_population = max(country_pop_arr)

    

#Normalizing data
for x in range(len(country_name_arr)):
        #Using a for loop to convert each data into normalized data
        
        
        #After converting a data, store it in normalized_data...
        normalized_crime = 1 - normalized_data(crime_rate_arr[x], min_crime,max_crime)
        normalized_safety_index = normalized_data(safety_index_arr[x],min_safety_index,max_safety_index)

        log_pop = math.log(float(country_pop_arr[x]) + 1)
        normalized_pop = normalized_data(log_pop, min_population, max_population)  # ✅ log_pop, not log_pop[x]

        
        normalized_ttdi = normalized_data(ttdi_arr[x],min_ttdi,max_ttdi)

        normalized_crime_arr.append(normalized_crime)
        normalized_safety_index_arr.append(normalized_safety_index)
        normalized_population_arr.append(normalized_pop)
        normalized_ttdi_arr.append(normalized_ttdi)
      

        #Displays the touriticity score for each country, based on this formula
        score = (
            0.3 * normalized_crime + 0.3 * normalized_safety_index + 0.2 * normalized_ttdi + 0.2 * normalized_pop
        )

        touriticity_score_arr.append(score) 
        #The touriticity score: touriticity_score_arr

        


#Converting the score to stars
min_touriticity_score = min(touriticity_score_arr)
max_touriticity_score = max(touriticity_score_arr)

touriticity_star_arr = []
for score in touriticity_score_arr:
    normalized = (score-min_touriticity_score)/(max_touriticity_score-min_touriticity_score)
    stars = 1 + 4 * normalized
    stars = round(stars,1)
    touriticity_star_arr.append(stars)
    


touriticity_star_data = [{"index": i, "rating": touriticity_star_arr[i]} for i in range(len(touriticity_star_arr))]

stars_json = json.dumps(touriticity_star_data)
star_element = document.getElementById("starRating")
star_element.setAttribute("data-stars",stars_json)
 

#Natural Language Generation
url_sentence_bank = "https://raw.githubusercontent.com/JonasTheW/Tourism-AI-Chatbot/main/Sentence%20Bank%20Updated%203.csv"
df_sen_bank = pd.read_csv(open_url(url_sentence_bank), encoding='utf-8')
df_sen_bank = df_sen_bank.applymap(lambda x: str(x) if pd.notnull(x) else "")



opening_line = df_sen_bank["opening_line"].tolist()
introduction_to_alt_country_name = df_sen_bank["Introduction_to_alternative_country_name"].tolist()
introduction_to_capital = df_sen_bank["Introduction_to_capital"].tolist()
introduction_to_alt_location = df_sen_bank["Introduction_to_alt_location"].tolist()
introduction_to_attraction = df_sen_bank["Introduction_to_attraction"].tolist()
introduction_to_restaurant = df_sen_bank["Introduction_to_restaurants"].tolist()
introduction_to_hotels = df_sen_bank["Introduction_to_hotels"].tolist()

#Categories and Adjectives
positive_adjective = df_sen_bank["positive_adjective"].tolist()
natural_beauty = df_sen_bank["natural_beauty"].tolist()
adventure = df_sen_bank["adventure"].tolist()
cultural = df_sen_bank["cultural"].tolist()
religious = df_sen_bank["religious"].tolist()
artistic = df_sen_bank["foodie"].tolist()
historical = df_sen_bank["historical"].tolist()
wildlife = df_sen_bank["wildlife"].tolist()
tropical_paradise = df_sen_bank["tropical_paradise"].tolist()
foodie = df_sen_bank["foodie"].tolist()

#AI Section
def generatedResponse(userQuery):
    #Mix and Match Sentences
    chosen_opening_sentence = random.choice(opening_line)
    chosen_capital = random.choice(introduction_to_capital)
    chosen_alt_location = random.choice(introduction_to_alt_location)
    chosen_attraction = random.choice(introduction_to_attraction)
    chosen_restaurant = random.choice(introduction_to_restaurant)
    chosen_hotel = random.choice(introduction_to_hotels)

    #Assembly the response
    response =  f"{chosen_opening_sentence} {chosen_capital} {chosen_alt_location} {chosen_attraction} {chosen_restaurant} {chosen_hotel}"


    userQuery = userQuery.strip().lower() #Takes the user input and lower cases it eg.Hello Japan to hello japan
    print(userQuery)
    
    country_pairs = list(zip(country_name_arr,alt_country_name_arr))

    #isinstance checks if the variable is a specific type, in this case a string

    for country_name, alt_country_name in country_pairs: #From 0 to 216
        

        if(str(alt_country_name)):
             if (isinstance(country_name, str) and country_name.strip().lower() in userQuery) or \
   (isinstance(alt_country_name, str) and alt_country_name.strip().lower() in userQuery):

                index = country_name_arr.index(country_name) #What row was it found? What index is it?
                
                print(index)
                actual_country_name = country_name_arr[index]
                actual_alt_country_name = alt_country_name_arr[index]
                actual_capital = capital_arr[index]
                actual_alt_location = alt_location_arr[index]
                actual_place_to_visit = place_to_visit_arr[index]
                actual_place_to_eat = place_to_eat_arr[index]
                actual_place_to_stay = place_to_stay_arr[index]
                actual_country_pop = country_pop_arr[index]
                actual_category = category_arr[index]
                actual_crime_rate = crime_rate_arr[index]
                actual_safety_index = safety_index_arr[index]
                actual_ttdi = ttdi_arr[index]

                actual_category_separated = [category.strip() for category in actual_category.split(',')] #Gets each individual category into its own place in an array.
                #What I want now is this, for example, actual_category_separated = [natural beauty, artistic], what I want is to only use terms from these 2 categories. So, to make that, I would need to feed it into a for loop, and then use some if structures to compare it to the structure
                #Good thing is, actual_category_separated already has the form [category 1, category 2, ...] and is the country mentioned. I also need to make another loop with the positive adjectives, could be something like "whenever you encounter{positive_adjective}, put a word in it"
            
                keywords = {
                    "cultural":cultural,
                    "adventure": adventure,
                    "historical":historical,
                    "religious": religious,
                    "artistic":artistic,
                    "wildlife":wildlife,
                    "foodie":foodie,
                    "natural_beauty": natural_beauty,
                    "tropical_paradise": tropical_paradise
                }
                
                
                selected_keywords = {}
                for category in actual_category_separated: #eg 2, natural_beauty & artistic
                    category = category.lower().strip()
            
                    if category in keywords:
                        selected_keywords[category] = random.choice(keywords[category])

                for category, word in selected_keywords.items():
                    response = response.replace("{category}", word, 1)

                for _ in range(response.count("{positive_adjective}")):
                    response = response.replace("{positive_adjective}", random.choice(positive_adjective))

                response = response.replace("{country_name}", str(actual_country_name))
                response = response.replace("{capital_name}", str(actual_capital))
                response = response.replace("{alt_location}", str(actual_alt_location))
                response = response.replace("{attraction_name}", str(actual_place_to_visit))
                response = response.replace("{restaurant_name}", str(actual_place_to_eat))
                response = response.replace("{places_to_stay}", str(actual_place_to_stay))

                

                
                return  response, index, actual_country_name, actual_category_separated
    
    return "Sorry, I couldn't find information on that location.", None, None, None
            



def addQueryFunction(event):
    event.preventDefault()
    #Get the text Query, when this is clicked, I want it to store the textContent of textQuery into userQuery
  
    userQuery = textQuery.value  # Get the value of the input field
    
    lightOrDarkTheme = localStorage.getItem('theme')

    #User Code
    inputContainer = document.createElement("div")
    inputContainer.className = "inputContainer"

    inputText = document.createElement("p")
    inputText.className = "inputText"
    inputText.textContent = userQuery  # Display the user's query in inputText

    if lightOrDarkTheme == 'dark':
        inputContainer.className = "inputContainer darkModeInputContainer"
        inputText.className = "inputText darkModeText"

    


    inputContainer.appendChild(inputText)
    queryAndResponse.appendChild(inputContainer)

    #AI Response
    ai_response, index, actual_country_name, actual_category_separated = generatedResponse(userQuery)

    responseContainer = document.createElement("div")
    responseContainer.className = "responseContainer"



    responseText = document.createElement("p")

    responseText.textContent = ai_response
    responseContainer.appendChild(responseText)

    if lightOrDarkTheme == 'dark':
        responseContainer.className = "responseContainer darkModeResponseContainer"
        responseText.className = "responseText darkModeText"


    if index is not None:
        touriticityRating = document.createElement("p")
        touriticityRating.textContent = "Our final rating for " + actual_country_name + " is: "
        touriticity_star = touriticity_star_arr[index]
        touriticity_star = round(touriticity_star, 1)

        # Create star container div
        starDiv = document.createElement("div")
        starDiv.className = "starRating"
        starDiv.setAttribute("data-stars", f"[{touriticity_star}]")  # Send as JSON string

        #Create country vibes div
        countryVibes = document.createElement("div")
        countryVibes.className = "countryVibes"

        cultural = "fa-people-group"
        adventure = "fa-backpack"
        natural_beauty = "fa-tree"
        foodie = "fa-pot-food"
        tropical_paradise = "fa-wave"
        wildlife = "fa-hippo"
        religious = "fa-church"
        artistic = "fa-palette"
        historical = "fa-castle"


        category_to_icon = {
                    "cultural":cultural,
                    "adventure": adventure,
                    "historical":historical,
                    "religious": religious,
                    "artistic":artistic,
                    "wildlife":wildlife,
                    "foodie":foodie,
                    "natural_beauty": natural_beauty,
                    "tropical_paradise": tropical_paradise
                }
        normalized_categories = [cat.strip().lower().replace(" ", "_") for cat in actual_category_separated]


        for category in normalized_categories:
            if category in category_to_icon:
                icon_element = document.createElement("i")
                icon_element.className = f"fa-solid {category_to_icon[category]}"
                countryVibes.appendChild(icon_element)

        cntyVibesWords = document.createElement("p")
        cntyVibesWords.textContent = "Country Vibes: "

        if lightOrDarkTheme == 'dark':
            touriticityRating.className = "touriticityRating darkModeText"
            cntyVibesWords.className = "cntyVibesWords darkModeText"


        responseContainer.appendChild(responseText)
        responseContainer.appendChild(touriticityRating)
        responseContainer.appendChild(starDiv)
        responseContainer.appendChild(cntyVibesWords)
        responseContainer.appendChild(countryVibes)



    queryAndResponse.appendChild(responseContainer)   
    queryAndResponse.appendChild(document.getElementById("scrollToBottom"))


    

    textQuery.value = ""



def detectEnterKey(event):
    if event.key == "Enter":
        addQueryFunction(event) 


addQueryProxy = create_proxy(addQueryFunction)
paperPlaneIcon.addEventListener("click", addQueryProxy)

handleKeyPressProxy = create_proxy(detectEnterKey)
textQuery.addEventListener("keydown", handleKeyPressProxy)


