# Research Task 1 · Descriptive Statistics

**Phase 1: Exploring Facebook political advertising with pure Python**

This project profiles the supplied `fb_ads_president_scored_anon(1).csv` using only Python's standard library. It reports every original column and provides reproducible descriptive statistics that can serve as the baseline for an independent Pandas implementation in Phase 2.

## Dataset at a glance

| Measure | Verified result |
| --- | ---: |
| Rows | 246,745 |
| Columns | 40 |
| Unique ad IDs | 246,745 |
| Unique page IDs | 4,475 |
| Unique page names | 4,546 |
| Numeric columns | 26 |
| Other columns | 14 |
| Currencies | 18 |

The 26 numeric columns are binary annotation flags. The remaining columns include identifiers, names, dates, hashed message identifiers, dictionary-like ranges, and list-like fields. The task describes a 2024 election dataset, but creation and delivery-start dates span **July 6, 2021–November 5, 2024**. This analysis retains all supplied records rather than silently filtering them.

## Run the analysis

Requires **Python 3.9+**. No package installation is needed. Place the supplied CSV beside the script, or provide its actual path:

```bash
python pure_python_stats.py "fb_ads_president_scored_anon(1).csv"
```

To reproduce both saved reports:

```bash
python pure_python_stats.py "fb_ads_president_scored_anon(1).csv" --json-output statistics.json > statistics.txt
```

| File | Purpose |
| --- | --- |
| `pure_python_stats.py` | CSV loading, type inference, reusable statistics functions, readable reporting |
| `statistics.txt` | Full human-readable output for all 40 columns |
| `statistics.json` | Full machine-readable output for later comparison |

The input dataset is supplied separately and is not included in the deliverable archive.

## Statistical choices

- **Numeric columns:** nonmissing count, arithmetic mean, minimum, maximum, median, and sample standard deviation. Mean uses the sum divided by count; standard deviation uses the sum of squared deviations divided by `n − 1`. Median is computed from sorted values. No statistics package is used by the analysis.
- **Other columns:** nonmissing count, unique count, mode and frequency, and top five values by frequency. Dates and structured fields receive these categorical statistics. Frequencies for lists describe the whole stored list, not individual members.
- **Missing values:** whitespace-only cells and case-insensitive `N/A`, `NA`, `NULL`, `None`, and `NaN` are missing. Zero is valid. Literal `[]` is an empty list, not a missing cell.
- **Type inference:** all nonmissing values must parse numerically for a column to receive numeric statistics. Otherwise, ISO dates, dictionary-like strings, list-like strings, mixed numeric/text values, and text are distinguished. Structured detection describes appearance; it does not validate every nested object.
- **Formatted numbers:** the parser accepts dollar-prefixed numbers, correctly grouped thousands separators, decimals, and scientific notation. Currency values are not converted between currencies.
- **Mixed columns:** categorical output retains all nonmissing values and includes a numeric-parseable count. Invalid text is never silently discarded to calculate a numeric mean.
- **Empty and single-value cases:** empty numeric inputs return undefined statistics as `null`; sample standard deviation is `null` for fewer than two observations. All-empty CSV columns receive an `empty` type and zero categorical counts. Constant numeric columns with at least two values have standard deviation zero.
- **Ties:** frequency ties are resolved alphabetically; the reported mode is one representative of a possible tie. Top five means at most five values.
- **CSV safety:** `csv.reader` handles quoted fields, commas, and embedded newlines. UTF-8 BOMs are supported. Blank records are skipped; malformed row widths and duplicate/empty headers produce a clear error rather than corrupting column alignment.

## Verified findings

### Ad volume is concentrated among a few page names

| Page name | Ad rows |
| --- | ---: |
| Kamala Harris | 55,503 |
| Donald J. Trump | 23,988 |
| Joe Biden | 14,822 |
| The Daily Scroll | 10,461 |
| Kamala HQ | 7,564 |

These are counts of records grouped by page name. They do not establish spending leadership, persuasion, or electoral impact. Page names are not guaranteed to uniquely identify organizations: the dataset contains more distinct page names than page IDs.

### Call-to-action and advocacy flags are common

| Annotation | Share of rows flagged 1 |
| --- | ---: |
| Call to action | 57.28% |
| Advocacy | 54.86% |
| Issue | 38.16% |
| Attack | 27.19% |
| Incivility | 18.75% |

For a 0/1 column, its mean is the proportion of records flagged 1. Labels may overlap, so these percentages should not be added. Annotation accuracy and label definitions cannot be established from the CSV alone.

### Missingness and scope need attention

| Column | Missing records |
| --- | ---: |
| `ad_delivery_stop_time` | 2,159 |
| `bylines` | 1,009 |
| `estimated_audience_size` | 579 |

All other columns have zero missing records under the documented policy. In addition, **73,205 records contain `[]` in `illuminating_mentions`**. An empty annotation list does not prove that the ad contains no candidate reference; it does mean that the task's candidate-mention description cannot be assumed to hold in this field for every row.

### Spend and reach are intervals

`spend`, `impressions`, and `estimated_audience_size` contain dictionary-like bounds rather than exact measurements. For example, 135,950 rows have the spend interval `0–99`; 100,146 rows have an audience lower bound of `1,000,001` without an upper bound. These fields are summarized as stored categories. No exact spend mean or total is claimed.

USD occurs in 246,599 rows; the remaining 146 rows use other currencies. Any subsequent spend analysis must retain currency groups or use a documented conversion method. Range endpoints could support a separate bounds analysis, but midpoint estimates would introduce assumptions and open-ended intervals need special handling.

## Validation and reproducibility

The script was run against the complete supplied CSV. Numeric functions were independently checked against standard-library `statistics` results for representative values. Additional checks covered empty inputs, missing tokens, all-zero columns, single numeric observations, mixed numeric/text columns, formatted currency, invalid comma grouping, and categorical ties.

The script loads columns into memory and sorts numeric values for medians; memory use grows with dataset size. This is appropriate for the task's focus on clarity over efficiency.

## Phase 2 comparison plan

The independent Pandas script remains future work. It should use identical missing-value and parsing policies, preserve the 40-column schema, use `std(ddof=1)`, and apply the same frequency tie-breaking. Counts, medians, extrema, and frequencies should agree exactly; means and standard deviations should be compared using a small floating-point tolerance. Pandas will shorten aggregation code, while this implementation makes parsing decisions and edge cases explicit.
