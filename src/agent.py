from typing import Dict, List, Any, Optional, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage  # noqa
from pydantic import BaseModel, Field, field_validator, ConfigDict
from duckduckgo_search import DDGS
import os
import json  # noqa
from rich.pretty import pprint
from src.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()


class AssistantResponse(BaseModel):
    """Structured response from the assistant."""

    intent_category: Literal["dining", "travel", "gifting", "cab booking", "other"] = (
        Field(description="The category of the user's intent")
    )
    entities: Optional[Dict[str, Any]] = Field(
        description="Key entities extracted from the user request (date, time, location, cuisine, party_size, budget, etc.)",
    )
    confidence_score: float = Field(
        description="Confidence score between 0 and 1 indicating how confident the model is in categorizing the user query into the specified intent category",
        ge=0.0,
        le=1.0,
    )
    follow_up_questions: List[str] = Field(
        description="list of follow up questions to ask when information provided via the user query is missing or ambiguous",
        default=[],
    )
    web_search_results: Optional[List[Dict[str, str]]] = Field(
        description="Web search results for non-standard categories i.e. when intent category is 'other'",
        default=None,
    )
    model_config = ConfigDict(extra="allow")

    @field_validator("confidence_score")
    @classmethod
    def check_confidence_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Confidence score must be between 0 and 1")
        return v


class PersonalAssistant:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agent with OpenAI API key."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=self.api_key)
        self.structured_llm = self.llm.with_structured_output(
            AssistantResponse, include_raw=True, method="function_calling"
        )
        self.standard_categories = ["dining", "travel", "gifting", "cab booking"]

    def process_query(self, user_input: str) -> Dict[str, Any]:
        """Process the user query and return a structured JSON response string."""
        messages = [
            AIMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=f"Analyze this user query and return a structured JSON response : {user_input}"
            ),
        ]
        response = self.structured_llm.invoke(messages)
        pprint(response)
        result = response.get("parsed", response.get("raw", {}).tool_calls[0]["args"])
        # handle non-standard intent categories
        if isinstance(result, AssistantResponse):
            result = result.model_dump()
        if isinstance(result, dict):
            if result["intent_category"] == "other":
                web_search_results = self._perform_web_search(user_input)
                result["web_search_results"] = web_search_results

        return result

    def _perform_web_search(
        self, query: str, num_results: int = 5
    ) -> List[Dict[str, str]]:
        """Perform web search for non-standard queries."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=num_results))

            formatted_results = []
            for result in results:
                formatted_results.append(
                    {
                        "title": result.get("title", ""),
                        "link": result.get("href", ""),
                        "snippet": result.get("body", ""),
                    }
                )

            return formatted_results
        except Exception as e:
            print(f"Web search error: {e}")
            return [
                {
                    "title": "Search error",
                    "link": "",
                    "snippet": "Unable to perform web search.",
                }
            ]


if __name__ == "__main__":
    # Example usage
    assistant = PersonalAssistant()
    user_query = "I need a gift for my mom's birthday under $100"
    response = assistant.process_query(user_query)
    print(json.dumps(response, indent=2, ensure_ascii=False))
