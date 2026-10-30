# Campaign Audit Quiz — AI Conversation

AI tool: ChatGPT

## Project setup
I created a repository named python-final-assignment and opened it in Codespaces.
I will save my prompts, AI responses, tests, and any errors and fixes as I work.
## Step 1 — Program planning

### My prompt 01
Please help me plan my Campaign Audit Quiz before writing code. Suggest a simple set of functions, including main(). Explain each function's purpose, inputs, and return value. Use the assignment guidelines and campaigns_A.csv I uploaded. Do not write the full program yet.

### ChatGPT response 01
I recommend **eight small functions**, each with one clear job. This follows your assignment’s flow: read the dataset, calculate indicators, ask five questions, check answers, display the score, and save `result.csv`. 03_Session_8_Final_Exam

**First, plan around your actual CSV**

Your `campaigns_A.csv` uses:

- A **semicolon (`;`) delimiter**.
- The columns `Campaign`, `Channel`, `Period`, `Impressions`, `Clicks`, `Cost (€)`, `Conversions`, an **unnamed empty column**, and `Revenue (€)`.
- **Decimal commas** in money values, such as `11088,60`.
- Missing impressions for **Monthly Newsletter**.
- Zero conversions for **Black Friday** and **App Install**. campaigns_A

The unnamed column can be ignored.

**Suggested functions**

The names below describe the structure only—there is no implementation yet.

| Function | Purpose | Inputs | Return value |
|---|---|---|---|
| `load_campaigns(filename)` | Read the CSV, skip blank rows and campaigns with missing impressions, convert numeric text into numbers, and ignore the unnamed column. | File path, such as `"campaigns_A.csv"`. | A **list of campaign dictionaries**, containing cleaned data. |
| `calculate_metrics(campaigns)` | Calculate CTR, CPA, and ROAS for each included campaign. Set CPA to `None` when conversions are zero. | The cleaned campaign list. | A campaign list with `CTR`, `CPA`, and `ROAS` added. |
| `build_questions(campaigns)` | Compute the five correct answers and pair each with its question and expected answer type. | Campaigns with calculated metrics. | A **list of five question dictionaries**. |
| `get_player_name()` | Ask for the player’s name and repeat the prompt if it is blank. | No function arguments; the player types a name. | The name as a **string**. |
| `check_answer(player_answer, correct_answer, answer_type)` | Compare text answers without case or surrounding-space differences; compare numeric answers as numbers. | The player’s answer, the calculated correct answer, and its type. | `True` if correct; otherwise `False`. |
| `run_quiz(questions)` | Ask the five questions, validate numeric input, call `check_answer()`, and add one point for each correct answer. | The question list. | The final score as an **integer from 0 to 5**. |
| `save_result(filename, player_name, score)` | Write the player’s name, score, and current date to the output CSV. | Output path, name, and score. | `None`; its result is the saved file. |
| `main()` | Coordinate all functions, display the final score, and handle errors with a message identifying the function that failed. | No arguments. | `None`. |

A **dictionary** stores named pieces of information about one item. For example, one campaign dictionary holds its name, channel, impressions, and other values. A **list** holds all those campaign dictionaries together.

**What `build_questions()` must calculate**

The correct answers must come from the data rather than being typed into the program. 03_Session_8_Final_Exam

| Question | Planned calculation | Answer type |
|---|---|---|
| Which campaign has the best CTR? | Find the campaign with the largest CTR. | Text: campaign name |
| Which campaign has the highest CPA? | Find the largest CPA, ignoring `None`. | Text: campaign name |
| How many campaigns have a ROAS above 3? | Count campaigns where ROAS is **strictly greater than 3**. | Integer |
| Which channel generated the most conversions in total? | Add conversions for each channel, then find the highest total. | Text: channel name |
| What is the average CTR, rounded to two decimals? | Add the individual CTR values, divide by the number of included campaigns, then round. | Decimal number |

