import os

from dotenv import load_dotenv

from app.models.requests import TextTranslateRequest, UrlTranslateRequest
from app.services.pipeline import translate_text_pipeline, translate_url_pipeline


def main() -> None:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

    print("== Text translate ==")
    text_req = TextTranslateRequest(text="I know you're somewhere out there, somewhere far away")
    text_res = translate_text_pipeline(text_req)
    print(text_res.model_dump_json(indent=2))

    print("\n== URL translate ==")
    url_req = UrlTranslateRequest(url="https://dev.to/")
    url_res = translate_url_pipeline(url_req)
    print(url_res.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
