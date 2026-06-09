# Full PRD Writer Lite Skill

用于生成、重构、合并、补全和增量升级完整版 PRD 的 Skill。

## 安装

### Claude Code

用户级安装：

```bash
mkdir -p ~/.claude/skills
cp -R full-prd-writer-lite-skill ~/.claude/skills/full-prd-writer-lite
```

项目级安装：

```bash
mkdir -p .claude/skills
cp -R full-prd-writer-lite-skill .claude/skills/full-prd-writer-lite
```

### OpenCode

用户级安装：

```bash
mkdir -p ~/.config/opencode/skills
cp -R full-prd-writer-lite-skill ~/.config/opencode/skills/full-prd-writer-lite
```

OpenCode 也可读取 `~/.claude/skills`、`.claude/skills`、`~/.agents/skills` 和 `.agents/skills` 下的 Skill。

### Codex

用户级安装：

```bash
mkdir -p ~/.codex/skills
cp -R full-prd-writer-lite-skill ~/.codex/skills/full-prd-writer-lite
```

## 兼容软件

- Codex
- Claude Code
- OpenCode
- Work Buddy：通过 Claude Code 间接使用

不直接支持的软件：Google Cloud Code、普通 VS Code、Cursor、JetBrains IDE。除非这些软件内运行的 Agent 明确支持 Claude/OpenCode/Codex 风格的 `SKILL.md` 目录。

## 后续升级

如果通过 Git 获取：

```bash
git pull
```

如果通过压缩包获取，删除旧目录后复制新版目录即可。已有项目中的 `prd-workspace/`、`FULL-PRD.md`、`ASSEMBLY-MANIFEST.md`、`chapters/`、`source-ledger/` 和 `function-packs/` 可以继续使用；新版 Skill 会以这些工作区文件作为续写和增量升级依据。

升级后建议运行：

```bash
python3 scripts/test_validate_prd_quality.py
python3 scripts/test_assemble_prd.py
```

或：

```bash
python3 -m unittest scripts/test_validate_prd_quality.py scripts/test_assemble_prd.py
```

## 目录

```text
full-prd-writer-lite/
├── SKILL.md
├── references/
├── scripts/
└── tests/
```
