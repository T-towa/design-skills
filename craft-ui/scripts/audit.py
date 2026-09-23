#!/usr/bin/env python3
"""Flag visual values that fall outside the craft-ui scale in CSS / TSX / JSX / HTML / Vue / Svelte files.

usage:
  python3 audit.py src/ app/ --surface app      # app | lp | mobile
  python3 audit.py components/Button.tsx

ERROR = breaks a scale rule (type size, weight, radius, spacing step, px font on inputs for mobile).
WARN  = worth a second look (italic in Japanese UI, decorative diagonals, gradient text, raw hex colors).
Exit code 1 when any ERROR is found.
"""
import argparse
import os
import re
import sys

EXTS = (".css", ".scss", ".tsx", ".jsx", ".ts", ".js", ".html", ".vue", ".svelte", ".mdx")
SKIP_DIRS = {"node_modules", ".next", "dist", "build", ".git", "out", "coverage", ".turbo"}

TEXT_OK = {
    "app": {"xs", "sm", "base", "xl", "display-sm", "display"},
    "mobile": {"xs", "sm", "base", "xl", "display-sm", "display"},
    "lp": {"xs", "sm", "base", "xl", "display-sm", "display", "display-lg", "display-xl"},
}
PX_OK = {"app": {12, 14, 16, 20, 28, 40}, "mobile": {12, 14, 16, 20, 28, 40}, "lp": {12, 14, 16, 20, 28, 40, 56, 72}}
TW_TEXT_SIZES = {"xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl", "8xl", "9xl",
                 "display-sm", "display", "display-lg", "display-xl"}
WEIGHT_BAD = {"thin", "extralight", "light", "semibold", "extrabold", "black"}
RADIUS_BAD = {"rounded-xs", "rounded-2xl", "rounded-3xl", "rounded-4xl"}
RADIUS_PX_OK = {0, 4, 8, 9999}

R_TW_TEXT = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*text-(xs|sm|base|lg|xl|[2-9]xl|display(?:-sm|-lg|-xl)?)(?![\w-])")
R_TW_TEXT_ARB = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*text-\[(\d+(?:\.\d+)?)(px|rem)\]")
R_TW_WEIGHT = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black)(?![\w-])")
R_TW_RADIUS = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*(rounded(?:-[trblse]{1,2})?(?:-(?:xs|sm|md|lg|xl|2xl|3xl|4xl|none|full))?)(?![\w-])")
R_TW_RADIUS_ARB = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*rounded(?:-[trblse]{1,2})?-\[(\d+(?:\.\d+)?)(px|rem)\]")
R_TW_HALF = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*-?(?:p|px|py|pt|pb|pl|pr|ps|pe|m|mx|my|mt|mb|ml|mr|ms|me|gap|gap-x|gap-y|space-x|space-y|inset|top|left|right|bottom)-(0\.5|1\.5|2\.5|3\.5)(?![\w.-])")
R_TW_SPACE_ARB = re.compile(r"(?<![\w-])(?:[a-z0-9]+:)*-?(?:p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|gap|gap-x|gap-y)-\[(\d+(?:\.\d+)?)px\]")
R_CSS_FS = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)(px|rem)")
R_CSS_FW = re.compile(r"font-weight\s*:\s*(\d{3})")
R_CSS_RAD = re.compile(r"border-radius\s*:\s*([^;}{\n]+)")
R_ITALIC = re.compile(r"(?<![\w-])italic(?![\w-])|font-style\s*:\s*italic")
R_DIAG = re.compile(r"(?<![\w-])-?skew-[xy]-|skewX\(|skewY\(|clip-path\s*:\s*polygon")
R_GRAD_TEXT = re.compile(r"bg-clip-text|background-clip\s*:\s*text")
R_HEX = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z])")


def to_px(v, unit):
    v = float(v)
    return v * 16 if unit == "rem" else v


