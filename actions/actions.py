# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

correct_answer_1 = "Chicago"
correct_answer_2 = "Jack"
correct_answer_3 = "123456"

class ActionVerifyLocation(Action):

    def name(self) -> Text:
        return "action_verify_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")

        if location.lower() == correct_answer_1.lower():
            dispatcher.utter_message(text="{} is correct! \n We are contacting the nearest field agent. Please stand by...".format(correct_answer_1))
            #dispatcher.utter_message("We are contacting the nearest field agent. Please stand by...")
            return [SlotSet("solution_1", correct_answer_1)]
        else:
            dispatcher.utter_message(text="{} is wrong!".format(location))
            return []


class ActionVerifyName(Action):

    def name(self) -> Text:
        return "action_verify_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")

        if name.lower() == correct_answer_2.lower():
            dispatcher.utter_message(text="{} is correct!".format(correct_answer_2))
            return [SlotSet("solution_2", correct_answer_2)]
        else:
            dispatcher.utter_message(text="{} is wrong!".format(name))
            return []


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
#     #     return ["facility_type", "location"]

#     def validate_slot_facility_type(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:

#         print("VALIDATING FACILITY SLOT")

#         return {"slot_facility_type": slot_value}
