import json
import re

def parse_llm_json(text):
    try:
        return json.loads(text)

    except json.JSONDecodeError as e:
        # Remove ```json
        text = re.sub(r"^```(?:json)?", "", text)

        # Remove ending ```
        text = re.sub(r"```$", "", text)

        print("FIRST ERROR:", e)

        fixed = re.sub(
            r'\\(?!["\\/bfnrtu])',
            r'\\\\',
            text
        )

        print("\nORIGINAL AROUND ERROR:")
        pos = e.pos
        print(repr(text[pos-30:pos+30]))

        print("\nFIXED AROUND ERROR:")
        print(repr(fixed[pos-30:pos+30]))

        try:
            return json.loads(fixed)

        except json.JSONDecodeError as e2:
            print("\nSECOND ERROR:", e2)
            raise