For the average CTR, use the **arithmetic mean of individual campaign CTRs**, rather than total clicks divided by total impressions. Keep full precision until the final rounding.

The brief defines CTR as `clicks / impressions`. I would therefore keep it as a decimal ratio and explicitly say **“enter a decimal ratio, not a percentage”** in the question, so the player knows the expected unit. 03_Session_8_Final_Exam

**Important rules for the functions**

- **Missing impressions:** remove the campaign before any calculations—including channel conversion totals. Your file should therefore produce **11 included campaigns**.
- **Zero conversions:** keep the campaign for CTR, ROAS, and other calculations, but give it no CPA. Do not use zero as its CPA.
- **Decimal commas:** convert money values before doing arithmetic.
- **Invalid numeric answers:** ask the player to try again instead of crashing.
- **File errors:** let `main()` report a clear error if loading or saving fails. The assignment specifically asks for error handling and clear function names. 03_Session_8_Final_Exam

The intended order inside `main()` is:

1. Load `campaigns_A.csv`.
2. Calculate the metrics.
3. Build the questions and calculated answers.
4. Get the player’s name.
5. Run the quiz.
6. Display the score out of five.
7. Save `result.csv`.

When you start coding, work on **one function at a time**. Your teacher asks you to write comments in your own words, check a calculation by hand, and record AI exchanges—including errors and fixes—in `CONVERSATION.md` as you go. 03_Session_8_Final_Exam

### My prompt 02
Let's implement only the CSV loading function now.

My plan:
- Function name: load_campaigns(filename).
- Input: the CSV filename.
- Process: read the file using utf-8-sig encoding and a semicolon delimiter.
- Output: return a list of dictionaries, one per campaign.

The actual headers are:
Campaign;Channel;Period;Impressions;Clicks;Cost (€);Conversions;;Revenue (€)

For this step, keep values as strings and preserve all campaign records.
Do not calculate metrics or remove records yet.
The unnamed column can remain for now.
Let file-reading errors propagate so main() can handle them later.

Please use Python's built-in csv module and beginner-friendly syntax.
Give only this function, its necessary import, and a short temporary test.
Explain the code briefly so I can write my own comments.
Do not write the rest of the program.
### ChatGPT response 02
```python
import csv


def load_campaigns(filename):
    campaigns = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            campaigns.append(row)

    return campaigns


# Temporary test
campaigns = load_campaigns("campaigns_A.csv")
print("Number of campaigns:", len(campaigns))
print("First campaign:", campaigns[0])
```

- `utf-8-sig` handles UTF-8 files with or without a byte-order mark.
- `newline=""` lets the `csv` module handle line endings.
- `DictReader` uses the headers as dictionary keys. The unnamed column gets the key `""`.
- The loop adds each campaign dictionary to the list. All values remain strings, including empty cells.
- `with` closes the file automatically. Errors propagate because the function does not catch them.

Run the temporary test with the CSV in your current working directory. You should see **12 campaigns**, with **Winter Sale** printed first.

### Test result
I ran python campaign_audit.py.
It loaded 12 campaigns.
The first campaign was Winter Sale, and its cost was 11088,60.
These results matched the source CSV.

### My prompt 03
The loading test passed: 12 campaigns were loaded, the first campaign was Winter Sale, and its raw cost was 11088,60.

Now help me implement only clean_campaigns(raw_campaigns).

Input: the list of dictionaries returned by load_campaigns().
Process:
- Exclude any record with missing or whitespace-only Impressions.
- Remove surrounding whitespace from Campaign, Channel and Period.
- Convert Impressions, Clicks and Conversions to integers.
- Convert Cost (€) and Revenue (€) to floats after replacing decimal commas with decimal points.
- Remove the unnamed empty column.
- Keep campaigns with zero conversions.
- Copy each retained dictionary so the raw records are unchanged.
Output: return a new list of cleaned campaign dictionaries, keeping the original named column headers.

