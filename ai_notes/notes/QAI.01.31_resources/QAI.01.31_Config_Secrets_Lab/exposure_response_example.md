# Completed practice response: invented label, no real credential

- **Observed:** 25 Sep 2026 at 10:00 local time; an invented value labelled `SIMULATED_KEY_A` appeared in a *hypothetical* practice commit.
- **Scope:** Assume a public remote repository; anyone who accessed its commit history might have seen it. Verify publication time, forks/copies, logs and hypothetical usage. No real remote was created in this lab.
- **Immediate containment:** Mark `SIMULATED_KEY_A` revoked at 10:05 in the exercise. In a real incident, disable it with the issuer; do not rely on deleting text.
- **Replacement:** Mark `SIMULATED_KEY_B` as the replacement at 10:10. In reality, create a new credential with only required permissions and place it through approved secret delivery.
- **Verification:** Confirm old access fails and new access works using the issuer's safe validation procedure; inspect account activity and possible charges. This exercise has no real account to verify.
- **Removal:** Remove the value from the code path. If it entered published history, coordinate repository-specific cleanup; copies may persist. Never place actual secret bytes in this report.
- **Prevention and owner:** Developer checks staging and output; team owner reviews secret scanning, least privilege, spending/usage limits, and rotation process.
- **Status:** Simulation complete; no real key or external account was touched.
