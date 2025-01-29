# **Web Scraping and Data Extraction with AI**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.30%2B-green)
![Google Generative AI](https://img.shields.io/badge/Google%20Generative%20AI-0.1%2B-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red)

This repository contains a Python-based solution for automating web scraping, data extraction, and reporting using **Playwright**, **Google Generative AI (Gemini Pro)**, and **crawl4ai**. The script extracts structured data from websites, validates it using AI, and generates reports in JSON and CSV formats. It also includes a **Streamlit app** for user-friendly interaction.

---

## **Features**

- **Web Scraping**: Extract clean, structured content from websites using Playwright and crawl4ai.
- **AI-Powered Data Extraction**: Use Google's Generative AI (Gemini Pro) to extract specific fields like ratings, price, and review summaries.
- **JSON Validation**: Ensure the extracted data is in the correct JSON format using retry logic.
- **CSV Export**: Convert the results into a CSV file for easy analysis.
- **Streamlit App**: Upload a CSV file containing URLs, process them, and download the results.

---

## **Prerequisites**

Before running the script, ensure you have the following installed:

1. **Python 3.8+**
2. **Playwright**: Install Playwright and its browsers.
   ```bash
   pip install playwright
   playwright install
   ```
3. **Google Generative AI Library**:
   ```bash
   pip install google-generativeai
   ```
4. **crawl4ai**:
   ```bash
   pip install crawl4ai
   ```
5. **Pandas**:
   ```bash
   pip install pandas
   ```
6. **Streamlit** (for the app):
   ```bash
   pip install streamlit
   ```

---

## **Getting Started**

### 1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/web-scraping-ai.git
   cd web-scraping-ai
   ```

### 2. **Set Up Google API Key**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the **Generative AI API**.
   - Generate an API Key from the **Credentials** page.
   - Set the API Key in your environment:
     ```bash
     export GOOGLE_API_KEY='your-api-key-here'
     ```
   - Alternatively, add the API Key directly in the script:
     ```python
     import os
     os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'
     ```

### 3. **Prepare the CSV File**
   Create a CSV file (`urls.csv`) with a column named `url`. Each row should contain a unique URL to be processed. Example:
   ```csv
   url
   https://example.com/product1
   https://example.com/product2
   https://example.com/product3
   ```

---

## **Usage**

### **Option 1: Run the Script Directly**
1. **Process a Single URL**:
   ```bash
   python script.py --url "https://example.com"
   ```
2. **Process Multiple URLs from a CSV File**:
   ```bash
   python script.py --csv urls.csv
   ```

   The results will be saved in the `results` directory as:
   - Individual JSON files (`result_1.json`, `result_2.json`, etc.).
   - A combined JSON file (`combined_results.json`).
   - A CSV file (`combined_results.csv`).

### **Option 2: Use the Streamlit App**
1. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```
2. **Upload a CSV File**:
   - Open the app in your browser.
   - Upload a CSV file containing URLs.
3. **Start Processing**:
   - Click the "Start Processing" button to extract data from the URLs.
4. **Download Results**:
   - View the extracted data in the app.
   - Download the results as a CSV file.

---

## **Code Structure**

- **`script.py`**: The main script for web scraping and data extraction.
- **`app.py`**: The Streamlit app for user-friendly interaction.
- **`results/`**: Directory where the output files (JSON and CSV) are saved.
- **`urls.csv`**: Example CSV file containing URLs to be processed.

---

## **Example Output**

### **JSON Output**
```json
{
  "report": {
    "extraction": [
      {
        "fields": {
          "Ratings": "47",
          "Rated": "4.86",
          "Price": "$99",
          "ReviewSummary": "Great product with excellent features.",
          "url": "https://example.com/product1",
          "title": "Product 1"
        }
      }
    ]
  }
}
```

### **CSV Output**
| Ratings | Rated | Price | ReviewSummary               | url                          | title     |
|---------|-------|-------|-----------------------------|------------------------------|-----------|
| 47      | 4.86  | $99   | Great product with excellent features. | https://example.com/product1 | Product 1 |

---

## **Contributing**

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- [Playwright](https://playwright.dev/) for browser automation.
- [Google Generative AI](https://ai.google.dev/) for data extraction.
- [crawl4ai](https://github.com/crawl4ai/crawl4ai) for web crawling and content filtering.
- [Streamlit](https://streamlit.io/) for building the interactive app.

---

## **Contact**

For questions or feedback, please contact:  
**Your Name**  
**Email**: your.email@example.com  
**GitHub**: [your-username](https://github.com/your-username)

---

**Happy Scraping!** 🚀


