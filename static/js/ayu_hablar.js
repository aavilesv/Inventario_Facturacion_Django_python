
          function speaknow () {
            var speech = new SpeechSynthesisUtterance();
            speech.rate = .7;
            speech.pitch = -2;
            speech.volume = 7;
            speech.voice =speechSynthesis.getVoices()[0];
            speech.text = text.value;

            speechSynthesis.speak(speech);
          }
          speaknow();