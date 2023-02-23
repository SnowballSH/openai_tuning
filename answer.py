import polars as pl
import openai

with open("secret.txt", "r") as f:
    openai.api_key = f.read().strip()


def get_answers(context: str, questions: list) -> str:
    qs = [f"{i+1}. {q}" for i, q in enumerate(questions)]
    ret = []
    try:
        for i in range(0, len(questions), 5):
            s = "\n".join(qs[i:min(i+5, len(questions))])
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"""{context}
回答以下问题：
{s}
""",
                temperature=0.2,
                max_tokens=1023,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            k = response['choices'][0]['text']
            print(k)
            ret += k.split("\n")
        return ret
    except Exception as e:
        print(e)
        return ""


with open("questions.txt", "r") as f:
    data = f.read().strip().split("\n")
    res = get_answers("""
""", data)
    print(res)
