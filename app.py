import os
import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags using Groq AI.")

# Sidebar for API Key input
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input(
        "Enter Groq API Key:",
        type="password",
        help="Get your free key from console.groq.com"
    )
    
    # Try fetching key from environment variables (useful for Streamlit Cloud secrets)
    api_key = api_key_input or os.environ.get("GROQ_API_KEY")

# App Main Interface
st.subheader("Post Parameters")

col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "Blog Post"]
    )
    content_type = st.selectbox(
        "Content Type",
        ["Informational / Educational", "Promotional / Sales", "Storytelling / Personal", "Question / Engagement Prompt"]
    )
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual & Friendly", "Witty & Humorous", "Inspirational", "Persuasive"]
    )

with col2:
    topic = st.text_input("Topic", placeholder="e.g., Remote work best practices")
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Developers, Managers")

# Generation Trigger
if st.button("Generate Post", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert social media strategist and content creator.
            Create a complete post based on the following requirements:
            
            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            
            Structure your response as follows:
            1. **Main Post Content**: Clean formatted copy formatted specifically for {platform}.
            2. **Call to Action (CTA)**: A clear engagement trigger suited for the audience.
            3. **Relevant Hashtags**: 3 to 7 high-impact hashtags.
            """
            
            with st.spinner("Generating content with Groq..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI content creation assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                generated_text = response.choices[0].message.content
                
                st.success("Post generated successfully!")
                st.markdown("---")
                st.markdown(generated_text)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")