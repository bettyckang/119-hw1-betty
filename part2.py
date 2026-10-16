"""
Part 2: Performance Comparisons

In this part, we will explore comparing the performance
of different pipelines.
First, we will set up some helper classes.
Then we will do a few comparisons
between two or more versions of a pipeline
to report which one is faster.
"""

import part1
import time 
import matplotlib.pyplot as plt
import pandas as pd

"""
=== Questions 1-5: Throughput and Latency Helpers ===

We will design and fill out two helper classes.

The first is a helper class for throughput (Q1).
The class is created by adding a series of pipelines
(via .add_pipeline(name, size, func))
where name is a title describing the pipeline,
size is the number of elements in the input dataset for the pipeline,
and func is a function that can be run on zero arguments
which runs the pipeline (like def f()).

The second is a similar helper class for latency (Q3).

1. Throughput helper class

Fill in the add_pipeline, eval_throughput, and generate_plot functions below.
"""

# Number of times to run each pipeline in the following results.
# You may modify this as you go through the file if you like, but make sure
# you set it back to 10 at the end before you submit.
NUM_RUNS = 10

class ThroughputHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline input sizes
        self.sizes = []

        # Pipeline throughputs
        # This is set to None, but will be set to a list after throughputs
        # are calculated.
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        self.names.append(name)
        self.sizes.append(size)
        self.pipelines.append(func)
        return

    def compare_throughput(self):
        self.throughputs = []

        for size, func in zip(self.sizes, self.pipelines):
            total_time = 0

            for i in range(NUM_RUNS):
                start = time.perf_counter() # Timestamp at start of function
                func()
                end = time.perf_counter() # Timestamp at end of function
                run_time = end - start # Calculate runtime
                total_time += run_time # Add to cumulative sum of runtimes

            # Calculate throughput and append to list
            throughput = (size * NUM_RUNS) / total_time
            self.throughputs.append(throughput)

        return self.throughputs

    def generate_plot(self, filename):
        plt.figure()
        plt.bar(self.names, self.throughputs, label="Throughput")
        plt.xticks(rotation=45)
        plt.xlabel("Pipeline")
        plt.ylabel("Throughput (Items Per Second)")
        plt.title("Pipeline Throughput Comparison")
        plt.legend()

        plt.savefig(filename, bbox_inches='tight')
        return

"""
As your answer to this part,
return the name of the method you decided to use in
matplotlib.

(Example: "boxplot" or "scatter")
"""

def q1():
    return "bar chart"

"""
2. A simple test case

To make sure your monitor is working, test it on a very simple
pipeline that adds up the total of all elements in a list.

We will compare three versions of the pipeline depending on the
input size.
"""

LIST_SMALL = [10] * 100
LIST_MEDIUM = [10] * 100_000
LIST_LARGE = [10] * 100_000_000

def add_list(l):
    total = 0
    for item in l:
        total += item
    return total

def q2a():
    # Create a ThroughputHelper object
    h = ThroughputHelper()
    
    # Add the 3 pipelines.
    h.add_pipeline("small", len(LIST_SMALL), lambda: add_list(LIST_SMALL))
    h.add_pipeline("medium", len(LIST_MEDIUM), lambda: add_list(LIST_MEDIUM))
    h.add_pipeline("large", len(LIST_LARGE), lambda: add_list(LIST_LARGE))

    # Generate throughputs and create plot
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q2a.png')

    return throughputs

"""
2b.
Which pipeline has the highest throughput?
Is this what you expected?

=== ANSWER Q2b BELOW ===

No, it found that the medium size pipeline had the highest throughput. 
I expected throughput to be proportional/increasing such that the largest dataset would have the largest throughput.

=== END OF Q2b ANSWER ===
"""

"""
3. Latency helper class.

Now we will create a similar helper class for latency.

The helper should assume a pipeline that only has *one* element
in the input dataset.

It should use the NUM_RUNS variable as with throughput.
"""

LIST_ONE_ITEM = [10]

class LatencyHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline latencies
        # This is set to None, but will be set to a list after latencies
        # are calculated.
        self.latencies = None

    def add_pipeline(self, name, func):
        self.names.append(name)
        self.pipelines.append(func)
        return

    def compare_latency(self):
        self.latencies = []

        for func in self.pipelines:
            total_time = 0

            for i in range(NUM_RUNS):
                start = time.perf_counter() # Timestamp at start of function
                func()
                end = time.perf_counter() # Timestamp at end of function
                total_time += end - start

            # Calculate latency in milliseconds and append to list 
            latency = (total_time / NUM_RUNS) * 1000 
            self.latencies.append(latency)

        return self.latencies

    def generate_plot(self, filename):
        plt.figure()
        plt.bar(self.names, self.latencies, label="Latency")
        plt.xlabel("Pipeline")
        plt.xticks(rotation=45)
        plt.ylabel("Latency (Milliseconds)")
        plt.title("Pipeline Latency Comparison")
        plt.legend()

        plt.savefig(filename, bbox_inches='tight')
        return

"""
As your answer to this part,
return the number of input items that each pipeline should
process if the class is used correctly.
"""

def q3():
    # Return the number of input items in each dataset,
    # for the latency helper to run correctly.
    return 1

"""
4. To make sure your monitor is working, test it on
the simple pipeline from Q2.

For latency, all three pipelines would only process
one item. Therefore instead of using
LIST_SMALL, LIST_MEDIUM, and LIST_LARGE,
for this question run the same pipeline three times
on a single list item.
"""

LIST_SINGLE_ITEM = [10] # Note: a list with only 1 item

def q4a():
    # Create a LatencyHelper object
    h = LatencyHelper()

    # Add the 3 pipelines.
    h.add_pipeline("one", lambda: add_list(LIST_SINGLE_ITEM))
    h.add_pipeline("two", lambda: add_list(LIST_SINGLE_ITEM))
    h.add_pipeline("three", lambda: add_list(LIST_SINGLE_ITEM))

    # Generate latencies and create plot
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q4a.png')

    return latencies

"""
4b.
How much did the latency vary between the three copies of the pipeline?
Is this more or less than what you expected?

=== ANSWER Q4b BELOW ===

About the same as expected. Since the calculation is so simple and the runtime is fast, I didn't expect for much variation in latency.
A difference of tenths of a microsecond is very small but expected.

=== END OF Q4b ANSWER ===
"""

"""
Now that we have our helpers, let's do a simple comparison.

NOTE: you may add other helper functions that you may find useful
as you go through this file.

5. Comparison on Part 1

Finally, use the helpers above to calculate the throughput and latency
of the pipeline in part 1.

Remember that for latency you should use a version of the pipeline with only one input row!
You may need to write a new version of the pipeline for this to work.
"""

# You will need these:
# part1.load_input
# part1.PART_1_PIPELINE

def q5a():
    t = ThroughputHelper()
    # Get size 
    dfs = part1.load_input()
    input_size = sum(len(df) for df in dfs)
    # Add part1 pipeline
    t.add_pipeline("part1_pipeline", input_size, part1.PART_1_PIPELINE)
    # Generate throughput
    throughput = t.compare_throughput()

    return throughput[0]

# Create new one line datasets and write them back to csv for latency problem
# I'm going to retain the row for UC Berkeley across the three dataframes
# This allows merge to work successfully (since the same University is in all dataframes) and requires the least adjustment to questions 20/21

def q5b_create_dataset():
    dfs = part1.load_input()
    year = 2019 # Start with first year (2019) and increment to 2021
    for df in dfs:
        df_singular = df[df['university'] == 'University of California, Berkeley (UCB)'].copy() # Retain only UC Berkeley observation
        assert len(df_singular) == 1
        df_singular.to_csv(f"data/{year}_singular.csv", encoding='latin-1', index=False) # Create and write out dataframes
        year += 1
    return 

# Run this first to create necessary files
q5b_create_dataset()

