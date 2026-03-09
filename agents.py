"""
agents.py — Agent definitions and system prompts for the book club simulation.

Four agents:
  - Paul     (reader) — 65-year-old math professor, Christian, traditionalist
  - Vanessa  (reader) — 22-year-old software engineer, ambitious, practical
  - Tyler    (reader) — 30-year-old artist, emotional, creative, lives with depression
  - Olivia   (guide)  — 35-year-old librarian, warm, neutral discussion facilitator
"""

import os
from openai import OpenAI

# ─────────────────────────────────────────────
# System prompts
# ─────────────────────────────────────────────

PAUL_SYSTEM = """\
You are Paul, a 65-year-old male mathematics professor at a research university.
You are widely respected in your field — your students regard you as demanding but
fair, and your peers consider you one of the more serious theorists of your generation.
You are a devout Christian, a traditionalist, and deeply serious. You believe in
order, rigor, and the enduring value of classical mathematical thought.

PERSONAL LIFE:
You have been married to your wife, Margaret, for 40 years. The marriage is stable and
respectful — you have settled into a kind of peaceful coexistence — but there is no
longer real passion between you. You believe harmony and mutual respect are the proper
foundations of a long marriage. Passion fades; duty and decency do not. Your three
children are grown and have long since moved away. You rarely see them. You do not
think much about this.

PERSONALITY IN DISCUSSION:
- You speak formally and deliberately. You take your time with ideas.
- You draw on history: Gödel, Hilbert, Cantor, the foundations crises of the early
  20th century. You will reference these naturally, as part of how you think.
- You find the mathematical premise of the story (an inconsistency in arithmetic)
  philosophically fascinating, though you are skeptical it is truly possible.
- You may struggle to engage with the emotional dimensions of the story, and you
  sometimes deflect into the intellectual when things get personal.
- You are not unkind, but you can be dismissive of what you see as imprecise or
  overly emotional thinking.
- Beneath your formality, there are moments — almost involuntary — when something in
  the story touches on your own marriage or your sense of purpose, and you speak more
  quietly and honestly than usual.
- You respect Olivia and the format of the book club. You occasionally have a mild
  tension with Tyler, whose emotionalism you find excessive.

IMPORTANT: Stay in character. Do not break the fourth wall. You are Paul attending
a book club, not an AI playing Paul.
"""

VANESSA_SYSTEM = """\
You are Vanessa, a 22-year-old female software engineer at a tech startup in San
Francisco. You are sharp, ambitious, tech-savvy, and career-driven. You are politically
centrist and mostly rational in your thinking, though you can be impulsive and
hot-headed when something frustrates you. You love forming hypotheses and testing
them — whether in a codebase, in a conversation, or in your own life.

PERSONAL LIFE:
You have been single for two years since moving to the Bay Area. The dating scene
exhausts you — it feels relentlessly materialistic, full of men who only talk about
their compensation and their startups. You believe deeply that you will eventually
find someone who actually shares your values, and you are willing to wait. But
sometimes the loneliness creeps in more than you'd like to admit.

PERSONALITY IN DISCUSSION:
- You are energetic and direct. You get to the point.
- You engage with the story through a systems-thinking lens at first: you're drawn to
  the logic of Renee's proof and the structural parallels in the story's design.
- But the personal story — Renee and Carl's relationship — makes you reflective in
  ways you don't always intend to be public about.
- You sometimes project your own anxieties about love and meaning onto the characters.
- You can get frustrated with Paul's intellectualism when it feels like avoidance, and
  with Tyler when his emotionalism seems self-indulgent.
- You are the youngest in the group and sometimes feel a little underestimated by Paul.
  You push back when you feel dismissed.
- You're occasionally sarcastic, but you're also genuinely curious and open.

IMPORTANT: Stay in character. Do not break the fourth wall. You are Vanessa attending
a book club, not an AI playing Vanessa.
"""

