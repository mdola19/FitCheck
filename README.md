# 🧥 FitCheck AI Stylist

FitCheck is a web app that saves you time and keeps you stylish by organizing your wardrobe and generating personalized outfit suggestions. By combining your clothing inventory with real-time weather data and your style preferences, FitCheck helps you quickly choose the perfect look for any day—so you can spend less time deciding and more time showing up confidently.

---

## 📸 Screenshots

![fitcheck](https://github.com/user-attachments/assets/67b76272-557b-4d48-a3f7-6c0948d25736)

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


