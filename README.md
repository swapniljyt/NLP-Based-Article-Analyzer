Project Description
This project aims to extract textual data from a list of articles provided in an Excel file and perform various text analysis computations. The goal is to compute specific variables related to the text's sentiment and complexity, which are described in detail below.

Objective
The objective of this assignment is to:

Extract textual data from articles listed in the provided input.xlsx file.
Perform text analysis to compute the following variables:
POSITIVE SCORE
NEGATIVE SCORE
POLARITY SCORE
SUBJECTIVITY SCORE
AVG SENTENCE LENGTH
PERCENTAGE OF COMPLEX WORDS
FOG INDEX
AVG NUMBER OF WORDS PER SENTENCE
COMPLEX WORD COUNT
WORD COUNT
SYLLABLE PER WORD
PERSONAL PRONOUNS
AVG WORD LENGTH
Features
Data Extraction from URLs
Text Preprocessing
Sentiment Analysis
Readability Analysis
Statistical Analysis
Methodology
Data Extraction
Input Data: The URLs of the articles are provided in input.xlsx.
Text Extraction: Using Python libraries such as BeautifulSoup, Selenium, or Scrapy, the article title and text are extracted from each URL, excluding any headers, footers, or other non-article content. The extracted text is saved in a text file named with the corresponding URL_ID.
Text Analysis
For each extracted article, the following analyses are performed:

Positive and Negative Score: Calculated based on the presence of positive and negative words in the text.
Polarity Score: Measures the overall sentiment of the text (-1 to 1 scale).
Subjectivity Score: Determines the degree to which the text is subjective or objective.
Average Sentence Length: Average number of words per sentence.
Percentage of Complex Words: Proportion of complex words in the text.
Fog Index: A readability test to determine the complexity of the text.
Average Number of Words per Sentence: Similar to average sentence length but considers different segmentation.
Complex Word Count: Total number of complex words in the text.
Word Count: Total number of words in the text.
Syllable per Word: Average number of syllables per word.
Personal Pronouns: Count of personal pronouns in the text.
Average Word Length: Average length of the words in the text.
Output
The computed variables are saved in an output file following the structure provided in Output Data Structure.xlsx.

Results
The results of the text analysis are saved in a CSV or Excel file as specified in the output structure. The file includes all input variables along with the computed output variables.

Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch.
Make your changes.
Submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or inquiries, please contact swapnil Jyot at swapniljytkd888@gmail.com