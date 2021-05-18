# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

correct_answer_city = "Chicago"
correct_answer_last_street_guess = "First Street"
correct_answer_street_2 = "Oak Street"
correct_answer_3 = "123456"

class ActionVerifycity(Action):

    def name(self) -> Text:
        return "action_verify_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        #print(city)

        if city == None:
            dispatcher.utter_message(text="I don't think that is a city. Did you spell correctly?")
            return []
        elif city.lower() == correct_answer_city.lower():
            dispatcher.utter_message(text="{} is correct! \n We will send someone there. Thanks for your help!".format(correct_answer_city))
            return [SlotSet("solution_city", correct_answer_city)]
        else:
            dispatcher.utter_message(text="{} is wrong!".format(city))
            return [SlotSet("city", None)]


class ActionVerifyStreet(Action):

    def name(self) -> Text:
        return "action_verify_street"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get slot of last single street guess
        last_street_guess = tracker.get_slot("last_street_guess")
        print("last_street_guess: {} ".format(last_street_guess))

        # list for detected street values
        streets = []

        # go through all entities    
        for entity in tracker.latest_message['entities']:
            # check if entity was detected as a street and append text value
            if entity['entity'] == 'street':
                streets.append(entity['value'])

        print(streets)
        # validate if solution is correct if two streets were given (both have to be correct)
        if len(streets) == 2:            
            if streets[0].lower() == correct_answer_last_street_guess.lower() and streets[1].lower() == correct_answer_street_2.lower() or streets[1].lower() == correct_answer_last_street_guess.lower() and streets[0].lower() == correct_answer_street_2.lower():
                dispatcher.utter_message(text="Two street names were given: {} and {} - they are correct!".format(streets[0], streets[1]))
                return [SlotSet("solution_street", "{} & {}".format(correct_answer_last_street_guess, correct_answer_street_2))]
            else:
                dispatcher.utter_message(text="Two street names were given: {} and {} - they are NOT correct!".format(streets[0], streets[1]))
                return [SlotSet("last_street_guess", None)]

        # validate if solution is correct if only one street was given
        elif len(streets) == 1:
            # if last_street_guess has no saved value
            if last_street_guess == None:
                dispatcher.utter_message(text="One street name was given: {}. What's the other street?".format(streets[0]))
                return [SlotSet("last_street_guess", streets[0])]
            # if there was a saved street name
            else:
                streets.append(last_street_guess)
                if streets[0].lower() == correct_answer_last_street_guess.lower() and streets[1].lower() == correct_answer_street_2.lower() or streets[1].lower() == correct_answer_last_street_guess.lower() and streets[0].lower() == correct_answer_street_2.lower():
                    dispatcher.utter_message(text="Two street names were given: {} and {} - they are correct!".format(streets[0], streets[1]))
                    return [SlotSet("solution_street", "{} & {}".format(correct_answer_last_street_guess, correct_answer_street_2))]
                else:
                    dispatcher.utter_message(text="Two street names were given: {} and {} - they are NOT correct!".format(streets[0], streets[1]))
                    return [SlotSet("last_street_guess", None)]
                
        # complain if 0 or more than 2 street names were given 
        else:
            dispatcher.utter_message(text="I don't get it. Can you please specify one specific intersection of two streets?")
            return [SlotSet("last_street_guess", None)]



        # check if solution is correct once two streets have been entered


        # first street correct
        #return [SlotSet("last_street_guess", correct_answer_last_street_guess), SlotSet("street_2", None)]
        
        # second street correct
        #return [SlotSet("last_street_guess", None), SlotSet("street_2", correct_answer_street_2)]

        # first and second street correct
        #return [SlotSet("last_street_guess", correct_answer_last_street_guess), SlotSet("street_2", correct_answer_street_2)]

        
        # if street.lower() == correct_answer_street.lower():
        #     dispatcher.utter_message(text="{} is correct!".format(correct_answer_street))
        #     return [SlotSet("solution_street", correct_answer_street)]
        # else:
        #     dispatcher.utter_message(text="{} is wrong!".format(street))
        #     return []


class ActionVerifyPasscode(Action):

    def name(self) -> Text:
        return "action_verify_passcode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        passcode = tracker.get_slot("passcode")

        if passcode == correct_answer_3:
            dispatcher.utter_message(text="{} is correct!".format(correct_answer_3))
            return [SlotSet("solution_3", correct_answer_3)]
        else:
            dispatcher.utter_message(text="{} is wrong!".format(passcode))
            return []

       
# class FacilityForm(FormValidationAction):

#     def name(self) -> Text:
#         return "validate_facility_form"

#     # @staticmethod
#     # def required_slots(tracker: Tracker) -> List[Text]:        
#     #     return ["facility_type", "city"]

#     def validate_slot_facility_type(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:

#         print("VALIDATING FACILITY SLOT")

#         return {"slot_facility_type": slot_value}
