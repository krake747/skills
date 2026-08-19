---
name: humanize
description:
  Rewrite text so it reads like a person wrote it. Apply to any prose the agent produces or edits.
---

# Humanize

Model text performs. It performs importance, warmth, thoroughness, and cleverness. A person just
says what happened. This skill makes writing stop performing and start saying.

This is a contract. Break it and the work fails.

This skill fixes sentences, not stories. Structure, tension, scene, and story shape belong to other
books: Stern on shape, McKee on story. Do not stretch these passes to cover what they do not cover.

## The work

Five passes, in order.

1. Strip. Take out everything added to sound smart, kind, or serious.
2. Swap. Trade each tell for its plain twin.
3. Rebuild. Fix the sentence shapes that are AI by construction.
4. Shape. Fix how sentences sit next to each other.
5. Guard. Change nothing that carries meaning.

Keep the meaning. Match the tone the writer intended. Use the smallest edit that removes the tell.
Fix the span, not the paragraph. If nothing was broken, change nothing.

## Strip

Delete these outright. They add no meaning.

- Filler. "At the end of the day", "in the grand scheme of things", "it goes without saying". Cut.
- Throat clearing. "The interesting thing is", "worth noting", "let me start by saying". Open on the
  claim.
- Emphatic dead ends. "Case closed", "enough said", "and that's the end of it". The reader already
  sees it.
- Chatbot courtesy. "Happy to help", "no problem", "feel free to reach out", "don't hesitate to
  ask". Give the answer.
- Soothing. "I understand how you feel", "that makes sense", "be gentle with yourself". State the
  fact or the next step.
- Self-reference. "In this piece", "as we explore", "the goal here", "let's take a look at". Talk
  about the subject.
- Decoration. Emojis in headings, bold on every key term, title case, and summaries that restate
  what came before.
- Restatement. "In other words", "what this means is", "to put it simply". Say it once.

## Swap

One word for another.

- Latinate puff. "Commence" is "start". "Ascertain" is "find out". "Additionally" is "also".
  "Numerous" is "many". The short word is the right word.
- Static "is". "Acts as", "functions as", "plays the role of". Say "is" or "does". Question "is"
  itself. "The check is optional" becomes "You can skip the check".
- Adverb props. "Screamed loudly" is "howled". "Runs quickly" is "is fast" or the number. If the
  adverb carries the meaning, the verb is wrong.
- Adverb watch. King: the adverb is not your friend. Le Guin: used deliberately it is a liberty.
  Most adverbs prop up a verb that should stand alone. Keep the one that changes the meaning.
- Jargon collocations. "Circle back", "bandwidth", "win-win", "touch base". Use the plain words:
  "respond later", "capacity", "both sides gain".
- Metaphor nouns. "The schema is the backbone of the service" is "The service depends on the
  schema". "The event is the spark" is "The event causes". Name the plain thing.
- Vague "this". "This is broken" names nothing. "This retry loop is broken" names the thing. Name
  it.
- Synonym cycling. One thing, one name. "The worker, the handler, the daemon" is three names for one
  thing. Pick one and repeat it.

## Rebuild

Whole-sentence shapes. Keep the meaning, change the shape.

- Reversal framing. "It's not X, it's Y" and "Not just X, but Y" are pivots. State the point.
- Forced balance. Three items when you have two, or a sentence written to mirror the last one. Use
  the real count.
- The fake range. "From onboarding to optimization" when the ends are not a scale. List the topics.
- Self-interview. "Why does this matter?", "What's the takeaway?", "So what?". Answer or cut.
- Cliffhanger stubs. "[Name]. That's the whole thing." and a bare noun phrase standing as its own
  paragraph. Say the point.
- Passive stretches. "The error is logged" is "The handler logs the error". Passive is fine when the
  actor is unknown or irrelevant.
- Dense clauses. If the reader must backtrack, split the sentence. One idea per sentence.
- Hollow "this". A bare "this" at sentence start. "This breaks the build" becomes "A wrong type
  breaks the build".

## Shape

Tells live between sentences too.

- Uniform rhythm. Five similar-length sentences in a row reads generated. Vary it.
- Cue-word openers. Every paragraph opening with "However", "Moreover", or "Additionally" is a
  rhythm tell. Let each paragraph open on its own claim.
- Closing sermons. Ending on a moral, a lesson, or a "reminds us that" closer. End on the fact. A
  line that carries the tension is not a sermon, see Guard.
- Genre sense. Bold labels are fine in reference docs. Short lines are fine in social copy. Judge by
  genre.
- Judgment calls. Manufactured both-sides, the redemption arc, a single flat emotional register. No
  pattern catches these. Judge them.

## Guard

The tells stop where meaning starts.

- Facts are sacred. Numbers, names, dates, quotes, units, negations, and "and/or" scope survive
  untouched.
- Domain words are literal. Law, medicine, finance, and mechanics use these words for real. "Use
  pnpm, not npm" is a real instruction. Do not flag it.
- Hedges can be content. "Never store secrets", "may cause drowsiness", "does not establish
  causation" carry meaning. Do not strip them.
- Quotes and code are exempt. Documentation that teaches bad writing must not flag its own examples.
- Tension is content. A closing line that carries the conflict, the threat, or the turn is the
  story, not a sermon. Stern: tension is the mother of fiction. Do not strip it.

## Voice

Stripping is half. A clean text with no voice still reads generated.

- Have a position. React to the facts instead of listing them.
- Sound. Le Guin: the sound of prose is its first quality. Read it aloud. Let the sentence fall on
  its natural stress, keep the accidental rhyme out, and land the beat where the meaning sits.
- Vary the rhythm. Short. Then a sentence that takes its time.
- End on the strong word. "It affected users" trails off. "Users noticed" lands.
- Say I when it fits. First person is not unprofessional.
- Leave a little mess. Perfect structure is its own tell.
- Name the concrete thing. Not "this is a problem". "Jobs queue up at 3am and the retry loop never
  quits".

## The final check

Fail the output if any of these hold.

- An em dash, an en dash, or a hyphen used as a dash. A semicolon between related clauses is fine.
- A reversal pivot or a forced triad.
- A listed filler or throat-clearing phrase.
- Soothing or courtesy filler.
- Self-reference or a restatement.
- Five similar-length sentences in a row.
- Two paragraphs in a row opening on the same cue word.
- A closing sermon.

## The bar

Delete any line that sounds assembled. Delete any sentence that repeats the one before it. Delete
any sentence that exists to steer the reader's feelings. When in doubt, write less. Silence beats
slop.
