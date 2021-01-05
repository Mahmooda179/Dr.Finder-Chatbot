# CS 421: Natural Language Processing
# University of Illinois at Chicago
# Fall 2020
# Chatbot Project - Evaluation
#
# Do not rename/delete any functions or global variables provided in this template and write your solution
# in the specified sections. Use the main function to test your code when running it from a terminal.
# Avoid writing that code in the global scope; however, you should write additional functions/classes
# as needed in the global scope. These templates may also contain important information and/or examples
# in comments so please read them carefully.
# =========================================================================================================

# Import any necessary libraries here, but check with the course staff before requiring any external
# libraries.
import re
from collections import defaultdict
import random
import requests
import json

dst = defaultdict(list)

with open('doctors.json') as json_file:
    data = json.load(json_file)

doctor_info = data['Doctor']
global n_doctor_list

list_doctors = ["primary care physician", "pediatrician",  "dermatologist", "cardiologist", "opthamologist", "psychiatrist", "oncologist", "radiologist"]
list_days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
list_insurances = ["ambetter insured by celtic", "blue cross and blue shield of illinois", "cigna healthcare of illinois, inc.", "celtic insurance company", "health alliance medical plans, inc.", "quartz health benefit plans corporation", "my health alliance"]

# nlu(input): Interprets a natural language input and identifies relevant slots and their values
# Input: A string of text.
# Returns: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is most
#          appropriate for the corresponding slot.  If no slot values are extracted, the function should
#          return an empty list.
def nlu(input=""):
    # [YOUR CODE HERE]

    # Dummy code for sample output (delete or comment out when writing your code!):
    slots_and_values = []

    current_state = dialogue_policy(dst)[0]
    
    # To narrow the set of expected slots, you may (optionally) first want to determine the user's intent,
    # based on what the chatbot said most recently.
    if (current_state == "greeting"):
        slots_and_values.append(("greeting", input))

    elif (current_state == "doctor"):
        pattern = re.compile(r"\b([Pp]rimary [Cc]are [Pp]hysician)|([Pp][Cc][Pp]) \b")
        contains_pcp = re.search(pattern, input)

        pattern = re.compile(r"\b([Pp]ediatrician)|([Pp]ediatric)\b")
        contains_pediatrician = re.search(pattern, input)

        pattern = re.compile(r"\b([Aa]llergist)\b")
        contains_allergist = re.search(pattern, input)

        pattern = re.compile(r"\b([Dd]ermatologist)\b")
        contains_derm = re.search(pattern, input)

        pattern = re.compile(r"\b([Cc]ardiologist)\b")
        contains_card = re.search(pattern, input)

        pattern = re.compile(r"\b([Ii]nfectious [Dd]isease [Dd]octor)|([Ii][Dd] Doctor)\b")
        contains_id = re.search(pattern, input)

        pattern = re.compile(r"\b([Oo]pthamologist)\b")
        contains_optham = re.search(pattern, input)

        pattern = re.compile(r"\b([Oo]b(-)?[Gg]yn)|([Oo]bstetrician)|([Gg]ynegcologist)\b")
        contains_obgyn = re.search(pattern, input)

        pattern = re.compile(r"\b([Ee]ndocrinologist)\b")
        contains_endo = re.search(pattern, input)

        pattern = re.compile(r"\b([Pp]sychiatrist)\b")
        contains_psych = re.search(pattern, input)

        pattern = re.compile(r"\b([Oo]ncologist)\b")
        contains_onco = re.search(pattern, input)

        pattern = re.compile(r"\b([Rr]adiologist)\b")
        contains_radi = re.search(pattern, input)

        if contains_allergist:
            slots_and_values.append(("doctor", "allergist"))
        if contains_card:
            slots_and_values.append(("doctor", "cardiologist"))
        if contains_derm:
            slots_and_values.append(("doctor", "dermatologist"))
        if contains_endo:
            slots_and_values.append(("doctor", "endocrinologist"))
        if contains_id:
            slots_and_values.append(("doctor", "infectious disease doctor"))
        if contains_obgyn:
            slots_and_values.append(("doctor", "obgyn"))
        if contains_onco:
            slots_and_values.append(("doctor", "oncologist"))
        if contains_optham:
            slots_and_values.append(("doctor", "opthamologist"))
        if contains_pcp:
            slots_and_values.append(("doctor", "primary care physician"))
        if contains_pediatrician:
            slots_and_values.append(("doctor", "pediatrician"))
        if contains_psych:
            slots_and_values.append(("doctor", "psychiatrist"))
        if contains_radi:
            slots_and_values.append(("doctor", "radiologist"))

    elif (current_state == "zip_code"):
        pattern = re.compile(r"\b([0-9]{5})\b")
        contains_zip = re.search(pattern, input)

        if contains_zip:
            slots_and_values.append(("zip_code", contains_zip.group(0)))

    elif (current_state == "use_insurance"):
        pattern = re.compile(r"\b([Nn]o)\b")
        contains_dont_use = re.search(pattern, input)

        pattern = re.compile(r"\b[Yy]es\b")
        contains_use = re.search(pattern, input)

        if contains_dont_use:
            slots_and_values.append(("use_insurance", "no"))
        if contains_use:
            slots_and_values.append(("use_insurance", "yes"))
  
    elif (current_state == "insurance"):
        pattern = re.compile(r"\b([Aa]mbetter [Ii]nsured ([Bb]y [Cc]eltic)?)\b")
        contains_aic = re.search(pattern, input)

        pattern = re.compile(r"\b([Bb]lue [Cc]ross (and [Bb]lue [Ss]hield)?(of [Ii]llinois)?)|([Bb][Cc][Bb][Ss])\b")
        contains_bcbs = re.search(pattern, input)

        pattern = re.compile(r"\b([Cc]igna [Hh]ealthcare)|([Cc]igna [Hh]ealthcareof [Ii]llinois)\b")
        contains_chi = re.search(pattern, input)

        pattern = re.compile(r"\b([Cc]eltic ([Ii]nsurance)?([Cc]ompany)?)\b")
        contains_cic = re.search(pattern, input)

        pattern = re.compile(r"\b([Hh]ealth [Aa]lliance([Mm]edical [Pp]lans)?)\b")
        contains_hamp = re.search(pattern, input)

        pattern = re.compile(r"\b([Qq]uartz [Hh]ealth ([Bb]enefit)?([Pp]lans)?(([Cc]orporation)|([Cc]orp))?)\b")
        contains_quartzHealth = re.search(pattern, input)

        pattern = re.compile(r"\b([Mm]y [Hh]ealth [Aa]lliance)\b")
        contains_mha = re.search(pattern, input)

        if contains_aic:
            slots_and_values.append(("insurance", "ambetter insured by celtic"))
        if contains_bcbs:
            slots_and_values.append(("insurance", "blue cross blue shield"))
        if contains_chi:
            slots_and_values.append(("insurance", "cigna healthcare of illinois"))
        if contains_cic:
            slots_and_values.append(("insurance", "celtic insurance company"))
        if contains_hamp:
            slots_and_values.append(("insurance", "health alliance medical plans"))
        if contains_quartzHealth:
            slots_and_values.append(("insurance", "quartz health benefit corporation"))
        if contains_mha:
            slots_and_values.append(("insurance", "my health alliance"))

    elif (current_state == "day"):
        pattern = re.compile(r"\b([Mm]on(day)?)\b")
        contains_mon = re.search(pattern, input)

        pattern = re.compile(r"\b([Tt]ues(day)?)\b")
        contains_tue = re.search(pattern, input)

        pattern = re.compile(r"\b([Ww]ed(nesday)?)\b")
        contains_wed = re.search(pattern, input)

        pattern = re.compile(r"\b([Tt]hurs(day)?)\b")
        contains_thu = re.search(pattern, input)

        pattern = re.compile(r"\b([Ff]ri(day)?)\b")
        contains_fri = re.search(pattern, input)

        pattern = re.compile(r"\b([Ss]at(day)?)\b")
        contains_sat = re.search(pattern, input)

        pattern = re.compile(r"\b([Ss]un(day)?)\b")
        contains_sun = re.search(pattern, input)

        pattern = re.compile(r"\b([Ww]eekday)\b")
        contains_week = re.search(pattern, input)

        pattern = re.compile(r"\b([Ww]eekend)\b")
        contains_wend = re.search(pattern, input)

        if contains_mon:
            slots_and_values.append(("day", ["monday"]))
        if contains_tue:
            slots_and_values.append(("day", ["tuesday"]))
        if contains_wed:
            slots_and_values.append(("day", ["wednesday"]))
        if contains_thu:
            slots_and_values.append(("day", ["thursday"]))
        if contains_fri:
            slots_and_values.append(("day", ["friday"]))
        if contains_sat:
            slots_and_values.append(("day", ["saturday"]))
        if contains_sun:
            slots_and_values.append(("day", ["sunday"]))
        if contains_week:
            slots_and_values.append(("day", ["monday", "tuesday", "wednesday", "thursday", "friday"]))
        if contains_wend:
            slots_and_values.append(("day", ["saturday", "sunday"]))

    elif (current_state == "doctors_list"):
        pattern = re.compile(r"\b()\b")
        contains_noInput = re.search(pattern, input)

        pattern = re.compile(r"\b(([oO][kK](ay)?) | ([Tt]hank(s)?(you)?))\b")
        contains_input = re.search(pattern, input)

        if contains_noInput:
            slots_and_values.append(("doctors_list", contains_noInput.group(0)))
        if contains_input:
            slots_and_values.append(("doctors_list", contains_input.group(0)))
        
    elif (current_state == "anything_else"):
        pattern = re.compile(r"\b([Nn]o)\b")
        contains_no = re.search(pattern, input)

        pattern = re.compile(r"\b[Yy]es\b")
        contains_yes = re.search(pattern, input)

        if contains_no:
            slots_and_values.append(("anything_else", "no"))
        if contains_yes:
            slots_and_values.append(("anything_else", "yes"))
        
    return slots_and_values


