# NuupXe - Amateur Radio Voice Services

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)](https://openai.com)

**NuupXe** is an advanced voice services system for amateur radio operators, integrating modern AI/LLM capabilities with traditional ham radio services. Originally designed for IRLP repeater nodes, NuupXe now provides state-of-the-art AI-powered features including natural language interaction, automated scheduling, and intelligent assistance.

## 🎯 Features

### Core Capabilities
- **Voice Synthesis**: High-quality text-to-speech using OpenAI TTS, Google TTS, eSpeak, or Festival
- **Speech Recognition**: Automatic speech recognition via OpenAI Whisper and Google Speech API
- **Scheduled Services**: Automated announcements for time, weather, news, identification, and more
- **DTMF Control**: Radio command interface via push-to-talk signals
- **Multiple Modules**: 17+ service modules including weather, news, APRS tracking, seismology, and more

### AI/LLM Features
- **🤖 Intelligent Assistant**: Natural language command processing with GPT-4
- **💬 Conversational AI**: Context-aware conversations with memory (proposed)
- **🎓 Exam Preparation**: Interactive study sessions for ham radio licensing (proposed)
- **📊 Band Analysis**: AI-powered propagation condition reports (proposed)
- **🎨 QSL Card Generator**: Automated QSL card creation with DALL-E (proposed)
- **📝 Net Scripts**: Automated net control script generation (proposed)

### Traditional Ham Radio Services
- **Clock**: Automated time and date announcements
- **Weather**: Real-time weather reports and forecasts
- **News**: RSS feed aggregation and announcements
- **APRS**: Position tracking and messaging
- **Seismology**: Earthquake monitoring and alerts
- **Morse Code**: Interactive morse code teaching and contests
- **SSTV**: Slow-scan television decoding
- **Voice Mail**: Message recording and playback system

## 📋 Requirements

- **Python**: 3.8 or higher (3.12+ recommended)
- **Operating System**: Linux (Debian/Ubuntu preferred)
- **API Keys**: OpenAI API key (required for AI features)

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/NuupXe/NuupXe.git
cd NuupXe
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp configuration/services.config.example configuration/services.config
# Edit configuration files with your API keys
```

### Basic Usage

```bash
# Text-to-Speech
python nuupxe.py -v "Hello amateur radio world"

# Get current time
python nuupxe.py -m hour

# Interactive mode
python nuupxe.py -s writing

# AI Query
python nuupxe.py -d PS7
```

## 📖 Documentation

See [PROPOSAL.md](PROPOSAL.md) for comprehensive enhancement plans and detailed feature documentation.

- [Installation Guide](documentation/Installation.md)
- [Module Documentation](documentation/Modules.md)
- [Services Guide](documentation/Services.md)

## 📜 License

Copyright 2014-2026, NuupXe Project

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) file for details.

---

**73 de NuupXe** 📻✨
