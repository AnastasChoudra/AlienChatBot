#!/usr/bin/env python3
"""
alien_bot.py  –  conversational alien, now with 120 curated questions
MIT licence
"""
from __future__ import annotations
import json
import random
import os
import re
from typing import List, Optional


class AlienBot:
    EXIT_WORDS = {"quit", "pause", "exit", "goodbye", "bye", "later", "got to go", "see you", "farewell", "catch you later", "i'm out", "i am out"}
    YES = {"yes", "yeah", "yep", "y", "sure", "ok", "okay", "definitely", "absolutely", "of course", "certainly", "affirmative", "indeed", "yessir", "yea"}
    NO = {"no", "nope", "nah", "naw", "not really", "never", "nope", "negative", "nay", "absolutely not", "not at all"}
    GREET_WORDS = {"hi", "hello", "hey", "greetings", "hiya", "yo", "salutations", "sup", "good morning", "good afternoon", "good evening", "howdy"}

    # ---------- regex intents ----------
    INTENT_RE = {
        "describe_planet": re.compile(r".*\b(?:your|alien|et cetera['’]?s?)\s+planet\b.*", re.I),
        "why_here": re.compile(r".*\bwhy\s+are\s+you\s+(?:here|on\s+earth)\b.*", re.I),
        "cube": re.compile(r".*\bcube(?:\s+the\s+number)?\s+(\d+)\b.*", re.I),
        "weather": re.compile(r".*\bweather\s+(?:in|on|at)\s+([a-z]{2,})\b.*", re.I),
        "count Humans": re.compile(r".*\b(how\s+many|number\s+of)\s+humans?\b.*", re.I),
        "eat": re.compile(r".*\bwhat\s+do\s+(?:you|humans?)\s+eat\b.*", re.I),
    }

    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.asked: set[str] = set()
        self._load_questions()

    # --------------------------------------------------
    # 1.  QUESTION LOADER
    # --------------------------------------------------
    def _load_questions(self) -> None:
        path = os.path.join(os.path.dirname(__file__), "questions.json")
        with open(path, encoding="utf-8") as fh:
            self.question_bank: dict[str, list[str]] = json.load(fh)

    def next_question(self) -> str:
        """Return a question never asked before (cycle when exhausted)."""
        pool = [q for qs in self.question_bank.values() for q in qs if q not in self.asked]
        if not pool:
            self.asked.clear()
            pool = [q for qs in self.question_bank.values() for q in qs]
        q = random.choice(pool)
        self.asked.add(q)
        return q

    # --------------------------------------------------
    # 2.  CONVERSATION FLOW
    # --------------------------------------------------
    def run(self) -> None:
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  Hello Earthling!  I’m Etcetera from the Wayward Galaxies. ║")
        print("║  I’d love to learn about your planet.  (Say bye to exit.)  ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        self._ask_name()
        self.chat()
        print("\nSafe travels across the stars ✨")

    def _ask_name(self) -> None:
        ans = input("What should I call you? > ").strip()
        self.name = ans or "Earthling"
        print(f"Nice to meet you, {self.name}!\n")

    def chat(self) -> None:
        while True:
            user = input("> ").strip()
            if not user:
                continue
            if self._wants_exit(user):
                return
            print(self._reply(user))

    def _wants_exit(self, text: str) -> bool:
        return any(w in text.lower() for w in self.EXIT_WORDS)

    # --------------------------------------------------
    # 3.  REPLY ENGINE
    # --------------------------------------------------
    def _reply(self, text: str) -> str:
        t = text.lower()

        # small talk
        if any(g in t for g in self.GREET_WORDS):
            return random.choice(["Hello again!", "Greetings 🖖", "Salutations!"])
        if t in self.YES:
            return "Splendid!"
        if t in self.NO:
            return "Understood."

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

        # fallback → ask something new
        return self.next_question()

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


# --------------------------------------------------
if __name__ == "__main__":
    AlienBot().run()