def PART_1_PIPELINE_SINGLE():
    dfs = part1.q5b_load_input()
    # Q1-Q6
    part1.q1(dfs)
    part1.q2(dfs)
    part1.q3(dfs)
    part1.q4(dfs)
    part1.q5a(dfs)
    part1.q5b(dfs)
    part1.q5c()
    part1.q6c()

    # Q7-Q10
    part1.q7(dfs)
    part1.q8a(dfs)
    part1.q9(dfs)

    avg_2021 = part1.q10_helper(dfs)
    part1.q10(avg_2021)

    # Q11-Q14
    part1.q11(avg_2021)
    part1.q12a_adjusted(avg_2021) # Adjusted to use new dataframe with one row
    part1.q13a(avg_2021)
    part1.q14a(avg_2021)

    # Q15-Q17
    top_10 = part1.q15_helper(dfs)
    part1.q15(top_10)
    part1.q16(top_10)
    part1.q17a(top_10)

    # Q18
    part1.q18(dfs)

    # Q20-Q21
    part1.q20a(dfs)
    part1.q20b(dfs)
    part1.q21_adjusted() # Adjusted to use new dataframe with one row
    
    return

def q5b():
    l = LatencyHelper()
    l.add_pipeline("part1_pipeline_singular", PART_1_PIPELINE_SINGLE)
    latency = l.compare_latency()

    return latency[0]

"""
===== Questions 6-10: Performance Comparison 1 =====

For our first performance comparison,
let's look at the cost of getting input from a file, vs. in an existing DataFrame.

6. We will use the same population dataset
that we used in lecture 3.

Load the data using load_input() given the file name.

- Make sure that you clean the data by removing
  continents and world data!
  (World data is listed under OWID_WRL)

Then, set up a simple pipeline that computes summary statistics
for the following:

- *Year over year increase* in population, per country

    (min, median, max, mean, and standard deviation)

How you should compute this:

- For each country, we need the maximum year and the minimum year
in the data. We should divide the population difference
over this time by the length of the time period.

- Make sure you throw out the cases where there is only one year
(if any).

- We should at this point have one data point per country.

- Finally, as your answer, return a list of the:
    min, median, max, mean, and standard deviation
  of the data.

Hints:
You can use the describe() function in Pandas to get these statistics.
You should be able to do something like
df.describe().loc["min"]["colum_name"]

to get a specific value from the describe() function.

You shouldn't use any for loops.
See if you can compute this using Pandas functions only.
"""

def load_input(filename):
    df = pd.read_csv(filename, encoding='latin-1')
    df = df.dropna(subset=['Code']) # Remove continents and other regions with missing codes
    df = df[df['Code'] != 'OWID_WRL'] # Remove World population

    return df

def population_pipeline(df):
    # Sort chronologically and group by country for calculations
    by_country = df.sort_values('Year').groupby('Entity') 

    # Find first and last years
    min_year = by_country['Year'].min().astype(int)
    max_year = by_country['Year'].max().astype(int)

    # Since dataframe is sorted by date within countries, ,first() and .last() will obtain population in first/last years
    first_population = by_country['Population (historical)'].first().astype(int)
    last_population = by_country['Population (historical)'].last().astype(int)

    # Calculate population increases, drop NAs (only one year available)
    population_increase = ((last_population - first_population) / (max_year - min_year)).dropna()
    metrics = population_increase.describe()

    # Returns as np float -> investigate in case of potential autograder problems
    return [float(metrics['min']), float(metrics['50%']), float(metrics['max']), float(metrics['mean']), float(metrics['std'])]

def q6():
    df = load_input('data/population.csv')
    result = population_pipeline(df)
    return result

"""
7. Varying the input size

Next we want to set up three different datasets of different sizes.

Create three new files,
    - data/population-small.csv
      with the first 600 rows
    - data/population-medium.csv
      with the first 6000 rows
    - data/population-single-row.csv
      with only the first row
      (for calculating latency)

You can edit the csv file directly to extract the first rows
(remember to also include the header row)
and save a new file.

Make four versions of load input that load your datasets.
(The _large one should use the full population dataset.)
Each should return a dataframe.

The input CSV file will have 600 rows, but the DataFrame (after your cleaning) may have less than that.
"""

