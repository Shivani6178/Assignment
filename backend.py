# from transformers import pipeline
# from pytrends.request import TrendReq
# import logging
# import json
# from huggingface_hub import InferenceClient

# # Load configurations
# def load_config():
#     try:
#         with open("config.json", "r") as f:
#             config = json.load(f)
#         return config
#     except Exception as e:
#         logging.error(f"Error loading config: {str(e)}")
#         return {
#             "brandMessage": "At Renu Oberoi Luxury Jewellery, we celebrate the art of fine craftsmanship and timeless beauty. Our creations are for the discerning, sophisticated woman who values elegance and exclusivity.",
#             "toneOfVoice": {"description": "Luxurious, elegant, and aspirational."},
#         }

# # Fetch trending keywords
# def fetch_trending_keywords(max_keywords=5):
#     try:
#         pytrends = TrendReq(hl="en-US", tz=360)
#         trending_data = pytrends.trending_searches(pn="united_states")
#         keywords = trending_data[0].tolist()
#         logging.info(f"Fetched trending keywords: {keywords[:max_keywords]}")
#         return keywords[:max_keywords]
#     except Exception as e:
#         logging.error(f"Error fetching trending keywords: {str(e)}")
#         return []

# # Initialize LLM client
# def initialize_client(model_name="meta-llama/Llama-3.2-3B-Instruct"):
#     try:
#         return InferenceClient(model=model_name)
#     except Exception as e:
#         logging.error(f"Error initializing LLM client: {str(e)}")
#         return None

# # Function to analyze a single keyword
# def analyze_keyword(keyword, brand_message, llm_client):
#     try:
#         input_prompt = (
#             f"Keyword: '{keyword}'\n"
#             f"Brand Message: '{brand_message}'\n"
#             "Does the keyword align with the brand message? Answer with Yes or No, followed by one sentence explaining your reasoning"
#         )

#         # Use the client to generate the analysis
#         response = llm_client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": input_prompt},
#             ],
#             stream=False,
#             max_tokens=200,
#         )

#         analysis_text = response["choices"][0]["message"]["content"].strip()

#         # Parse the result for relevance
#         if "Yes" in analysis_text:
#             is_relevant = True
#         elif "No" in analysis_text:
#             is_relevant = False
#         else:
#             raise ValueError("Unexpected response format.")

#         concise_analysis = analysis_text.split(".")[0] + "."  # Extract the first sentence
#         return {
#             "keyword": keyword,
#             "relevance": "✅ Relevant" if is_relevant else "❌ Not Relevant",
#             "analysis": concise_analysis,
#         }
#     except ValueError as ve:
#         # Handle specific parsing issues
#         return {
#             "keyword": keyword,
#             "relevance": "❌ Not Relevant",
#             "analysis": f"Error during analysis: {str(ve)}",
#         }
#     except Exception as e:
#         # General error handling
#         return {
#             "keyword": keyword,
#             "relevance": "❌ Not Relevant",
#             "analysis": f"Error during analysis: {str(e)}",
#         }

# # Function to generate a tweet
# def generate_tweet(keyword, tone, llm_client):
#     try:
#         input_prompt = (
#             f"Generate a luxury-themed tweet for the keyword '{keyword}' "
#             f"with the tone: '{tone}'. The tweet should be concise and aspirational."
#         )

#         # Use the client to generate the tweet
#         response = llm_client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": input_prompt},
#             ],
#             stream=False,
#             max_tokens=100,
#         )

#         tweet = response["choices"][0]["message"]["content"].strip()
#         return tweet
#     except Exception as e:
#         return f"Error generating tweet: {str(e)}"

import os
import time
import logging
import json
from transformers import pipeline
from huggingface_hub import InferenceClient
from pytrends.request import TrendReq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Load configurations
def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        return {
            "brandMessage": "At Renu Oberoi Luxury Jewellery, we celebrate the art of fine craftsmanship and timeless beauty. Our creations are for the discerning, sophisticated woman who values elegance and exclusivity.",
            "toneOfVoice": {"description": "Luxurious, elegant, and aspirational."},
        }

# Fetch trending keywords
def fetch_trending_keywords(max_keywords=5):
    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        trending_data = pytrends.trending_searches(pn="united_states")
        keywords = trending_data[0].tolist()
        logging.info(f"Fetched trending keywords: {keywords[:max_keywords]}")
        return keywords[:max_keywords]
    except Exception as e:
        logging.error(f"Error fetching trending keywords: {str(e)}")
        return []

# Initialize LLM client
def initialize_client(model_name="meta-llama/Llama-3.2-3B-Instruct"):
    api_token = os.getenv("HF_API_TOKEN")  # Securely fetch token
    if not api_token:
        raise ValueError("Hugging Face API token not found in environment variables.")
    try:
        return InferenceClient(model=model_name, token=api_token)
    except Exception as e:
        logging.error(f"Error initializing LLM client: {str(e)}")
        return None

# Analyze a single keyword
def analyze_keyword(keyword, brand_message, llm_client, retries=3):
    input_prompt = (
        f"Keyword: '{keyword}'\n"
        f"Brand Message: '{brand_message}'\n"
        "Does the keyword align with the brand message? Answer with Yes or No, followed by one sentence explaining your reasoning."
    )

    for attempt in range(retries):
        try:
            response = llm_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_prompt},
                ],
                stream=False,
                max_tokens=200,
            )
            analysis_text = response["choices"][0]["message"]["content"].strip()

            # Parse response
            is_relevant = "Yes" in analysis_text
            concise_analysis = analysis_text.split(".")[0] + "."
            return {
                "keyword": keyword,
                "relevance": "✅ Relevant" if is_relevant else "❌ Not Relevant",
                "analysis": concise_analysis,
            }
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logging.error(f"Error analyzing keyword '{keyword}': {str(e)}")
                return {
                    "keyword": keyword,
                    "relevance": "❌ Not Relevant",
                    "analysis": f"Error during analysis: {str(e)}",
                }

# Generate a tweet
def generate_tweet(keyword, tone, llm_client):
    input_prompt = (
        f"Generate a luxury-themed tweet for the keyword '{keyword}' "
        f"with the tone: '{tone}'. The tweet should be concise and aspirational."
    )
    try:
        response = llm_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_prompt},
            ],
            stream=False,
            max_tokens=100,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"Error generating tweet for '{keyword}': {str(e)}")
        return f"Error generating tweet: {str(e)}"
