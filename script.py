import pandas as pd

# download from here: https://www.kaggle.com/datasets/stefanocoretta/yoda-speech-corpus?resource=download

FILE_PATH = r"-\yoda-corpus.csv"   # Replace with your actual path
df = pd.read_csv(FILE_PATH)

COL_SPEAKER = "character"  
COL_SCENE   = "slug"  
COL_MOVIE   = "movie"
COL_TYPE    = "component"
COL_TEXT    = "text"

# The top 10 scenes with the highest number of dialogue lines.
print("\n1")
dialogue_lines = df[COL_SCENE].value_counts().head(10)
print("The top 10 scenes with the highest number of dialogue lines:")
print(dialogue_lines.to_string())

# Total dialogue lines per movie.
print("\n2")
lines_per_movie = (
    df.groupby(COL_MOVIE)
      .size()
      .sort_values(ascending=False)
      .rename("line_count")
)
print("Total dialogue lines per movie:")
print(lines_per_movie.to_string())

# Per-movie top speaker
print("\n3")
counts = (
    df.groupby([COL_MOVIE, COL_SPEAKER])
      .size()
      .reset_index(name="line_count")
)

top_per_movie = (
    counts.sort_values([COL_MOVIE, "line_count"], ascending=[True, False])
          .drop_duplicates(COL_MOVIE)
)

print("Top speaker per movie:")
print(top_per_movie.to_string(index=False))

top = top_per_movie[COL_SPEAKER].value_counts().rename("movie_top")
print("\nRanking by number of top speaking:")
print(top.to_string())

# Scene ratio per movie, sorted by ratio
print("\n4")
type_counts = (
    df.groupby([COL_MOVIE, COL_TYPE])
      .size()
      .unstack(fill_value=0)
)
print("Scene ratio per movie, sorted by ratio:")
print("Counts:")
print(type_counts.to_string())

ratio = type_counts["action"] / type_counts["character"].where(
    type_counts["character"] > 0
)
ratio = ratio.sort_values(ascending=False).rename("action_per_character")

print("\nAction-to-character ratio, sorted high to low:")
print(ratio.to_string())

# Per-character peak movie, then rank by peak count
print("\n5a")

counts = (
    df.groupby([COL_SPEAKER, COL_MOVIE])
      .size()
      .reset_index(name="line_count")
)

peak = (
    counts.sort_values("line_count", ascending=False)
          .drop_duplicates(COL_SPEAKER)
          .set_index(COL_SPEAKER)
          .rename(columns={COL_MOVIE: "movie",
                           "line_count": "line_count"})
          .sort_values("line_count", ascending=False)
)
print("Per-character peak movie, then rank by peak count")
print(peak.to_string())

print("\n5b")
# Highest and lowest lines for Clones
names = peak.index.to_series().str.upper()
clone_mask     = names.str.match(r"^CLONE(\s|-|$)")   # CLONE SORTING
clone_peaks    = peak[clone_mask]

if clone_peaks.empty:
    print("None")
else:
    clone_peaks.to_string()

    hi_val = clone_peaks["line_count"].max()
    lo_val = clone_peaks["line_count"].min()

    highest = clone_peaks[clone_peaks["line_count"] == hi_val]
    lowest  = clone_peaks[clone_peaks["line_count"] == lo_val]
    print("Highest and lowest lines for Clones:")
    print(highest.to_string())
    print(lowest.to_string())