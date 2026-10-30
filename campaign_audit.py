import csv
from datetime import date

# Read the raw campaign data from the semicolon-separated CSV file.
def load_campaigns(filename):
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)

# Skip campaigns with missing impressions and convert text values to numbers.
# Keep a separate copy so the raw data stays unchanged.
def clean_campaigns(raw_campaigns):
    cleaned_campaigns = []

    for row in raw_campaigns:
        if not (row.get("Impressions") or "").strip():
            continue

        cleaned = row.copy()
        cleaned.pop("", None)

        for column in ["Campaign", "Channel", "Period"]:
            cleaned[column] = cleaned[column].strip()

        for column in ["Impressions", "Clicks", "Conversions"]:
            cleaned[column] = int(cleaned[column].strip())

        for column in ["Cost (€)", "Revenue (€)"]:
            cleaned[column] = float(cleaned[column].strip().replace(",", "."))

        cleaned_campaigns.append(cleaned)

    return cleaned_campaigns
# Calculate CTR, CPA and ROAS for each campaign.
# Use None for CPA when conversions are zero because division by zero is undefined.
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


# Calculate the five correct answers from the campaign data.
# Add conversions by channel and use the arithmetic mean for average CTR.
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
        "average_ctr_percent": average_ctr_percent,
    }
# Ask five questions and give one point for each correct answer.
# Ask again if numeric input is invalid so the quiz does not crash.
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


# Save the player's name, score and today's date.
# Overwrite the file to keep only the latest result.
def save_result(player_name, score, filename="result.csv"):
    today = date.today().isoformat()

    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Player Name", "Score", "Date"])
        writer.writerow([player_name, score, today])


# Run the data preparation, quiz and saving steps in order.
# Stop if the data is invalid and report any problem saving the score.
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