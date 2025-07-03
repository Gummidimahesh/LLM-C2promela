from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt(code):
    with open("prompts/prompt_template.txt", "r") as f:
        template = f.read()
    return template.replace("{code}", code)

def convert_c_to_promela(code):
    prompt = load_prompt(code)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()

def main(input_path, output_path):
    with open(input_path, "r") as f:
        c_code = f.read()

    promela_code = convert_c_to_promela(c_code)

    with open(output_path, "w") as f:
        f.write(promela_code)

    print(f"✅ Promela code written to {output_path}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python convert.py <input.c> <output.pml>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
