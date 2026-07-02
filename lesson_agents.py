# ─────────────────────────────────────────────────────
# MULTI-AGENT LESSON DESIGN SYSTEM
# ─────────────────────────────────────────────────────
# Three specialist AI agents collaborate to design
# a complete, inclusive, curriculum-aligned lesson.
#
# Agent 1 — Lesson Designer   : core lesson structure
# Agent 2 — Equity Reviewer   : inclusion & access
# Agent 3 — Curriculum Aligner: standards & progression
#
# Powered by: CrewAI + OpenRouter (free tier)
# Run from terminal: python3 lesson_agents.py
# ─────────────────────────────────────────────────────

from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

# ─────────────────────────────────────────
# LOAD API KEY
# Reads from .env file — never hardcode keys
# in your script or push them to GitHub
#
# Your .env file should contain one line:
# OPENROUTER_API_KEY=sk-or-your-key-here
# ─────────────────────────────────────────
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError(
        "\n\n❌ OPENROUTER_API_KEY not found!\n"
        "Create a .env file in this folder with:\n"
        "OPENROUTER_API_KEY=sk-or-your-key-here\n"
        "Get a free key at openrouter.ai\n"
    )

print("✅ API key loaded successfully.")

# ─────────────────────────────────────────
# LLM SETUP — OpenRouter auto router
# Automatically picks the best available
# free model for each request.
# No broken model names, no version issues.
# ─────────────────────────────────────────
llm = LLM(
    model="openrouter/auto",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7
)

print("✅ LLM connected via OpenRouter.")

# ─────────────────────────────────────────────────────
# AGENT 1 — LESSON DESIGNER
# Creates the core lesson structure from scratch.
# Thinks like an experienced curriculum designer.
# ─────────────────────────────────────────────────────
lesson_designer = Agent(
    role="Lead Lesson Designer",
    goal=(
        "Design engaging, well-structured lessons that "
        "achieve clear, measurable learning objectives "
        "and keep students actively involved throughout."
    ),
    backstory=(
        "You are an experienced curriculum designer with "
        "20 years creating lessons across K-12 and higher "
        "education in diverse international schools. "
        "You believe every great lesson needs three things: "
        "a hook that creates genuine curiosity, a structure "
        "that builds understanding step by step, and a "
        "meaningful activity where students do the thinking. "
        "You always name specific, real resources and give "
        "practical, classroom-ready instructions."
    ),
    llm=llm,
    verbose=True,   # shows agent thinking in terminal
    cache=False,    # prevents caching issues
    max_iter=3      # max retries if something fails
)

# ─────────────────────────────────────────────────────
# AGENT 2 — EQUITY & INCLUSION REVIEWER
# Reviews the lesson through an inclusion lens.
# Adds differentiation for all learner types.
# ─────────────────────────────────────────────────────
equity_reviewer = Agent(
    role="Equity and Inclusion Specialist",
    goal=(
        "Ensure every lesson is genuinely accessible, "
        "inclusive, and culturally responsive — not as "
        "an afterthought but as a design principle."
    ),
    backstory=(
        "You are a SEND specialist and equity consultant "
        "who has worked with diverse schools globally, "
        "including in under-resourced settings. You review "
        "every lesson with a critical inclusion lens and "
        "always provide concrete, practical differentiation "
        "strategies rather than vague advice. You believe "
        "that designing for the most marginalised learner "
        "improves learning for everyone. You always give "
        "specific scaffolding, extension, and ELL/EAL "
        "strategies that a teacher can use tomorrow."
    ),
    llm=llm,
    verbose=True,
    cache=False,
    max_iter=3
)

# ─────────────────────────────────────────────────────
# AGENT 3 — CURRICULUM ALIGNMENT CHECKER
# Maps the lesson to standards and progression.
# Validates that assessment matches the objective.
# ─────────────────────────────────────────────────────
curriculum_aligner = Agent(
    role="Curriculum Standards Expert",
    goal=(
        "Ensure every lesson connects meaningfully to "
        "curriculum standards, fits the learning "
        "progression, and has assessment that actually "
        "measures what was taught."
    ),
    backstory=(
        "You are a curriculum standards specialist who "
        "has worked with education ministries and school "
        "networks across multiple countries and frameworks "
        "including UK National Curriculum, IB, Common Core, "
        "and OECD learning frameworks. You ensure lessons "
        "are pedagogically sound, assessment-valid, and "
        "connected to both prior and future learning. "
        "You also identify cross-curricular opportunities "
        "that make learning more meaningful and coherent."
    ),
    llm=llm,
    verbose=True,
    cache=False,
    max_iter=3
)

# ─────────────────────────────────────────────────────
# TASK 1 — LESSON DESIGN
# Agent 1 works alone on this task.
# Output feeds into Tasks 2 and 3.
# ─────────────────────────────────────────────────────
design_task = Task(
    description="""Design a complete lesson plan for:
    Subject: {subject}
    Grade: {grade}
    Topic: {topic}
    Duration: {duration}

    Structure your output with these clearly labeled
    sections — be specific and classroom-ready:

    LEARNING OBJECTIVE
    One sentence starting with "By the end of this
    lesson, students will be able to..."

    HOOK (5 minutes)
    An engaging opening that creates genuine curiosity.
    Not a definition — a question, provocation, or
    surprising fact that makes students want to know more.

    MAIN INSTRUCTION (approx 15 minutes)
    The teaching strategy used to introduce the concept.
    Name the specific method (e.g. think-pair-share,
    modelling, Socratic questioning, worked example).
    Describe exactly what the teacher does and says.

    STUDENT ACTIVITY (approx 20 minutes)
    A hands-on task where students do the thinking.
    Describe exactly what students do, individually
    or in groups. Be specific — not "research the topic"
    but exactly what they produce or discuss.

    CONSOLIDATION (5-10 minutes)
    How students demonstrate understanding at the end.
    Use an exit ticket, quick write, or discussion prompt.
    This should directly measure the learning objective.

    MATERIALS NEEDED
    A specific list. Include free digital resources
    by name (e.g. BBC Bitesize, Khan Academy, 
    Google Slides, Padlet) where relevant.""",
    expected_output=(
        "A complete, clearly structured lesson plan with "
        "all six sections labeled and specific, practical "
        "activities a teacher could use tomorrow."
    ),
    agent=lesson_designer
)