Do not calculate CTR, CPA or ROAS yet.
Let invalid numeric values raise an error for main() to handle later instead of silently dropping them.
Use beginner-friendly syntax. Give this function and a short temporary test only, with a concise explanation.
### ChatGPT response 03
```python
def clean_campaigns(raw_campaigns):
    cleaned_campaigns = []

    for raw_campaign in raw_campaigns:
        impressions = raw_campaign["Impressions"]

        if impressions is None or impressions.strip() == "":
            continue

        campaign = raw_campaign.copy()

        campaign["Campaign"] = campaign["Campaign"].strip()
        campaign["Channel"] = campaign["Channel"].strip()
        campaign["Period"] = campaign["Period"].strip()

        campaign["Impressions"] = int(impressions)
        campaign["Clicks"] = int(campaign["Clicks"])
        campaign["Conversions"] = int(campaign["Conversions"])

        campaign["Cost (€)"] = float(
            campaign["Cost (€)"].replace(",", ".")
        )
        campaign["Revenue (€)"] = float(
            campaign["Revenue (€)"].replace(",", ".")
        )

        if "" in campaign:
            del campaign[""]

        cleaned_campaigns.append(campaign)

    return cleaned_campaigns


# Temporary test
raw_campaigns = load_campaigns("campaigns_A.csv")
cleaned_campaigns = clean_campaigns(raw_campaigns)

print("Campaign counts:", len(raw_campaigns), len(cleaned_campaigns))
print("Raw cost:", raw_campaigns[0]["Cost (€)"])
print("Cleaned first campaign:", cleaned_campaigns[0])

for campaign in cleaned_campaigns:
    if campaign["Conversions"] == 0:
        print("Zero conversions retained:", campaign["Campaign"])
```

- `continue` skips records with missing or whitespace-only impressions.
- `.copy()` creates a separate dictionary, preserving the raw record.
- `.strip()` removes surrounding whitespace; `int()` and `float()` convert numeric strings.
- `.replace(",", ".")` prepares European decimal values for conversion.
- `del` removes the unnamed column. All named headers stay unchanged.
- Invalid numeric values raise an error naturally.

Expected results: **12 raw records, 11 cleaned records**, raw cost still **`11088,60`**, cleaned cost **`11088.6`**, and both **Black Friday** and **App Install** retained.

### clean_campaigns — Actual test result

Command:
```bash
python campaign_audit.py
```

### My Prompt 04
The cleaning test passed:
- 12 raw records and 11 cleaned records.
- The first cleaned cost is 11088.6.
- The original raw cost remains "11088,60".
- Both zero-conversion campaigns are retained.

Now help me implement only calculate_metrics(campaigns).

Input: cleaned campaign dictionaries with numeric values under
"Impressions", "Clicks", "Conversions", "Cost (€)" and "Revenue (€)".

Process:
- Calculate CTR = Clicks / Impressions.
- Calculate CPA = Cost (€) / Conversions.
- When Conversions is zero, set CPA to None, keeping that campaign
  and still calculating its CTR and ROAS.
- Calculate ROAS = Revenue (€) / Cost (€).
- Keep full precision; do not round yet.
- Copy each dictionary so the input records remain unchanged.

Output: a new list of dictionaries containing the original fields
plus "CTR", "CPA" and "ROAS".

Use beginner-friendly syntax. Give only this function and a short
temporary test that shows the metrics for Winter Sale and both
zero-conversion campaigns. Briefly explain the code.
Do not build the quiz or write result.csv yet.

