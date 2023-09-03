import gradio as gr

def chatbot(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi there! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a chatbot, but I'm here and ready to assist!"
    elif "what's your name" in user_input:
        return "You can call me ChatBot. What's your name?"
    elif "my name is" in user_input:
        user_name = user_input.replace("my name is", "").strip()
        return f"Nice to meet you, {user_name}!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't quite understand. Can you tell me more?"

inputs = gr.inputs.Textbox(lines=2, placeholder="Type your message here...")
outputs = gr.outputs.Textbox()
gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs).launch()