# update_dst(input): Updates the dialogue state tracker
# Input: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is
#        most appropriate for the corresponding slot.  Defaults to an empty list.
# Returns: Nothing
def update_dst(input=[]):
	# [YOUR CODE HERE]
    # global dst
    # Dummy code for sample output:

    for item in input:
        key = item[0]
        value = item[1]

        # key does not exist in dictionary
        if(dst.get(key) == None):
            dst.setdefault(key, value)
        # key exists in dictionary
        else:
            dst[key] = value

    return

# get_dst(slot): Retrieves the stored value for the specified slot, or the full dialogue state at the
#                current time if no argument is provided.
# Input: A string value corresponding to a slot name.
# Returns: A dictionary representation of the full dialogue state (if no slot name is provided), or the
#          value corresponding to the specified slot.
def get_dst(slot=""):
    # [YOUR CODE HERE]
    global dst
    # Dummy code for sample output (delete or comment out when writing your code!):
    if (slot == ""):
        return dst

    elif (dst.get(slot) == None):
        print("State does not exist\n")
        return dst

    else:
        key = slot
        value = dst[key]
        state = {}
        state.setdefault(key, value)
    return dst


# dialogue_policy(dst): Selects the next dialogue state to be uttered by the chatbot.
# Input: A dictionary representation of a full dialogue state.
# Returns: A string value corresponding to a dialogue state, and a list of (slot, value) pairs necessary
#          for generating an utterance for that dialogue state (or an empty list if no (slot, value) pairs
#          are needed).
def dialogue_policy(dst=[]):
	# [YOUR CODE HERE]
 
    # Dummy code for sample output (delete or comment out when writing your code!):

    slot_values = []
    next_state = ""
    global n_doctor_list

    if (len(dst)>0):
        current_state = list(dst.keys())[-1]

    else:
        current_state = ""
    
    if (len(dst) == 0):
        next_state = "greeting"

    elif (current_state == "greeting"):
        next_state = "doctor"

    elif(current_state=="doctor"):
        doctor_type = dst[current_state]
        doctor_type = doctor_type.lower()

        if doctor_type in list_doctors:
            n_doctor_list = doctor_info[doctor_type]
            next_state = "zip_code"

        else:
            print(f"I'm sorry, we can't seem to find any {doctor_type}s in our database")
            next_state = "anything_else"

    elif(current_state=="zip_code"):
        if (len(dst[current_state])==5):

            length = len(n_doctor_list)
            n_d = []

            for i in range(length):
                item = n_doctor_list[i]
                if (item['Zip Code'] == dst[current_state]):
                    n_d.append(item)

            n_doctor_list = n_d

            if(len(n_doctor_list) == 0):
                doc = dst["doctor"]
                print(f"Sorry, we do not have any {doc}s in this area.")
                next_state = "anything_else"
            else:
                next_state = "use_insurance"

        else:
            print("Your input was invalid")
            next_state = "zip_code"

    elif(current_state=="use_insurance"):
        if (dst[current_state] == "no"):
            next_state = "day"

        elif (dst[current_state] == "yes"):
            next_state = "insurance"

    elif(current_state=="insurance"):
        name = dst[current_state]
        name = name.lower()

        n_state = ""
        count = 0
        
        for doctor in n_doctor_list:
            n_insurance = doctor["Insurance"]
    
            for insurance in n_insurance:
                words = name.split()
                words2 = insurance.split()

                for word in words:
                    if word in words2:
                        n_state = "day"

                    else:
                        n_state = "anything_else"

                if n_state == 'day':
                    count += 1
                    break

            if (n_state == "anything_else"):
                n_doctor_list.remove(doctor)

        if (count > 0):
            next_state = "day"

        elif (len(n_doctor_list) == 0):
            doc = dst["doctor"]
            print(f"I'm sorry, there are not any {doc}s in this area that carry your insurance")
            next_state = "anything_else"
            
    elif(current_state=="day"):
        days = dst[current_state]

        n_state = ""
        count = 0

        for doctor in n_doctor_list:
            d_days = doctor["Days"]
            for day in days:
                day = day.lower()
                if day in d_days:
                    n_state = "doctors_list"
                    count+=1
                    break
                    
            if (n_state != "doctors_list"):
                n_doctor_list.remove(doctor)

        if (count > 0):
            next_state = "doctors_list"

        elif (len(n_doctor_list) == 0):
            doc = dst["doctor"]
            print(f"I'm sorry, there are not any {doc}s in this area that are open on your available days")
            next_state = "anything_else"
    
    elif(current_state=="doctors_list"):
        next_state = "anything_else"
    
    elif(current_state=="anything_else"):
        if (dst[current_state] == "no"):
            next_state = "good_bye"

        elif (dst[current_state] == "yes"):
            dst.clear()
            next_state = "greeting"

    return next_state, slot_values
	
