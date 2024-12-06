# Renu Oberoi Luxury Brand Keyword Analysis

## Overview

This application analyzes trending keywords in the context of a luxury brand's message and tone of voice. Specifically designed for **Renu Oberoi Luxury Jewellery**, the tool determines whether a keyword aligns with the brand's values and generates aspirational tweets for relevant keywords.

---

## Requirements

### Prerequisites
- Python 3.8 or higher.
- Virtual environment recommended (e.g., `venv`, `conda`).

### Libraries and Dependencies
Install required libraries using the following command:
```bash
pip install -r requirements.txt
```

### Key Dependencies
- `transformers`: For text generation using GPT-2.
- `streamlit`: For building the web application interface.
- `pytrends`: For fetching trending keywords from Google Trends.
- `logging`: For error handling and debugging.

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Shivani6178/assignment.git
   cd assignment
   ```

2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.json` file in the root directory with the following structure:
   ```json
   {
       "brandMessage": "At Renu Oberoi Luxury Jewellery, we celebrate the art of fine craftsmanship and timeless beauty. Our creations are for the discerning, sophisticated woman who values elegance and exclusivity.",
       "toneOfVoice": {
           "description": "Our tone of voice is luxurious, elegant, and aspirational, designed to engage a high-end clientele while maintaining a personal connection."
       }
   }
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Open the app in your browser at `http://localhost:8501`.

---

## Usage

### Fetch Trending Keywords
1. Use the slider to set the number of trending keywords to fetch (1–10).
2. Click **Fetch and Analyze Keywords** to retrieve the keywords.

### Analyze Keywords
- The app will analyze each keyword against the brand message to determine relevance.
- Results are displayed in a table with:
  - **Keyword**: The trending keyword.
  - **Relevance**: Whether the keyword aligns with the brand (`✅ Relevant` or `❌ Not Relevant`).
  - **LLM Analysis**: Concise reasoning for alignment or non-alignment.

### Generate Tweets
- For relevant keywords, the app will generate luxury-themed tweets tailored to the brand’s tone of voice.

---

## Code Structure

### File Breakdown
- `streamlit_app.py`: Contains the Streamlit application code.
- `backend.py`: Backend logic for fetching keywords, analyzing them, and generating tweets.
- `config.json`: Configuration file for brand-specific details.
- `requirements.txt`: List of required Python libraries.

### Key Functions
- **`fetch_trending_keywords(max_keywords)`**: Fetches trending keywords from Google Trends.
- **`analyze_keyword(keyword, brand_message, model_pipeline)`**: Analyzes a keyword for relevance to the brand.
- **`generate_tweet(keyword, tone, model_pipeline)`**: Generates a luxury-themed tweet for a relevant keyword.
- **`initialize_pipeline(model_name)`**: Initializes the llama pipeline for text generation.

---

## Example Output

### Keyword Analysis Table
| **Keyword**          | **Relevance**     | **LLM Analysis**                                                                 |
|----------------------|-------------------|----------------------------------------------------------------------------------|
| UnitedHealthcare CEO | ❌ Not Relevant   | Does not align because it relates to healthcare leadership, not luxury jewellery.|
| Bitcoin              | ❌ Not Relevant   | Does not align because it focuses on cryptocurrency, not exclusivity or elegance.|
| Fine Diamonds        | ✅ Relevant       | Aligns because it reflects exclusivity and craftsmanship valued by the brand.    |

### Generated Tweet
**Keyword**: Fine Diamonds  
**Generated Tweet**:  
"Unveiling the brilliance of fine diamonds – where timeless beauty meets unparalleled craftsmanship. ✨ #RenuOberoiLuxury #FineJewellery"

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
