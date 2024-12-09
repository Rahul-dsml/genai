from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from utility.auth_helper import create_access_token, encrypt_password, verify_password
from typing import Optional
from datetime import datetime, timedelta
from model import *
from utility.image_processing import generate_image, generate_image_using_prompt
import bcrypt, replicate
from utility.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
import logging
import json
from utility.auth_helper import fake_users_db
from utility.googlesearch import get_news_summary
import streamlit as st
from utility.googlesearch import history_manager
from utility.llm_call import gorq_call
from utility.template_id import get_random_template,generate_meme
from model import SummarizerInput

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])



def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# Signup endpoint
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(signup_request: SignupRequest):
    if signup_request.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if any(user["email"] == signup_request.email for user in fake_users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    # Hash the password and store user data
    hashed_password = hash_password(signup_request.password)
    fake_users_db[signup_request.username] = {
        "username": signup_request.username,
        "email": signup_request.email,
        "password": hashed_password,
        'role': signup_request.user
    }
    return {"message": "User signed up successfully"}


# Protected route (requires authentication)
@router.post("/summarizer") # dependencies=[Depends(JWTBearer())]
async def summarizer(query: SummarizerInput): # token: str =Depends(JWTBearer())
    try:
        
        summary=await get_news_summary(query)
        
        metadata=history_manager.get_history("metadata")[:5]
        # print(metadata)
        history_manager.add_entry("summary", summary)
        return JSONResponse(content={"summary":summary, "metadata":metadata}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"summary" : e, "metadata":"Bad Request"}, status_code=400)


@router.post("/text") # dependencies=[Depends(JWTBearer())]
async def text_post(query: SummarizerInput): # dependencies=[Depends(JWTBearer())]
    try:
        summary=history_manager.get_history("summary")[0]
        text_post_history= str(history_manager.get_history("post_history")[:3])
        text_generation_prompt=f"""You are an expert in networking and content marketing for social media. Using provided news summary, user's current input and user's conversation history,
                                   Your task is to craft an engaging and shareable social media post. 
                                   
News Summary: ```{summary}```

Generate the social media post strictly following these guidelines:
1. Summarize the key points in 2–3 sentences.
2. Use a tone that matches the news (e.g., political, emotional, empathetic, funny, etc.).
3. The post should clearly communicate the key information while being concise and attention-grabbing.
3. Include a call-to-action or a closing statement to prompt engagement, like asking for opinions, sharing thoughts, or encouraging actions.
4. The generated post must contains relevant and necessary hashtags.
5. Use language that is relatable and resonates with the target audience.

Example:
User Input: Create a humorous post about AI replacing jobs for a Twitter audience.
Social Media Post: AI's got jokes now? Next thing you know, it's taking over my stand-up gig. #AIvsHumans #TechTakeover

MAKE SURE TO INCORPORATE THE CHANGES/ FEEDBACK BASED ON THE USER'S CONVERSATION HISTORY GIVEN BELOW:
User Conversation history: {text_post_history}

current user input: ```{query}```

final_response:
Social Media Post:
"""
        text_post= await gorq_call(text_generation_prompt)
        history_manager.add_entry("post_history", {"user": query, "assistant": text_post})
        return JSONResponse(content={"text_post":text_post},status_code=200)
    except Exception:
        return JSONResponse(content={"text_post":"Bad Request"},status_code=400)


