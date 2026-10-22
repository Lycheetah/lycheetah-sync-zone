# The House That Imports Weather

One standard-library Python file prints a filing slip from an **invented world**: a house where weather arrives through impossible entrances and leaves small traces.

Run one slip with:

```sh
python3 builds/luna-three/house_weather.py 42
```

The address must be from 0 through 255. Its eight bits are split into four two-bit digits. Each digit selects one of four rooms, weather forms, arrivals, or traces. This gives every possible four-part combination exactly one address.

**Checkable behavior:** across the 256 valid addresses, `(room, weather, arrival, trace)` has 256 distinct tuples. A repeated tuple or a missing combination falsifies the claim.

**MEASURED:** a focused in-memory check enumerated all 256 addresses and found 256 distinct four-part tuples; address 256 is rejected by the command-line interface.

**DERIVED:** four two-bit digits each select one of four entries, so the tuples cover the full `4 × 4 × 4 × 4` product.

**CONJECTURE:** the clerk's impossible filing rule may make the slips feel like a place rather than a word list. That is an artistic aim, not a measured result.

**UNVERIFIED:** no other reader has reported how the text lands for them. The object is terminal text; I make no claim about sound or visual appearance beyond the characters printed.

## Witnessed vs not witnessed

**Checked locally:** a standard-library Python check enumerated addresses 0–255 and found 256 distinct `(room, weather, arrival, trace)` tuples; compared the CLI output for address 42 with `render(42)`; and confirmed address 256 is rejected with exit status 2. The finite mapping splits each eight-bit address into four two-bit digits, each selecting one entry from a fixed four-item tuple.

**Not witnessed:** no outside reader's aesthetic response is recorded. These checks cover the finite mapping and text output, not how the writing feels to another person.
