#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
內容檢核：依 Mac 的文案規則檢查 src/content 下的文章。

    python3 scripts/check_content.py              只檢查相對 origin/main 有異動的文章（CI 用）
    python3 scripts/check_content.py --all        檢查全部文章（產報告）
    python3 scripts/check_content.py 檔案1.md ... 檢查指定檔案

規則（market-view、industry-data 為錯誤；insights 只警告）：
  1. 禁用語：scripts/forbidden.txt（! 開頭為錯誤，其餘警告）
  2. 敏感字串：scripts/sensitive.txt（錯誤）
  3. 有成交數字或提到實價登錄 → 必須寫「內政部」+「實價登錄」來源
  4. 必須有「僅供市場參考」免責句（sourceNote 或內文）
  5. 「不是…而是…」句型 → 警告（規則：不武斷）
  6. 門牌 → 警告（實登成交表可有門牌，在手物件不可）；地號 → 錯誤
  7. frontmatter 必須有 title / date / excerpt
結束碼：有錯誤 1，否則 0。
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "src", "content")
STRICT_DIRS = {"market-view", "industry-data"}

def load_list(name):
    out = []
    p = os.path.join(ROOT, "scripts", name)
    if not os.path.exists(p):
        return out
    for line in io.open(p, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out

FORBIDDEN = load_list("forbidden.txt")
SENSITIVE = load_list("sensitive.txt")

def changed_files():
    try:
        base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], cwd=ROOT).decode().strip()
        diff = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD", "--"], cwd=ROOT).decode()
    except Exception:
        return []
    files = [os.path.join(ROOT, f) for f in diff.splitlines() if f.startswith("src/content/") and f.endswith(".md")]
    # 工作區未提交的也算
    try:
        wt = subprocess.check_output(["git", "status", "--porcelain", "--", "src/content"], cwd=ROOT).decode()
        for line in wt.splitlines():
            f = line[3:].strip()
            if f.endswith(".md"):
                files.append(os.path.join(ROOT, f))
    except Exception:
        pass
    return sorted(set(f for f in files if os.path.exists(f)))

def all_files():
    out = []
    for d, _, fs in os.walk(CONTENT):
        for f in fs:
            if f.endswith(".md"):
                out.append(os.path.join(d, f))
    return sorted(out)

def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return "", text
    return m.group(1), m.group(2)

def strip_html(s):
    return re.sub(r"<[^>]+>", " ", s)

def check(path):
    rel = os.path.relpath(path, ROOT)
    section = rel.split(os.sep)[2] if rel.count(os.sep) >= 2 else ""
    strict = section in STRICT_DIRS
    errors, warns = [], []
    text = io.open(path, encoding="utf-8").read()
    fm, body = split_frontmatter(text)
    plain = strip_html(body)
    whole = fm + "\n" + plain

    # 7 frontmatter
    for k in ("title", "date", "excerpt"):
        if not re.search(r"^%s:" % k, fm, re.M):
            errors.append("frontmatter 缺 %s" % k)
    if re.search(r"^draft:\s*true", fm, re.M):
        warns.append("draft: true（不會發布）")

    # 1 forbidden
    for item in FORBIDDEN:
        hard = item.startswith("!")
        w = item[1:] if hard else item
        for m in re.finditer(re.escape(w), whole):
            if whole[max(0, m.start() - 1):m.start()] == "不":   # 「不一定」「不必然」不算
                continue
            ctx = whole[max(0, m.start() - 15): m.end() + 15].replace("\n", " ")
            msg = "禁用語「%s」：…%s…" % (w, ctx)
            (errors if (hard and strict) else warns).append(msg)

    # 2 sensitive
    for w in SENSITIVE:
        if w and w in whole:
            errors.append("敏感字串「%s」" % w)

    # 3 source line
    mentions_data = bool(re.search(r"實價登錄|成交|萬/坪|萬／坪|元/坪|筆成交", plain))
    has_source = ("內政部" in whole and "實價登錄" in whole)
    if mentions_data and not has_source:
        (errors if strict else warns).append("有成交數字或提到實價登錄，但沒有「內政部…實價登錄」來源句")
    if "實價登錄" in whole and re.search(r"(?<!內政部)(?<!內政部不動產交易)實價登錄", whole) and "內政部實價登錄" not in whole and "內政部不動產交易實價登錄" not in whole:
        warns.append("實價登錄來源建議統一寫「內政部不動產交易實價登錄」")

    # 4 disclaimer
    if "僅供市場參考" not in whole:
        (errors if strict else warns).append("缺免責句「僅供市場參考，非正式估價與投資建議」")

    # 5 不是…而是
    for m in re.finditer(r"不是[^。！？\n]{1,20}而是", plain):
        warns.append("「不是…而是」句型（不武斷規則）：%s" % m.group(0))

    # 6 門牌／地號：實價登錄公開成交表可以有門牌，所以只警告；在手物件描述若出現門牌請人工改掉
    addr = [m.group(0) for m in re.finditer(r"[\u4e00-\u9fff]{1,6}(路|街|巷)[\u4e00-\u9fff0-9]{0,6}\d{1,4}(之\d+)?號", plain)]
    if addr:
        warns.append("內文有 %d 個門牌（實登成交表可接受；在手物件不可）：%s%s" % (len(addr), "、".join(addr[:3]), "…" if len(addr) > 3 else ""))
    for m in re.finditer(r"[\u4e00-\u9fff]{1,6}段\s?\d{1,4}(-\d+)?\s?地號", plain):
        errors.append("疑似地號：%s" % m.group(0))

    return rel, strict, errors, warns

def main(argv):
    if len(argv) > 1 and argv[1] == "--all":
        files = all_files()
    elif len(argv) > 1:
        files = [os.path.abspath(a) for a in argv[1:]]
    else:
        files = changed_files()
        if not files:
            print("沒有異動的文章，略過。")
            return 0
    total_err = 0
    for f in files:
        rel, strict, errors, warns = check(f)
        flag = "✗" if errors else ("△" if warns else "✓")
        print("%s %s%s" % (flag, rel, "" if strict else "（非嚴格分類）"))
        for e in errors:
            print("    錯誤：" + e)
        for w in warns:
            print("    警告：" + w)
        total_err += len(errors)
    print("\n共 %d 篇，%d 個錯誤。" % (len(files), total_err))
    return 1 if total_err else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