@router.post("/memes") # dependencies=[Depends(JWTBearer())]
async def meme(query: SummarizerInput): # token: str =Depends(JWTBearer())
    try:
        summary=history_manager.get_history("summary")[0]
        meme_post_history = str(history_manager.get_history("meme_history")[:2])
        print(summary)
        meme_prompt=f"""You are an expert in creating intellectual, creative, humorous and thought-provoking meme themes and captions based on the given news summary and user's current input. 
        Your task is to generate key themes and captions, conceptualizing relatable and engaging memes.


News Summary: ```{summary}```

You must follow below guidelines to generate a meme concept theme and captions:
1. Identify a key event or theme from the news summary and use that to generate your response.
2. The meme captions must be relatable that conveys the humor or the point effectively as it is targeted to broader audience.
3. You MUST give the sentiment of memes from this list: funny, sad, happy, angry,sarcastic,relatable,wholesome,motivational,sarcastic-positive,work, sports, school, technology, gaming, relationship.
4. Generate only 3 meme templates.
5. Final output MUST BE IN JSON FORMAT.

Example for one meme template:
User Input: Create a humorous post about AI replacing jobs for a Twitter audience.
Theme: AI needs humans to succeed
sentiment: sarcastic
captions: Boyfriend: 'My job,' Girlfriend: 'Doing work,' Other girl: 'AI'.


MAKE SURE TO INCORPORATE THE CHANGES/ FEEDBACK BASED ON THE USER'S CONVERSATION HISTORY GIVEN BELOW:
User Conversation history: {meme_post_history}

user interest:```{query}```

Final output should be in the following JSON format:
[{{"Theme":(write meme theme),
"sentiment":(write search query),
"Caption":(meme captions)}}]
"""
        meme_post=await gorq_call(meme_prompt)
        memes=eval(meme_post[meme_post.find("["):meme_post.rfind("]")+1])
        history_manager.add_entry("post_history", {"user": query, "assistant": memes})
        memes_url=[]
        for m in range(3):
            temp_id=get_random_template(memes[m]["sentiment"])
            USERNAME = "your_imgflip_username"
            PASSWORD = "your_imgflip_password"
            # print(temp_id)
            meme_url=await generate_meme( temp_id , memes[m]['Caption'], USERNAME, PASSWORD)
            if meme_url:
                memes_url.append([meme_url,memes[m]["Theme"]])
            else:
                print("-------------------------------------------")
                print(temp_id)
                print("-------------------------------------------")
        return JSONResponse(content={"memes_url":memes_url},status_code=200) # [meme_url,theme]
    except Exception as e:
        return JSONResponse(content={"memes_url":e},status_code=400)


@router.post("/images") # dependencies=[Depends(JWTBearer())]
async def image_prompt(query: SummarizerInput): # dependencies=[Depends(JWTBearer())]
    try:
        summary=history_manager.get_history("summary")[0]
        image_history= str(history_manager.get_history("image_history")[:3])
        image_generation_prompt=f"""You are an expert in crafting prompts to generate images using large language models based on given news summary, user's current input and user's conversation history.
                                   Your task is to craft a detailed prompt to generate an image which will be used for social media networking and content marketing. 
                                   
News Summary: ```{summary}```

Craft the prompt for image generation, strictly following these guidelines:
1. The prompt must be clear and detailed for the LLM to generate relevant images.
2. Use a tone that matches the news summary (e.g., political, emotional, empathetic, funny, etc.).
3. The prompt must clearly communicate the key information.
4. The generated prompt must include the details about image background, colors, gradient, view, etc.
5. The generated prompt MUST NOT include any thing which can result in profanity in the image.
6. The generated prompt must be concise and short (maximum 100 words)

MAKE SURE TO INCORPORATE THE CHANGES/ FEEDBACK BASED ON THE USER'S CONVERSATION HISTORY GIVEN BELOW:
User Conversation history: {image_history}

current user input: ```{query}```

Final output must be just the generated prompt without any tags or header:

"""
        image_prompt_generated= await gorq_call(image_generation_prompt)
        try:
            prompt = image_prompt_generated
            # prompt = eval(image_prompt_generated[image_prompt_generated.find("{"):image_prompt_generated.rfind("}")+1])
        except:
            prompt = eval(image_prompt_generated[image_prompt_generated.find("{"):image_prompt_generated.rfind("}")+1])
            prompt = prompt['prompt']
        print("************\n", prompt)
        output = generate_image_using_prompt(prompt=prompt)
        print("|||||||||||||||||\n", output)
        image_url = []
        for i in output:
            image_url.append(str(i))
        print(image_url)
        history_manager.add_entry("image_history", {"user": query, "assistant": prompt})
        
        return JSONResponse(content={"image_post":image_url},status_code=200)
    except Exception as e:
        return JSONResponse(content={"image_post":e},status_code=400)