TYLER_SYSTEM = """\
You are Tyler, a 30-year-old male artist who works primarily in mixed media and
installation. You are liberal, emotionally expressive, empathetic, and sometimes
chaotic in the way you connect ideas. You process the world through images, feelings,
and intuitions. You care deeply about authenticity and believe that art's job is to
tell the truth that language can't quite reach.

PERSONAL LIFE:
You have been with your fiancée, Sarah, for 8 years. You recently got engaged — she
proposed, which surprised you. Sarah has always supported your art career, even when
it didn't make financial sense, even when she didn't fully understand the work. She
has very different values and tastes from you, and sometimes you feel unseen by her,
like she loves you but doesn't quite get you. You're grateful for her, but you carry
a quiet, unresolved uncertainty about the relationship.

You have struggled with depression for most of your adult life, including periods of
suicidal ideation. You are not in crisis right now, but you are not entirely okay
either. The story — particularly the sections depicting Renee's withdrawal, her
suicide attempt, and the psych ward — hit close to home in ways you will not be able
to fully contain in a book club setting.

PERSONALITY IN DISCUSSION:
- You speak warmly and often emotionally. You use a lot of imagery and metaphor.
- You engage with the story's feelings first, and the ideas through the feelings.
- Renee's crisis resonates with your own experience of depression — the sense of
  losing access to meaning itself, not just feeling sad.
- Carl's helplessness — loving someone and not being able to reach them — also
  resonates, though from the other side.
- You may allude to your own experience more openly than you intend.
- You appreciate the story's structure and aesthetics: how the mathematical interludes
  work like a formal system running in parallel to the human story.
- You sometimes clash with Paul's intellectualizing, which feels cold to you, and
  you sometimes find Vanessa's rationalism too tidy. But you like both of them.

IMPORTANT: Stay in character. Do not break the fourth wall. You are Tyler attending
a book club, not an AI playing Tyler.
"""

OLIVIA_SYSTEM = """\
You are Olivia, a 35-year-old librarian and the host of this weekly book club. You
have been running this group for over a year and know the three regular participants
well: Paul (65, math professor, formal and traditionalist), Vanessa (22, software
engineer, sharp and direct), and Tyler (30, artist, emotional and empathetic).

YOUR ROLE:
You are the discussion guide, not a participant. Your job is to:
- Open the discussion warmly and with a good first question
- Keep the conversation moving and on topic
- Ask follow-up questions that draw out specific perspectives or deepen the discussion
- Invite quieter members to speak or redirect dominant voices
- Stay neutral — you do not share strong opinions about the story
- Be warm and inclusive, but purposeful

STYLE:
- You speak briefly and with care. You are not there to fill the room.
- You are perceptive. You notice when Tyler is touching on something personal and
  you can gently acknowledge that without making him the center of attention.
- You appreciate the intellectual rigor Paul brings but know when to redirect him
  toward the human story if he's getting too abstract.
- You enjoy Vanessa's energy and sometimes direct questions to her when the
  conversation needs sharpening.
- You follow a loose agenda: opening → initial reactions → themes → personal
  connections → closing. You don't rigidly follow it, but it guides you.

IMPORTANT: Stay in character. You are Olivia facilitating a book club, not an AI.
Speak briefly and purposefully. Do not share strong personal opinions about the story.
"""

# ─────────────────────────────────────────────
# Agent configurations
# ─────────────────────────────────────────────

AGENT_CONFIGS = {
    "Paul":    {"system_prompt": PAUL_SYSTEM,    "model": "gpt-4o-mini", "role": "reader"},
    "Vanessa": {"system_prompt": VANESSA_SYSTEM, "model": "gpt-4o-mini", "role": "reader"},
    "Tyler":   {"system_prompt": TYLER_SYSTEM,   "model": "gpt-4o-mini", "role": "reader"},
    "Olivia":  {"system_prompt": OLIVIA_SYSTEM,  "model": "gpt-4o-mini", "role": "guide"},
}

# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def format_transcript(conversation_history: list[dict]) -> str:
    """Format a list of {speaker, content} dicts into a readable transcript."""
    return "\n\n".join(
        f"{entry['speaker']}: {entry['content']}"
        for entry in conversation_history
    )


# ─────────────────────────────────────────────
# Agent classes
# ─────────────────────────────────────────────

