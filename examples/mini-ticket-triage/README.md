# Mini Ticket Triage — Golden Example

This is intentionally small. It demonstrates a compiled G1 Engineering Pack, not a production application implementation.

Run:

```bash
python ../../scripts/doctor.py --strict .
```

Expected: declared-stage structural/readiness checks PASS with no warnings.

`docs/engineering/work/WP-001.md` is the reference Work Packet: every frontmatter field is filled, the risk level matches the surface (schema + public API → R2), the approver differs from the author, and each acceptance item is traced to a WP.