# Generate new files
def generate_small():
    original = pd.read_csv('data/population.csv', encoding='latin-1')
    small = original.head(600)
    small.to_csv('data/population-small.csv', encoding='latin-1', index=False)
    return

def generate_medium():
    original = pd.read_csv('data/population.csv', encoding='latin-1')
    medium = original.head(6000)
    medium.to_csv('data/population-medium.csv', encoding='latin-1', index=False)
    return

def generate_single():
    original = pd.read_csv('data/population.csv', encoding='latin-1')
    single = original.head(1)
    single.to_csv('data/population-single-row.csv', encoding='latin-1', index=False)
    return

# Run to get new files
generate_small()
generate_medium()
generate_single()

# Use old load_input function to replicate cleaning on the new dataframes generated
def load_input_small():
    return load_input('data/population-small.csv')

def load_input_medium():
    return load_input('data/population-medium.csv')

def load_input_large():
    return load_input('data/population.csv')

def load_input_single_row():
    return load_input('data/population-single-row.csv')

def q7():
    # Don't modify this part
    s = load_input_small()
    m = load_input_medium()
    l = load_input_large()
    x = load_input_single_row()
    return [len(s), len(m), len(l), len(x)]

"""
8.
Create baseline pipelines

First let's create our baseline pipelines.
Create four pipelines,
    baseline_small
    baseline_medium
    baseline_large
    baseline_latency

based on the three datasets above.
Each should call your population_pipeline from Q6.

Your baseline_latency function will not be very interesting
as the pipeline does not produce any meaningful output on a single row!
You may choose to instead run an example with two rows,
or you may fill in this function in any other way that you choose
that you think is meaningful.
"""

def baseline_small():
    s = load_input_small()
    result = population_pipeline(s)
    return result

def baseline_medium():
    m = load_input_small()
    result = population_pipeline(m)
    return result

def baseline_large():
    l = load_input_small()
    result = population_pipeline(l)
    return result

def baseline_latency():
    x = load_input_small()
    result = population_pipeline(x)
    return result

def q8():
    # Don't modify this part
    _ = baseline_medium()
    return ["baseline_small", "baseline_medium", "baseline_large", "baseline_latency"]

"""
9.
Finally, let's compare whether loading an input from file is faster or slower
than getting it from an existing Pandas dataframe variable.

Create four new dataframes (constant global variables)
directly in the script.
Then use these to write 3 new pipelines:
    fromvar_small
    fromvar_medium
    fromvar_large
    fromvar_latency

These pipelines should produce the same answers as in Q8.

As your answer to this part;
a. Generate a plot in output/part2-q9a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, fromvar_small, fromvar_medium, fromvar_large
b. Generate a plot in output/part2-q9b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, fromvar_latency
"""

POPULATION_SMALL = load_input_small()
POPULATION_MEDIUM = load_input_medium()
POPULATION_LARGE = load_input_large()
POPULATION_SINGLE_ROW = load_input_single_row()

def fromvar_small():
    return population_pipeline(POPULATION_SMALL)

def fromvar_medium():
    return population_pipeline(POPULATION_MEDIUM)

def fromvar_large():
    return population_pipeline(POPULATION_LARGE)

def fromvar_latency():
    return population_pipeline(POPULATION_SINGLE_ROW)

def q9a():
    # Create a ThroughputHelper object
    h = ThroughputHelper()
    
    # Add the baseline pipelines
    h.add_pipeline("small_baseline", len(POPULATION_SMALL), baseline_small)
    h.add_pipeline("medium_baseline", len(POPULATION_MEDIUM), baseline_medium)
    h.add_pipeline("large_baseline", len(POPULATION_LARGE), baseline_large)

    # Add from var pipelines
    h.add_pipeline("small_fromvar", len(POPULATION_SMALL), fromvar_small)
    h.add_pipeline("medium_fromvar", len(POPULATION_MEDIUM), fromvar_medium)
    h.add_pipeline("large_fromvar", len(POPULATION_LARGE), fromvar_large)

    # Generate throughputs and create plot
    throughputs = h.compare_throughput()
    h.generate_plot('output/part2-q9a.png')

    return throughputs

