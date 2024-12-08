from backend.utility.googlesearch import get_news_summary
import streamlit as st
from dotenv import load_dotenv
from utility.llm_call import gorq_call
import ast
from utility.template_id import get_random_template,generate_meme

load_dotenv()

if "summary" not in st.session_state:
    st.session_state.summary =None

if "memes" not in st.session_state:
    st.session_state.memes =None

if "text_post" not in st.session_state:
    st.session_state.text_post =None

input_text=st.text_input("Enter somthing")

button=st.button("Submit")

if button:
    with st.spinner("Fetching news and generating summary..."):
        st.session_state.summary = get_news_summary(input_text)
        st.title("Summary")
        try:
            data = ast.literal_eval(st.session_state.summary )
            # data = json.loads(summary)
            st.json(data.get("SUMMARY", "No summary available."))
            
            st.subheader("References")
            references = data.get("REFERENCES", [])
            if references:
                for ref in references:
                    st.markdown(f"- [Source Link]({ref})")
            else:
                st.write("No references available.")
            print("json")
        except:
            data = str(st.session_state.summary).replace('{', '').replace('}', '')
            st.markdown(data)
            print("no json")
    st.text(st.session_state.summary )
    text_generation_prompt=f"""Your are the helpfull assistent. Use the provided news information, craft an engaging and shareable text post. 
Ensure the tone matches the context of the news—professional for formal news, empathetic for emotional news, or humorous for lighter stories. 
The post should clearly communicate the key information while being concise and attention-grabbing.

Here is the context: 
{st.session_state.summary }

Generate a text post suitable for social media. Follow these guidelines:
1. Summarize the key points in 2–3 sentences.
2. Use a tone that matches the news (e.g., formal, empathetic, or humorous).
3. Include a call-to-action or a closing statement to prompt engagement, like asking for opinions, sharing thoughts, or encouraging actions.
4. Use language that is relatable and resonates with the target audience.


Example:
User Input: Create a humorous post about AI replacing jobs for a Twitter audience.
Text Post: "AI's got jokes now? Next thing you know, itʼs taking over my stand-up gig. #AIvsHumans #TechTakeover"

User Input:{input_text}

final_response:
Text Post:
"""
    st.session_state.text_post=gorq_call(text_generation_prompt)
    st.title("Text Post")
    st.text(st.session_state.text_post)
    meme_prompt=f"""You are tasked with creating a humorous or thought-provoking meme based on a given context. Your role involves analyzing the context for key themes or events, conceptualizing relatable and engaging memes, and providing clear visual and textual descriptions to generate the meme.


Here is the news context: 
{st.session_state.summary}

Generate a meme concept based on this information. Follow these guidelines:
1. Identify a key event of or theme from the context that can be humorously or cleverly highlighted.
2. Create a humorous or thought-provoking concept based on the key ements of the context. 
3. The meme should be relatable, include visual elements described clearly and incorporate text that conveys the humor or the point effectively.
3. Suggest a visual description for the meme (e.g., background image, characters, expressions).
4. Always suggest the sentiment of memes from this list: funny, sad, happy, angry,sarcastic,relatable,wholesome,motivational,sarcastic-positive,work, sports, school, technology, gaming, relationship.
5. Write the meme in a relatable and engaging style. Suggest only 3 meme templates.
6. Ensure the humor or messaging is clear, appropriate, and resonates with a broad audience.
7. Write the visual description in such way that, to generate the images for meme using DALL-E 3 models. Do not use any real person's names. Do not asked to type any text on image.
8. Final output must only be in JSON format.

Example:
User Input: Create a humorous post about AI replacing jobs for a Twitter audience.
captions: Boyfriend: 'My job,' Girlfriend: 'Doing work,' Other girl: 'AI'.

user interest:{input_text}

Final output should be in the following JSON format:
[{{"Theme":(write meme theme),
"sentiment":(write search query),
"Visual Description":(write prompt to generate the image),
"Caption":(meme captions)}}]
"""
    meme_post=gorq_call(meme_prompt)
    # st.text(meme_post)
    st.session_state.memes =eval(meme_post[meme_post.find("["):meme_post.rfind("]")+1])
    st.title("Memes")
    for m in st.session_state.memes:
        st.text(m["Theme"])
        st.text(m["Visual Description"])
        st.text(m["Caption"])
        st.divider()

if st.session_state.summary!=None:
    st.title("Summary")
    st.text(st.session_state.summary )
    # Optionally display the saved search results after fetching
    if st.button("See Retrieved Results"):
        if "google_search_results" in st.session_state and st.session_state.google_search_results:
            st.sidebar.subheader("Retrieved Results")
            for i, result_set in enumerate(st.session_state.google_search_results):
                st.sidebar.write(f"Search {i + 1}:")
                for result in result_set:
                    st.sidebar.markdown(f"**{result['title']}**")
                    st.sidebar.markdown(f"[{result['link']}]({result['link']})")
                    st.sidebar.markdown(f"{result['snippet']}")
        else:
            st.write("No search results stored yet.")
    st.title("Text Post")
    st.markdown(st.session_state.text_post)
    st.title("Memes")
    cols=st.columns([1,1,1])
    for m in range(3):
        # st.text(m["Caption"])
        temp_id=get_random_template(st.session_state.memes[m]["sentiment"])
        USERNAME = "your_imgflip_username"
        PASSWORD = "your_imgflip_password"
        print(temp_id)
        meme_url=generate_meme(temp_id,st.session_state.memes[m]['Caption'],USERNAME,PASSWORD)
        if meme_url:
            cols[m].image(meme_url, caption=st.session_state.memes[m]["Theme"], use_container_width =True)
            cols[m].markdown(st.session_state.memes[m]["Visual Description"])
        else:
            print("-------------------------------------------")
            print(temp_id)
            print("-------------------------------------------")
        # st.divider()