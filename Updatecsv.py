from src.data_extractor import (
    url_to_dataframe,
    calculate_sentiment_scores,
    calculate_sentence_complexity_metrics,
    calculate_average_words_per_sentence,
    calculate_complex_word_count,
    calculate_total_cleaned_words,
    calculate_syllable_counts,
    count_personal_pronouns,
    calculate_average_word_length
)

import pandas as pd



input_file_path = '/root/src/NLP-Based-Article-Analyzer/Input.csv'
output_file_path = '/root/src/NLP-Based-Article-Analyzer/Output Data Structure.csv'

input_df = pd.read_csv(input_file_path)

output_df = pd.read_csv(output_file_path)

input_df.head(), output_df.head()

n=0
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    df = url_to_dataframe(url)

    sentiment_scores = calculate_sentiment_scores(df)

    sentence_complexity_metrics = calculate_sentence_complexity_metrics(df)
    avg_words_per_sentence = calculate_average_words_per_sentence(df)
    complex_word_count = calculate_complex_word_count(df)
    total_cleaned_words = calculate_total_cleaned_words(df)
    syllables_per_word_result, total_syllables_result, average_syllables_per_word_result = calculate_syllable_counts(df)
    personal_pronouns_count = count_personal_pronouns(df)
    avg_word_length = calculate_average_word_length(df)

    output_df.at[index, 'POSITIVE SCORE'] = sentiment_scores['Positive Score']
    output_df.at[index, 'NEGATIVE SCORE'] = sentiment_scores['Negative Score']
    output_df.at[index, 'POLARITY SCORE'] = sentiment_scores['Polarity Score']
    output_df.at[index, 'SUBJECTIVITY SCORE'] = sentiment_scores['Subjectivity Score']

    output_df.at[index, 'AVG SENTENCE LENGTH'] = sentence_complexity_metrics['Average Sentence Length']
    output_df.at[index, 'PERCENTAGE OF COMPLEX WORDS'] = sentence_complexity_metrics['Percentage of Complex Words']
    output_df.at[index, 'FOG INDEX'] = sentence_complexity_metrics['Fog Index']
    output_df.at[index, 'AVG NUMBER OF WORDS PER SENTENCE'] = avg_words_per_sentence
    output_df.at[index, 'COMPLEX WORD COUNT'] = complex_word_count
    output_df.at[index, 'WORD COUNT'] = total_cleaned_words
    output_df.at[index, 'SYLLABLE PER WORD'] = average_syllables_per_word_result
    output_df.at[index, 'PERSONAL PRONOUNS'] = personal_pronouns_count
    output_df.at[index, 'AVG WORD LENGTH'] = avg_word_length
    n=n+1
    print(f"{n}.URL DECODING........")

print("Parameter Updated in Dataframe Sucessfully....")


# Assuming output_df is the updated DataFrame you want to save
output_file_path = '/root/src/NLP-Based-Article-Analyzer/Output Data Structure.csv'

# Save the DataFrame to a CSV file
output_df.to_csv(output_file_path, index=False)

print(f"Updated DataFrame saved to {output_file_path}")