from fastapi import FastAPI, Request,HTTPException,status,Depends,Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union
from llm_handler import analyze_cultural_personality
from cultural_profiles import CULTURE_PROFILES
import json
import random
import requests
from schemas import SignUpSchema, LoginSchema
from fastapi.responses import JSONResponse
from config import firebaseConfig,SERVICE_ACCOUNT

from oauth2 import get_current_user


app = FastAPI(
    title= "Jhalak",
    description= "It is a web server that is made for predicting cultural profile",
    version= "1.0.0"
)

# Allow requests from frontend (localhost or your Vercel/Netlify domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jhalak-cultural-personality.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import firebase_admin
from firebase_admin import credentials,auth

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)


# Load the question bank once
with open("questions.json","r") as f:
    QUESTION_BANK = json.load(f)

# Pydantic model for incoming quiz data
class Answer(BaseModel):
    id: str
    value : Union[str,float]    # string for MCQ, float (0–1) for sliders


class QuizSubmission(BaseModel): 
    answers : list[Answer]

@app.post("/signup")
async def create_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email = email,
            password = password
        )
        return JSONResponse(content={
            "message": f"account created successfully for user {user.uid}"},
            status_code= status.HTTP_201_CREATED )
    except auth.EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail=f"Account already created for email {user_data.email}")
    
@app.post("/login")
async def create_access_token(user_data : LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        # Use Firebase REST API for sign-in
        api_key = firebaseConfig['apiKey']
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Invalid credentials"
            )
        user = resp.json()
        token = user['idToken']
        return JSONResponse(content={
            "message": f"Login successful from {email}",
            "token": token,
            "user": user
            },
            status_code=status.HTTP_202_ACCEPTED
        ) 
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f"Login failed: {str(e)}"
        )


# FIXED: Better ping endpoint using the existing get_current_user dependency
@app.post("/ping")
async def validate_token(user = Depends(get_current_user)):
    """
    Validate the JWT token and return user info
    """
    return {
        "message": "Token is valid",
        "user_id": user['user_id'],
        "email": user.get('email', 'N/A')
    }


@app.get("/get-quiz")
async def get_quiz(user = Depends(get_current_user)):
    num_questions = 15
    categories = list(QUESTION_BANK.keys())

    questions_per_cat = num_questions // len(categories)
    
    selected_questions = []

    for category in categories:
        category_questions = QUESTION_BANK[category]
        selected_questions.extend(random.sample(category_questions, questions_per_cat))
    random.shuffle(selected_questions)
    return {
        "questions": selected_questions
    }

@app.post("/submit-quiz")
async def submit_quiz(submission: QuizSubmission,user = Depends(get_current_user)):
    if len(submission.answers) != 15:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Please answer all questions before submitting."
        )
    answer_dicts = [a.model_dump() for a in submission.answers]
    llm_result = analyze_cultural_personality(submission.answers)
    if "cultural_match" in llm_result:
        culture_key = llm_result["cultural_match"]
        cultural_profile_name = CULTURE_PROFILES.get(culture_key, {})

        extra_data_from_file = {
            "facts" : cultural_profile_name.get("facts",[]),
            "core_traits" : cultural_profile_name.get("core_traits",[]),
            "motifs" : cultural_profile_name.get("visual_theme",{}).get("motifs",[]),
        }
        result =  {**llm_result, **extra_data_from_file}
        return result
    else:   
        return llm_result


@app.get("/")
async def root():
    return {"message": "API running successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
