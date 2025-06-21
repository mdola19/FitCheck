# 🧥 FitCheck AI Stylist

AI-powered, real-time outfit analysis and style advice web app.

---

## 📸 Screenshots

Add your screenshots below:

- **Image 1:** (e.g., app landing screen)  
- **Image 2:** (e.g., voice interaction in progress)  
- **Image 3:** (e.g., Pinterest recommendations panel)  
- **Image 4:** (e.g., accessibility options UI)

---

## 🚀 Features

- Custom-trained YoloV8 model to add new clothes 
- AI fashion guidance via image and text understanding  
- Pinterest integration for visual outfit suggestions  
- Outfit history: save, review, and compare your looks 

---

## ⚙️ Installation

1. Clone the repo:  
   ```bash
   git clone https://github.com/mdola19/FitCheck.git
   cd FitCheck
   ```

2. Create & activate virtual environment:  
   ```bash
   python -m venv venv
   ```  
   On Windows CMD:  
   ```cmd
   venv\Scripts\activate
   ```  
   On PowerShell:  
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```  
   On macOS/Linux:  
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Configure API keys:  
   Create a file named `config.json` and add:
   ```json
   {
     "openweather_api_key": "YOUR_OPENWEATHER_API_KEY",
     "groq_api_key": "YOUR_GROQ_API_KEY",
     "deepgram_api_key": "YOUR_DEEPGRAM_API_KEY",
     "google_api_key": "YOUR_GOOGLE_API_KEY"
   }
   ```

---

## 🚀 Running the App

```bash
python app.py
```

Then open your browser and visit:  
`http://localhost:8080`

Allow microphone and camera access, then interact with the assistant using your voice and outfit.

---

## 🧩 Key Components

- Voice Interaction: Deepgram for speech-to-text and text-to-speech  
- Outfit Recognition: YOLOv8 (via Ultralytics) for visual garment detection  
- Style Intelligence: Google AI / Groq for fashion recommendations  
- Visual Suggestions: Pinterest API fetches similar outfit inspirations  
- Accessibility Features: contrast toggle, font-size controls, color-blind filters

---

## 🎯 Future Enhancements

- Mobile device compatibility  
- E-commerce integration  
- User profiles and saved styles  
- Trend-aware outfit rating


