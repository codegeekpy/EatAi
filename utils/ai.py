from transformers import pipeline

def generate_recipe(prompt):
    generator = pipeline('text-generation', model='gpt2')
    return generator(
        f"Generate a detailed Indian recipe for: {prompt}\n\nRecipe:",
        max_length=500,
        temperature=0.7
    )[0]['generated_text']