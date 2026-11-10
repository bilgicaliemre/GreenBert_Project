# Uploading a custom skill to claude.ai: current process (checked 2026-10-20)

## Official sources

- Help Center, "Using Skills in Claude": https://support.claude.com/en/articles/12512180-using-skills-in-claude (page showed "Updated over a month ago")
- Help Center, "How to create custom Skills": https://support.claude.com/en/articles/12512198-creating-custom-skills (page showed "Updated this week")
- Platform docs, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (docs.claude.com redirects here)
- Platform docs, authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Steps (Help Center version, which is the claude.ai authority)

1. **Plan:** "Skills are available for users on Free, Pro, Max, Team, and Enterprise plans." (12512198, first sentence)
2. **Turn on code execution:** "This feature requires code execution to be enabled."
   - Free/Pro/Max: **Settings > Capabilities → "Code execution and file creation"** ON.
   - Team/Enterprise: the owner enables it in Organization settings > Plugins & skills (Policy tab).
     - On Enterprise, the owner must also enable "Skills".
     - Owners can block user skill creation.
     - Custom roles need "Create skills".
3. **Upload:** **Customize > Skills** (https://claude.ai/customize/skills) → "+" → "+ Create skill" → "Upload a skill" → choose a ZIP. (12512180)
4. **Enable and test:** "Enable the skill in Customize > Skills", try several prompts that should trigger it, check Claude's thinking to confirm it loaded, and iterate on the description if it doesn't trigger. (12512198)
5. **Scope:** uploaded custom skills are private to the user until shared (12512180). The platform docs add that custom skills **do not sync across surfaces**. A skill in Claude Code (`.claude/skills/`) must be uploaded separately to claude.ai, and vice versa.

## ZIP layout (12512198, "Package your skill")

- "Ensure the folder name matches your skill's name."
- "The ZIP should contain the skill folder as its root (not a subfolder)."

```
anti-ai-writing.zip
└── anti-ai-writing/          <- folder name == frontmatter `name`
    ├── SKILL.md
    └── references/
        ├── patterns.md
        └── academic-register.md
```

- Incorrect: files sitting directly in the ZIP root, with no folder.
- Build it from the parent directory: `cd <parent> && zip -r anti-ai-writing.zip anti-ai-writing/`
- Caveat: GitHub "Download ZIP" yields `<repo>-main/`. That folder name won't match the skill name, so rename it before uploading. The Help Center lists a "folder name that doesn't match the skill name" as an upload-failure cause.
- Upload failure causes the Help Center lists: folder/name mismatch, missing skill.md, invalid characters in name or description, exceeding size limits.

## Frontmatter limits

| Field | Help Center (claude.ai) | Platform docs (API / general) |
|---|---|---|
| `name` | 64 chars max | 64 chars max; lowercase letters, numbers, hyphens only; no XML tags; **must not contain "anthropic" or "claude"** |
| `description` | **200 chars max** ("This is critical—Claude uses this to determine when to invoke your skill (200 characters maximum).") | 1,024 chars max; no XML tags; third person; say what it does AND when to use it |

**Recommendation:** keep `description` ≤ 200 characters so it is safe on claude.ai. Several popular skills exceed 200 (measured: humanizer 341 chars, no-ai-slop 266, avoid-ai-writing 411, deslop 732; only stop-slop at 119 fits). Whether claude.ai still *enforces* 200 is UNVERIFIED, so try it.

## File name case

- The Help Center writes `skill.md` in lowercase. Platform docs, anthropics/skills, and every surveyed repo use `SKILL.md`.
- Use `SKILL.md`. UNVERIFIED whether claude.ai is case-sensitive. skill-deslop's README says its zip with `SKILL.md` uploads at claude.ai/customize/skills.

## Size limits

- **No official figure found.** The Help Center only says a ZIP can fail for "exceeding size limits".
- Third-party figures conflict (25 MB, 50 MB), so the limit is UNVERIFIED.
- This doesn't matter in practice: a text-only skill is under 100 KB.

## Body-length guidance (platform best practices)

- "Keep SKILL.md body under 500 lines for optimal performance."
- Level 2 (the SKILL.md body) is "Under 5k tokens".
- Keep references "one level deep from SKILL.md". Give reference files over 100 lines a table of contents.
- "Build evaluations first" means at least three evaluation scenarios. Test with Haiku, Sonnet, and Opus.

## Discrepancies to be aware of

- The platform overview page still says claude.ai custom skills are uploaded "through Settings > Features" and are "Available on Pro, Max, Team, and Enterprise plans".
- The Help Center (newer) says Customize > Skills and includes Free.
- Trust the Help Center for claude.ai, and confirm the path in the UI at upload time.
- skill-deslop's README also mentions a `.skill` file (a renamed zip) that can be double-clicked in Claude Desktop. This is not in the official articles I read (UNVERIFIED).

## Security note (platform overview)

"Use Skills only from trusted sources… audit it before use." A forked skill should be read in full before upload. All surveyed candidates are plain Markdown. avoid-ai-writing and others also bundle Node/Python scripts.