### ChatGPT response 04
```python
def calculate_metrics(campaigns):
    campaigns_with_metrics = []

    for campaign in campaigns:
        updated_campaign = campaign.copy()

        updated_campaign["CTR"] = (
            campaign["Clicks"] / campaign["Impressions"]
        )

        if campaign["Conversions"] == 0:
            updated_campaign["CPA"] = None
        else:
            updated_campaign["CPA"] = (
                campaign["Cost (€)"] / campaign["Conversions"]
            )

        updated_campaign["ROAS"] = (
            campaign["Revenue (€)"] / campaign["Cost (€)"]
        )

        campaigns_with_metrics.append(updated_campaign)

    return campaigns_with_metrics


# Temporary test
raw_campaigns = load_campaigns("campaigns_A.csv")
cleaned_campaigns = clean_campaigns(raw_campaigns)
campaigns_with_metrics = calculate_metrics(cleaned_campaigns)

for campaign in campaigns_with_metrics:
    if campaign["Campaign"] in ["Winter Sale", "Black Friday", "App Install"]:
        print(campaign["Campaign"])
        print("CTR:", campaign["CTR"])
        print("CPA:", campaign["CPA"])
        print("ROAS:", campaign["ROAS"])
        print()
```

- `.copy()` preserves the input dictionary while allowing new metric fields.
- The `if` statement prevents division by zero for CPA. `None` means CPA is unavailable.
- CTR and ROAS are calculated for every campaign, including those with zero conversions.
- No rounding is applied.

The test should show numeric metrics for **Winter Sale**, and **CPA: None** with **ROAS: 0.0** for both zero-conversion campaigns.

### calculate_metrics — Actual test result

Command:
```bash
python campaign_audit.py
```

Output:
```text
Winter Sale
CTR: 0.017095406360424028
CPA: 38.23655172413793
ROAS: 5.268179030716231

Black Friday
CTR: 0.018252252252252254
CPA: None
ROAS: 0.0

App Install
CTR: 0.04052920560747664
CPA: None
ROAS: 0.0
```

### Manual calculation check — Winter Sale CPA

Formula: Cost / Conversions
Calculation: 11088.60 / 290
Program result: 38.23655172413793

My calculator result: 38.23655172413793
Does it match the program result? YES

### My Prompt 05
The metric tests passed for Winter Sale, Black Friday and App Install.

Now help me implement only get_quiz_answers(campaigns).

Input: the list returned by calculate_metrics(), containing the
original campaign fields plus CTR, CPA and ROAS.

Calculate and return a dictionary with these five keys:
- best_ctr_campaign: the campaign name with the highest CTR.
- highest_cpa_campaign: the campaign name with the highest CPA,
  excluding records whose CPA is None.
- roas_above_three: the number of campaigns with ROAS strictly > 3.
- top_conversion_channel: the channel with the highest total
  Conversions, summed across all its retained campaigns.
- average_ctr_percent: the arithmetic mean of the campaign CTR
  values, multiplied by 100 and rounded to two decimal places.

Use only the supplied cleaned records. Do not hard-code answers.
Keep zero-conversion campaigns in every calculation except CPA.
Do not modify the input records.
Raise ValueError with a clear message if the input is empty or
there are no valid CPA values.

Use beginner-friendly loops and clear variable names.
Give only this function and a short temporary test printing the
five answers, followed by a brief explanation.
Do not ask the player questions or save result.csv yet.

