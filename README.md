# Frontend – Reconnaissance vocale (Speech Recognition)

Ce projet est le frontend React de l’application de reconnaissance vocale.  
Il permet d’enregistrer un fichier audio (via le microphone), de l’envoyer à l’API backend FastAPI (modèle CTC), et d’afficher la transcription en temps réel.

---

## 🚀 Fonctionnalités

- Enregistrement audio depuis le microphone (format WebM/WAV)
- Envoi du fichier audio à l’API backend (`/api/v1/transcribe`)
- Affichage de la transcription
- Interface simple et réactive (micro-frontend prêt pour Module Federation)

---

## 📋 Prérequis

- **Node.js** (version 16 ou supérieure) et **npm** (ou yarn)
- Le **backend FastAPI** doit être en cours d’exécution sur `http://localhost:8000` (ou une autre URL)

---

## 🔧 Installation

1. **Cloner le dépôt** (ou placer les sources dans un dossier) :
   ```bash
   git clone https://github.com/votre-compte/frontend-speech-recognition.git
   cd frontend-speech-recognition
   ```
