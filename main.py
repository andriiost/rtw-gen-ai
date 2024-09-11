from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[{"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello GPT-4!"}],
  temperature=1,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  response_format={
    "type": "text"
  }
)
print(response.choices[0].message.content)

