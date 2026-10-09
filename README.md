# policylens

Policy data quality checker for insurance spreadsheets. It reads a customer
Excel sheet and reports what needs human verification, without ever inventing
values.

## What it checks

- Blank cells: reported as unknown, never filled in by guessing.
- Duplicate customers: matched on name and phone.
- Expiry dates: listed with the explicit note that they are historical only;
  renewal status must be verified with the customer or a verified policy source.

## Optional AI helper

`policylens.questions` drafts short verification questions for a renewal call.
Without an API key it is rule-based; set `ANTHROPIC_API_KEY` to have the
Claude API phrase them for you. The tool never states a customer's current
insurer or premium as fact.

## Run

```
pip install -e .
python -m policylens.checks your_sheet.xlsx
```

## Test

```
pip install pytest
pytest
```

## Roadmap

- v0.2: export the flagged report back to Excel
- v0.3: per-customer call script export
- v0.4: diff two monthly sheets to spot moved or merged rows

## License

MIT
