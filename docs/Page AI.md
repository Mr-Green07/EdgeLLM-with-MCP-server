# Page AI

## *Major Small Components*

WAKE WORD DETECTION

* detects user input i.e.("Hey, Page")
* use picovoice/porcupine(PyAudio, PortAudio)

AUTOMATIC SPEECH RECOGNITION (ASR)

* convert speech input to text input
* use open AI whisper model to convert speech to text

NATURAL LANGUAGE UNDERSTANDING (NLU)

* parse text to extract user intent of input
* use Rasa NLU + custom intent matcher
* returns structured JSON with confidence scores

TASK EXECUTION ENGINE

* Execute actions based on parsed intent
* uses Custom Python handler + Device APIs
* in this direct OS/Device funciton calls 

RESPONSE GENERATION
* template based response + Optional Local LLM 
* use Rasa responses and Gemma3:4b as a LLM
* Rasa Delivers Natural Sounding text 
* where as, Gemma generate response text 
TEXT-TO-SPEECH (TTS)
* convert response from text to speech(TTS) as natural Sounding audio
* Coqui TTS(open source TTS engine)

AUDIO INPUT/OUTPUT MANAGER
* Handle microphone and speaker cleanly
* uses PyAudio/Port audio to process and handle ouput and input device

STATE MACHINE \& ORCHESTRATION
* Coordinate all components in correct sequence
* State Flow: -> IDLE -> LISTENING(wake word)-> RECORDING (CAPTURING SPEECH) -> PROCESSING -> RESPONDING (TTS PLAYBACK) -> IDLE
LOCAL STORAGE \& LEARNING
* Store user data, preferences, conversation history
* SQLite
