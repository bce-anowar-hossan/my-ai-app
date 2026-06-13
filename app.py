import streamlit as st
from google import genai

# ১. অ্যাপের টাইটেল এবং সেটআপ
st.set_page_config(page_title="আমার AI চ্যাটবট", page_icon="🤖")
st.title("🤖 আমার নিজস্ব AI চ্যাটবট")
st.write("Gemini API দ্বারা চালিত আপনার ব্যক্তিগত সহকারী।")

# ২. Gemini API কী সেটআপ
API_KEY = "# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-flash-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        tools=tools,
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if text := chunk.text:
            print(text, end="")

if __name__ == "__main__":
    generate()


" # এখানে আপনার আসল API Key বসান
client = genai.Client(api_key=API_KEY)

# ৩. চ্যাট হিস্ট্রি (মেসেজ রেকর্ড) ধরে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের কথাগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৪. ইউজারের কাছ থেকে ইনপুট নেওয়া
if user_input := st.chat_input("আমাকে যেকোনো প্রশ্ন করুন..."):
    
    # ইউজারের মেসেজ স্ক্রিনে দেখানো এবং হিস্ট্রিতে সেভ করা
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # বটের উত্তরের জন্য লোডিং অ্যানিমেশন
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Gemini থেকে উত্তর আনা
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
            )
            bot_reply = response.text
            
            # বটের উত্তর স্ক্রিনে দেখানো
            message_placeholder.markdown(bot_reply)
            
            # বটের উত্তর হিস্ট্রিতে সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            message_placeholder.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
      
