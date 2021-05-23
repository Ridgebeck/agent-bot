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
correct_answer_street_1 = "First Street"
correct_answer_street_2 = "Oak Street"
correct_answer_password = "123456"

class ActionVerifycity(Action):

    def name(self) -> Text:
        return "action_verify_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        #print(city)

        if city == None:
            dispatcher.utter_message(response="utter_no_city")
            return []
        elif city.lower() == correct_answer_city.lower():
            dispatcher.utter_message(response="utter_correct_city", city=correct_answer_city)
            return [SlotSet("solution_city", correct_answer_city)]
        else:
            dispatcher.utter_message(response="utter_incorrect_city", city=city)
            return [SlotSet("city", None)]


class ActionVerifyStreet(Action):

    def name(self) -> Text:
        return "action_verify_street"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get slot of last single street guess
        last_street_guess = tracker.get_slot("last_street_guess")

        # list for detected street values
        streets = []

        # assmeble solution string of correct intersection
        solution_string = "{} & {}".format(correct_answer_street_1, correct_answer_street_2)

        # go through all entities from last message   
        for entity in tracker.latest_message['entities']:
            # check if entity was detected as a street and append text value
            if entity['entity'] == 'street':
                streets.append(entity['value'])

        # validate if solution is correct if two streets were given (both have to be correct)
        if len(streets) == 2:
            if streets[0].lower() == correct_answer_street_1.lower() and streets[1].lower() == correct_answer_street_2.lower() or streets[1].lower() == correct_answer_street_1.lower() and streets[0].lower() == correct_answer_street_2.lower():
                dispatcher.utter_message(response="utter_correct_intersection")
                return [SlotSet("solution_street", "{} & {}".format(correct_answer_street_1, correct_answer_street_2))]
            else:
                dispatcher.utter_message(response="utter_incorrect_intersection")
                return [SlotSet("last_street_guess", None)]

        # validate if solution is correct if only one street was given
        elif len(streets) == 1:
            # if last_street_guess has no saved value
            if last_street_guess == None:
                dispatcher.utter_message(response="utter_one_street", street=streets[0])
                return [SlotSet("last_street_guess", streets[0])]
            # if there was a saved street name
            else:
                streets.append(last_street_guess)
                if streets[0].lower() == correct_answer_street_1.lower() and streets[1].lower() == correct_answer_street_2.lower() or streets[1].lower() == correct_answer_street_1.lower() and streets[0].lower() == correct_answer_street_2.lower():
                    dispatcher.utter_message(response="utter_correct_intersection", intersection=solution_string)
                    return [SlotSet("solution_street", "{} & {}".format(correct_answer_street_1, correct_answer_street_2))]
                else:
                    dispatcher.utter_message(response="utter_incorrect_intersection")
                    return [SlotSet("last_street_guess", None)]
                
        # complain if 0 or more than 2 street names were given 
        else:
            dispatcher.utter_message(response="utter_no_two_streets")
            return [SlotSet("last_street_guess", None)]


class ActionVerifyPassword(Action):

    def name(self) -> Text:
        return "action_verify_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        passcode = tracker.get_slot("password")

        # remove everything thats not a digit
        passcode = "".join(filter(str.isdigit, passcode))       
        #print(passcode)

        # check if length is correct

        if passcode == correct_answer_password:
            dispatcher.utter_message(response="utter_correct_password", password=correct_answer_password)
            return [SlotSet("solution_password", correct_answer_password)]
        else:
            dispatcher.utter_message(response="utter_incorrect_password", password=passcode)
            return [SlotSet("password", None)]

       
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
