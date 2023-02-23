import polars as pl

outputs = []

with open("ans.txt", "r") as f:
    txt = f.read()
    sections = txt.split("\n\n")
    for section in sections:
        qa = [q.strip() for q in section.split("\n") if q.strip()]
        for i in range(0, len(qa), 2):
            outputs.append((qa[i][3:], qa[i+1][2:]))

df = pl.DataFrame(outputs, schema=["prompt", "completion"])
df.write_csv("qa.csv")
