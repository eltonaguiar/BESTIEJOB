# SUCCESS_PACKS_MERGED

Every `SUCCESS_PACK*` file found on any branch of `eltonaguiar/bestiejob`, copied here
onto `main` so all the packs sit in one place. Originals are untouched.

| File | Author / model | Source branch | Lines |
|------|----------------|---------------|-------|
| `SUCCESS_PACK_FREEBUFF.MD` | Freebuff | `main` | 126 |
| `SUCCESS_PACK_KILO.MD` | Kilo | `restore-truncated-board-2026-11-03` | 248 |
| `SUCCESS_PACK_KILOCODE.MD` | Kilocode | `restore-truncated-board-2026-11-03` | 215 |
| `SUCCESS_PACK_MUSE.MD` | MUSE (arlo) | `arlo/success-pack-2026-11-05` | 167 |
| `SUCCESS_PACK_OPENCODE.MD` | opencode | `restore-truncated-board-2026-11-03` | 398 |

Search used (all remote branches):

```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  git ls-tree -r --name-only "$b" | grep -i success_pack | sed "s|^|$b: |"
done
```

Branches that existed at the time of the sweep but carried no pack: the `Copilot/*`,
`buffy/*`, `hermes/*`, `docs/*`, `feat/*` and `inbox/*` lines.

To refresh after another agent lands a pack:

```bash
git fetch --all --prune
# repeat the loop above, then copy any new file into this folder
```