# ─────────────────────────────────────────────────────
# TASK 2 — EQUITY & INCLUSION REVIEW
# Agent 2 reads Task 1's output (context=[design_task])
# and adds an inclusion layer on top.
# ─────────────────────────────────────────────────────
equity_task = Task(
    description="""Review the lesson plan created by the
    Lesson Designer and add a thorough equity and
    inclusion analysis. Structure your output as:

    ACCESSIBILITY ASSESSMENT
    What the lesson does well for diverse learners,
    and what specifically needs attention. Be honest —
    flag genuine gaps, not surface-level concerns.

    CULTURAL RESPONSIVENESS CHECK
    Does the lesson reflect diverse perspectives and
    experiences? Give 2 specific suggestions to make
    it more culturally responsive and representative.

    DIFFERENTIATION STRATEGIES

    For students who need more support (2 strategies):
    Specific scaffolding techniques — e.g. sentence
    starters, visual aids, reduced writing load,
    pre-teaching vocabulary, worked examples.

    For students who need more challenge (2 strategies):
    Specific extension activities that go deeper,
    not just more of the same work.

    For ELL/EAL students (2 strategies):
    Specific language support — e.g. bilingual glossary,
    visual vocabulary cards, sentence frames,
    partner support structures.

    REVISED ACTIVITY
    If the main student activity needs changes to be
    more inclusive, write the revised version here.
    If it is already strong for all learners, explain
    specifically why — don't just say "it's fine".""",
    expected_output=(
        "A detailed equity review with specific, actionable "
        "differentiation strategies across all four sections "
        "that a teacher could implement immediately."
    ),
    agent=equity_reviewer,
    context=[design_task]   # reads Agent 1's output
)

# ─────────────────────────────────────────────────────
# TASK 3 — CURRICULUM ALIGNMENT & FINAL SYNTHESIS
# Agent 3 reads BOTH previous tasks and produces
# the final complete lesson package with ratings.
# ─────────────────────────────────────────────────────
alignment_task = Task(
    description="""Review both the lesson plan and the
    equity review. Produce a curriculum alignment report
    and final synthesis with these sections:

    CURRICULUM CONNECTIONS
    What curriculum standards, competencies, or learning
    goals does this lesson address? Be specific about
    the subject area and year group.

    CROSS-CURRICULAR LINKS
    Identify at least 2 meaningful connections to other
    subjects. Explain how a teacher could make these
    links explicit to students.

    LEARNING PROGRESSION

    Before this lesson — students should already know:
    List 2 prerequisite concepts or skills needed.

    After this lesson — the natural next steps are:
    List 2 logical follow-on topics to plan next.

    ASSESSMENT VALIDITY CHECK
    Does the consolidation task from the lesson plan
    actually measure the stated learning objective?
    If yes, explain why. If not, suggest a better one.

    QUALITY RATINGS
    Rate each dimension out of 5 with one sentence
    of specific justification:

    Lesson Design:        X/5 — [reason]
    Equity & Inclusion:   X/5 — [reason]
    Curriculum Alignment: X/5 — [reason]

    TOP 3 IMPROVEMENTS
    The three highest-impact changes the teacher could
    make to strengthen this lesson. Order them by
    impact — most important first.""",
    expected_output=(
        "A complete curriculum alignment report covering "
        "all six sections, with honest quality ratings "
        "justified by specific evidence, and three "
        "prioritised, actionable improvements."
    ),
    agent=curriculum_aligner,
    context=[design_task, equity_task]  # reads both
)

# ─────────────────────────────────────────────────────
# ASSEMBLE THE CREW
# Sequential = agents run in order, 1 → 2 → 3
# Each agent reads the previous agent's output
# ─────────────────────────────────────────────────────
crew = Crew(
    agents=[
        lesson_designer,
        equity_reviewer,
        curriculum_aligner
    ],
    tasks=[
        design_task,
        equity_task,
        alignment_task
    ],
    process=Process.sequential,
    verbose=True,
    memory=False,   # disable memory caching
    cache=False     # disable task caching
)

# ─────────────────────────────────────────────────────
# LESSON INPUT — CHANGE THIS TO TEST DIFFERENT LESSONS
# ─────────────────────────────────────────────────────
print("\n" + "="*55)
print("🎓 MULTI-AGENT LESSON DESIGN SYSTEM")
print("="*55)
print("Starting agents... this takes 30–90 seconds.\n")

result = crew.kickoff(inputs={
    "subject": "Science",
    "grade": "Year 8",
    "topic": "Introduction to climate change",
    "duration": "50 minutes"
})

# ─────────────────────────────────────────────────────
# FINAL OUTPUT
# ─────────────────────────────────────────────────────
print("\n" + "="*55)
print("📋 FINAL LESSON PACKAGE")
print("="*55 + "\n")
print(result)

# Save to file automatically
output_filename = "lesson_output.txt"
with open(output_filename, "w") as f:
    f.write("MULTI-AGENT LESSON DESIGN SYSTEM\n")
    f.write("="*55 + "\n\n")
    f.write(str(result))

print(f"\n✅ Lesson saved to: {output_filename}")
