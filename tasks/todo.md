
## 2026-10-07: Stop publishing source files

- [x] .github/workflows/pages.yml: deploy only site files (allowlist) via Actions
- [x] Local dry run of the collect step on a clean clone; caught and fixed _site copying into itself
- [x] Update CLAUDE.md, NOTES.md, build.py comments
- [ ] Commit and push workflow
- [ ] Switch Settings > Pages > Source to "GitHub Actions" and run the workflow
- [ ] Verify live: pages 200, build.py / NOTES.md / CLAUDE.md / .claude/settings.json 404
