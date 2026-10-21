"""
Prompt Engineering Agent for IT Project Delivery Guidance
---------------------------------------------------------
Guides project teams through the software development lifecycle (SDLC)
so that delivery follows IT industry standards: efficiency, compliance, quality.

How it works:
  1. NLP (spaCy, with NLTK fallback) cleans and normalises the user's query.
  2. The query is matched to an SDLC / project-delivery topic.
  3. A clear, concise prompt is built from a template (the "prompt engineering" part).
  4. A structured answer is returned: steps + efficiency + compliance + quality checks.

Run:   python agent-IP-11759.py            (interactive chat)
Test:  python agent-IP-11759.py --test     (automatic evaluation)
Show the engineered prompt too:  python agent-IP-11759.py --show-prompt
"""
import re
import sys

# ---------- NLP setup (spaCy preferred, NLTK fallback) ----------
try:
    import spacy
    NLP = spacy.load("en_core_web_sm")
    BACKEND = "spaCy (en_core_web_sm)"
except Exception:
    NLP = None
    BACKEND = "NLTK PorterStemmer (spaCy model not found)"

from nltk.stem import PorterStemmer
STEM = PorterStemmer()

STOP = set(
    "a an the is are was were be to of in on for and or i we you it my our how what "
    "do does should can with about this that me us need want please tell give who when "
    "which will would could any some".split()
)


def normalize(text):
    """Lowercase, remove stop words, reduce words to base form."""
    text = text.lower()
    if NLP:
        return [t.lemma_ for t in NLP(text)
                if t.is_alpha and not t.is_stop and t.lemma_ not in STOP]
    return [STEM.stem(w) for w in re.findall(r"[a-z]+", text) if w not in STOP]


