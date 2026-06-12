from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import re


# ======================================================
# LLM
# ======================================================

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2
    )


# ======================================================
# CLEAN TRANSCRIPT
# ======================================================

def clean_transcript(text):

    text = re.sub(r"\s+", " ", text)

    text = re.sub(
        r"(subscribe|like and share|share this video|thank you for watching|follow me)",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ======================================================
# SUMMARY
# ======================================================

def summarize(transcript):

    transcript = clean_transcript(transcript)

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert content summarizer.

Analyze the transcript and create a clean professional summary.

Rules:

- Ignore advertisements and promotions.
- Ignore repeated information.
- Ignore greetings and outro messages.
- Do not mention transcript chunks.
- Do not mention speaker actions.
- Keep only useful information.
- Write concise bullet points.
- Use professional language.

Return response exactly in this format:

# Overview

Write 2-3 sentences explaining the main topic.

# Key Points

- Point 1
- Point 2
- Point 3
- Point 4

# Important Details

- Detail 1
- Detail 2
- Detail 3

# Conclusion

Write a short conclusion.
"""
        ),
        ("human", "{text}")
    ])

    chain = (
        prompt
        | get_llm()
        | StrOutputParser()
    )

    return chain.invoke({
        "text": transcript[:15000]
    })


# ======================================================
# TITLE
# ======================================================

def generate_title(transcript):

    transcript = clean_transcript(transcript)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
Generate a professional title.

Rules:

- Maximum 6 words
- No quotes
- No hashtags
- No clickbait
- No punctuation
- Return title only
"""
        ),
        ("human", "{text}")
    ])

    chain = (
        prompt
        | get_llm()
        | StrOutputParser()
    )

    return chain.invoke({
        "text": transcript[:2000]
    }).strip()