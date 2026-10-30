# Pure Python and Pandas: what the comparison taught me

## Why I chose Pandas

I used Pandas because the task explicitly asks for `describe()`, `info()`, `value_counts()`, and `nunique()`. These provide readable, widely used tools for checking a dataset and summarizing its columns. The Pandas script calculates its own results; it does not import statistics or preprocessing functions from the pure Python script. The two implementations share a documented policy, not implementation code.

## Do the results agree?

These results refer to my successful Windows run using **Python 3.12, NumPy 2.2.6, and Pandas 2.2.3**, verified from the three submitted JSON files. All eight differences were in standard deviation; numeric means matched exactly.

**The full-data run passed: 306 shared column metrics agreed across all 40 columns, including all 26 numeric columns.** There were 8 floating-point differences; the largest absolute difference was 1.11e-16, within the declared tolerance.

The complete-data comparison is recorded in `comparison_results.json`. The 306 count refers to shared per-column metrics. Dataset row count, column count, column-name sets, and standard-deviation convention are checked separately. The comparison checks row and column counts, inferred logical types, missing counts, numeric statistics, and categorical counts, unique counts, modes, mode frequencies, and top-five lists. Counts, extrema, medians, types, and categorical results must match exactly. Means and standard deviations use relative and absolute tolerances of `1e-12` because floating-point aggregation can differ slightly between implementations. A failed comparison makes the Pandas script exit with status 1.

Both scripts use sample standard deviation (`ddof=1`), exclude the same missing tokens, and apply the same alphabetical tie-breaking. Missing percentages are an additional Pandas output, calculated as missing count divided by total rows times 100.

When the command redirects terminal output to `pandas_output.txt`, that file retains the raw `describe()` output. The three JSON result files do not contain the raw `info()` or `describe()` display. Its `top` value for a categorical tie may differ from the explicitly sorted mode in the comparison: any tied value is a valid mode, but the canonical per-column report chooses alphabetically. This matters for `ad_id`, where every value occurs once. Quartiles from numeric `describe()` are additional Pandas summaries, with no Phase 1 equivalent to compare.

## Which decisions did pure Python make explicit?

Writing the first script required me to define what counts as missing, how to recognize a number, what to do with invalid values, and whether to divide variance by `n` or `n−1`. I also had to handle empty inputs, a single observation, and ties deliberately.

Pandas can make some of these decisions automatically. `read_csv()` normally recognizes a default collection of missing-value tokens and infers storage types. That may be convenient, but it does not guarantee agreement with a researcher's intended policy. My second script therefore loads strings with default NA recognition disabled, strips surrounding whitespace, applies our explicit missing-value policy, and then converts only wholly numeric columns. Dates remain strings in the statistical frame so they receive the same categorical analysis as Phase 1; the report separately identifies their logical type as `date`.

Pandas storage dtypes and research-level logical types answer different questions. A date string can have a string dtype while representing a date; a dictionary encoded in a CSV cell can contain numbers while remaining a structured text field. Neither script silently treats such a field as an exact numeric measure.

## What might I have missed using Pandas alone?

The manual analysis made the dataset's representation especially visible. Spend, impressions, and audience size are intervals stored as dictionary-like text, sometimes with no upper bound. A numeric summary of binary flags alone would not reveal the assumptions needed for a spending analysis. Midpoints would be estimates, and different currencies would need separate treatment.

I also learned to distinguish a missing cell from the valid stored value `[]`. There are 73,205 empty candidate-mention lists, even though the task describes candidate-related ads. The date fields include records from before 2024, and page names do not map one-to-one to page IDs. These observations affect the questions I can responsibly answer and the grouping keys I should use.

## Trade-offs

Pure Python made the calculations and edge cases transparent, but required more code and more care to implement each statistic. Pandas made summaries, missingness, and frequency analysis more concise. It still required explicit preprocessing and interpretation. Matching results increases confidence in these descriptive computations; it does not validate the annotations, dataset coverage, or any causal interpretation of political advertising.
