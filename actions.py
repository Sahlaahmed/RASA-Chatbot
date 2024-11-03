# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# actions.py
import openai
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os

# Set up your OpenAI API key
openai.api_key = os.getenv("sk-frOEwZZFg2oxiSXa7YclELqn3uCSfCnVEPka0CXakTT3BlbkFJvmRVdIo8idfemuiiz3zXqEtYS7wk_veYqpSapMUd0A")  # Set your OpenAI API key in environment variables

class ActionFetchCricketInfo(Action):
    def name(self) -> str:
        return "action_fetch_cricket_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        user_intent = tracker.latest_message['intent'].get('name')
        user_query = tracker.latest_message['text']  # Get the user's original message

        if user_intent in [
            "ask_cricket_score",
            "ask_cricket_match_schedule",
            "ask_cricket_player_info",
            "ask_cricket_team_info",
            "ask_cricket_news",
            "ask_cricket_live_updates",
            "ask_cricket_ranking"
        ]:
            # Call OpenAI API to get a response
            response = self.get_chatgpt_response(user_query)
            dispatcher.utter_message(text=response)
        else:
            # Handle other intents if necessary
            dispatcher.utter_message(text="I'm not sure how to respond to that.")

        return []

    def get_chatgpt_response(self, query: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Specify the model you want to use
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Error fetching response from ChatGPT: {str(e)}"

