from collections.abc import Iterator
import itertools
import groq
from groq import Groq  



clients = [Groq(api_key=k) for k in GROQ_API_KEYS]
client_iterator = itertools.cycle(clients) #Round robin sulle chiavi
MODEL_NAME = "openai/gpt-oss-120b"

def call_Groq(user_prompt: str, lvl: str, sys_prompt: str, model_name: str) -> tuple[str|None, int|None]:
    max_attempts = len(clients)
    for attempt in range(max_attempts):
        client = next(client_iterator)


        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    #two roles "user" and "developer", because "system" is actually a "developer" role. The real system prompt for an Harmony format has higher priority but only metadata.
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2, #to have less variance
                max_completion_tokens=16384, #partivo da 4192
                reasoning_effort=lvl,
                reasoning_format="parsed" #parsed	Separates reasoning into a dedicated message.reasoning field while keeping the response concise.
                                        #raw	Includes reasoning within <think> tags in the main text content.
                                        #hidden	Returns only the final answer.
            )


            #DEPRECATED
            #reasoning_tokens = completion.usage.completion_tokens_details.reasoning_tokens
            raw_content = completion.choices[0].message.content

            finish_reason = completion.choices[0].finish_reason #used for debug

            usage = completion.usage
            details = getattr(usage, "completion_tokens_details", None)
            reasoning_tokens = getattr(details, "reasoning_tokens", None) if details else None
 
            if finish_reason == "length" or not raw_content:
                print(f"[{attempt + 1}/{max_attempts}] truncated/empty "
                      f"(retrying...")
                continue
 
            return raw_content, reasoning_tokens
 
        except groq.RateLimitError as e:
            print(f"[{attempt + 1}/{max_attempts}] key rate-limited, rotating to next key")
            last_error = e
            continue
 
        except groq.APIStatusError as e:
            print(f"API Error({e.status_code}): {e}")
            return None, None
 
        except groq.APIConnectionError as e:
            print(f"[{attempt + 1}/{max_attempts}] connection error, retrying: {e}")
            last_error = e
            continue
 
    print(f"Final attempt failed. Last error: {last_error}")
    return None, None


