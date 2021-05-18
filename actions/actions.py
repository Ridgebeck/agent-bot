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
correct_answer_street = "Oak Street"
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
            #print("spelling issue?")
            return []
        elif city.lower() == correct_answer_city.lower():
            dispatcher.utter_message(text="{} is correct! \n We will send someone there. Thanks for your help!".format(correct_answer_city))
            #print("correct city")
            return [SlotSet("solution_city", correct_answer_city)]
        else:
            dispatcher.utter_message(text="{} is wrong!".format(city))
            #print("wrong city")
            return [SlotSet("city", None)]


class ActionVerifyStreet(Action):

    def name(self) -> Text:
        return "action_verify_street"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #street = tracker.get_slot("street")

        dispatcher.utter_message("This is a street name!")
        return []

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