# ---------- Knowledge base: IT project delivery guidance ----------
TOPICS = {
    "planning": {
        "title": "Project Planning",
        "keywords": "plan planning scope schedule timeline milestone kickoff charter estimate estimation budget resource roadmap",
        "steps": [
            "Define project goals, scope and what is out of scope.",
            "Break work into milestones and tasks with owners and estimates.",
            "Identify resources, dependencies and a realistic timeline.",
            "Get written sign-off on the plan from the client/sponsor.",
        ],
        "efficiency": "Add 15-20% buffer to estimates and track progress weekly.",
        "compliance": "Record approvals and scope changes through a change-control log.",
        "quality": "Define measurable success criteria before work starts.",
    },
    "requirements": {
        "title": "Requirements Gathering",
        "keywords": "requirement story acceptance criterion stakeholder client specification gather elicitation",
        "steps": [
            "Interview stakeholders and list needs in plain language.",
            "Write each need as a user story: As a <user>, I want <goal>, so that <benefit>.",
            "Add testable acceptance criteria to every story.",
            "Prioritise (MoSCoW: Must/Should/Could/Won't) and get client approval.",
        ],
        "efficiency": "Clarify unclear items early; late requirement changes cost the most.",
        "compliance": "Keep a requirements traceability matrix linking requirement -> design -> test.",
        "quality": "Each requirement must be clear, testable and unambiguous.",
    },
    "design": {
        "title": "System Design",
        "keywords": "design architecture database diagram uml component module api interface schema",
        "steps": [
            "Choose an architecture (e.g. layered, microservices) that fits the requirements.",
            "Draw high-level diagrams: components, data flow, database schema.",
            "Define APIs/interfaces between modules.",
            "Review the design with the team before coding starts.",
        ],
        "efficiency": "Reuse proven patterns and existing libraries instead of building from scratch.",
        "compliance": "Document design decisions and follow security-by-design principles.",
        "quality": "Hold a design review; check scalability, maintainability and security.",
    },
    "development": {
        "title": "Development / Coding",
        "keywords": "code coding developer develop implementation implement git branch commit refactor programming build",
        "steps": [
            "Use version control (Git) with feature branches and clear commit messages.",
            "Follow a coding standard (e.g. PEP 8 for Python) and use a linter.",
            "Write small, modular functions with comments where logic is not obvious.",
            "Raise a pull request and get a peer code review before merging.",
        ],
        "efficiency": "Automate builds and linting; keep tasks small (1-2 days).",
        "compliance": "Check open-source licences and never commit passwords/API keys.",
        "quality": "Mandatory peer review and unit tests for new code.",
    },
    "testing": {
        "title": "Testing & QA",
        "keywords": "test testing case bug defect qa quality coverage unit integration regression uat verify validation",
        "steps": [
            "Write a test plan linked to the requirements.",
            "Write unit tests, then integration tests, then system/UAT tests.",
            "Log every defect with severity, steps to reproduce and owner.",
            "Re-test fixes and run regression tests before release.",
        ],
        "efficiency": "Automate repeatable tests and run them on every commit (CI).",
        "compliance": "Keep test reports as evidence for audits and client sign-off.",
        "quality": "Aim for agreed coverage (e.g. 80%) and zero open critical defects at release.",
    },
    "deployment": {
        "title": "Deployment & Release",
        "keywords": "deploy deployment release production rollback cicd pipeline launch environment staging golive",
        "steps": [
            "Prepare a release checklist and release notes.",
            "Deploy first to a staging environment and run smoke tests.",
            "Take a backup and define a rollback plan.",
            "Deploy to production in a planned window and monitor after release.",
        ],
        "efficiency": "Use a CI/CD pipeline to automate and repeat deployments.",
        "compliance": "Get formal release approval and record who deployed what and when.",
        "quality": "Run smoke tests and watch logs/metrics right after go-live.",
    },
    "agile": {
        "title": "Agile Execution",
        "keywords": "agile scrum sprint standup backlog retrospective kanban velocity iteration ceremony",
        "steps": [
            "Maintain a prioritised product backlog.",
            "Plan 1-2 week sprints with a clear sprint goal.",
            "Hold a short daily stand-up: done, next, blockers.",
            "End with a sprint review (demo) and a retrospective for improvements.",
        ],
        "efficiency": "Limit work in progress and remove blockers the same day.",
        "compliance": "Keep sprint records (goals, decisions, burndown) for traceability.",
        "quality": "Use a shared 'Definition of Done' for every story.",
    },
    "risk": {
        "title": "Risk Management",
        "keywords": "risk mitigate mitigation threat issue contingency uncertainty impact probability",
        "steps": [
            "List possible risks (technical, schedule, people, client).",
            "Score each by probability x impact.",
            "Assign an owner and a mitigation/contingency action to each high risk.",
            "Review the risk register in every weekly meeting.",
        ],
        "efficiency": "Focus effort on the top 5 risks, not every small one.",
        "compliance": "Keep a risk register and report high risks to the sponsor.",
        "quality": "Close risks with evidence, not assumptions.",
    },
    "documentation": {
        "title": "Documentation",
        "keywords": "documentation document readme manual wiki report notes record knowledge handover transfer",
        "steps": [
            "Keep one central place (wiki/repo) for all project documents.",
            "Use templates: requirements, design, test plan, release notes, user guide.",
            "Update docs in the same sprint as the code change.",
            "Prepare a handover/knowledge-transfer document at the end.",
        ],
        "efficiency": "Document as you work; short and current beats long and outdated.",
        "compliance": "Use version numbers, owners and approval dates on key documents.",
        "quality": "Have a teammate follow the document to check it is understandable.",
    },
    "decision": {
        "title": "Decision-Making & Communication",
        "keywords": "decision decide delay approve approval escalate escalation communication meeting update status blocker",
        "steps": [
            "State the decision needed, the options and the deadline.",
            "Name one decision owner and the people to consult.",
            "Escalate to the project manager if no decision within the agreed time.",
            "Record the decision and reason in a decision log and share it.",
        ],
        "efficiency": "Set decision deadlines; send a short weekly status update.",
        "compliance": "Keep written records of approvals and escalations.",
        "quality": "Decide with data (impact on time, cost, quality), not opinion alone.",
    },
    "compliance": {
        "title": "Compliance & Security",
        "keywords": "compliance audit regulation gdpr policy iso license licence security privacy standard legal",
        "steps": [
            "Identify the standards/regulations that apply (e.g. GDPR, ISO 27001, client policy).",
            "Turn them into a checklist for each SDLC phase.",
            "Handle personal data minimally and store secrets securely.",
            "Run periodic internal audits and fix findings with owners and dates.",
        ],
        "efficiency": "Build compliance checks into the pipeline instead of doing them at the end.",
        "compliance": "Keep evidence (logs, approvals, reports) ready for audit.",
        "quality": "Do a security review and dependency scan before every release.",
    },
}

