# The openai format: 
# [
#   {
#     "messages": [
#       {
#         # "role": "system", 
#         "role": "developer", # 脑瘫oai又改api了, 原来是system
#         "content": "system prompt (optional)"
#       },
#       {
#         "role": "user",
#         "content": "human instruction"
#       },
#       {
#         "role": "assistant",
#         "content": "model response"
#       }
#     ]
#   }
# ]
# 
# gemini format: 
# message=[
#     {"role": "model", "parts": [model_completion]},
#     {"role": "user", "parts": [user_prompt]},
# ]

import os
import threading

# Define locks for each API key provider
google_api_key_lock = threading.Lock()
openai_api_key_lock = threading.Lock()
together_api_key_lock = threading.Lock()

def get_model_provider(model_name):
    """
    Determine the provider based on the model name.
    Returns a tuple of (provider, normalized_model_name)
    """
    google_models = [
        'gemini-2.0-flash', 'gemini-2.0-flash-lite',
        'gemini-2.5-pro', 'gemini-2.5-flash',
        'gemini-2.5-pro-preview-03-25', 'gemini-2.5-flash-preview-04-17'
    ]
    openai_models = ['gpt-4o', 'chatgpt-4o-latest', 'gpt-4o-2024-08-06', 
                     'gpt-4o-mini', 'gpt-4o-mini-2024-07-18', 
                     'gpt-4.1', 'gpt-4.1-mini', 'gpt-4.1-nano']
    
    together_models = ['llama3.1-8b', 'llama3.1-70b', 
                       'gemma2-27b', 'gemma2-9b',
                       'qwen2-72b', 'qwen2.5-72b', 'qwen2.5-7b']
    
    model_name = model_name.strip().lower()
    
    if model_name in google_models:
        provider = 'google'
        if model_name == 'gemini-2.5-pro':
            model_name = 'gemini-2.5-pro-preview-03-25'
        elif model_name == 'gemini-2.5-flash':
            model_name = 'gemini-2.5-flash-preview-04-17'
    elif model_name in openai_models:
        provider = 'openai'
    elif model_name in together_models:
        provider = 'together'
    else:
        return None, model_name
    
    return provider, model_name

def get_openai_api_key():
    with openai_api_key_lock:
        if 'OPENAI_API_KEY' not in os.environ:
            api_key = input('Please enter your OpenAI API key:')
            os.environ['OPENAI_API_KEY'] = api_key
        return os.environ['OPENAI_API_KEY']

def get_google_api_key():
    with google_api_key_lock:
        if 'GOOGLE_API_KEY' not in os.environ:
            api_key = input('Please enter your Gemini API key:')
            os.environ["GOOGLE_API_KEY"] = api_key
        return os.environ["GOOGLE_API_KEY"]

def get_together_api_key():
    with together_api_key_lock:
        if 'TOGETHER_API_KEY' not in os.environ:
            api_key = input('Please enter your Together API key:')
            os.environ["TOGETHER_API_KEY"] = api_key
        return os.environ["TOGETHER_API_KEY"]

