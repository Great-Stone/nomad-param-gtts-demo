from gtts import gTTS

def create_voice_from_file(text_file, output_file):
    # Open and read the text file
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Convert text to speech
    tts = gTTS(text, lang="ko")
    tts.save(output_file)

# Specify your text file and output file
text_file_path = '../alloc/conversation.txt'
output_file_path = '../alloc/output.mp3'

# Generate the voice file
create_voice_from_file(text_file_path, output_file_path)