from openai import OpenAI
import time
from pygame import mixer
import os
import json

#https://platform.openai.com/playground/assistants
# Initialize the client and mixer
client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"})
mixer.init()

assistant_id = os.getenv('ASSISTANT_ID')


# Retrieve the assistant and thread
assistant = client.beta.assistants.retrieve(assistant_id)
def init():
    global thread
    thread = client.beta.threads.create()
    print(thread)


def ask_question_memory(question):
    client.beta.threads.messages.create(thread.id, role="user", content=question)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    
    while (run_status := client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)).status != 'completed':
        if run_status.status == 'failed':
            return "The run failed."
        from openai import OpenAI
        import time
        from pygame import mixer
        import os
        import json

        # https://platform.openai.com/playground/assistants
        # Initialize the client and mixer
        client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"})
        mixer.init()

        assistant_id = os.getenv('ASSISTANT_ID')

        # Retrieve the assistant and thread
        assistant = client.beta.assistants.retrieve(assistant_id)

        def init():
            global thread
            thread = client.beta.threads.create()
            print(thread)

        def ask_question_memory(question):
            client.beta.threads.messages.create(thread.id, role="user", content=question)
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

            while (
            run_status := client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)).status != 'completed':
                if run_status.status == 'failed':
                    return "The run failed."
                if run_status.status == 'requires_action':
                    print("Requires Action")
                    required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                    print(required_actions)
                    tools_output = []
                    for action in required_actions["tool_calls"]:
                        func_name = action["function"]["name"]
                        arguments = json.loads(action["function"]["arguments"])
                        if func_name == "get_stock_price":
                            output = 80
                            tools_output.append({
                                "tool_call_id": action["id"],
                                "output": str(output)
                            })
                        else:
                            print("Function not found")
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tools_output
                    )
                time.sleep(1)

            messages = client.beta.threads.messages.list(thread_id=thread.id)
            return messages.data[0].content[0].text.value

        def generate_tts(sentence, speech_file_path):
            response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
            response.stream_to_file(speech_file_path)
            return str(speech_file_path)

        def play_sound(file_path):
            mixer.music.load(file_path)
            mixer.music.play()

        def TTS(text):
            speech_file_path = generate_tts(text, "speech.mp3")
            play_sound(speech_file_path)
            while mixer.music.get_busy():
                time.sleep(1)
            mixer.music.unload()
            os.remove(speech_file_path)
            return "done"

        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

def generate_tts(sentence, speech_file_path):
    response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"