def q9b():
    # Create a LatencyHelper object
    h = LatencyHelper()

    # Add the 2 pipelines
    h.add_pipeline("baseline", baseline_latency)
    h.add_pipeline("fromvar", fromvar_latency)

    # Generate latencies and create plot
    latencies = h.compare_latency()
    h.generate_plot('output/part2-q9b.png')

    return latencies

"""
10.
Comment on the plots above!
How dramatic is the difference between the two pipelines?
Which differs more, throughput or latency?
What does this experiment show?

===== ANSWER Q10 BELOW =====

The difference between the baseline and fromvar pipelines is large and increases exponentially with dataset size. 
The latency of the baseline was twice as large as the fromvar, and the large baseline throughput was three times bigger than the large fromvar throughput
Throughput differs more for large dataset, but latency differs more when considering the small and medium dataset throughput comparisons
Surprisingly, the fromvar small throughput actually appears larger than the baseline
This experience shows that loading an input from file is measurably slower than from a local pandas dataframe and that the difference increases with dataset size

===== END OF Q10 ANSWER =====
"""

"""
===== Questions 11-14: Performance Comparison 2 =====

Our second performance comparison will explore vectorization.

Operations in Pandas use Numpy arrays and vectorization to enable
fast operations.
In particular, they are often much faster than using for loops.

Let's explore whether this is true!

11.
First, we need to set up our pipelines for comparison as before.

We already have the baseline pipelines from Q8,
so let's just set up a comparison pipeline
which uses a for loop to calculate the same statistics.

Your pipeline should produce the same answers as in Q6 and Q8.

Create a new pipeline:
- Iterate through the dataframe entries. You can assume they are sorted.
- Manually compute the minimum and maximum year for each country.
- Compute the same answers as in Q6.
- Manually compute the summary statistics for the resulting list (min, median, max, mean, and standard deviation).
"""

