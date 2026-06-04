# Instrument catalog

The six shipped instruments, what each is for, and its template + worked example. Every template
carries a DRAFT/scaffold banner, a required-elements checklist, inline `[⚠ ATTORNEY: ...]` flags,
and a consolidated attorney-flags section. Omitting a required element is the most common way these
instruments fail in court — the checklist is load-bearing, not decorative.

| Instrument | When it applies | Output | Template | Worked example |
| --- | --- | --- | --- | --- |
| CWA §505 notice of intent | Pre-suit notice for a Clean Water Act citizen suit | 60-day notice of intent | [`cwa-505-notice-of-intent.md`](../../../templates/cwa-505-notice-of-intent.md) | [`cwa-304m-deadline-suit.md`](../../examples/cwa-304m-deadline-suit.md) |
| CAA §304(a)(1) emission-violation notice | Emission violation, served on Administrator + State + violator | 60-day notice | [`caa-304-emissions-notice.md`](../../../templates/caa-304-emissions-notice.md) | [`caa-304-emissions-notice.md`](../../examples/caa-304-emissions-notice.md) |
| CAA §304(a)(2) failure-to-act notice | Agency failure to perform a nondiscretionary duty | 60-day notice on the Administrator | [`caa-304-failure-to-act-notice.md`](../../../templates/caa-304-failure-to-act-notice.md) | [`caa-304-failure-to-act-suit.md`](../../examples/caa-304-failure-to-act-suit.md) |
| Rulemaking petition | Asking an agency to make or change a rule (no court) | Administrative petition | [`rulemaking-petition.md`](../../../templates/rulemaking-petition.md) | [`rulemaking-petition.md`](../../examples/rulemaking-petition.md) |
| Deadline complaint (CWA / CAA) | First court filing after the notice period runs | "Failure to perform a nondiscretionary duty" complaint | [`cwa-505-deadline-complaint.md`](../../../templates/cwa-505-deadline-complaint.md) · [`caa-304-deadline-complaint.md`](../../../templates/caa-304-deadline-complaint.md) | [`cwa-304m-deadline-suit.md`](../../examples/cwa-304m-deadline-suit.md) |
| Consent-decree scaffold | Negotiated resolution of a deadline/duty suit | Statute-agnostic decree scaffold (no terms proposed) | [`consent-decree-deadline.md`](../../../templates/consent-decree-deadline.md) | [`cwa-304m-deadline-suit.md`](../../examples/cwa-304m-deadline-suit.md) |
| State ERA packet | A state-constitution environmental right may apply | Per-state orientation packet, law-as-of stamped | [`state-era-pa.md`](../../../templates/state-era-pa.md) · [`state-era-mt.md`](../../../templates/state-era-mt.md) · [`state-era-ny.md`](../../../templates/state-era-ny.md) · [`state-era-hi.md`](../../../templates/state-era-hi.md) | [`state-era-pa.md`](../../examples/state-era-pa.md) |

## Notes on use

- **Standing, jurisdiction, and venue are pleaded, not asserted.** The deadline complaints scaffold
  these elements and flag them for you to establish on the facts — they are not represented as met.
- **The consent-decree scaffold proposes no terms.** Every term is left blank for the parties to
  negotiate; the software supplies structure, not substance.
- **State ERA packets are framed by maturity of the law.** Pennsylvania (Art. I §27) and Montana are
  developed; New York's Green Amendment and Hawaiʻi (art. XI) are framed as **developing** law and
  each packet carries a law-as-of stamp. Treat the developing packets as orientation, not settled
  doctrine.