### ChatGPT response 05
```python
def get_quiz_answers(campaigns):
    if len(campaigns) == 0:
        raise ValueError("Cannot calculate quiz answers: no campaigns supplied.")

    best_ctr_campaign = campaigns[0]
    highest_cpa_campaign = None
    roas_above_three = 0
    channel_conversions = {}
    total_ctr = 0

    for campaign in campaigns:
        if campaign["CTR"] > best_ctr_campaign["CTR"]:
            best_ctr_campaign = campaign

        if campaign["CPA"] is not None:
            if highest_cpa_campaign is None:
                highest_cpa_campaign = campaign
            elif campaign["CPA"] > highest_cpa_campaign["CPA"]:
                highest_cpa_campaign = campaign

        if campaign["ROAS"] > 3:
            roas_above_three += 1

        channel = campaign["Channel"]

        if channel not in channel_conversions:
            channel_conversions[channel] = 0

        channel_conversions[channel] += campaign["Conversions"]
        total_ctr += campaign["CTR"]

    if highest_cpa_campaign is None:
        raise ValueError("Cannot calculate quiz answers: no valid CPA values.")

    top_conversion_channel = None

    for channel in channel_conversions:
        if top_conversion_channel is None:
            top_conversion_channel = channel
        elif (
            channel_conversions[channel]
            > channel_conversions[top_conversion_channel]
        ):
            top_conversion_channel = channel

    average_ctr_percent = round(total_ctr / len(campaigns) * 100, 2)

    return {
        "best_ctr_campaign": best_ctr_campaign["Campaign"],
        "highest_cpa_campaign": highest_cpa_campaign["Campaign"],
        "roas_above_three": roas_above_three,
        "top_conversion_channel": top_conversion_channel,
        "average_ctr_percent": average_ctr_percent
    }


# Temporary test
raw_campaigns = load_campaigns("campaigns_A.csv")
cleaned_campaigns = clean_campaigns(raw_campaigns)
campaigns_with_metrics = calculate_metrics(cleaned_campaigns)
quiz_answers = get_quiz_answers(campaigns_with_metrics)

for answer_name, answer_value in quiz_answers.items():
    print(answer_name, ":", answer_value)
```

- The first loop finds the highest CTR and valid CPA, counts ROAS values above three, totals conversions by channel, and adds all CTR values.
- The second loop finds the channel with the highest conversion total.
- The average uses each campaign’s CTR equally, converts it to a percentage, and rounds only the final result.
- Input records are only read. Zero-conversion campaigns remain included except in the CPA comparison.
- Empty input or no valid CPA raises `ValueError`. Ties keep the first campaign or channel encountered.

### My Prompt 06
The get_quiz_answers() test passed. Its output was:
best_ctr_campaign: Aurora Launch
highest_cpa_campaign: Blog Traffic
roas_above_three: 7
top_conversion_channel: YouTube Ads
average_ctr_percent: 2.6

Now implement only run_quiz(quiz_answers).

Ask these five questions in order:
1. Which campaign has the highest CTR?
2. Which campaign has the highest CPA?
3. How many campaigns have ROAS strictly greater than 3?
4. Which channel has the highest total conversions?
5. What is the arithmetic mean campaign CTR as a percentage,
   rounded to two decimal places? Tell the player to enter a
   number without the % symbol.

Compare answers with the corresponding values in quiz_answers.
Do not hard-code the correct answers.

For text answers, ignore capitalization and surrounding whitespace.
For question 3, accept an integer.
For question 5, accept a decimal point or decimal comma and compare
the input rounded to two decimal places with the expected answer.

If numeric input is invalid, explain and ask that question again.
Award one point per correct answer. After each valid answer, show
whether it was correct and show the correct answer if it was wrong.
Return the integer score out of five.

Use beginner-friendly code. Provide only this function and a short
temporary test using the existing functions.
Do not request the player's name, write result.csv, or implement
main() yet.