def for_loop_pipeline(df):
    # Ensure sorted by year
    df = df.sort_values('Year')
    country_data = {}

    # Iterate through rows
    for i, row in df.iterrows():
        country = row['Entity'] 
        population = row['Population (historical)']
        year = row['Year']

        # For first observation of country set both min and max values
        if country not in country_data:
            country_data[country] = {
                'min_year': year,
                'max_year': year,
                'first_population': population,
                'last_population': population
            }
        else: 
            # Iteratively replace max values for year and population until there are no more observations
            country_data[country]['max_year'] = year
            country_data[country]['last_population'] = population

    increases = []
    for country, values in country_data.items():
        years = values['max_year'] - values['min_year']
        # Account for countries with only one year
        if years > 0: 
            increase = (values['last_population'] - values['first_population']) / years
            increases.append(increase)

    increases.sort() # Sort to simplify min and max search
    n = len(increases)
    minimum = increases[0]
    maximum = increases[-1]
    mean = sum(increases) / n

    # Calculate median, accounting for even and odd length 
    if n % 2 != 0:
        median = increases[n // 2] # Odd
    else:
        median = (increases[n/2] + increases[n/2 - 1]) / 2 # Even = find average of middle two

    # Calculate standard deviation manually
    variance = sum((x - mean) ** 2 for x in increases) / (n - 1)
    std = variance ** 0.5

    return [float(minimum), float(median), float(maximum), float(mean), float(std)]
        

def q11():
    df = load_input('data/population.csv')
    result = for_loop_pipeline(df)
    return result

"""
12.
Now, let's create our pipelines for comparison.

As before, write 4 pipelines based on the datasets from Q7.
"""

def for_loop_small():
    raise NotImplementedError

def for_loop_medium():
    raise NotImplementedError

def for_loop_large():
    raise NotImplementedError

def for_loop_latency():
    raise NotImplementedError

def q12():
    # Don't modify this part
    _ = for_loop_medium()
    return ["for_loop_small", "for_loop_medium", "for_loop_large", "for_loop_latency"]

"""
13.
Finally, let's compare our two pipelines,
as we did in Q9.

a. Generate a plot in output/part2-q13a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, for_loop_small, for_loop_medium, for_loop_large

b. Generate a plot in output/part2-q13b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, for_loop_latency
"""

def q13a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in output/part2-q13a.png
    # Return list of 6 throughputs
    raise NotImplementedError

def q13b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in output/part2-q13b.png
    # Return list of 2 latencies
    raise NotImplementedError

"""
14.
Comment on the results you got!

14a. Which pipelines is faster in terms of throughput?

===== ANSWER Q14a BELOW =====

===== END OF Q14a ANSWER =====

14b. Which pipeline is faster in terms of latency?

===== ANSWER Q14b BELOW =====

===== END OF Q14b ANSWER =====

14c. Do you notice any other interesting observations?
What does this experiment show?

===== ANSWER Q14c BELOW =====

===== END OF Q14c ANSWER =====
"""

"""
===== Questions 15-17: Reflection Questions =====
15.

Take a look at all your pipelines above.
Which factor that we tested (file vs. variable, vectorized vs. for loop)
had the biggest impact on performance?

===== ANSWER Q15 BELOW =====

===== END OF Q15 ANSWER =====

16.
Based on all of your plots, form a hypothesis as to how throughput
varies with the size of the input dataset.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q16 BELOW =====

===== END OF Q16 ANSWER =====

17.
Based on all of your plots, form a hypothesis as to how
throughput is related to latency.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q17 BELOW =====

===== END OF Q17 ANSWER =====
"""

"""
===== Extra Credit =====

This part is optional.

Use your pipeline to compare something else!

Here are some ideas for what to try:
- the cost of random sampling vs. the cost of getting rows from the
  DataFrame manually
- the cost of cloning a DataFrame
- the cost of sorting a DataFrame prior to doing a computation
- the cost of using different encodings (like one-hot encoding)
  and encodings for null values
- the cost of querying via Pandas methods vs querying via SQL
  For this part: you would want to use something like
  pandasql that can run SQL queries on Pandas data frames. See:
  https://stackoverflow.com/a/45866311/2038713

As your answer to this part,
as before, return
a. the list of 6 throughputs
and
b. the list of 2 latencies.

and generate plots for each of these in the following files:
    output/part2-ec-a.png
    output/part2-ec-b.png
"""

# Extra credit (optional)

def extra_credit_a():
    raise NotImplementedError

def extra_credit_b():
    raise NotImplementedError

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part2-answers.txt"
UNFINISHED = 0

def log_answer(name, func, *args):
    try:
        answer = func(*args)
        print(f"{name} answer: {answer}")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},{answer}\n')
            print(f"Answer saved to {ANSWER_FILE}")
    except NotImplementedError:
        print(f"Warning: {name} not implemented.")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},Not Implemented\n')
        global UNFINISHED
        UNFINISHED += 1

def PART_2_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    log_answer("q2a", q2a)
    # 2b: commentary
    log_answer("q3", q3)
    log_answer("q4a", q4a)
    # 4b: commentary
    log_answer("q5a", q5a)
    log_answer("q5b", q5b)

    # Q6-10
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    log_answer("q9a", q9a)
    log_answer("q9b", q9b)
    # 10: commentary

    # Q11-14
    log_answer("q11", q11)
    log_answer("q12", q12)
    log_answer("q13a", q13a)
    log_answer("q13b", q13b)
    # 14: commentary

    # 15-17: reflection
    # 15: commentary
    # 16: commentary
    # 17: commentary

    # Extra credit
    log_answer("extra credit (a)", extra_credit_a)
    log_answer("extra credit (b)", extra_credit_b)

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 2 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 2", PART_2_PIPELINE)
