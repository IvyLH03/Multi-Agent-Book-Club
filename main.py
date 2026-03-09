"""
main.py — Entry point for the Multi-Agent Literature Discussion Simulation.

Usage:
    python main.py                      # 3 discussion rounds, reads story.txt
    python main.py --rounds 2           # 2 discussion rounds
    python main.py --story myfile.txt   # use a custom story file
    python main.py --stage1-only        # run only Stage 1 (reading / note-taking)

Setup:
    1. Copy .env.example to .env and add your OpenAI API key.
    2. pip install -r requirements.txt
    3. (Optional) Replace story.txt with the full text of "Division by Zero".
    4. python main.py
"""

import argparse
import os
import sys

from dotenv import load_dotenv

# Load .env before importing anything that uses OpenAI
load_dotenv()


def check_api_key() -> bool:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key.startswith("sk-...") or len(key) < 20:
        print("❌  OPENAI_API_KEY is not set or is still the placeholder value.")
        print("    1. Copy .env.example → .env")
        print("    2. Add your real OpenAI API key to .env")
        return False
    return True


def load_story(story_path: str) -> str:
    """Load story text from file, falling back to the built-in synopsis."""
    if os.path.exists(story_path):
        with open(story_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if text:
            print(f"✅  Loaded story from '{story_path}' ({len(text):,} characters)")
            return text

    print(f"ℹ️   '{story_path}' not found or empty — using built-in story synopsis.")
    print("    For richer results, provide the full text of the story in story.txt.\n")

    # Fall back to the synopsis bundled in this repo
    synopsis_path = os.path.join(os.path.dirname(__file__), "story.txt")
    if os.path.exists(synopsis_path):
        with open(synopsis_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    # Last resort: inline minimal summary
    return (
        '"Division by Zero" by Ted Chiang.\n\n'
        "Renee, a brilliant mathematician, proves that arithmetic is self-contradictory. "
        "The discovery destroys her sense of meaning and triggers a mental breakdown and "
        "suicide attempt. Her husband Carl, loving but helpless, watches and wonders "
        "whether their relationship can survive — and whether what he felt was ever "
        "truly love or merely borrowed certainty."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Multi-Agent Literature Discussion Simulation — 'Division by Zero'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        metavar="N",
        help="Number of discussion rounds (default: 3). Each round = all three readers speak.",
    )
    parser.add_argument(
        "--story",
        type=str,
        default="story.txt",
        metavar="FILE",
        help="Path to the story text file (default: story.txt).",
    )
    parser.add_argument(
        "--stage1-only",
        action="store_true",
        help="Run only Stage 1 (private reading / note-taking) and exit.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        metavar="DIR",
        help="Directory to save the discussion log (default: output/).",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    print()
    print("━" * 60)
    print("  Multi-Agent Literature Discussion Simulation")
    print('  "Division by Zero" by Ted Chiang')
    print("━" * 60)
    print()

    # Guard: API key must be present
    if not check_api_key():
        sys.exit(1)

    story_text = load_story(args.story)

    # Late import so OpenAI client is created after load_dotenv()
    from simulation import Simulation

    sim = Simulation(output_dir=args.output_dir)

    if args.stage1_only:
        sim.stage1_reading(story_text)
        sim._save()
    else:
        sim.run(story_text, num_rounds=args.rounds)


if __name__ == "__main__":
    main()