SYSTEM_PROMPT = (
    "You are PEA, a Prompt Engineering Agent that guides IT project teams "
    "(project managers, engineers, consultants, interns) through project delivery. "
    "Follow IT industry standards for efficiency, compliance and quality. "
    "Be clear and concise. Use numbered steps. State any assumption you make."
)

PROMPT_TEMPLATE = (
    "{system}\n\n"
    "Topic: {title}\n"
    "User question: {query}\n\n"
    "Answer format:\n"
    "1) Short direct answer (1-2 sentences)\n"
    "2) Numbered action steps (max 5)\n"
    "3) Efficiency tip, Compliance check, Quality check\n"
    "Keep it under 150 words."
)

FALLBACK = (
    "I could not match that to a project-delivery topic. I can help with: "
    + ", ".join(t["title"] for t in TOPICS.values())
    + ". Try rephrasing, e.g. 'How do we plan a sprint?'"
)


class PromptEngineeringAgent:
    def __init__(self):
        self.topic_tokens = {k: set(normalize(v["keywords"])) for k, v in TOPICS.items()}
        self.history = []

    def classify(self, query):
        tokens = set(normalize(query))
        scores = {k: len(tokens & kw) for k, kw in self.topic_tokens.items()}
        best = max(scores, key=scores.get)
        return (best, scores[best]) if scores[best] > 0 else (None, 0)

    def build_prompt(self, topic_key, query):
        return PROMPT_TEMPLATE.format(
            system=SYSTEM_PROMPT, title=TOPICS[topic_key]["title"], query=query
        )

    def respond(self, query):
        topic, score = self.classify(query)
        self.history.append(query)
        if topic is None:
            return {"topic": None, "prompt": None, "answer": FALLBACK}
        t = TOPICS[topic]
        steps = "\n".join(f"  {i}. {s}" for i, s in enumerate(t["steps"], 1))
        answer = (
            f"[{t['title']}]\n{steps}\n"
            f"  Efficiency: {t['efficiency']}\n"
            f"  Compliance: {t['compliance']}\n"
            f"  Quality:    {t['quality']}"
        )
        return {"topic": topic, "prompt": self.build_prompt(topic, query), "answer": answer}


TEST_CASES = [
    ("How do I write requirements for the client?", "requirements"),
    ("How should we run our daily standup and sprint retrospective?", "agile"),
    ("What test cases do we need before release?", "testing"),
    ("How do we deploy to production safely?", "deployment"),
    ("What are the risks and how do we mitigate them?", "risk"),
    ("Our documentation is outdated, how do we fix it?", "documentation"),
    ("We keep delaying decisions, who approves?", "decision"),
    ("Which architecture should we use for the database?", "design"),
    ("What coding standards should developers follow?", "development"),
    ("Do we need a security audit for GDPR?", "compliance"),
    ("Help me create a project timeline and milestones", "planning"),
    ("tell me a joke", None),
]


def run_tests(agent):
    print(f"NLP backend: {BACKEND}\n")
    passed = 0
    for q, expected in TEST_CASES:
        got = agent.respond(q)["topic"]
        ok = got == expected
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} | {q!r} -> {got} (expected {expected})")
    print(f"\nAccuracy: {passed}/{len(TEST_CASES)} = {100 * passed / len(TEST_CASES):.0f}%")


def main():
    agent = PromptEngineeringAgent()
    if "--test" in sys.argv:
        run_tests(agent)
        return
    show_prompt = "--show-prompt" in sys.argv
    print(f"Prompt Engineering Agent (NLP: {BACKEND})")
    print("Ask a project-delivery question. Type 'quit' to exit.\n")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in {"quit", "exit", "q"}:
            break
        if not q:
            continue
        result = agent.respond(q)
        if show_prompt and result["prompt"]:
            print("\n--- Engineered prompt ---\n" + result["prompt"] + "\n-------------------------")
        print("\nAgent:\n" + result["answer"] + "\n")


if __name__ == "__main__":
    main()