### ChatGPT response 06
def run_quiz(quiz_answers):
    questions = [
        (
            "1. Which campaign has the highest CTR?",
            "best_ctr_campaign",
            "text"
        ),
        (
            "2. Which campaign has the highest CPA?",
            "highest_cpa_campaign",
            "text"
        ),
        (
            "3. How many campaigns have ROAS strictly greater than 3?",
            "roas_above_three",
            "integer"
        ),
        (
            "4. Which channel has the highest total conversions?",
            "top_conversion_channel",
            "text"
        ),
        (
            "5. What is the arithmetic mean campaign CTR as a percentage, "
            "rounded to two decimal places?\n"
            "Enter a number without the % symbol.",
            "average_ctr_percent",
            "decimal"
        )
    ]

    score = 0

    for question, answer_key, answer_type in questions:
        correct_answer = quiz_answers[answer_key]

        while True:
            player_answer = input(question + "\nYour answer: ").strip()

            try:
                if answer_type == "integer":
                    is_correct = int(player_answer) == correct_answer

                elif answer_type == "decimal":
                    numeric_answer = float(player_answer.replace(",", "."))

                    if (
                        numeric_answer != numeric_answer
                        or numeric_answer == float("inf")
                        or numeric_answer == float("-inf")
                    ):
                        raise ValueError("Please enter a finite number.")

                    is_correct = (
                        round(numeric_answer, 2) == round(correct_answer, 2)
                    )

                else:
                    is_correct = (
                        player_answer.lower() == correct_answer.strip().lower()
                    )

                break

            except ValueError:
                if answer_type == "integer":
                    print("Invalid input. Please enter an integer, such as 4.")
                else:
                    print(
                        "Invalid input. Please enter a finite number "
                        "using a decimal point or comma, without %."
                    )

        if is_correct:
            score += 1
            print("Correct!")
        else:
            print("Incorrect. The correct answer is:", correct_answer)

        print()

    return score


# Temporary test
raw_campaigns = load_campaigns("campaigns_A.csv")
cleaned_campaigns = clean_campaigns(raw_campaigns)
campaigns_with_metrics = calculate_metrics(cleaned_campaigns)
quiz_answers = get_quiz_answers(campaigns_with_metrics)

score = run_quiz(quiz_answers)
print("Final score:", score, "/ 5")

### My Prompt 07
The interactive quiz test is complete.

Now help me implement only:
save_result(player_name, score, filename="result.csv")

Requirements:
- Use csv.writer to save the player's name, score and today's date.
- Use these column headings: Player Name, Score, Date.
- Format the date as YYYY-MM-DD using date.today().isoformat().
- Open the file in write mode with encoding="utf-8" and newline="".
- Each save should overwrite the previous file with one header row
  and one result row.
- Use the supplied player_name and score; do not hard-code them
  inside the function.
- Let file-writing errors propagate so main() can handle them later.

The program already imports csv.
Show any additional import separately.

Give only this function and a short temporary test calling it with
"Test Player" and 5, then reading the CSV back to print its contents.
These are temporary test values, not a real quiz result.

Use beginner-friendly code and briefly explain it.
Do not implement main() or rewrite the existing functions yet.

### ChatGPT response 07
Additional import:

```python
from datetime import date
```

Function:

```python
def save_result(player_name, score, filename="result.csv"):
    today = date.today().isoformat()

    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Player Name", "Score", "Date"])
        writer.writerow([player_name, score, today])
```

Temporary test:

```python
save_result("Test Player", 5)

with open("result.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

- `date.today().isoformat()` produces today’s date as `YYYY-MM-DD`.
- `"w"` overwrites the file each time.
- The two `writerow()` calls write the headings and supplied result.
- Writing errors propagate because the function does not catch them.
- The test saves temporary values, then reads and prints both rows.

### My Prompt 08
The save_result() test passed. Reading the file back printed:
['Player Name', 'Score', 'Date']
['Test Player', '5', '2026-10-30']

Now implement only main() and the if __name__ == "__main__" guard.

Reuse these existing functions without rewriting them:
- load_campaigns(filename)
- clean_campaigns(raw_campaigns)
- calculate_metrics(campaigns)
- get_quiz_answers(campaigns)
- run_quiz(quiz_answers)
- save_result(player_name, score, filename="result.csv")

The main() function should:
1. Load campaigns_A.csv, clean the records, calculate metrics,
   and get the quiz answers.
2. Display a short welcome message.
3. Ask for the player's name, strip surrounding whitespace,
   and ask again if the name is empty.
4. Run the quiz.
5. Display the player's name and final score out of five.
6. Save the actual name and returned score to result.csv.
7. Confirm saving only after it succeeds.

Handle missing or unreadable input files, malformed CSV data,
invalid numeric data, missing required columns and division by
zero with clear messages, then stop before starting the quiz.

Handle output-file errors separately. If saving fails, explain
that the displayed score could not be saved.

Use specific exception types instead of a bare except.
Use beginner-friendly code.

Give only main() and its entry-point guard, followed by a brief
explanation. Explain which temporary test code I should remove.

### ChatGPT response 08
```python
def main():
    stage = "load_campaigns"

    try:
        raw_campaigns = load_campaigns("campaigns_A.csv")

        stage = "CSV validation"
        required_columns = [
            "Campaign", "Channel", "Period", "Impressions",
            "Clicks", "Cost (€)", "Conversions", "Revenue (€)"
        ]

        for campaign in raw_campaigns:
            if None in campaign:
                raise csv.Error("A row contains more fields than the header.")

            for column in required_columns:
                if column not in campaign:
                    raise KeyError(column)

                if campaign[column] is None:
                    raise csv.Error("A row contains fewer fields than the header.")

        stage = "clean_campaigns"
        cleaned_campaigns = clean_campaigns(raw_campaigns)

        stage = "calculate_metrics"
        campaigns_with_metrics = calculate_metrics(cleaned_campaigns)

        stage = "get_quiz_answers"
        quiz_answers = get_quiz_answers(campaigns_with_metrics)

    except FileNotFoundError:
        print("Input error: campaigns_A.csv was not found.")
        return

    except PermissionError:
        print("Input error: permission was denied when reading campaigns_A.csv.")
        return

    except OSError as error:
        print("Input error: campaigns_A.csv could not be read:", error)
        return

    except UnicodeError as error:
        print("Input error: campaigns_A.csv is not valid UTF-8:", error)
        return

    except csv.Error as error:
        print("CSV error during", stage + ":", error)
        return

    except KeyError as error:
        print("Missing required column during", stage + ":", error)
        return

    except ValueError as error:
        print("Data error during", stage + ":", error)
        return

    except ZeroDivisionError:
        print(
            "Data error during", stage + ":",
            "Impressions and Cost (€) must not be zero."
        )
        return

    print("Welcome to the Campaign Audit Quiz!")

    while True:
        player_name = input("Enter your name: ").strip()

        if player_name != "":
            break

        print("Your name cannot be empty. Please try again.")

    score = run_quiz(quiz_answers)

    print(player_name + ", your final score is:", score, "/ 5")

    try:
        save_result(player_name, score)

    except (OSError, UnicodeError, csv.Error) as error:
        print("Your displayed score could not be saved to result.csv:", error)
        return

    print("Your result was saved to result.csv.")


if __name__ == "__main__":
    main()