def chat_complete(message, 
                  model_name='gemini-2.0-flash', # openai format
                  provider=None,
                  base_url=None,
                  max_tokens=512,
                  temperature=0.5,
                  n=1, # number of completions to generate
                  api_key=None,
                  ):
    """
    A wrapper function to call chat completion from different providers
    Args:
        message: message in openai format. It is a list of dictionaries with keys 'role' and 'content'. The 'role' can be 'system', 'user', or 'assistant'. The 'content' is the message content.
        model_name: the model name to use for chat completion. It can be a model name from openai, google, or together.
        provider: the provider to use for chat completion. If None, it will be inferred based on the model_name.
        max_tokens: the maximum number of tokens to generate.
        temperature: the temperature for sampling.
    """
    together_to_full_name = {'llama3.1-8b': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
                             'llama3.1-70b': 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo',
                             'gemma2-27b': 'google/gemma-2-27b-it',
                             'gemma2-9b': 'google/gemma-2-9b-it',
                             'qwen2-72b': 'Qwen/Qwen2-72B-Instruct',
                             'qwen2.5-72b': 'Qwen/Qwen2.5-72B-Instruct-Turbo',
                             'qwen2.5-7b': 'Qwen/Qwen2.5-7B-Instruct-Turbo'}
    
    # Determine provider if not specified
    if provider is None:
        provider, model_name = get_model_provider(model_name)
        if provider is None:
            raise ValueError('Please specify a valid provider or model name')
    
    if provider == 'openai':
        # Use provided API key or get from environment
        if api_key is None:
            api_key = get_openai_api_key()
            
        # Initialize the client with the determined key
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        chat_completion = client.chat.completions.create(
            model=model_name,
            messages=message,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n,
        )
        if n == 1:
            return chat_completion.choices[0].message.content
        else:
            return [choice.message.content for choice in chat_completion.choices]

    if provider == 'google':
        try:
            from google import genai
            from google.genai import types
        except:
            print ("Please install google-genai with: ")
            print ("pip install -q -U google-genai")
            return None

        # Use provided API key or get from environment
        if api_key is None:
            api_key = get_google_api_key()
            
        client = genai.Client(api_key=api_key)

        gemini_message = []
        system_prompt = None # Initialize system_prompt

        # Handle potential system prompt first
        if message and (message[0]['role'] == 'system' or message[0]['role'] == 'developer'):
            system_prompt = message[0]['content']
            message_turns = message[1:] # Process the rest of the messages
        else:
            message_turns = message # Process all messages if no system prompt

        for turn in message_turns:
            # Each item in the 'parts' list should be a 'Part' object (e.g., {"text": "..."})
            part = {"text": turn['content']} 
            if turn['role'] == 'user':
                gemini_message.append({"role": "user", "parts": [part]}) # Wrap Part object in list
            elif turn['role'] == 'assistant':
                gemini_message.append({"role": "model", "parts": [part]}) # Wrap Part object in list

        # Simplified API call logic
        config = types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
            ],
        )

        # Add system instruction to config if it exists
        if system_prompt:
            config.system_instruction = system_prompt
        
        if n > 1:
            config.candidate_count = n
        
        # Turn off thinking for 2.5 flash preview models
        # if model_name == 'gemini-2.5-pro-preview-03-25' or model_name == 'gemini-2.5-flash-preview-04-17':
        if model_name == 'gemini-2.5-flash-preview-04-17':
            config.thinking_config=types.ThinkingConfig(thinking_budget=0)

        response = client.models.generate_content(
            model=model_name,
            config=config,
            contents=gemini_message
        )
        if n == 1:
            return response.text
        else:
            return [candidate.content.parts[0].text for candidate in response.candidates]
    
    if provider == 'together':
        model_name = together_to_full_name[model_name]
        
        # Use provided API key or get from environment
        if api_key is None:
            api_key = get_together_api_key()
        
        try:
            from openai import OpenAI
        except:
            print ("Please install openai")
            print ("pip install openai")
            exit()
        client = OpenAI(
            api_key=api_key,
            base_url='https://api.together.xyz/v1'
        )

        chat_completion = client.chat.completions.create(
            model=model_name,
            messages=message,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n,
        )
        if n == 1:
            return chat_completion.choices[0].message.content
        else:
            return [choice.message.content for choice in chat_completion.choices]

    else:  
        raise NotImplementedError('Only Gemini API is supported for now')
        
