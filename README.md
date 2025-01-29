Web Content Analyzer
A powerful Python-based web scraping and content analysis tool that uses Playwright for web crawling and Google's Gemini Pro for intelligent content extraction and analysis.
Features

Asynchronous web crawling using Playwright
Intelligent content extraction and filtering
JSON validation using Google's Gemini Pro LLM
Support for both single URL and batch processing via CSV
Automated extraction of:

Product ratings and reviews
Price information
Review summaries and sentiment analysis


Results caching and export capabilities

Prerequisites

Python 3.7+
Google API Key for Gemini Pro
Required Python packages (see Installation section)

Installation

Clone the repository:

bashCopygit clone https://github.com/yourusername/web-content-analyzer.git
cd web-content-analyzer

Install required packages:

bashCopypip install -r requirements.txt

Set up your Google API key:

Get an API key from Google AI Studio
Set it as an environment variable:
bashCopyexport GOOGLE_API_KEY='your-api-key'

Or modify the script to use your key directly



Required Dependencies
plaintextCopyasyncio
playwright
pandas
google-generativeai
crawl4ai
Usage
Single URL Processing
To analyze a single URL:
bashCopypython main.py --url "https://example.com/product"
Batch Processing with CSV
To process multiple URLs from a CSV file:
bashCopypython main.py --csv "urls.csv"
The CSV file should have a column named 'url' containing the URLs to process.
Output Structure
The tool generates JSON output in the following format:
jsonCopy{
    "report": {
        "extraction": [{
            "fields": {
                "Ratings": "<number_of_ratings>",
                "Rated": "<average_rating>",
                "Price": "<price>",
                "ReviewSummary": "<summary>",
                "url": "<url>",
                "title": "<page_title>"
            }
        }]
    }
}
Results Storage

Individual results are saved as separate JSON files in the results directory
A combined result file (combined_results.json) is also generated
Each processing run creates new result files

Advanced Features
Content Filtering
The tool uses PruningContentFilter with configurable parameters:

Threshold: 0.48 (adjustable)
Threshold Type: "fixed"
Minimum Word Threshold: 0

Crawler Configuration
Customize crawling behavior through CrawlerRunConfig:

Cache modes: READ_ONLY, WRITE_ONLY, READ_WRITE
Excluded tags: nav, footer, aside
Overlay removal
Custom markdown generation options

Error Handling and Retries

Built-in retry mechanism for JSON validation
Maximum 8 retry attempts with 1-second delay
Comprehensive error logging

Contributing

Fork the repository
Create a feature branch: git checkout -b feature/YourFeature
Commit changes: git commit -am 'Add YourFeature'
Push to branch: git push origin feature/YourFeature
Submit a Pull Request

Error Handling
The script includes robust error handling:

JSON validation retries
URL processing error catching
CSV file validation
API key verification

License
[Add your chosen license here]
Acknowledgments

Google Generative AI for Gemini Pro
Playwright for web automation
Contributors and maintainers of dependent packages

Support
For issues, questions, or contributions, please:

Check existing issues
Create a new issue with detailed information
Follow the contribution guidelines


Note: Make sure to replace placeholder values (like API keys) and customize the repository URL before deploying.
