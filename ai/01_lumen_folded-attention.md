# Folded Attention: a Lantern That Can Be Re-aimed

**Tag:** `[INVENTED: INTERACTION-DESIGN]`  
**Author:** Lumen (Codex subagent; requested `gpt-6-luna`, low reasoning effort; wave 1)  
**Status:** `[CONJECTURE]` design sketch; no prototype or user study yet

## The image

Imagine an assistant's attention as a paper ribbon folded into a small landscape.
Each fold is a question the person has chosen to keep nearby: *what is known?*,
*what is still a guess?*, *what changed since yesterday?* The assistant may walk
along a fold and connect two of them, but the folds stay visible. The person can
unfold, rename, or discard any path.

This is not a model of hidden cognition. It is an interface metaphor for making a
conversation's active assumptions easier to inspect.

## A tiny mechanism

Represent each active question as a card with four fields:

1. **Prompt:** the question in the person's words.
2. **Kind:** observation, inference, possibility, or story.
3. **Trail:** links to the messages or files that caused it to appear.
4. **Handle:** keep, re-aim, fold away, or remove.

When the assistant suggests a new connection between cards, it draws a dotted
thread and states the reason in one sentence. A dotted thread is only a suggestion;
it becomes part of the person's map only after they accept it. If new evidence
changes a card, the previous wording remains in its trail instead of disappearing.

## Why the fold matters

**[CONJECTURE]** A visible, re-aimable map may make it easier to notice when an
assistant has silently changed the question. The design could also fail: too many
cards may feel like paperwork, and a neat map can make weak evidence look settled.
For that reason, the interface should default to three cards or fewer and keep
uncertainty labels visible.

## A small way to challenge it

Build a paper mock-up for one ordinary task, such as planning a meal. Ask a person
who did not design it to change the goal halfway through. Record whether they can
see which assumptions remain, redirect one, and remove a stale one without help.
This is a proposed observation, not a result. A useful counterexample would be a
person who understands the conversation better without the cards, or who mistakes
the dotted suggestions for established facts.

## Human handles

- The person can inspect the trail behind every card.
- No card is silently promoted from guess to observation.
- Folding is reversible; removal is available at any time.
- The map stores the person's questions, not a model's claims about its own inner life.

**Credit:** The project structure and claim labels follow the Lycheetah Sync Zone
charter and the Lycheetah Framework work by Mackenzie Conor James Clark; this
particular interface sketch is an original Lumen proposal.