```

`main()` prepares the data before welcoming the player. Input or calculation errors stop the program before the quiz starts. Saving has its own error handler, so a failed save does not hide the displayed score. The guard starts `main()` only when this file is run directly.

Remove **all previous temporary test blocks**, including standalone loading, cleaning, metric printing, answer printing, quiz calls, and the `"Test Player"` save/read-back test. Keep your imports and six existing function definitions, then place this code at the bottom.

### Development tests and final run — Actual terminal output

Command:
```bash
python campaign_audit.py
```

Output:
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
Campaigns loaded: 12
First campaign: Winter Sale
First cost: 11088,60
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
Raw campaigns: 12
Cleaned campaigns: 11
First cleaned cost: 11088.6
First raw cost: 11088,60
Zero-conversion campaigns kept: 2
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
Winter Sale
CTR: 0.017095406360424028
CPA: 38.23655172413793
ROAS: 5.268179030716231

Black Friday
CTR: 0.018252252252252254
CPA: None
ROAS: 0.0

App Install
CTR: 0.04052920560747664
CPA: None
ROAS: 0.0

@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
best_ctr_campaign: Aurora Launch
highest_cpa_campaign: Blog Traffic
roas_above_three: 7
top_conversion_channel: YouTube Ads
average_ctr_percent: 2.6
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
1. Which campaign has the highest CTR?
Your answer: AURORA LAUNCH
Correct!

2. Which campaign has the highest CPA?
Your answer:    Winter Sale
Incorrect. The correct answer is: Blog Traffic

3. How many campaigns have ROAS strictly greater than 3?
Your answer: abc
Invalid input. Please enter an integer, such as 4.
3. How many campaigns have ROAS strictly greater than 3?
Your answer: 7
Correct!

4. Which channel has the highest total conversions?
Your answer:    youtube ads
Correct!

5. What is the arithmetic mean campaign CTR as a percentage, rounded to two decimal places?
Enter a number without the % symbol.
Your answer: 260
Incorrect. The correct answer is: 2.6

Final score: 3 / 5
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
1. Which campaign has the highest CTR?
Your answer: Aurora Launch
Correct!

2. Which campaign has the highest CPA?
Your answer: Blog Traffic
Correct!

3. How many campaigns have ROAS strictly greater than 3?
Your answer: 7
Correct!

4. Which channel has the highest total conversions?
Your answer: YouTube Ads
Correct!

5. What is the arithmetic mean campaign CTR as a percentage, rounded to two decimal places?
Enter a number without the % symbol.
Your answer: hello
Invalid input. Please enter a finite number using a decimal point or comma, without %.
5. What is the arithmetic mean campaign CTR as a percentage, rounded to two decimal places?
Enter a number without the % symbol.
Your answer: 2.60
Correct!

Final score: 5 / 5
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
['Player Name', 'Score', 'Date']
['Test Player', '5', '2026-10-30']
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
Welcome to the Campaign Audit Quiz!
Enter your name:        Aurora Launch
1. Which campaign has the highest CTR?
Your answer:    Blog Traffic
Incorrect. The correct answer is: Aurora Launch

2. Which campaign has the highest CPA?
Your answer: 7
Incorrect. The correct answer is: Blog Traffic

3. How many campaigns have ROAS strictly greater than 3?
Your answer: 
Invalid input. Please enter an integer, such as 4.
3. How many campaigns have ROAS strictly greater than 3?
Your answer: 
Invalid input. Please enter an integer, such as 4.
3. How many campaigns have ROAS strictly greater than 3?
Your answer: 
Invalid input. Please enter an integer, such as 4.
3. How many campaigns have ROAS strictly greater than 3?
Your answer: 
Invalid input. Please enter an integer, such as 4.
3. How many campaigns have ROAS strictly greater than 3?
Your answer: python campaign_audit.py
Invalid input. Please enter an integer, such as 4.
3. How many campaigns have ROAS strictly greater than 3?
Your answer: 7
Correct!

4. Which channel has the highest total conversions?
Your answer:    YouTube Ads
Correct!

5. What is the arithmetic mean campaign CTR as a percentage, rounded to two decimal places?
Enter a number without the % symbol.
Your answer: 2.60
Correct!

Aurora Launch, your final score is: 3 / 5
Your result was saved to result.csv.
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ python campaign_audit.py
Welcome to the Campaign Audit Quiz!
Enter your name: 
Your name cannot be empty. Please try again.
Enter your name: YU SHAN YEH
1. Which campaign has the highest CTR?
Your answer:    Aurora Launch
Correct!

2. Which campaign has the highest CPA?
Your answer:    Blog Traffic
Correct!

3. How many campaigns have ROAS strictly greater than 3?
Your answer: 7
Correct!

4. Which channel has the highest total conversions?
Your answer:    YouTube Ads
Correct!

5. What is the arithmetic mean campaign CTR as a percentage, rounded to two decimal places?
Enter a number without the % symbol.
Your answer: 2.60
Correct!

YU SHAN YEH, your final score is: 5 / 5
Your result was saved to result.csv.
@yushanyeh-skema ➜ /workspaces/python-final-assignment (main) $ 
```