from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.0.199", 9559)
tts.say("Hello, world!")
