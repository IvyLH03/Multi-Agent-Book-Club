"""
simulation.py — Orchestrates the two-stage book club simulation.

Stage 1 — Reading:
  Each reader agent independently reads the story and writes private notes.
  Notes are stored on the agent object and never shared with other agents.

Stage 2 — Discussion:
  Part A — Structured rounds:
    Olivia opens the meeting.
    Reader agents take turns (Paul → Vanessa → Tyler), each producing a
    private inner thought and a public spoken response.
    Olivia moderates between rounds.
  Part B — Free discussion:
    Olivia signals the shift to open conversation.
    Agents respond casually and reactively — no inner thought, shorter turns.
    Olivia gives a light nudge each exchange to direct or open the floor;
    the named agent (or next in rotation) replies.
    Olivia closes the meeting at the end.

Output is printed to the console and saved to output/discussion_<timestamp>.txt.
"""

import os
import re
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

    # ─────────────────────────────────────────────
    # Free discussion helpers
    # ─────────────────────────────────────────────

    def _pick_next_speaker(self, last_content: str, last_speaker_name: str) -> Agent:
        """
        Determine who speaks next in free discussion.
        Only the last sentence of `last_content` is scanned for a name, because
        that's where direct address lives ("...What do you think, Tyler?").
        Scanning the full text causes false positives when earlier names are
        mentioned in passing ("I see your point, Paul, but... Tyler?").
        Falls back to the next reader in rotation if no name is found.
        """
        # Split on sentence-ending punctuation and take the final fragment
        sentences = [s.strip() for s in re.split(r'[.!?]', last_content.strip()) if s.strip()]
        search_text = sentences[-1] if sentences else last_content

        for agent in self.readers:
            if agent.name == last_speaker_name:
                continue  # the speaker can't address themselves
            if re.search(r'\b' + re.escape(agent.name) + r'\b', search_text, re.IGNORECASE):
                return agent
        # Fallback: next in rotation
        names = [a.name for a in self.readers]
        try:
            idx = names.index(last_speaker_name)
        except ValueError:
            idx = -1
        return self.readers[(idx + 1) % len(self.readers)]

    # ─────────────────────────────────────────────
    # Part B — Free discussion
    # ─────────────────────────────────────────────

    def stage2b_free_discussion(self, num_exchanges: int = 24, olivia_every: int = 4):
        self._log()
        self._divider("═")
        self._log("STAGE 2B  ·  FREE DISCUSSION")
        self._divider("═")
        self._log()

        # Olivia signals the shift, then mostly steps back
        transition = self.guide.transition_to_free_discussion(self.public_history)
        self.public_history.append({"speaker": "Olivia", "content": transition})
        self._log(f"Olivia: {transition}")
        self._log()

        # Kick off with the first reader so there's something to react to
        first_speaker = self.readers[0]
        first_reply = first_speaker.free_reply(self.public_history)
        self.public_history.append({"speaker": first_speaker.name, "content": first_reply})
        self._log(f"{first_speaker.name}: {first_reply}")
        self._log()
        last_speaker_name = first_speaker.name
        last_content = first_reply

        for exchange_num in range(1, num_exchanges + 1):
            # Olivia steps in lightly every olivia_every exchanges
            if exchange_num % olivia_every == 0:
                nudge = self.guide.nudge(self.public_history)
                self.public_history.append({"speaker": "Olivia", "content": nudge})
                self._log(f"Olivia: {nudge}")
                self._log()
                # Olivia's nudge may name someone; treat it as the last content for picking
                last_content = nudge
                last_speaker_name = "Olivia"  # so _pick_next_speaker won't skip Olivia

            # Readers talk directly to each other
            speaker = self._pick_next_speaker(last_content, last_speaker_name)
            reply = speaker.free_reply(self.public_history)
            self.public_history.append({"speaker": speaker.name, "content": reply})
            self._log(f"{speaker.name}: {reply}")
            self._log()

            last_speaker_name = speaker.name
            last_content = reply

    # ─────────────────────────────────────────────
    # Entry point
    # ─────────────────────────────────────────────

    def run(self, story_text: str, num_rounds: int = 3, free_exchanges: int = 24, olivia_every: int = 4):
        """Run both stages, then save the full log to a file."""
        self.stage1_reading(story_text)
        self.stage2_discussion(num_rounds)
        self.stage2b_free_discussion(free_exchanges, olivia_every)
        # Closing (moved here so it wraps both parts)
        self._log()
        self._divider("─")
        self._log("  Olivia closes the meeting:")
        self._divider("─")
        closing = self.guide.close_discussion(self.public_history)
        self._log(f"\nOlivia: {closing}")
        self._log()
        self._divider("═")
        self._save()
