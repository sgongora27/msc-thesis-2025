"""Load models to use them as a narrator and a common-sense oracle in the PAYADOR pipeline."""
import google.generativeai as genai
import requests
import replicate
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name: str = "gemini-1.5-flash") -> object:

    google_models = ["gemini-1.0-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
    replicate_models = ["meta/meta-llama-3-70b", "meta/meta-llama-3-70b-instruct"]

    model = None

    if model_name in google_models:
        model = GeminiModel(API_key="GOOGLE_API_KEY", model_name=model_name)
    elif model_name in replicate_models:
        model = ReplicateModel(API_key="REPLICATE_API_TOKEN", model_name=model_name)

    return model


class ReplicateModel():
    def __init__ (self, API_key:str, model_name:str = "meta/meta-llama-3-70b-instruct") -> None:
        self.temperature = 0.7
        self.model_name = model_name

    def prompt_model(self,system_msg: str, user_msg:str) -> str:
        """Prompt the Replicate model."""

        system_instructions = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_msg}<|eot_id|><|start_header_id|>user<|end_header_id|>"

        input = {
            "top_p": 0.1,
            "min_tokens": 0,
            "temperature": self.temperature,
            "prompt": user_msg,
            "prompt_template": system_instructions + "\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        }

        output = replicate.run(self.model_name,input=input)
        
        return "".join(output)

class GeminiModel():
    def __init__ (self, API_key:str, model_name:str = "gemini-1.0-pro") -> None:
        """"Initialize the Gemini model using an API key."""
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_name)

    def prompt_model(self,system_msg: str, user_msg:str) -> str:
        """Prompt the Gemini model."""
        return self.model.generate_content(system_msg + "\n\n" + user_msg, safety_settings=self.safety_settings).text
