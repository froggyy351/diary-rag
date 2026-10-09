from google import genai

def main() -> None:
    """APIキーが通るか確かめ、埋め込みに使えるモデルを一覧する。"""
    client = genai.Client()
    for model in client.models.list():
        if "embedContent" in (model.supported_actions or []):
            print(model.name)

if __name__ == "__main__":
    main()
