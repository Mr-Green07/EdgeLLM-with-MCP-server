# from openai import OpenAI
# import os
# import sys

# _USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
# _REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
# _RESET_COLOR = "\033[0m" if _USE_COLOR else ""

# client = OpenAI(
#   base_url = "https://integrate.api.nvidia.com/v1",
#   api_key = "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"
# )


# completion = client.chat.completions.create(
#   model="z-ai/glm-5.2",
#   messages=[{"role":"user","content":""}],
#   temperature=1,
#   top_p=1,
#   max_tokens=16384,
#   seed=42,
#   extra_body={"chat_template_kwargs":{"enable_thinking":True,"clear_thinking":False}},
#   stream=True
# )

# for chunk in completion:
#   if not getattr(chunk, "choices", None):
#     continue
#   if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
#     continue
#   delta = chunk.choices[0].delta
#   reasoning = getattr(delta, "reasoning_content", None)
#   if reasoning:
#     print(f"{_REASONING_COLOR}{reasoning}{_RESET_COLOR}", end="")
#   if getattr(delta, "content", None) is not None:
#     print(delta.content, end="")



# import os
# from openai import OpenAI

# client = OpenAI(
#     base_url="https://router.huggingface.co/v1",
#     api_key=os.environ["HF_TOKEN"],
# )

# completion = client.chat.completions.create(
#     model="zai-org/GLM-5.2:together",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the capital of France?"
#         }
#     ],
# )

# print(completion.choices[0].message)

<<<<<<< HEAD
# print(completion.choices[0].message)
=======

# import random
# from src.response_generation import PROMPT_SAMPLES, get_prompt   # (you can create a tiny loader similar to `get_prompt`)

# sample = random.choice(PROMPT_SAMPLES["question"])
# # response = llm.generate(system_prompt=get_prompt("question"), user_input=sample)
# print(sample)


# import wave
# from piper import PiperVoice

# voice = PiperVoice.load("./offline_models/en_US-hfc_female-medium.onnx")
# with wave.open("test.wav", "wb") as wav_file:
#     voice.synthesize_wav("Welcome to the world of speech synthesis!", wav_file)
>>>>>>> 1bb33cbb1dcf5e9fd02dab74389d493abeaf5bc3
