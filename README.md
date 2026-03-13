# Multi-Agent Literature Discussion Simulation

In this project, we want to test AI’s role as a reader/evaluator by running a simulation with multiple AI agents participating in a book club discussion. There will be multiple, separate AI agents, each with different model configurations and system prompts to define different personalities. There will be 1 discussion guide and 3 reader/discussion participants.

---

## Literary Reference

**“Division by Zero”** by Ted Chiang. This novella lends itself well to different personalities having different feelings, opinions, and interpretations.

---

## Agents

### Reader Agents

- **Paul** — Math professor, 65-year-old male, Christian, traditionalist, serious, rigid, and a theorist himself. He is very reputable among his students and fellow researchers. He will focus on his knowledge of math history and the setup of the self-contradictory proof in the story. He’s in a respectful but loveless relationship with his wife of 40 years. They have 3 children, all of whom have moved out decades ago. He believes in harmony in relationships over passion or deep spiritual connections.

- **Vanessa** — Software engineer, 22-year-old female, politically centrist, career-oriented, ambitious, tech-savvy, and practical. She is mostly rational, but also young, immature, and impulsive at times. She’s also a creative experimentalist, making a lot of hypotheses and attempts both in reading and in life. She is single and has been struggling with the Bay Area dating scene for 2 years, tired of all the materialistic tech bros. She strongly believes she will only find someone who shares her values to spend her life with.

- **Tyler** — Artist, 30-year-old male, liberal, creative, emotional, empathetic, and sometimes chaotic. He has been with his fiancée for 8 years and recently gotten engaged. She has been very supportive of his art career, even if she doesn’t quite understand it and has very different values. He has also been struggling with depression for a long time and has suicidal thoughts, so he will relate to the graphic descriptions of suicidal attempts and the psych ward.

### Discussion Guide Agent

- **Olivia** — Librarian, 35-year-old female. She hosts the book club discussion, follows the meeting agenda, asks questions to prompt discussion among the three readers, and steers them back on topic when the conversation drifts. She will try to stay neutral and not participate in the discussion herself as much as possible.

> **Setting:** The four of them have known each other and have been participating in a weekly book club discussion for a year.

---

## Simulation Stages

**Stage 1 — Reading (private)**
Each agent independently reads the story and writes private notes — what stood out, their emotional and intellectual reactions, personal connections, and talking points they want to raise. Notes are never shared with the other agents; they are injected only into that agent's own context during the discussion.

**Stage 2A — Structured Discussion**
Olivia opens the meeting with a first question. The three readers then take turns in fixed order (Paul → Vanessa → Tyler). Each turn, the agent privately thinks first (an inner thought visible only in the log), then speaks. Only the spoken response enters the shared transcript. Olivia moderates briefly between rounds to deepen or redirect the conversation.

**Stage 2B — Free Discussion**
After the structured rounds, Olivia transitions the group into open conversation and then mostly steps back. Readers talk *directly to each other* — short, reactive, 1–2 sentence responses. Who speaks next is determined by who the last speaker addressed by name; if no one is named, the next reader in rotation responds. Olivia steps in lightly every few exchanges with a one-line nudge to keep things from stalling, then closes the meeting at the end.

---

## Outcomes & Expectations

We want to see if the agents will “act” according to their personalities — whether their different opinions will spark new ideas and perspectives, or whether the agents will get stuck in a loop and converge to a single viewpoint. We also want to see if their different background stories prompt interesting opinions, or if the agents end up only reproducing what was available in their model training data.


---

## Project Structure

```
.
├── main.py          ← entry point (run this)
├── agents.py        ← Agent & DiscussionGuide classes + all 4 system prompts
├── simulation.py    ← Simulation orchestration (Stage 1 + Stage 2)
├── story.txt        ← detailed synopsis of "Division by Zero"
├── requirements.txt
├── .env.example
└── output/          ← auto-created; discussion logs saved here
```

---

## How to Run

1. Copy `.env.example` → `.env` and add your OpenAI API key.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. *(Optional)* Replace `story.txt` with the full text of *Division by Zero* for richer agent responses.
4. Run the simulation:
   ```
   python main.py
   ```

**Optional flags:**
- `--rounds N` — number of structured discussion rounds (default: 3)
- `--free-exchanges N` — number of back-and-forth exchanges in the free discussion phase (default: 8)
- `--olivia-every N` — how often Olivia steps in during free discussion, in exchanges (default: 4)
- `--story myfile.txt` — use a custom story file
- `--stage1-only` — run only Stage 1 (private reading & note-taking)

The full transcript — including each agent's private inner thoughts — is automatically saved to `output/discussion_<timestamp>.txt`.
