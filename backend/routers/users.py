from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from utility.auth_helper import create_access_token, encrypt_password, verify_password
from typing import Optional
from datetime import datetime, timedelta
from model import *
import bcrypt
from utility.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
import logging
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
@router.get("/summarizer") # dependencies=[Depends(JWTBearer())]
async def summarizer(query: SummarizerInput): # token: str =Depends(JWTBearer())
    try:
        summary=await get_news_summary(query)
        # print(summary)
        metadata=history_manager.get_history("xyz")[:5]
        # print(metadata)
        history_manager.add_entry("summary", summary)
        return JSONResponse(content={"summary":summary, "metadata":metadata},status_code=200)
    except Exception as e:
        return JSONResponse(content={"summary":e, "metadata":"Bad Request"},status_code=400)


@router.get("/text_post") # dependencies=[Depends(JWTBearer())]
async def text_post(query: SummarizerInput): # dependencies=[Depends(JWTBearer())]
    try:
        summary=history_manager.get_history("summary")[0]
        text_generation_prompt=f"""Your are the helpfull assistent. Use the provided news information, craft an engaging and shareable text post. 
Ensure the tone matches the context of the news—professional for formal news, empathetic for emotional news, or humorous for lighter stories. 
The post should clearly communicate the key information while being concise and attention-grabbing.

Here is the context: 
{summary}

Generate a text post suitable for social media. Follow these guidelines:
1. Summarize the key points in 2–3 sentences.
2. Use a tone that matches the news (e.g., formal, empathetic, or humorous).
3. Include a call-to-action or a closing statement to prompt engagement, like asking for opinions, sharing thoughts, or encouraging actions.
4. Use language that is relatable and resonates with the target audience.


Example:
User Input: Create a humorous post about AI replacing jobs for a Twitter audience.
Text Post: "AI's got jokes now? Next thing you know, it's taking over my stand-up gig. #AIvsHumans #TechTakeover"

User Input:{query}

final_response:
Text Post:
"""
        text_post= await gorq_call(text_generation_prompt)

        return JSONResponse(content={"text_post":text_post},status_code=200)
    except Exception as e:
        return JSONResponse(content={"text_post":"Bad Request"},status_code=400)


@router.get("/meme") # dependencies=[Depends(JWTBearer())]
async def meme(query: SummarizerInput): # token: str =Depends(JWTBearer())
    try:
        summary=history_manager.get_history("summary")[0]
        print(summary)
        meme_prompt=f"""You are tasked with creating a humorous or thought-provoking meme based on a given context. Your role involves analyzing the context for key themes or events, conceptualizing relatable and engaging memes, and providing clear visual and textual descriptions to generate the meme.


Here is the news context: 
{summary}

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

user interest:{query}

Final output should be in the following JSON format:
[{{"Theme":(write meme theme),
"sentiment":(write search query),
"Visual Description":(write prompt to generate the image),
"Caption":(meme captions)}}]
"""
        meme_post=await gorq_call(meme_prompt)
        memes=eval(meme_post[meme_post.find("["):meme_post.rfind("]")+1])
        memes_url=[]
        for m in range(3):
            temp_id=get_random_template(memes[m]["sentiment"])
            USERNAME = "your_imgflip_username"
            PASSWORD = "your_imgflip_password"
            # print(temp_id)
            meme_url=await generate_meme(temp_id,memes[m]['Caption'],USERNAME,PASSWORD)
            if meme_url:
                memes_url.append([meme_url,memes[m]["Theme"]])
            else:
                print("-------------------------------------------")
                print(temp_id)
                print("-------------------------------------------")
        return JSONResponse(content={"memes_url":memes_url},status_code=200) # [meme_url,theme]
    except Exception as e:
        return JSONResponse(content={"memes_url":e},status_code=400)


