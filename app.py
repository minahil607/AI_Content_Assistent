import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Content Assistant", page_icon="✍️", layout="centered"
)

st.title("✍️ AI Content Assistant")
st.write(
    "Generate complete posts, captions, and relevant hashtags using Groq!"
)

# API Key Handling (Reads from Streamlit Secrets or manual input)
groq_api_key = st.secrets.get("GROQ_API_KEY", "")

if not groq_api_key:
    groq_api_key = st.sidebar.text_input(
        "Enter Groq API Key", type="password", help="Get key at console.groq.com"
    )

if not groq_api_key:
    st.info(" Please enter your Groq API key in the sidebar to continue.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=groq_api_key)

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)

    with col1:
        platform = st.selectbox(
            "Target Platform",
            [
                "LinkedIn",
                "Instagram",
                "Twitter / X",
                "Facebook",
                "TikTok",
                "Blog Post",
            ],
        )
        content_type = st.selectbox(
            "Content Format",
            [
                "Promotional",
                "Educational",
                "Storytelling",
                "Product Announcement",
                "Call to Action",
            ],
        )

    with col2:
        tone = st.selectbox(
            "Tone of Voice",
            [
                "Professional",
                "Casual & Friendly",
                "Witty & Humorous",
                "Inspirational",
                "Persuasive",
            ],
        )
        target_audience = st.text_input(
            "Target Audience", placeholder="e.g., Software Engineers, Small Business Owners"
        )

    topic = st.text_area(
        "Topic / Key Message",
        placeholder="e.g., Launching a new AI productivity tool for remote workers...",
    )

    submitted = st.form_submit_button("Generate Content")

# Generation Logic
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic or key message.")
    else:
        with st.spinner("Crafting your content..."):
            prompt = f"""
            You are an expert social media content manager.
            Create a high-performing post based on these inputs:

            - Platform: {platform}
            - Content Type: {content_type}
            - Tone: {tone}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Topic: {topic}

            Format your response clearly with:
            1. **Post Title / Hook**
            2. **Main Caption Body**
            3. **Call to Action (CTA)**
            4. **Relevant Hashtags**
            """

            try:
                # Using Groq's fast, free Llama model
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                generated_text = response.choices[0].message.content

                st.subheader("🎉 Your Generated Content")
                st.markdown(generated_text)

                # Easy copy button for output text
                st.download_button(
                    label="📥 Download Content as Text",
                    data=generated_text,
                    file_name="generated_post.txt",
                    mime="text/plain",
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