def scan(path, surface, out):
    try:
        text = open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return
    is_css = path.endswith((".css", ".scss"))
    in_token_file = is_css and (":root" in text and "--background" in text)
    for n, line in enumerate(text.splitlines(), 1):
        def add(level, msg):
            out.append((level, path, n, msg))

        for m in R_TW_TEXT.finditer(line):
            size = m.group(1)
            if size in TW_TEXT_SIZES and size not in TEXT_OK[surface]:
                add("ERROR", "text-%s is off the type scale (use xs/sm/base/xl/display-sm/display%s)"
                    % (size, "/display-lg/display-xl" if surface == "lp" else ""))
        for m in R_TW_TEXT_ARB.finditer(line):
            px = to_px(m.group(1), m.group(2))
            if px not in PX_OK[surface]:
                add("ERROR", "text-[%s%s] = %gpx is off the type scale" % (m.group(1), m.group(2), px))
        for m in R_TW_WEIGHT.finditer(line):
            if m.group(1) in WEIGHT_BAD:
                add("ERROR", "font-%s: use font-normal (400) / font-medium (500) / font-bold (700)" % m.group(1))
        for m in R_TW_RADIUS.finditer(line):
            if any(m.group(1).endswith(b[len("rounded"):]) and b != "rounded" for b in RADIUS_BAD):
                add("ERROR", "%s: radius is 4px (rounded-sm), 8px (rounded-md / rounded-lg) or rounded-full" % m.group(1))
        for m in R_TW_RADIUS_ARB.finditer(line):
            px = to_px(m.group(1), m.group(2))
            if px not in RADIUS_PX_OK:
                add("ERROR", "rounded-[%s%s]: radius is 4px, 8px or full" % (m.group(1), m.group(2)))
        for m in R_TW_HALF.finditer(line):
            add("ERROR", "half step '-%s' breaks the 4px spacing grid" % m.group(1))
        for m in R_TW_SPACE_ARB.finditer(line):
            if float(m.group(1)) % 4:
                add("ERROR", "spacing [%spx] is not a multiple of 4" % m.group(1))
        if is_css and not in_token_file:
            for m in R_CSS_FS.finditer(line):
                px = to_px(m.group(1), m.group(2))
                if px not in PX_OK[surface]:
                    add("ERROR", "font-size %g%s is off the type scale" % (float(m.group(1)), m.group(2)))
            for m in R_CSS_FW.finditer(line):
                if m.group(1) not in ("400", "500", "700"):
                    add("ERROR", "font-weight %s: use 400 / 500 / 700" % m.group(1))
            for m in R_CSS_RAD.finditer(line):
                val = m.group(1).strip()
                if "var(" in val or "calc(" in val or "%" in val:
                    continue
                for num, unit in re.findall(r"(\d+(?:\.\d+)?)(px|rem)", val):
                    px = to_px(num, unit)
                    if px not in RADIUS_PX_OK and px < 999:
                        add("ERROR", "border-radius %s: use 4px, 8px or 9999px" % val)
                        break
        if R_ITALIC.search(line):
            add("WARN", "italic: Japanese has no true italics; use weight or color for emphasis")
        if R_DIAG.search(line):
            add("WARN", "diagonal shape (skew / polygon clip): keep only if the brand explicitly asks for it")
        if R_GRAD_TEXT.search(line):
            add("WARN", "gradient text: prefer solid ink; gradient headlines read as template output")
        if not in_token_file and not path.endswith((".svg",)) and R_HEX.search(line) and ("class" in line or "style" in line or is_css):
            add("WARN", "raw hex color: use a token (bg-primary, text-muted-foreground, bg-status-*, bg-category-*)")
        if surface == "mobile" and re.search(r"<(input|textarea|select)\b", line) and re.search(r"text-(xs|sm)(?![\w-])", line):
            add("ERROR", "form field below 16px on mobile: iOS zooms the page on focus; use text-base")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--surface", choices=("app", "lp", "mobile"), default="app")
    a = ap.parse_args()
    files = []
    for p in a.paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                files += [os.path.join(root, f) for f in names if f.endswith(EXTS)]
        elif p.endswith(EXTS):
            files.append(p)
    out = []
    for f in sorted(files):
        scan(f, a.surface, out)
    for level, path, n, msg in out:
        print("%s %s:%d  %s" % (level, path, n, msg))
    errors = sum(1 for o in out if o[0] == "ERROR")
    warns = len(out) - errors
    print("\n%d file(s) scanned for surface '%s': %d error(s), %d warning(s)" % (len(files), a.surface, errors, warns))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
