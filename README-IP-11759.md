# Prompt Engineering Agent for IT Project Delivery Guidance

Individual project (120 hours) - Global Professional Internship (GPI).

## Objective
Create an intelligent agent, using prompt engineering techniques, that guides project teams
in delivering projects according to IT industry standards: efficiency, compliance and quality.

## How it works
1. NLP (spaCy, NLTK fallback) cleans and normalises the user's query.
2. The query is matched to an SDLC / project-delivery topic.
3. A clear, concise prompt is built from a template.
4. The agent returns numbered steps plus efficiency, compliance and quality checks.

## Setup
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-IP-11759.txt
python -m spacy download en_core_web_sm
```

## Run
```
python agent-IP-11759.py                 # interactive chat
python agent-IP-11759.py --show-prompt   # also print the engineered prompt
python agent-IP-11759.py --test          # evaluation on 12 sample queries
```

## Files
- agent-IP-11759.py - the agent (NLP, topic knowledge base, prompt template, CLI, tests)
- requirements-IP-11759.txt - dependencies
- docs/design_and_assumptions-IP-11759.md - design flow and assumptions
- screenshots/ - add your test and chat screenshots here
