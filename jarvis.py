from RealtimeSTT import AudioToTextRecorder
import assist
import tools

if __name__ == '__main__':
    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", silero_sensitivity = 0.4)
    hot_words = ["jarvis"]
    skip_hot_word_check = False
    print("Say something...")
    assist.init()
    while True:
        current_text = recorder.text()
        print(current_text)
        if any(hot_word in current_text.lower() for hot_word in hot_words) or skip_hot_word_check:
                    if current_text:
                        print("User: " + current_text)
                        recorder.stop()
                        response = assist.ask_question_memory(current_text)
                        print(response)
                        speech = response.split('#')[0]
                        done = assist.TTS(speech)
                        recorder.start()
                        skip_hot_word_check = True if "?" in response else False
                        if len(response.split('#')) > 1:
                            command_string = response.split('#')[1]
                            command_parts = command_string.split('-')
                            command = command_parts[0]
                            args = command_parts[1:]
                            response = tools.parse_command(command, *args)