# nlg(state, slots=[]): Generates a surface realization for the specified dialogue act.
# Input: A string indicating a valid state, and optionally a list of (slot, value) tuples.
# Returns: A string representing a sentence generated for the specified state, optionally
#          including the specified slot values if they are needed by the template.
def nlg(state, slots=[]):
    # [YOUR CODE HERE]
    
    # Dummy code for sample output (delete or comment out when writing your code!):
    templates = defaultdict(list)

    if (state == ""):
        state = "greeting"

    # Build at least two templates for each dialogue state that your chatbot might use.
    templates["greeting"] = []
    templates["greeting"].append("Hi! I'm Dr. Finder!")
    templates["greeting"].append("Hello! This is Dr. Finder")

    templates["doctor"] = []
    templates["doctor"].append("Can you please let me know what kind of doctor you are looking for?")
    templates["doctor"].append("I can help you find medical care in your area. What kind of doctor are you looking for?")
    
    templates["zip_code"] = []
    templates["zip_code"].append("What is the zip code of the area you live in?")
    templates["zip_code"].append("Can you please provide me with the zip code of the area you would like to visit your doctor in?")

    templates["use_insurance"] = []
    templates["use_insurance"].append("Is there insurance you would like to use?")
    templates["use_insurance"].append("Would you like to use insurance with your visit?")

    templates["insurance"] = []
    templates["insurance"].append("Ok, what is your insurance?")
    templates["insurance"].append("What's the insurance you would like to use for your visit?")
    templates["insurance"].append("What kind of insurance would you like to use with your visit at the doctor's?")

    templates["day"] = []
    templates["day"].append("Is there a certain day you would like to visit?")
    templates["day"].append("Which days are you available to visit your doctor?")
    templates["day"].append("Alright, which day would you like to go to see your doctor?")
    templates["day"].append("Which days are you available for your visit?")

    templates["doctors_list"] = []
    templates["doctors_list"].append("Okay, here is a list of doctors that meet your criteria: ")
    templates["doctors_list"].append("The following is a list of doctors in your area: ")
    templates["doctors_list"].append("Okay, here is a list of doctors you can visit: ")

    templates["anything_else"] = []
    templates["anything_else"].append("Is there anything else I can help you with?")
    templates["anything_else"].append("Would you like help with anything else?")

    templates["good_bye"] = []
    templates["good_bye"].append("Thank you for using Dr. Finder!")
    templates["good_bye"].append("Ok, good bye!")
    
    # When you implement this for real, you'll need to randomly select one of the templates for
    # the specified state, rather than always selecting template 0.  You probably also will not
    # want to rely on hardcoded input slot positions (e.g., slots[0][1]).  Optionally, you might
    # want to include logic that handles a/an and singular/plural terms, to make your chatbot's
    # output more natural (e.g., avoiding "did you say you want 1 pizzas?").
    output = ""
    output_template = templates[state]

    size = len(output_template)
    if (size == 0):
        size = 1

    index = random.randrange(0,size,1)

    output = templates[state][index]
    return output



