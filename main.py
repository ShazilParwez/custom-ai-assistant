import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_response(user_query):
    """
    Generate a response for any user query using Groq's API,
    with no hard-coding of topics.
    """

    # System message that instructs the model to answer any query
    system_message = (
        "You are a helpful assistant capable of answering questions on a wide range of topics, "
        "including programming, history, science, general knowledge, mathematics, education, and more. "
        "Provide clear, concise, and accurate answers to any question the user asks."
    )

    # User message
    user_message = user_query

    # Create chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        model="mixtral-8x7b-32768"
    )

    return chat_completion.choices[0].message.content


# Example programming query
programming_query = "What is Backward propagation in Neural networks and how it works step by step?"
print("User:", programming_query)
print("AI:", generate_response(programming_query))


def interactive_chat():
    """
    Start an interactive chat session where the user can ask questions.
    """

    print("Welcome! You can ask any question, and I will provide the answer.")
    print("Type 'exit' to end the conversation.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Exiting the chat...")
            break

        response = generate_response(user_input)
        print(f"AI: {response}")


# -------------------------
# MEMORY CHAT SYSTEM
# -------------------------

conversation_history = [
    {
        "role": "system",
        "content":
        "You are a highly capable and helpful assistant, trained to answer a wide variety of questions on various topics. "
        "Your main goal is to assist users by providing clear, concise, and accurate answers. "
        "When responding to a user's query, keep your answers short, focused, and easy to understand, without unnecessary details. "
        "Only provide more detailed explanations if the user specifically requests more information (e.g., 'explain in more detail', 'elaborate'). "
        "If the user is asking a complex question, break down your response into manageable chunks and provide step-by-step explanations where needed. "
        "Be polite and encouraging, and make sure to provide accurate information at all times. "
        "You should also remember all previous exchanges in the conversation and use that information to provide better context and relevant responses."
    }
]


def generate_response_with_memory(user_query):
    """
    Generate a response while remembering previous conversation history.
    """

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_query
    })

    # Create chat completion
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="mixtral-8x7b-32768"
    )

    ai_response = chat_completion.choices[0].message.content

    # Add AI response to history
    conversation_history.append({
        "role": "assistant",
        "content": ai_response
    })

    return ai_response


def interactive_chat_with_memory():
    """
    Start an interactive chat session where the model remembers conversation history.
    """

    print("Welcome! You can ask any question, and I will provide the answer.")
    print("I remember everything you ask!")
    print("Type 'exit' to end the conversation.\n")

    while True:

        print("")
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Exiting the chat...")
            break

        response = generate_response_with_memory(user_input)
        print(f"AI: {response}")


# Start the interactive chat with memory
interactive_chat_with_memory()