# Voice Module Integration Setup Guide

## Overview
The voice module has been successfully integrated into your BhashaSetu application. It provides:
- **Speech-to-Text**: Convert audio to text with support for 10+ languages
- **Text-to-Speech**: Convert text to speech with both offline and online modes
- **REST API Endpoints**: Full FastAPI integration for voice operations

## Quick Start

### Step 1: Install Voice Module Dependencies
Run this command in your project root directory:

```bash
pip install -r speach_module/requirements.txt
```

**Dependencies installed:**
- `SpeechRecognition==3.10.0` - Speech recognition engine
- `pydub==0.25.1` - Audio processing
- `pyaudio==0.2.13` - Audio input/output
- `pyttsx3==2.90` - Offline text-to-speech
- `google-cloud-texttospeech==2.14.1` - Online TTS (optional)
- `librosa==0.10.0` - Audio analysis
- `fastapi>=0.104.0` - Already installed
- `pydantic>=2.0.0` - Already installed
- `python-dotenv` - Environment configuration

**Note**: On macOS/Linux, PyAudio might require system-level portaudio:
```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Step 2: (Optional) Configure Environment Variables
Create or update your `.env` file:

```env
# Voice Module Configuration (all optional)
VOICE_LANGUAGE=en                    # Default language (en, hi, mr, fr, es, de, pt, ru, ja, zh)
USE_OFFLINE_TTS=true                 # Use offline pyttsx3 (true) or Google Cloud TTS (false)
VOICE_SAMPLE_RATE=16000              # Audio sample rate in Hz
VOICE_CHANNELS=1                     # Audio channels (1 for mono, 2 for stereo)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json  # Only needed if using online TTS
```

### Step 3: Start Backend Server
```bash
cd "Backend API INT"
python main.py
```

You should see in logs:
```
Voice module loaded successfully
```

### Step 4: Verify Voice Module is Running
Open browser or API client and check:
```
http://localhost:8000/api/voice/health
```

Expected response:
```json
{
  "status": "healthy",
  "voice_service": "available",
  "version": "1.0.0"
}
```

## Available Voice Endpoints

### 1. Get Supported Languages
```bash
curl http://localhost:8000/api/voice/languages
```
Returns list of 10 supported languages with codes

### 2. Convert Speech to Text
```bash
curl -X POST http://localhost:8000/api/voice/recognize-command \
  -F "file=@audio.wav" \
  -F "language=en"
