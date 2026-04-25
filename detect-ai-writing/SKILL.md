---
name: detect-ai-writing
description:
  Use when user asks to review, check, audit, detect, or improve writing quality. Also use when user
  mentions "AI detection", "human-sounding writing", "avoid AI patterns", "natural writing", or
  receives feedback that writing sounds "too AI-generated" or "robotic".
---

# AI Writing Detection

Flag AI patterns and suggest human rewrites.

## Workflow

1. **Ask context** - What type of writing? (email, document, code comments, blog post)
2. **Get files** - Ask for file paths or paste text to analyze
3. **Scan and flag** - Identify patterns with severity levels
4. **Show findings** - Display issues with rewrite suggestions
5. **Apply rewrites** - Ask user before applying changes

## Severity Levels

| Level    | Patterns                                           |
| -------- | -------------------------------------------------- |
| Critical | Em dashes (—) overuse, formulaic openings/closings |
| High     | Overused verbs, adjectives, filler words clusters  |
| Medium   | Transitions, hedging language, passive voice       |
| Low      | Individual filler words, light intensifiers        |

## Pattern Guide

### Critical: Em Dashes

Replace with commas, colons, or parentheses.

| Instead of                                   | Use                                          |
| -------------------------------------------- | -------------------------------------------- |
| results, which were surprising, showed       | results, which were surprising, showed       |
| approach, unlike traditional methods, allows | approach, unlike traditional methods, allows |

### Critical: Formulaic Phrases

**Openings:** "In today's fast-paced world...", "In today's digital age...", "It's important to
note...", "Let's delve into..."

**Closings:** "In conclusion...", "To sum up...", "At the end of the day...", "All things
considered..."

### High: Overused Verbs

delve, leverage, optimise, utilise, facilitate, foster, bolster, underscore, unveil, navigate,
streamline, enhance, ascertain, elucidate

→ explore, use, improve, help, encourage, strengthen, reveal, manage, simplify, find out, explain

### High: Overused Adjectives

robust, comprehensive, pivotal, crucial, vital, transformative, cutting-edge, groundbreaking,
innovative, seamless, intricate, nuanced, multifaceted, holistic

→ strong, complete, key, important, new, smooth, complex

### High: Filler Words

basically, actually, essentially, interestingly, clearly, obviously, quite, really, significantly,
simply

→ Remove or replace with specific meaning

### Medium: Transitions

furthermore, moreover, notwithstanding, that being said, at its core, to put it simply, in the realm
of, in today's world

→ also, however, essentially, in short, in, currently

### Medium: Hedging

"it is believed that", "it seems that", "one could argue", "it is often the case that"

→ Remove hedge or be direct

### Medium: Passive Voice

Overuse of "was/were + past participle"

→ Convert to active voice

### Academic Tells

"shed light on", "pave the way for", "a myriad of", "a plethora of", "paramount", "prior to",
"subsequent to", "in light of", "with respect to"

→ clarify, enable, many, essential, before, after, because, regarding

### Additional Tells

- Nominalization: "make a decision" → "decide", "give consideration to" → "consider"
- Same-word repetition (adjacent duplicates)
- Uniform sentence length (all sentences same length = AI)

## Output Format

```
## Analysis: [filename]
### Flags Found
| Severity | Pattern | Instance | Location |
|----------|---------|---------|----------|
| Critical | En dash used as example | "results, which were..." | Line 3 |
| High | "In today's..." | "In today's world" | Line 1 |

### AI Confidence
~[X]% likely AI-assisted

### Rewrites
[Line 3] "The results, which were surprising, showed..." → "The results, which were surprising, showed..."
```

## Self-Check

1. Read aloud, if it sounds unnatural, revise
2. Ask "Would I say this in conversation?"
3. Vary sentence lengths
