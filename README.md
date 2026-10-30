# Research Task 1 · Descriptive Statistics

**Phases 1 and 2: Exploring Facebook political advertising with pure Python and Pandas**

The pure Python implementation profiles the supplied `fb_ads_president_scored_anon.csv` using only Python's standard library. It reports every original column and provides reproducible descriptive statistics that serve as the baseline for the independent Pandas implementation in Phase 2.

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

## Files and setup

| File | Purpose |
| --- | --- |
| `pure_python_stats.py` | Standard-library analysis; no third-party dependencies |
| `pandas_stats.py` | Independent Pandas analysis and comparison |
| `pure_python_results.json` | Phase 1 baseline |
| `pandas_results.json` | Phase 2 results, including missing percentages |
| `comparison_results.json` | Verification results and floating-point differences |
| `COMPARISON.md` | Required reflection on both approaches |

Keep the scripts and `fb_ads_president_scored_anon.csv` in the project folder. The CSV is supplied separately. Pass its filename in the command; retain `csv_path` as the argument name inside both scripts.

**Verified Windows environment:** Python 3.12, NumPy 2.2.6, Pandas 2.2.3. Phase 1 uses only the standard library. This environment successfully ran Phase 2 after the original Python 3.14 environment encountered a NumPy DLL loading error; that error did not establish that Python 3.14 itself was the cause.

If the `.venv312` environment has already been created and verified, skip installation. Otherwise, with Python 3.12 installed, run these commands in PowerShell from the project folder:

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install numpy==2.2.6 pandas==2.2.3
```

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

### Page-level structure

The dataset contains **4,475 distinct page IDs** and **4,546 distinct page names**. Page names should not be assumed to identify a unique organization; page IDs are the more appropriate starting point for grouping and identity checks.

Individual people, page names, organization names, and identifying examples are omitted from this README. Findings are presented at an aggregate level.

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

## Phase 2: Pandas analysis and verified comparison

Pandas was chosen because its built-in methods directly support the task requirements. The scripts compute their results independently. See **[COMPARISON.md](COMPARISON.md)** for the required reflection on agreement, implicit decisions, and lessons from manual analysis.

The Pandas script displays shape, storage dtypes, `info()`, numeric and non-numeric `describe()` output, missing counts and percentages, and categorical results using `value_counts()` and `nunique()`. It verifies every original numeric statistic against a JSON baseline produced by the pure Python script. It also compares the categorical results and missing counts.

**Verified result from the submitted JSON files:** all 306 shared column metrics passed comparison on 246,745 rows and 40 columns. All 26 numeric columns agreed within tolerance. Eight standard deviations differed slightly; the largest absolute difference was **1.11 × 10⁻¹⁶**, below the `1e-12` tolerance. There were zero failures. Dataset structure checks also passed.

### Reproduce both analyses

Run Phase 1 first, then Phase 2, from the project folder:

```powershell
.\.venv312\Scripts\python.exe pure_python_stats.py "fb_ads_president_scored_anon.csv" --json-output pure_python_results.json
.\.venv312\Scripts\python.exe pandas_stats.py "fb_ads_president_scored_anon.csv" --baseline pure_python_results.json --json-output pandas_results.json --comparison-output comparison_results.json
```

These commands print human-readable results in the terminal and create the three JSON files. To save the terminal output as well, add `> pure_python_output.txt` to the first command and `> pandas_output.txt` to the second. Those text files are optional and are not created by `--json-output`.

For another environment, replace `.\.venv312\Scripts\python.exe` with the Python executable where the required packages are installed.

A successful comparison returns exit status 0; a mismatch returns 1. Both scripts need the original dataset supplied separately. Pandas results contain an additional `missing_percentage` field (0–100). Mean and standard deviation comparisons allow relative and absolute tolerances of `1e-12`; other shared statistics must match exactly.

| Additional file | Purpose |
| --- | --- |
| `pandas_stats.py` | Independent Pandas implementation and optional comparison |
| `requirements.txt` (if used) | Pin `numpy==2.2.6` and `pandas==2.2.3` for the verified Python 3.12 setup |
| `pure_python_output.txt`, `pure_python_results.json` | Fresh Phase 1 results |
| `pandas_output.txt`, `pandas_results.json` | Complete Phase 2 results |
| `comparison_results.json` | Machine-readable verification, failures, and numerical differences |
| `COMPARISON.md` | Required reflection |

Synthetic checks cover all-empty columns, zeros, mixed text/numbers, a single numeric observation, formatted currency, dates, and categorical ties. They confirm agreement between the two implementations for those cases. The uploaded JSON files verify the comparable per-column results, not the terminal-only `info()` and `describe()` displays. Both implementations load data into memory; neither is intended as a streaming solution. The Pandas script relies on its CSV reader for malformed input handling; the Phase 1 script has additional explicit row-width and header validation.