```

**Response:**
```json
{
  "success": true,
  "text": "What is machine learning",
  "confidence": 0.95,
  "language": "en",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 3. Convert Text to Speech
```bash
curl -X POST http://localhost:8000/api/voice/generate-answer \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning is a subset of artificial intelligence",
    "language": "en",
    "save_audio": true
  }'
```

**Response:**
```json
{
  "success": true,
  "audio_file": "voice_responses/response_abc123.mp3",
  "method": "offline",
  "timestamp": "2024-01-15T10:30:05"
}
```

### 4. Complete Voice Interaction
```bash
curl -X POST http://localhost:8000/api/voice/process-interaction \
  -F "audio_file=@question.wav" \
  -F "language=en" \
  -F "response_text=Here is the answer to your question" \
  -F "generate_audio=true"
```

### 5. Set Language
```bash
curl -X POST http://localhost:8000/api/voice/set-language \
  -H "Content-Type: application/json" \
  -d '{"language": "hi"}'
```

## Integration Points in Your Code

### Using Voice Service Directly
```python
from speach_module.voice_service import VoiceService

# Initialize voice service
voice_service = VoiceService(language="en", use_offline=True)

# Speech to text
result = voice_service.speech_to_text("command.wav")
print(f"User said: {result['text']}")

# Text to speech
result = voice_service.text_to_speech("Hello, how can I help?", "response.mp3")
print(f"Audio saved to: {result['audio_file']}")
```

### Using REST API from Frontend
```javascript
// Speech Recognition
async function recognizeCommand(audioFile) {
  const formData = new FormData();
  formData.append('file', audioFile);
  formData.append('language', 'en');
  
  const response = await fetch('/api/voice/recognize-command', {
    method: 'POST',
    body: formData
  });
  return await response.json();
}

// Text to Speech
async function generateAnswer(text) {
  const response = await fetch('/api/voice/generate-answer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      text: text,
      language: 'en',
      save_audio: true
    })
  });
  return await response.json();
}
```

### In Chat Application
```python
from speach_module.voice_service import VoiceService
from api.routes import router  # Your existing routes

voice_service = VoiceService()

@router.post("/chat/voice")
async def voice_chat(user_audio: UploadFile):
    """Process voice input and respond with voice output"""
    
    # Step 1: Convert speech to text
    question = voice_service.speech_to_text(user_audio.filename)
    
    # Step 2: Process with RAG pipeline (existing code)
    answer = await process_with_rag(question['text'])
    
    # Step 3: Convert answer to speech
    audio_file = voice_service.text_to_speech(answer)
    
    return {
        "question": question['text'],
        "answer": answer,
        "audio": audio_file['audio_file']
    }
```

## Troubleshooting

### "Module not found: speach_module"
**Solution**: Run `pip install -r speach_module/requirements.txt`

### "No module named 'speech_recognition'"
**Solution**: Install dependencies:
```bash
pip install SpeechRecognition==3.10.0
```

### Audio input not working (PyAudio errors)
**Windows**: Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```bash
pip install PyAudio-0.2.13-cp311-cp311-win_amd64.whl
```

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Google Cloud TTS not working
**Solution**: Download Google Cloud credentials JSON and set:
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
USE_OFFLINE_TTS=false
```

Get credentials from: https://console.cloud.google.com/apis/credentials

### Voice responses too slow
**Solution**: Use offline mode in .env:
```env
USE_OFFLINE_TTS=true
```
Offline TTS (pyttsx3) is much faster than Google Cloud.

### Language not recognized
**Solution**: Use supported language codes:
- English: `en`
- Hindi: `hi`
- Marathi: `mr`
- French: `fr`
- Spanish: `es`
- German: `de`
- Portuguese: `pt`
- Russian: `ru`
- Japanese: `ja`
- Chinese: `zh`

## Testing the Integration

### Test 1: Health Check
```bash
curl http://localhost:8000/api/voice/health
```

### Test 2: Get Languages
```bash
curl http://localhost:8000/api/voice/languages
```

### Test 3: Text-to-Speech (No Audio Equipment Needed)
```bash
curl -X POST http://localhost:8000/api/voice/generate-answer \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "language": "en", "save_audio": true}'
```

### Test 4: Full API Documentation
Visit: `http://localhost:8000/docs`

## Features

### Offline Mode (Recommended for Speed)
- Uses `pyttsx3` library
- No Internet required
- Faster response times
- No API costs
- Works offline and on low bandwidth

### Online Mode (Premium Quality)
- Uses Google Cloud Text-to-Speech
- Natural sounding voices
- Multiple voice options
- Multi-lingual support
- Requires API credentials

### Automatic Fallback
Voice module automatically falls back to offline mode if:
- Google Cloud credentials not found
- Network unavailable
- API errors occur

## Next Steps

1. **Install dependencies**: `pip install -r speach_module/requirements.txt`
2. **Start server**: `python Backend\ API\ INT/main.py`
3. **Test health**: `curl http://localhost:8000/api/voice/health`
4. **Check documentation**: `http://localhost:8000/docs`
5. **(Optional) Configure for online TTS**: Set Google Cloud credentials in `.env`
6. **Integrate with frontend**: Add voice buttons to Chat.jsx

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs
- **Voice Module README**: See `speach_module/README.md`
- **Integration Examples**: See `speach_module/integration.py`
- **Configuration**: See `speach_module/settings.py`

## Summary of Changes

✅ **Modified Files:**
- `Backend API INT/main.py` - Added voice module import and router inclusion

✅ **New Files:**
- `speach_module/` - Complete voice module with 8 files
  - `voice_service.py` - Core implementation
  - `routes.py` - FastAPI endpoints
  - `models.py` - Pydantic data models
  - `settings.py` - Configuration
  - `requirements.txt` - Dependencies
  - `README.md` - Full documentation
  - `integration.py` - Integration examples
  - `__init__.py` - Module entry point

✅ **Backward Compatibility:**
- All existing code preserved
- Voice module optional (graceful degradation if dependencies not installed)
- No breaking changes to existing APIs

---

**Status**: Voice module is fully integrated and ready to use!