def batch_chat_complete(messages, # openai format
                        model_name='gemini-2.0-flash', 
                        provider=None,
                        base_url=None,
                        max_tokens=512,
                        temperature=0.5,
                        concurrent_calls=10,
                        n=1,
                        api_key=None):

    # import exponential backoff decorator 
    from tenacity import retry, stop_after_attempt, wait_exponential, RetryError, retry_if_exception_type, retry_if_exception
    import requests.exceptions
    import openai  # For openai.APIStatusError
    from google.genai.errors import ClientError # Corrected import for Google GenAI errors

    # Determine provider if not specified to handle API key checks upfront
    if provider is None:
        provider, model_name = get_model_provider(model_name)
        if provider is None:
            raise ValueError('Please specify a valid provider or model name')
    
    # Pre-check for API keys before starting batch processing
    if api_key is None:
        if provider == 'openai':
            api_key = get_openai_api_key()
        elif provider == 'google':
            api_key = get_google_api_key()
        elif provider == 'together':
            api_key = get_together_api_key()

    def _should_retry_specific_errors(e):
        # Retry on general network issues
        if isinstance(e, requests.exceptions.RequestException):
            print (f"RequestException: {e}")
            return True
        # For OpenAI errors, retry only on 429 status code
        if isinstance(e, openai.APIStatusError):
            print (f"OpenAI APIStatusError: {e}")
            return getattr(e, 'status_code', None) == 429
        # For Google GenAI errors, retry only on ClientError with code 429
        if isinstance(e, ClientError): # ClientError from google.genai.errors
            print (f"Google GenAI ClientError: {e}")
            return getattr(e, 'code', None) == 429
        return False

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, exp_base=4, min=1, max=60),
        retry=retry_if_exception(_should_retry_specific_errors) # Use custom predicate
    )
    def call_chat_complete(message):
        return chat_complete(message, model_name=model_name, provider=provider, base_url=base_url, max_tokens=max_tokens, temperature=temperature, n=n, api_key=api_key)

    def func(message):
        try:
            response = call_chat_complete(message)
            # print (f"Got response for message: {message}, response: {response}")
            return response
        except RetryError as e:
            print(f"Failed to get response for RetryError for message: {message}")
            return str(e)
        except Exception as e:
            print(f"Failed to get response for message: {message}")
            print(e)
            return str(e)
    import concurrent.futures 
    from tqdm import tqdm
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_calls) as executor:
        results = list(tqdm(executor.map(func, messages), total=len(messages), desc="Processing messages"))
    
    pairs = list(zip(messages, results))
    return pairs

if __name__ == '__main__':
    print ("Testing chat_complete")
    message = [{"role": "user", "content": f"What is the capital of France?"}]
    # model_names = ['gemini-2.0-flash', 'gpt-4o-mini', 'qwen2.5-7b']
    model_names = ['gemini-2.0-flash', 'gpt-4o-mini']
    # model_names = ['gemini-2.5-pro-preview-03-25', 'gemini-2.5-flash-preview-04-17']
    # model_names = ['gpt-4.1-nano']
    # model_names = ['gemini-2.0-flash']
    # for model_name in model_names:
    #     print (f'Testing {model_name} model')
    #     response = chat_complete(message, model_name=model_name)
    #     print (response)
    #     print ('-'*20)

    
    messages = []
    for i in range(10):
        message = [{"role": "user", "content": f"hello, what is 10+{i}?"}]
        messages.append(message)
    
    for model_name in model_names:
        print ('-'*20)
        print (f"Testing batch_chat_complete with 10 messages and 3 concurrent calls for {model_name} model\n")
        responses = batch_chat_complete(messages, model_name=model_name, concurrent_calls=3)
        for i, response in enumerate(responses):
            print (f"Response {i}: {response}")
            print (f'response str: {response[1]}')
    
    people = ['girl', 'boy', 'man', 'woman', 'child']
    messages = []
    for person in people:
        message = [{"role": "user", "content": f"Give a {person}'s name. Only return the name, no other text."}]
        messages.append(message)
    for model_name in model_names:
        print ('-'*20)
        print (f"Testing batch_chat_complete with 5 messages with 5 responses for {model_name} model\n")
        responses = batch_chat_complete(messages[:5], model_name=model_name, concurrent_calls=5, n=5)
        for i, response in enumerate(responses):
            print (f"Response {i}: {response}")
            print ('response str list: [')
            for r in response[1]:
                print (f'    {r}')
            print (']')
    


