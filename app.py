import chainlit as cl
from src.agent import PersonalAssistant
from src.utils import format_json_response
import os  # noqa

agent = PersonalAssistant()


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    await cl.Message(
        content="👋 Hello! I'm your personal assistant. I can understand fuzzy requests like 'Need a sunset-view table for two tonight; gluten-free menu a must' and convert them into structured information.",
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Process incoming messages."""
    user_input = message.content

    with cl.Step("Processing your request...") as step:
        response = agent.process_query(user_input)

        formatted_response = format_json_response(response)

        response_message = f"```json\n{formatted_response}\n```"

        if (
            response.get("follow_up_questions")
            and len(response["follow_up_questions"]) > 0
        ):
            response_message += "\n\n**Follow-up questions:**\n"
            for i, question in enumerate(response["follow_up_questions"], 1):
                response_message += f"{i}. {question}\n"

        if (
            response.get("web_search_results")
            and len(response["web_search_results"]) > 0
        ):
            response_message += "\n\n**Web search results:**\n"
            for i, result in enumerate(response["web_search_results"], 1):
                response_message += f"{i}. [{result['title']}]({result['link']})\n   {result['snippet']}\n\n"

        step.output = response_message

    await cl.Message(content=response_message).send()


if __name__ == "__main__":
    pass