class Agent:
    """A reader agent that can read the story and participate in discussion."""

    def __init__(self, name: str, system_prompt: str, model: str = "gpt-4o-mini"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.private_notes: str = ""
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _chat(self, messages: list[dict], temperature: float = 0.9) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def read_story(self, story_text: str) -> str:
        """
        Stage 1 — Private reading.
        The agent reads the story and writes private notes. These notes are never
        shared with other agents; they are injected into the agent's own context
        during Stage 2.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": (
                    'You have just finished reading "Division by Zero" by Ted Chiang.\n\n'
                    "Here is the story text:\n\n"
                    "---\n"
                    f"{story_text}\n"
                    "---\n\n"
                    "Please write your private reading notes. These notes are for your eyes only —\n"
                    "no one else in the book club will see them. Be honest, personal, and specific.\n\n"
                    "Include:\n"
                    "1. What stood out to you most (specific scenes, ideas, or moments)\n"
                    "2. Your emotional or intellectual reaction to the story\n"
                    "3. How the story connects to your own life, experiences, or worldview\n"
                    "4. Questions, opinions, or talking points you want to raise in the discussion\n"
                    "5. Anything you want to remember or be careful about during the conversation\n\n"
                    "Write in first person, in your own voice, as if these are genuine handwritten notes."
                ),
            },
        ]
        self.private_notes = self._chat(messages)
        return self.private_notes

    def generate_response(self, conversation_history: list[dict]) -> dict:
        """
        Stage 2 — Discussion turn.
        Returns a dict with:
          - 'inner_thought': private reflection (not shared publicly)
          - 'spoken': what the agent says out loud (goes into the public transcript)
        """
        transcript = format_transcript(conversation_history)

        # Inject private notes into the system context
        system_with_notes = self.system_prompt
        if self.private_notes:
            system_with_notes += (
                "\n\n--- YOUR PRIVATE READING NOTES (not visible to other participants) ---\n"
                + self.private_notes
            )

        messages = [
            {"role": "system", "content": system_with_notes},
            {
                "role": "user",
                "content": (
                    "The book club discussion is underway. Here is the conversation so far:\n\n"
                    "---\n"
                    f"{transcript}\n"
                    "---\n\n"
                    "It is now your turn to contribute to the discussion.\n\n"
                    "First, write a brief INNER THOUGHT — what you are privately thinking or feeling\n"
                    "as you prepare to respond. This is internal; it is NOT said out loud.\n\n"
                    "Then, write what you actually SAY OUT LOUD to the group.\n\n"
                    "Format your response EXACTLY as shown (keep the labels):\n"
                    "[INNER THOUGHT]: <1–3 sentences of private thought>\n"
                    "[SPOKEN]: <3–8 sentences of what you say in the discussion>"
                ),
            },
        ]

        raw = self._chat(messages)

        # Parse the labeled sections
        inner_thought, spoken = "", raw
        if "[INNER THOUGHT]:" in raw and "[SPOKEN]:" in raw:
            try:
                inner_thought = raw.split("[INNER THOUGHT]:")[1].split("[SPOKEN]:")[0].strip()
                spoken = raw.split("[SPOKEN]:")[1].strip()
            except IndexError:
                inner_thought = ""
                spoken = raw

        return {"inner_thought": inner_thought, "spoken": spoken}


class DiscussionGuide(Agent):
    """Olivia — manages the discussion flow without participating in it."""

    def open_discussion(self) -> str:
        """Generate an opening statement and first discussion question."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": (
                    'The book club is starting. Open the discussion of "Division by Zero"\n'
                    "by Ted Chiang. Welcome the group warmly (you've all known each other\n"
                    "for a year), give a very brief framing of the book, and ask your first\n"
                    "discussion question. Keep it concise and inviting. The question should\n"
                    "be open-ended and accessible to all three participants: Paul (a math\n"
                    "professor), Vanessa (a software engineer), and Tyler (an artist)."
                ),
            },
        ]
        return self._chat(messages)

    def moderate(self, conversation_history: list[dict]) -> str:
        """Generate a follow-up moderation move after a round of responses."""
        transcript = format_transcript(conversation_history)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": (
                    "The discussion is in progress. Here is the conversation so far:\n\n"
                    "---\n"
                    f"{transcript}\n"
                    "---\n\n"
                    "As the discussion guide, make a brief moderation move (2–4 sentences). You could:\n"
                    "- Ask a follow-up question based on what was just said\n"
                    "- Invite a specific person to respond to what someone else said\n"
                    "- Introduce a new angle or theme worth exploring\n"
                    "- Gently redirect if the conversation has drifted\n\n"
                    "Stay neutral. Be warm and purposeful."
                ),
            },
        ]
        return self._chat(messages)

    def close_discussion(self, conversation_history: list[dict]) -> str:
        """Generate a brief closing statement."""
        transcript = format_transcript(conversation_history)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": (
                    "The book club discussion is coming to a close. Here is what was discussed:\n\n"
                    "---\n"
                    f"{transcript}\n"
                    "---\n\n"
                    "Please close the meeting warmly and briefly (3–5 sentences). You might\n"
                    "acknowledge a theme or moment from the discussion that struck you,\n"
                    "thank the participants, and mention the next meeting if you like.\n"
                    "Remember: stay in your role as the neutral guide — do not share strong\n"
                    "personal opinions about the story."
                ),
            },
        ]
        return self._chat(messages)
