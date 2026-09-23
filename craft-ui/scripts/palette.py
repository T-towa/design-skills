#!/usr/bin/env python3
"""Generate a complete light/dark token set for shadcn/ui + Tailwind v4 from ONE brand color,
and verify every text pair against WCAG AA.

usage:
  python3 palette.py --brand "#0b63c5"                 # CSS to stdout, report to stderr
  python3 palette.py --brand "#0b63c5" --brand-dark "#5aa2ff"
  python3 palette.py --brand "#b8480d" --report-only   # contrast report only

Exit code 1 when any required pair fails (text < 4.5:1, focus ring < 3:1).
"""
import argparse
import math
import sys

# ---------- color math (sRGB <-> OKLCH) ----------

def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError("expected #rrggbb, got %r" % h)
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def rgb_to_hex(rgb):
    return "#" + "".join("%02x" % max(0, min(255, round(c * 255))) for c in rgb)


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def rgb_to_oklch(rgb):
    r, g, b = (_lin(c) for c in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    C = math.hypot(A, B)
    H = math.degrees(math.atan2(B, A)) % 360
    return L, C, H


def oklch_to_rgb_raw(L, C, H):
    A = C * math.cos(math.radians(H))
    B = C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return [_gam(c) if c >= 0 else -_gam(-c) for c in (r, g, b)]


def oklch_to_hex(L, C, H):
    """Gamut-map by reducing chroma until the color fits in sRGB."""
    lo, hi = 0.0, C
    rgb = oklch_to_rgb_raw(L, C, H)
    if all(-1e-4 <= c <= 1 + 1e-4 for c in rgb):
        return rgb_to_hex(rgb)
    for _ in range(30):
        mid = (lo + hi) / 2
        rgb = oklch_to_rgb_raw(L, mid, H)
        if all(-1e-4 <= c <= 1 + 1e-4 for c in rgb):
            lo = mid
        else:
            hi = mid
    return rgb_to_hex(oklch_to_rgb_raw(L, lo, H))


def oklch_css(hexv):
    L, C, H = rgb_to_oklch(hex_to_rgb(hexv))
    return "oklch(%.3f %.3f %s)" % (L, C, "0" if C < 0.002 else "%.1f" % H)


def mix(a, b, t):
    """sRGB mix, identical to CSS color-mix(in srgb, a t*100%, b)."""
    x, y = hex_to_rgb(a), hex_to_rgb(b)
    return rgb_to_hex([x[i] * t + y[i] * (1 - t) for i in range(3)])


def luminance(hexv):
    r, g, b = (_lin(c) for c in hex_to_rgb(hexv))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------- fixed meaning palettes (independent of the brand) ----------
# status: what state a thing is in.  category: which group a thing belongs to (people, kinds, tags).
STATUS = {
    "light": {"info": ("#e0edff", "#0b4fa8"), "progress": ("#eee6ff", "#5530b0"), "success": ("#d7f7e8", "#1b6b48"),
              "warning": ("#fff1c2", "#7a5600"), "danger": ("#ffe2de", "#ae2e24")},
    "dark": {"info": ("#0c2d5c", "#b3d4ff"), "progress": ("#2e1d59", "#d8c8ff"), "success": ("#143f2e", "#9ae8c4"),
             "warning": ("#4a3a06", "#f8e08a"), "danger": ("#521f1a", "#ffc2bb")},
}
CATEGORY = {
    "light": [("#d3f1ec", "#0e5a50"), ("#e9e2ff", "#4a2d9e"), ("#fcebc9", "#734800"),
              ("#fde0e6", "#962040"), ("#e2e8f0", "#334155"), ("#dcf5d9", "#2d5f1f")],
    "dark": [("#113f39", "#a6ecdf"), ("#2e2360", "#d4c8ff"), ("#4a3306", "#fbd99a"),
             ("#521a2a", "#ffc3d0"), ("#27303d", "#cbd5e1"), ("#1d3d17", "#bfe8b3")],
}
DESTRUCTIVE = {"light": ("#c42b20", "#ffffff"), "dark": ("#ff8a80", "#2a0703")}


# ---------- derivation ----------

def pick_ink(brand, dark_candidate):
    """Text color on a solid brand fill: white if it passes, otherwise a dark tinted ink."""
    if contrast("#ffffff", brand) >= 4.5:
        return "#ffffff"
    return dark_candidate


def derive(brand, brand_dark=None):
    L, C, H = rgb_to_oklch(hex_to_rgb(brand))
    if not brand_dark:
        brand_dark = oklch_to_hex(max(L, 0.74), min(C, 0.17), H)
    dark_ink = oklch_to_hex(0.2, min(C, 0.06), H)

    light = {
        "brand": brand, "brand-ink": pick_ink(brand, dark_ink),
        "bg": mix(brand, "#f4f4f5", .03), "surface": "#ffffff", "surface-2": mix(brand, "#f8f8f9", .02),
        "selected": mix(brand, "#ececee", .05), "line": mix(brand, "#e2e2e5", .06), "line-strong": mix(brand, "#c8c8cd", .08),
        "region-line": mix(brand, "#d9d9de", .08),
        "ink": mix(brand, "#141416", .12), "ink-2": mix(brand, "#50505a", .08), "ink-3": mix(brand, "#5f5f69", .06),
        "brand-soft": mix(brand, "#ffffff", .10), "brand-text": mix(brand, "#000000", .82),
    }
    dark = {
        "brand": brand_dark, "brand-ink": dark_ink if contrast(dark_ink, brand_dark) >= contrast("#ffffff", brand_dark) else "#ffffff",
        "bg": mix(brand_dark, "#111113", .04), "surface": mix(brand_dark, "#18181b", .03), "surface-2": mix(brand_dark, "#1e1e22", .04),
        "selected": mix(brand_dark, "#28282d", .06), "line": mix(brand_dark, "#2c2c32", .06), "line-strong": mix(brand_dark, "#3f3f46", .08),
        "region-line": mix(brand_dark, "#34343b", .08),
        "ink": mix(brand_dark, "#f0f0f2", .06), "ink-2": mix(brand_dark, "#b4b4bc", .06), "ink-3": mix(brand_dark, "#a2a2ab", .06),
        "brand-soft": mix(brand_dark, "#18181b", .18), "brand-text": mix(brand_dark, "#ffffff", .72),
    }
    # focus ring: the brand itself when it reaches 3:1, otherwise the same hue moved toward the text color
    for p, step in ((light, -0.02), (dark, 0.02)):
        L2, C2, H2 = rgb_to_oklch(hex_to_rgb(p["brand"]))
        ring = p["brand"]
        while min(contrast(ring, p["bg"]), contrast(ring, p["surface"])) < 3.2 and 0.05 < L2 < 0.97:
            L2 += step
            ring = oklch_to_hex(L2, C2, H2)
        p["ring"] = ring
    # keep brand-text readable on brand-soft even for very light / very dark brands
    for p, toward in ((light, "#000000"), (dark, "#ffffff")):
        t = 0.82 if toward == "#000000" else 0.72
        while contrast(p["brand-text"], p["brand-soft"]) < 4.6 and t > 0.2:
            t -= 0.04
            p["brand-text"] = mix(p["brand"], toward, t)
    return light, dark


def checks(mode, p):
    """Required pairs. (label, fg, bg, minimum)"""
    out = []
    for fg in ("ink", "ink-2", "ink-3"):
        for bg in ("bg", "surface", "surface-2", "selected", "brand-soft"):
            out.append(("%s on %s" % (fg, bg), p[fg], p[bg], 4.5))
    out.append(("brand-ink on brand (primary button)", p["brand-ink"], p["brand"], 4.5))
    out.append(("brand-text on brand-soft (current location)", p["brand-text"], p["brand-soft"], 4.5))
    out.append(("inverse text on ink (pressed toggle)", p["surface"], p["ink"], 4.5))
    out.append(("focus ring on bg", p["ring"], p["bg"], 3.0))
    out.append(("focus ring on surface", p["ring"], p["surface"], 3.0))
    for k, (b, f) in STATUS[mode].items():
        out.append(("status-%s" % k, f, b, 4.5))
    for i, (b, f) in enumerate(CATEGORY[mode], 1):
        out.append(("category-%d" % i, f, b, 4.5))
    d, di = DESTRUCTIVE[mode]
    out.append(("destructive button text", di, d, 4.5))
    return out


def css(light, dark):
    def block(sel, mode, p):
        d, di = DESTRUCTIVE[mode]
        v = [
            ("radius", None, "0.5rem"),
            ("background", p["bg"]), ("foreground", p["ink"]),
            ("card", p["surface"]), ("card-foreground", p["ink"]),
            ("popover", p["surface"]), ("popover-foreground", p["ink"]),
            ("primary", p["brand"]), ("primary-foreground", p["brand-ink"]),
            ("secondary", p["selected"]), ("secondary-foreground", p["ink"]),
            ("muted", p["surface-2"]), ("muted-foreground", p["ink-2"]),
            ("accent", p["brand-soft"]), ("accent-foreground", p["brand-text"]),
            ("destructive", d), ("destructive-foreground", di),
            ("border", p["line"]), ("input", p["line-strong"]), ("ring", p["ring"]),
            ("chart-1", p["brand"]), ("chart-2", STATUS[mode]["success"][1]), ("chart-3", STATUS[mode]["warning"][1]),
            ("chart-4", STATUS[mode]["progress"][1]), ("chart-5", p["ink-3"]),
            ("sidebar", p["surface"]), ("sidebar-foreground", p["ink"]),
            ("sidebar-primary", p["brand"]), ("sidebar-primary-foreground", p["brand-ink"]),
            ("sidebar-accent", p["brand-soft"]), ("sidebar-accent-foreground", p["brand-text"]),
            ("sidebar-border", p["region-line"]), ("sidebar-ring", p["ring"]),
            ("subtle-foreground", p["ink-3"]), ("region-border", p["region-line"]),
            ("inverse", p["ink"]), ("inverse-foreground", p["surface"]),
        ]
        lines = []
        for item in v:
            if len(item) == 3:
                lines.append("  --%s: %s;" % (item[0], item[2]))
            else:
                lines.append("  --%s: %s;" % (item[0], oklch_css(item[1])))
        lines.append("  /* meaning colors: independent of the brand */")
        for k, (b, f) in STATUS[mode].items():
            lines.append("  --status-%s: %s;" % (k, oklch_css(b)))
            lines.append("  --status-%s-foreground: %s;" % (k, oklch_css(f)))
        for i, (b, f) in enumerate(CATEGORY[mode], 1):
            lines.append("  --category-%d: %s;" % (i, oklch_css(b)))
            lines.append("  --category-%d-foreground: %s;" % (i, oklch_css(f)))
        return "%s {\n%s\n}" % (sel, "\n".join(lines))

    theme = ["@theme inline {",
             "  /* fonts: set --font-jp / --font-num with next/font (see references/tokens.md) */",
             "  --font-sans: var(--font-jp), \"Hiragino Sans\", \"Yu Gothic UI\", sans-serif;",
             "  --font-num: var(--font-num-src), var(--font-jp), sans-serif;",
             "  /* type scale: xs 12 / sm 14 / base 16 / xl 20 / display-sm 28 / display 40 (+ LP only: display-lg 56 / display-xl 72) */",
             "  --text-display-sm: 1.75rem;  --text-display-sm--line-height: 1.35;",
             "  --text-display: 2.5rem;      --text-display--line-height: 1.2;",
             "  --text-display-lg: 3.5rem;   --text-display-lg--line-height: 1.15;",
             "  --text-display-xl: 4.5rem;   --text-display-xl--line-height: 1.1;",
             "  /* radius: only 4px (sm), 8px (md = lg), full. shadcn's rounded-md/xl collapse onto 8px */",
             "  --radius-sm: calc(var(--radius) - 4px);",
             "  --radius-md: var(--radius);",
             "  --radius-lg: var(--radius);",
             "  --radius-xl: var(--radius);"]
    names = ["background", "foreground", "card", "card-foreground", "popover", "popover-foreground", "primary",
             "primary-foreground", "secondary", "secondary-foreground", "muted", "muted-foreground", "accent",
             "accent-foreground", "destructive", "destructive-foreground", "border", "input", "ring", "chart-1", "chart-2",
             "chart-3", "chart-4", "chart-5", "sidebar", "sidebar-foreground", "sidebar-primary",
             "sidebar-primary-foreground", "sidebar-accent", "sidebar-accent-foreground", "sidebar-border", "sidebar-ring",
             "subtle-foreground", "region-border", "inverse", "inverse-foreground"]
    names += ["status-%s%s" % (k, s) for k in STATUS["light"] for s in ("", "-foreground")]
    names += ["category-%d%s" % (i, s) for i in range(1, 7) for s in ("", "-foreground")]
    theme += ["  --color-%s: var(--%s);" % (n, n) for n in names]
    theme.append("}")
    head = "/* generated by craft-ui/scripts/palette.py --brand %s --brand-dark %s */" % (light["brand"], dark["brand"])
    return "\n\n".join([head, block(":root", "light", light), block(".dark", "dark", dark), "\n".join(theme)]) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brand", required=True, help="brand color for light mode, #rrggbb")
    ap.add_argument("--brand-dark", help="brand color for dark mode (derived when omitted)")
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    light, dark = derive(a.brand, a.brand_dark)
    failed = 0
    print("contrast report (brand %s / dark %s)" % (light["brand"], dark["brand"]), file=sys.stderr)
    for mode, p in (("light", light), ("dark", dark)):
        rows = checks(mode, p)
        worst = min(rows, key=lambda r: contrast(r[1], r[2]) / r[3])
        bad = [r for r in rows if contrast(r[1], r[2]) < r[3]]
        failed += len(bad)
        print("  %-5s %d pairs, lowest %.2f:1 (%s)" % (mode, len(rows), contrast(worst[1], worst[2]), worst[0]), file=sys.stderr)
        for r in bad:
            print("    FAIL %s: %.2f:1 < %.1f" % (r[0], contrast(r[1], r[2]), r[3]), file=sys.stderr)
    if not a.report_only:
        sys.stdout.write(css(light, dark))
    if failed:
        print("  %d pair(s) fail. Pick a brand with more contrast or pass --brand-dark explicitly." % failed, file=sys.stderr)
        sys.exit(1)
    print("  all pairs pass", file=sys.stderr)


if __name__ == "__main__":
    main()
