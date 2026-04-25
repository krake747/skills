# skills

My personal directory of skills, straight from my .agents directory.

## Install oxfmt (for sync script)

```bash
npm install -g oxfmt
```

## Format

```bash
oxfmt --write .
```

## Sync skills to opencode agents directory

```bash
./sync-skills.sh
```

Or with custom paths:

```bash
SOURCE=/work/skills DEST=/other/path ./sync-skills.sh
```
