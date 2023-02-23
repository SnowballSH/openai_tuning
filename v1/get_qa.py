import polars as pl
import openai

openai.organization = "org-Vfki9wAixkDQGPP3mkFNOYwC"
with open("secret.txt", "r") as f:
    openai.api_key = f.read().strip()

df = pl.read_csv("data.csv")

df = df.with_columns((pl.col("title") + "\n" + pl.col("section") +
                      "\n\n" + pl.col("content")).alias("context"))


def get_questions(context: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write 10 questions and answer the questions based on the text below, give your sentences in simplified Chinese 用中文回答. Make sure you answer your questions too.\n\nText: {context}\n\nYour questions and answers in 中文:\n1.",
            temperature=0,
            max_tokens=1023,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return ""


res = []

for ctx in df["context"]:
    q_a = get_questions(ctx)
    res.append(q_a)
    print(q_a)

print(res)
