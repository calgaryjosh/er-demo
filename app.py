
import streamlit as st
import openai

st.set_page_config(page_title="EchoRoute Demo", layout="centered")

st.title("EchoRoute")
st.markdown("### Where are you right now?")
location = st.text_input("Enter a location (e.g., Banff, Alberta)", placeholder="Try Victoria, BC")

preset = st.selectbox("Or choose a preset location:", ["", "Banff, Alberta", "Point Reyes, California", "Victoria, BC"])
if preset and not location:
    location = preset

st.markdown("*In the full version, EchoRoute will detect your location automatically and share stories in the background — no typing required.*")

if "history" not in st.session_state:
    st.session_state.history = []

def generate_story(loc):
    prompt = f"""You are a warm, wise, and curious storyteller. Your job is to share a short, fascinating, and true (or very likely true) story about a specific location.

The listener is currently traveling near {loc} — possibly by car. They want to learn something they might not already know.

Share a story that is either:
- A historical event or local legend
- A notable person from this area
- A surprising geographic or natural feature
- A quirky, true fact from this place

Use calm, natural language — like you’re reading from a beautifully written storybook.

Keep it under 200 words. Do not include references or citations. End with a subtle reflective or poetic note.

Location: {loc}

Now tell the story.""" 

    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

if st.button("Tell Me Something") and location:
    story = generate_story(location)
    st.session_state.history.append((location, story))
    st.markdown("---")
    st.markdown(f"#### Story from **{location}**:")
    st.write(story)

if st.button("Tell Me Another") and location:
    story = generate_story(location)
    st.session_state.history.append((location, story))
    st.markdown("---")
    st.markdown(f"#### Another story from **{location}**:")
    st.write(story)