# Use this main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 chatbot.py

def main():
    
    # You can choose whether your chatbot or the participant will make the first dialogue utterance.
    # In the sample here, the chatbot makes the first utterance.
    current_state_tracker = get_dst()

    next_state, slot_values = dialogue_policy(current_state_tracker)

    slots_and_values = (next_state, slot_values)

    global n_doctor_list

    output = nlg(next_state, slot_values)
    print(output)
    
    # With our first utterance complete, we'll enter a loop for the rest of the dialogue.  In some cases,
    # especially if the participant makes the first utterance, you can enter this loop directly without
    # needing the previous code block.
    while next_state != "good_bye":
        # Accept the user's input.
        user_input = input()

        if (user_input == "quit"):
            break
        
        # Perform natural language understanding on the user's input.
        slots_and_values = nlu(user_input)
        
        # Store the extracted slots and values in the dialogue state tracker.
        update_dst(slots_and_values)
        
        # Get the full contents of the dialogue state tracker at this time.
        current_state_tracker = get_dst()
        
        # Determine which state the chatbot should enter next.
        next_state, slot_values = dialogue_policy(current_state_tracker)

        # Generate a natural language realization for the specified state and slot values.
        output = nlg(next_state, slot_values)
        
        # Print the output to the terminal.
        print(output)

        if(next_state == "doctors_list"):
            for doctor in n_doctor_list:
                name = doctor["Name"]
                zip_c = doctor["Zip Code"]
                insur = doctor["Insurance"]
                days = doctor["Days"]

                print(f"Name: {name}\n")
                print(f"Zip Code: {zip_c}\n")
                print(f"Insurance Companies Accepted:")
                for i in insur:
                    print(i)
                print(f"Days Open:")
                for d in days:
                    print(d)
                
        


################ Do not make any changes below this line ################
if __name__ == '__main__':
    main()
