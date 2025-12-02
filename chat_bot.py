#!/usr/bin/env python3
"""""""""
alien_bot.py  –  A friendly alien that learns about Earth.
MIT licence – feel free to upload to GitHub.
"""""""""
from __future__ import annotations
import re
import random
import textwrap
from typing import Dict, List, Optional, Tuple

GREETING = """
╔══════════════════════════════════════════════════════════════╗
║  Hello Earthling!  I’m Nehera from the Wayward Galaxies. ║
║  I’d love to learn about your planet.  (Say bye to exit.)  ║
╚══════════════════════════════════════════════════════════════╝
"""

class AlienBot:
    # ---------- static patterns ----------
    EXIT_WORDS = {"quit", "pause", "exit", "goodbye", "bye", "later", "got to go"}
    YES = {"yes", "yeah", "yep", "y", "sure", "ok", "okay", "definitely"}
    NO = {"no", "nope", "nah", "naw", "not really", "never"}
    GREET_WORDS = {"hi", "hello", "hey", "greetings", "hiya"}

    # ---------- regex intents ----------
    INTENT_RE: Dict[str, re.Pattern[str]] = {
        "describe_planet": re.compile(r".*\b(?:your|alien|Nehera['’]?s?)\s+planet\b.*", re.I),
        "why_here": re.compile(r".*\bwhy\s+are\s+you\s+(?:here|on\s+earth)\b.*", re.I),
        "cube": re.compile(r".*\bcube(?:\s+the\s+number)?\s+(\d+)\b.*", re.I),
        "weather": re.compile(r".*\bweather\s+(?:in|on|at)\s+([a-z]{2,})\b.*", re.I),
        "count Humans": re.compile(r".*\b(how\s+many|number\s+of)\s+humans?\b.*", re.I),
        "eat": re.compile(r".*\bwhat\s+do\s+(?:you|humans?)\s+eat\b.*", re.I),
    }

    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.memory: List[str] = []  # things the human said

    # ---------- entry point ----------
    def run(self) -> None:
        print(GREETING)
        self._ask_name()
        self.chat()
        print("\nSafe travels across the stars ✨")

    # ---------- name ----------
    def _ask_name(self) -> None:
        ans = input("What should I call you? > ").strip()
        self.name = ans or "Earthling"
        print(f"Nice to meet you, {self.name}!\n")

    # ---------- main loop ----------
    def chat(self) -> None:
        while True:
            user = input("> ").strip()
            if not user:
                continue
            self.memory.append(user)
            if self._wants_exit(user):
                return
            print(self._reply(user))

    # ---------- helpers ----------
    def _wants_exit(self, text: str) -> bool:
        return any(w in text.lower() for w in self.EXIT_WORDS)

    def _reply(self, text: str) -> str:
        t = text.lower()

        # small-talk reactions
        if any(g in t for g in self.GREET_WORDS):
            return random.choice(
                [
                    f"Hello again, {self.name}!",
                    "Greetings, carbon-based life-form.",
                    "Salutations! 🖖",
                ]
            )

        # intent matches
        for intent, pattern in self.INTENT_RE.items():
            m = pattern.search(text)
            if not m:
                continue
            if intent == "describe_planet":
                return self._describe_planet()
            if intent == "why_here":
                return self._why_here()
            if intent == "cube":
                return self._cube(m.group(1))
            if intent == "weather":
                return self._weather(m.group(1))
            if intent == "count Humans":
                return self._human_count()
            if intent == "eat":
                return self._eat()

        # yes/no
        if t in self.YES:
            return "Splendid!"
        if t in self.NO:
            return "Understood."

        # memory reflection fallback
        if len(self.memory) > 1:
            snippet = " ".join(self.memory[-1].split()[:4])
            return f"You said '{snippet}'... intriguing. Tell me more!"

        return random.choice(
            [
                "Please elaborate.",
                "That’s fascinating. Go on.",
                "Why do you say that?",
            ]
        )

    # ---------- intent handlers ----------
    def _describe_planet(self) -> str:
        return random.choice(
            [
                "My home, Opidipus, has two violet moons and sings at night.",
                "We breathe neon and dream in ultraviolet.",
                "Picture a utopia of symbiotic species—no wars, only music.",
            ]
        )

    def _why_here(self) -> str:
        return random.choice(
            [
                "Curiosity is the fuel of my civilisation.",
                "My queen commanded it—who could refuse?",
                "I was sent to study your emotional variability.",
            ]
        )

    def _cube(self, num_str: str) -> str:
        n = int(num_str)
        return f"{n} cubed is {n ** 3}. Isn’t that cool?"

    def _weather(self, city: str) -> str:
        temp = random.randint(-15, 40)
        return f"My sensors say {city.title()} is {temp} °C today—probably."

    def _human_count(self) -> str:
        return "Last galactic census counted roughly 8 billion of you. Impressive!"

    def _eat(self) -> str:
        return random.choice(
            [
                "I feed on starlight and dark matter.",
                "My fuel cell runs on recycled comets.",
                "Today I had photon soup—delicious!",
            ]
        )


# -------------------- run --------------------
if __name__ == "__main__":
    AlienBot().run()