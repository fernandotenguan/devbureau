# What's New in DevBureau

**English** · [Português](RELEASE_NOTES_pt-BR.md)

What changes for you in each version, in plain language. `npx devbureau update` shows these notes since the version you had installed.

---

### [3.42.0] - 2026-09-24
- **Safeguards on Mac and Linux:** the automatic checks now work on all three systems. On Mac they used to be off without any warning. Installing also works now on Windows with the default Python install.
- **Refreshed user guide:** updated installation, a section on what the kit guards on its own and another on updating or removing it. The guide now ships in the package and is linked at the top of the README.
- **Stricter code reviews:** every problem flagged comes with the concrete scenario in which it fails. Without a scenario it becomes a question, not an alarm.
- **The agent doesn't undo what isn't its own:** changes and files you (or another session) are working on are never reverted or deleted. After installing dependencies, it checks whether anything changed by accident.
- **Fewer security false alarms:** reviews skip proven-harmless cases but keep pressing on what matters to anyone selling SaaS, such as attempt limits on login and payments.
- **Sites that look less alike:** when you don't set a style, colors or layout, the design specialist draws from curated options instead of repeating the same choice. Text you provide goes in exactly as written.
- **Cleaner package:** the kit's internal maintenance files no longer ship with the install. If your previous version brought them into your project, this update removes them, as long as you haven't changed them.

### [3.41.0] - 2026-09-10
- **New automatic locks:** the kit blocks the agent if it tries to write a password or access key into a file, delete or disable a test to make it "pass", or edit the main version of a shared project directly.
- **Rules survive long conversations:** when the tool summarizes the history, the kit re-inserts the essential rules.
- **Dead ends get recorded:** an approach that failed is noted so it isn't tried again the following week.
- **Important fixes:** the automatic sync at the start of each session works again, and the security check now actually stops critical problems it used to only report.

### [3.40.1] - 2026-08-17
- **Each project has its own memory:** every new project starts with an empty memory. It used to inherit the kit's own internal notes.

### [3.40.0] - 2026-08-17
- **Memory search by topic:** the agent finds lessons and mistakes already recorded before repeating them.
- **Quality warnings:** code changed without a matching test, and docs pointing at files that no longer exist, are now flagged.
- **Risk measured, not guessed:** before a sensitive change, the kit measures how many parts of the project depend on that file.
- **Brazilian data protected:** the personal-data check recognizes CNPJ, RG and CEP, besides CPF and phone numbers.

### [3.39.0] - 2026-08-13
- **Plans that avoid rework:** tasks are split by complete, testable feature, never "the whole database first, then the whole screen".
- **Two views on risky changes:** one review checks whether the work matches the request, another, independent one checks code quality.
- **Look before updating:** `npx devbureau update --dry-run` shows what would change without touching anything.

### [3.38.0] - 2026-08-11
- **More direct answers:** simple questions and small fixes are handled right away, without a round of questions.
- **Leaner rules:** the set loaded into every conversation got smaller, which lowers cost without loosening the safety locks.

### [3.36.1] - 2026-08-09
- **Second opinion on risky plans:** an independent reviewer reads the plan before it runs.
- **Impact map:** the kit shows which files a change would affect.

### [3.36.0] - 2026-07-13
- **An approved plan runs without interruptions:** once you approve, the agent works without asking permission at every step, but still asks before publishing or deleting anything.
- **Design requires the specialist:** the agent doesn't touch the visuals without first reading the design specialist's rules.
- **Hover effects:** a new collection of effects for buttons, cards and links.
