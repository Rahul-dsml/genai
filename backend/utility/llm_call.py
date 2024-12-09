import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

async def gorq_call(prompt, model_id="llama-3.2-90b-vision-preview"):
    """
    Makes an asynchronous call to the Groq API to generate a completion based on the provided prompt.

    Args:
        prompt (str): The text input for the model to generate a response.
        model_id (str, optional): The model ID to be used for the request. Defaults to "llama-3.2-90b-vision-preview".

    Returns:
        str: The content of the generated response from the model.

    Raises:
        KeyError: If the environment variable "GROQ_API_KEY" is not set.
        Exception: For other API-related issues or errors.
    """
    # Retrieve the API key from environment variables
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise KeyError("The GROQ_API_KEY environment variable is not set.")

    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)

    # Make the API call to generate a completion
    completion = client.chat.completions.create(
        model=model_id,  # Specify the model ID
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",  # Specify the type of content as text
                        "text": prompt  # Include the user-provided prompt
                    }
                ]
            }
        ],
        temperature=0.5,  # Control the randomness of the output
        max_tokens=1024,  # Limit the response length
        top_p=1,  # Use nucleus sampling with a probability of 1 (greedy decoding)
        stream=False,  # Disable streaming of response
        stop=None  # Do not specify any stopping sequences
    )

    # Return the generated content from the completion
    return completion.choices[0].message.content
