from llm.model import get_llm

llm = get_llm()

response = llm.invoke(
    "Reply with exactly: Hello"
)

print(response)
print("CONTENT:")
print(response.content)