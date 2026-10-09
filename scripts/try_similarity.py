import math

from google import genai

MODEL = "gemini-embedding-001"

SENTENCES = [
    "今日は悩んだ",
    "今日は悩んでん",
    "今日は悩んだんですよね～",
    "I was worried today",
    "Oggi ero preoccupato",
    "天気がよかった",
    "Hola!",
]

def cosine(a: list[float], b: list[float]) -> float:
    """2つのベクトルの向きの近さを-1~1 で返す。"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

def main() -> None:
    """文章を埋め込みに変換し、１つ目の文章と他の文章の近さを比べる。"""
    client = genai.Client()
    result = client.models.embed_content(model=MODEL, contents=SENTENCES)
    vectors = [e.values for e in result.embeddings]
    
    print(f"次元数： {len(vectors[0])}")
    print(f"先頭５個： {vectors[0][:5]}")
    print()
    base = SENTENCES[0]
    for sentence, vector in zip(SENTENCES[1:], vectors[1:]):
        print(f"{cosine(vectors[0], vector):.3f} 「{base}」と「{sentence}」")

if __name__ == "__main__":
    main()
