"""
simulation.py — Orchestrates the two-stage book club simulation.

Stage 1 — Reading:
  Each reader agent independently reads the story and writes private notes.
  Notes are stored on the agent object and never shared with other agents.

Stage 2 — Discussion:
  Olivia (the guide) opens the meeting.
  Reader agents take turns responding (Paul → Vanessa → Tyler).
  Each agent produces a private inner thought and a public spoken response.
  Only the spoken response is added to the shared transcript.
  Olivia moderates between rounds, then closes the meeting.

Output is printed to the console and saved to output/discussion_<timestamp>.txt.
"""

import os
from datetime import datetime

from agents import Agent, DiscussionGuide, AGENT_CONFIGS


READER_ORDER = ["Paul", "Vanessa", "Tyler"]


class Simulation:
    def __init__(self, output_dir: str = "output"):
        # Build reader agents in a fixed order
        self.readers: list[Agent] = [
            Agent(
                name=name,
                system_prompt=AGENT_CONFIGS[name]["system_prompt"],
                model=AGENT_CONFIGS[name]["model"],
            )
            for name in READER_ORDER
        ]

        # Build the discussion guide
        self.guide = DiscussionGuide(
            name="Olivia",
            system_prompt=AGENT_CONFIGS["Olivia"]["system_prompt"],
            model=AGENT_CONFIGS["Olivia"]["model"],
        )

        # Public conversation history — list of {"speaker": str, "content": str}
        self.public_history: list[dict] = []

        # Full log (public + inner thoughts) written to file
        self._log_lines: list[str] = []

        # Output file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path = os.path.join(output_dir, f"discussion_{timestamp}.txt")
        self._output_dir = output_dir

    # ─────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────

    def _log(self, text: str = ""):
        """Print to console and buffer for file output."""
        print(text)
        self._log_lines.append(text)

    def _divider(self, char: str = "─", width: int = 60):
        self._log(char * width)

    def _save(self):
        os.makedirs(self._output_dir, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._log_lines))
        self._log(f"\n💾  Full discussion saved → {self.output_path}")

    # ─────────────────────────────────────────────
    # Stage 1 — Reading
    # ─────────────────────────────────────────────

    def stage1_reading(self, story_text: str):
        self._log()
        self._divider("═")
        self._log("STAGE 1  ·  READING  (private — each agent reads alone)")
        self._divider("═")
        self._log()

        for agent in self.readers:
            self._log(f"📖  {agent.name} is reading...")
            notes = agent.read_story(story_text)

            self._log()
            self._divider()
            self._log(f"📝  {agent.name}'s PRIVATE NOTES  (not shared with others)")
            self._divider()
            self._log(notes)
            self._divider()
            self._log()

    # ─────────────────────────────────────────────
    # Stage 2 — Discussion
    # ─────────────────────────────────────────────

    def stage2_discussion(self, num_rounds: int = 3):
        self._log()
        self._divider("═")
        self._log("STAGE 2  ·  DISCUSSION")
        self._divider("═")
        self._log()

        # — Opening —
        self._log("🗣️   Olivia opens the discussion:\n")
        opening = self.guide.open_discussion()
        self.public_history.append({"speaker": "Olivia", "content": opening})
        self._log(f"Olivia: {opening}")

        # — Rounds —
        for round_num in range(1, num_rounds + 1):
            self._log()
            self._divider("─")
            self._log(f"  ROUND {round_num} of {num_rounds}")
            self._divider("─")

            for agent in self.readers:
                self._log(f"\n💬  {agent.name}'s turn:")
                response = agent.generate_response(self.public_history)

                inner = response["inner_thought"]
                spoken = response["spoken"]

                if inner:
                    self._log(f"\n  [💭 {agent.name} — inner thought]")
                    self._log(f"  {inner}")

                self._log(f"\n  {agent.name}: {spoken}")

                # Only the spoken response is public
                self.public_history.append({"speaker": agent.name, "content": spoken})

            # Olivia moderates between rounds (not after the last one)
            if round_num < num_rounds:
                self._log()
                moderation = self.guide.moderate(self.public_history)
                self.public_history.append({"speaker": "Olivia", "content": moderation})
                self._log(f"Olivia: {moderation}")

        # — Closing —
        self._log()
        self._divider("─")
        self._log("  Olivia closes the meeting:")
        self._divider("─")
        closing = self.guide.close_discussion(self.public_history)
        self._log(f"\nOlivia: {closing}")
        self._log()
        self._divider("═")

    # ─────────────────────────────────────────────
    # Entry point
    # ─────────────────────────────────────────────

    def run(self, story_text: str, num_rounds: int = 3):
        """Run both stages, then save the full log to a file."""
        self.stage1_reading(story_text)
        self.stage2_discussion(num_rounds)
        self._save()
