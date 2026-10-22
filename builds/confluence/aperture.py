"""Pure constructor for bounded, caller-supplied aperture reports."""

import json
import unicodedata


_ALLOWED_OUTCOMES = (
    "FOUND",
    "NOT DETECTED",
    "NO ACCESS",
    "AMBIGUOUS",
    "NO RECORD HERE",
)


def _description(name: str, value: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if any(
        unicodedata.category(character) == "Cc" or character in "\u2028\u2029"
        for character in value
    ):
        raise ValueError(f"{name} must not contain control or line-separator characters")

    cleaned = value.strip()
    if not allow_empty and not cleaned:
        raise ValueError(f"{name} must be a nonempty string")
    return cleaned


def make_slip(
    *,
    target: str,
    boundary: str,
    method: str,
    exposure: str,
    outcome: str,
    signal: str = "",
) -> dict:
    """Return a JSON-safe report while preserving its supplied scope.

    ``signal`` is reserved for ``FOUND``: it is required there and must be empty
    for every other outcome. This function records descriptions; it does not
    perform the search or validate the report independently.
    """
    target = _description("target", target)
    boundary = _description("boundary", boundary)
    method = _description("method", method)
    exposure = _description("exposure", exposure)
    signal = _description("signal", signal, allow_empty=True)

    if not isinstance(outcome, str):
        raise TypeError("outcome must be a string")
    if outcome not in _ALLOWED_OUTCOMES:
        raise ValueError(f"outcome must be one of: {', '.join(_ALLOWED_OUTCOMES)}")
    if outcome == "FOUND" and not signal:
        raise ValueError("signal must be nonempty when outcome is FOUND")
    if outcome != "FOUND" and signal:
        raise ValueError("signal is reserved for outcome FOUND")

    scope = (
        f"target={json.dumps(target, ensure_ascii=False)}; "
        f"boundary={json.dumps(boundary, ensure_ascii=False)}; "
        f"method={json.dumps(method, ensure_ascii=False)}; "
        f"exposure={json.dumps(exposure, ensure_ascii=False)}; "
        f"outcome={outcome}; signal={json.dumps(signal, ensure_ascii=False)}"
    )

    if outcome == "FOUND":
        result = "the supplied report says the signal was found"
    elif outcome == "NOT DETECTED":
        result = "the supplied report says no signal was detected within this scope"
    elif outcome == "NO ACCESS":
        result = "the supplied report says this boundary could not be fully examined"
    elif outcome == "AMBIGUOUS":
        result = "the supplied report says the result was ambiguous"
    else:
        result = "the supplied report says no record appeared within this scope"

    supported_sentence = f"{result}: {scope}."
    limitation = (
        "This is a supplied report, not independent validation. It does not verify "
        "that the described method ran or was complete, and supports no claim "
        "beyond the stated boundary and exposure."
    )

    return {
        "target": target,
        "boundary": boundary,
        "method": method,
        "exposure": exposure,
        "outcome": outcome,
        "signal": signal,
        "supported_sentence": supported_sentence,
        "limitation": limitation,
    }
