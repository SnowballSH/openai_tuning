import polars as pl
from transformers import GPT2TokenizerFast

import re

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))


def reduce_long(
    long_text: str, long_text_tokens: bool = False, max_len: int = 590
) -> str:
    while count_tokens(long_text) > max_len:
        long_text = long_text[:long_text.rfind("。") + 1]

    return long_text


def extract_sections(
    wiki_text: str,
    title: str,
    max_len: int = 1800,
) -> str:
    if len(wiki_text) == 0:
        return []

    # find all headings and the coresponding contents
    headings = re.findall("!.*!", wiki_text)
    for heading in headings:
        wiki_text = wiki_text.replace(heading, "!--!")
    contents = wiki_text.split("!--!")
    contents = [c.strip() for c in contents]
    assert len(headings) == len(contents) - 1

    cont = contents.pop(0).strip()
    outputs = [(title, "Summary", cont, count_tokens(cont)+4)]

    max_level = 100
    keep_group_level = max_level
    remove_group_level = max_level
    nheadings, ncontents = [], []
    for heading, content in zip(headings, contents):
        plain_heading = " ".join(heading.split(" ")[1:-1])
        num_equals = len(heading.split(" ")[0])
        if num_equals <= keep_group_level:
            keep_group_level = max_level

        if num_equals > remove_group_level:
            if (
                num_equals <= keep_group_level
            ):
                continue
        keep_group_level = max_level
        nheadings.append(heading.replace("!", "").strip())
        ncontents.append(content)
        remove_group_level = max_level

    # count the tokens of each section
    ncontent_ntokens = [
        count_tokens(c)
        + 3
        + count_tokens(" ".join(h.split(" ")[1:-1]))
        - (1 if len(c) == 0 else 0)
        for h, c in zip(nheadings, ncontents)
    ]

    # Create a tuple of (title, section_name, content, number of tokens)
    outputs += [(title, h, c, t) if t < max_len
                else (title, h, reduce_long(c, max_len), count_tokens(reduce_long(c, max_len)))
                for h, c, t in zip(nheadings, ncontents, ncontent_ntokens)]

    return outputs


with open("data.txt", "r") as f:
    data = f.read()
    s = extract_sections(data, "海飞丝")
    df = pl.DataFrame(s, schema=["title", "section", "content", "tokens"])
    df = df.filter(pl.col("tokens") > 40)
    print(df.head())
    df.write_csv("data.csv")
