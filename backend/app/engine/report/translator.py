"""
Translation module for the LegiSim Report Writer.
"""
from typing import Any, Dict
from langchain_core.messages import SystemMessage, HumanMessage

from backend.app.engine.report.prompts import TRANSLATION_SYSTEM_PROMPT

LANGUAGE_MAP = {
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "or": "Odia"
}

async def translate_report(report: Dict[str, Any], target_language: str, llm: Any) -> Dict[str, Any]:
    """Translate report to target language."""
    if target_language not in LANGUAGE_MAP and target_language.lower() != "en":
        return report # Unsupported or English
        
    lang_name = LANGUAGE_MAP.get(target_language, target_language)
    
    system_prompt = TRANSLATION_SYSTEM_PROMPT.format(target_language=lang_name)
    
    translated_report = report.copy()
    
    if "sections" in translated_report:
        for section in translated_report["sections"]:
            # Translate content
            content = section.get("content_markdown", "")
            if content:
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=content)
                ]
                response = await llm.ainvoke(messages)
                section["content_markdown"] = response.content
                section["content"] = response.content
                
            # Translate title
            title = section.get("title", "")
            if title:
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=title)
                ]
                response = await llm.ainvoke(messages)
                section["title"] = response.content
                
    return translated_report
