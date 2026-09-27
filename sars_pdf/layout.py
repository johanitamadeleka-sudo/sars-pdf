"""Fixed geometry of the report, measured from the original (US Letter, points)."""

# x of the 21 vertical grid lines (centre of line), left to right.
X = [31.56, 50.88, 85.20, 133.20, 174.00, 232.47, 252.72, 272.07, 290.76, 309.48, 328.20,
     346.92, 365.64, 388.47, 407.16, 429.99, 448.68, 471.51, 498.39, 572.76, 583.23]

# Columns (index -> key). Column i lies between X[i] and X[i+1].
COLS = ["sn", "region", "council", "centre_no", "school_name", "av", "grd",
        "a", "b", "c", "d", "f", "total", "a_c", "pct_a_c", "a_d", "pct_a_d",
        "gpa", "competency", "rank"]

THIN, THICK = 0.48, 0.84

# Thick border segments of the standard table.
#   V{k}:{band}  vertical grid line k within band h1 | h2 | body | ov
#   H{line}:{c0}-{c1}  horizontal line top | h1b (under GRADING PERFORMANCE) | hb (header bottom)
#                      | ovt (overall top) | bot (table bottom), from X[c0] to X[c1]
DEFAULT_THICK = [
    "Hbot:0-20", "Hh1b:7-17", "Hhb:0-19", "Hovt:5-18", "Htop:0-19",
    "V0:h1", "V0:h2", "V13:body", "V13:h2", "V15:h2", "V17:body", "V17:h2",
    "V18:ov", "V5:body", "V5:ov", "V7:body", "V7:h2", "V7:ov",
]

# Default layout (pages 6-9 of the original).
DEFAULT_LAYOUT = {
    "title_top": 71.3,
    "subject_top": 108.0,
    "subject_size": 6.11,
    "table_top": 117.66,
    "rows": [11.04, 11.04, 8.88, 11.04],
}

TITLE_PITCH = 8.87     # distance between heading lines
TITLE_CENTER = 307.75  # heading lines are centred on this x (spaces included)
