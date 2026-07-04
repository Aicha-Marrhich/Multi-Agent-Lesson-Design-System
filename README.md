# 🎓 Multi-Agent Lesson Design System

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://multi-agent-leappn-design-system-c6ywqysxuxtagt8pyintys.streamlit.app)

Three specialist AI agents collaborate to design 
complete, inclusive, curriculum-aligned lesson plans.

## 🚀 Try it live
👉 **[Launch the app](https://multi-agent-leappn-design-system-c6ywqysxuxtagt8pyintys.streamlit.app)**

---

## The three agents

| Agent | Role |
|---|---|
| 🎨 Lesson Designer | Creates core lesson structure with hook, instruction, activity and consolidation |
| ♿ Equity Reviewer | Reviews for inclusion, accessibility and differentiation across all learner types |
| 📌 Curriculum Aligner | Maps to standards, identifies cross-curricular links, validates assessment |

---

## Why multi-agent?

A single AI gives one perspective.  
Three specialist agents give a lesson that has been 
reviewed from three distinct expert lenses — the way 
real lesson design teams work.

---

## How to use

1. Open the app using the link above
2. Get a **free API key** at [openrouter.ai](https://openrouter.ai) 
   (no credit card required)
3. Fill in your subject, grade, topic and duration
4. Click **Design my lesson**
5. Download the result as a text file

---

## Run locally

```bash
git clone https://github.com/Aicha-Marrhich/Multi-Agent-Lesson-Design-System.git
cd Multi-Agent-Lesson-Design-System
pip install crewai litellm streamlit
cp .env.template .env
# Add your OpenRouter key to .env
streamlit run app.py
```

---

## Built with

- [CrewAI](https://crewai.com) — multi-agent framework
- [OpenRouter](https://openrouter.ai) — free LLM API
- [Streamlit](https://streamlit.io) — web interface

---

## About

Built as part of a portfolio on **AI in Education** —
exploring how AI can support teachers, students, and 
school leaders.

*Created by [Aicha Marrhich](https://github.com/Aicha-Marrhich)*