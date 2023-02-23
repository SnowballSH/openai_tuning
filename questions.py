import polars as pl
import openai

with open("secret.txt", "r") as f:
    openai.api_key = f.read().strip()


def get_questions(context: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"""你是一个普通的消费者。你想买洗发水和其他护理产品，但是选项太多了。你不知道哪个产品最适合你。请你问促销员二十个不同的关于洗发水的问题，来决定哪个产品最好。
比如：
这个洗发水哪个味道好闻呀？
洗发水和护发素一定要同一个牌子一起使用吗？

请根据以上例子再写二十个不一样的问题。发挥你的想象力。你可以问哪一些型号或者味道更好，适合哪一些人群。你也可以让促销员给你推荐一些。
""",
            temperature=0.8,
            max_tokens=1023,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        return ""


print(get_questions(""))
