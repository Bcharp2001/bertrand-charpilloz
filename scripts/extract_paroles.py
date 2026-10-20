"""Extrait les paroles propres (sans indications de production) des fichiers paroles_et_style."""
import re, sys
def clean(path):
    s = open(path, encoding='utf-8').read()
    s = s.split("**Paroles avec", 1)[1].split("\n", 1)[1].split("**Anecdote", 1)[0]
    s = s.replace("\\[", "[").replace("\\]", "]").replace("\\!", "!")
    out, cur = [], 0
    for line in s.split("\n"):
        l = line.strip()
        if not l:
            continue
        m = re.fullmatch(r"\*{0,2}\[(.*)\]\*{0,2}", l)
        if m:
            if len(m.group(1)) < 32 or cur >= 4:
                out.append(""); cur = 0
            continue
        if l.isupper() and len(l) > 3:
            continue
        out.append(l); cur += 1
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    open(dst, "w", encoding="utf-8").write(clean(src))
