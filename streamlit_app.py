import streamlit as st
from backend import (
    fetch_trending_keywords,
    analyze_keyword,
    generate_tweet,
    initialize_client,
    load_config,
)

# Initialize configurations and LLM client
config = load_config()
model_client = initialize_client(model_name="meta-llama/Llama-3.2-3B-Instruct")

# Title and instructions
st.title("Renu Oberoi Luxury Brand Keyword Analysis")
st.markdown(
    """
    Use this tool to analyze trending keywords for alignment with the Renu Oberoi Luxury Brand message. 
    Generate aspirational tweets for relevant keywords.
    """
)

# Input: Number of keywords to fetch
num_keywords = st.slider("Number of Keywords to Fetch", min_value=1, max_value=20, value=5)

if st.button("Fetch and Analyze Keywords"):
    with st.spinner("Fetching trending keywords..."):
        keywords = fetch_trending_keywords(max_keywords=num_keywords)

    if not keywords:
        st.error("No keywords fetched. Please check the logs for details.")
    else:
        st.success(f"Successfully fetched {len(keywords)} keywords.")

        # Analyze each keyword
        st.info("Analyzing keywords...")
        analysis_results = [
            analyze_keyword(keyword, config["brandMessage"], model_client)
            for keyword in keywords
        ]

        # Display results in a table
        st.subheader("Keyword Analysis Results")
        st.table({
            "Keyword": [result["keyword"] for result in analysis_results],
            "Relevance": [result["relevance"] for result in analysis_results],
            "LLM Analysis": [result["analysis"] for result in analysis_results],
        })

        # Generate tweets for relevant keywords
        st.subheader("Generated Tweets for Relevant Keywords")
        for result in analysis_results:
            if "✅" in result["relevance"]:
                tweet = generate_tweet(
                    result["keyword"], config["toneOfVoice"]["description"], model_client
                )
                st.write(f"**Keyword:** {result['keyword']}")
                st.write(f"**Generated Tweet:** {tweet}")

# Sidebar: Brand Guidelines
st.sidebar.subheader("Brand Guidelines")
st.sidebar.markdown(
    """
    - **Tone**: Luxurious, elegant, and aspirational.
    - **Audience**: Discerning women who value exclusivity.
    - **Focus**: Fine craftsmanship and timeless beauty.
    """
)
