"""Run once: python test_keys.py
Tests every key in .env individually, then lists the models the first working key can use."""
from google import genai

from llm import KEYS, MODEL


def main():
    print(f"Model: {MODEL} | {len(KEYS)} key(s) found\n")
    good_client = None

    for i, key in enumerate(KEYS, 1):
        tag = f"key {i} (...{key[-4:]})"
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=MODEL, contents="Reply with exactly one word: pong"
            )
            print(f"{tag}: OK -> {r.text.strip()}")
            good_client = good_client or client
        except Exception as e:
            print(f"{tag}: FAIL -> {str(e)[:200]}")

    if good_client:
        print("\nModels available to the first working key:")
        for m in good_client.models.list():
            print("  ", m.name)
    else:
        print("\nNo working keys. Check .env, or generate a fresh key in Google AI Studio.")


if __name__ == "__main__":
    main()
