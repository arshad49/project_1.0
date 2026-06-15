import google.generativeai as genai
# Configure the API key
genai.configure(api_key="api key")
# Initialize the GenerativeModel with the correct model name
model = genai.GenerativeModel("gemini-1.5-pro-latest")  
# def ask_gemini(prompt):
#     try:
#         # Check the correct method to generate text
#         response = model.generate(prompt)  # Adjust this line based on the correct method
#         print(response.text)  # Print the response for debugging
#         return response.text.strip()  # Adjust this line based on the response structure
#     except Exception as e:
#         print(f"Error communicating with Gemini: {e}")
#         return None

response = model.generate_content("What is the capital of France?")  # Example prompt
print(response.text)  # Print the response text
