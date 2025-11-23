import google.generativeai as genai

genai.configure(api_key="AIzaSyDmtCOWtrcgdWBLgGGT-7CI7dKiPKnglgg")

models = genai.list_models()

for m in models:
    print(m.name)
