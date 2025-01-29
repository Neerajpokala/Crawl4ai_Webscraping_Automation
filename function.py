import asyncio
import os
import json
import csv
import time
from playwright.async_api import async_playwright
import pandas as pd

from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

import google.generativeai as genai

# Configure Google Generative AI
os.environ['GOOGLE_API_KEY'] = 'Get Your API Key Here'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def validate_json_with_llm(content: str, max_retries=8, delay=1) -> dict:
    """
    Validate and format content using the LLM with retry logic.
    
    Args:
        content (str): Content to validate
        max_retries (int): Maximum number of retry attempts
        delay (int): Delay in seconds between retries
    """
    validation_prompt = """Format the content as JSON with this exact structure:
    {
        "report": {
            "extraction": [{
                "fields": {
                    "Ratings": "<value>",
                    "Rated": "<value>",
                    "Price": "<value>",
                    "ReviewSummary": "<value>",
                    "url": "<value>",
                    "title": "<value>"
                }
            }]
        }
    }"""

    for attempt in range(max_retries):
        try:
            # First try to parse as JSON directly
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                pass

            # If direct parsing fails, use LLM to format
            result = model.generate_content(validation_prompt + "\n\nContent to format:\n" + content)
            formatted_content = result.text.strip()
            
            # Try to parse the formatted content
            try:
                json_data = json.loads(formatted_content)
                print(f"Successfully validated JSON on attempt {attempt + 1}")
                return json_data
            except json.JSONDecodeError:
                # If we still can't parse it, try to clean up common issues
                cleaned_content = formatted_content.replace("```json", "").replace("```", "").strip()
                json_data = json.loads(cleaned_content)
                print(f"Successfully validated JSON after cleaning on attempt {attempt + 1}")
                return json_data
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise ValueError(f"Failed to generate valid JSON after {max_retries} attempts: {str(e)}")
    
    raise ValueError("Failed to generate valid JSON after all attempts")

def crawl_and_generate_response(url):
    async def clean_content():
        async with AsyncWebCrawler(verbose=True) as crawler:
            config = CrawlerRunConfig(
                cache_mode=CacheMode.READ_ONLY,
                excluded_tags=['nav', 'footer', 'aside'],
                remove_overlay_elements=True,
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter(threshold=0.48, threshold_type="fixed", min_word_threshold=0),
                    options={"ignore_links": True}
                ),
            )
            result = await crawler.arun(
                url=url,
                config=config,
            )
            return result.markdown_v2.fit_markdown

    async def get_title():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            title = await page.title()
            await browser.close()
            return title

    filtered_markdown = asyncio.run(clean_content())
    page_title = asyncio.run(get_title())

    prompt = (
        f"Extract the following information from the provided markdown content and provide it as a JSON report: \n"
        f"- Number of Ratings (This is how many members rated the product, example: 47 reviews. Ratings is a big number, it can be greater than 5 but rated cannot be greater than 5)\n"
        f"- Rating Score (It is the average score that all reviewers rated, it will be from 1 to 5, example: 4.86 rated)\n"
        f"- Price of the product\n"
        f"- Give what customers sentiment of the product. Review summary mentioning what is best and worst in the product in 2 lines\n"
        f"- Title: {page_title}\n"
        f"Response format: {{\"report\": {{\"extraction\": [{{\"fields\": {{\"Ratings\": \"<value>\", \"Rated\": \"<value>\", \"Price\": \"<value>\", \"ReviewSummary\": \"<value>\", \"url\": \"{url}\", \"title\": \"{page_title}\"}}}}]}}}}\n"
        f"Markdown Output: {filtered_markdown}"
    )

    result = model.generate_content(prompt)
    
    try:
        json_data = validate_json_with_llm(result.text)
        print("Valid JSON response received")
        return json_data
    except ValueError as e:
        print(f"JSON validation failed for URL {url}: {e}")
        return None

def process_csv_urls(csv_path):
    """
    Process multiple URLs from a CSV file.
    
    Args:
        csv_path (str): Path to the CSV file containing URLs
    """
    try:
        df = pd.read_csv(csv_path)
        if 'url' not in df.columns:
            raise ValueError("CSV must contain a column named 'url'")
        
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        
        all_results = []
        
        for index, row in df.iterrows():
            url = row['url'].strip()
            print(f"\nProcessing URL {index + 1}/{len(df)}: {url}")
            
            try:
                result = crawl_and_generate_response(url)
                if result:
                    all_results.append(result)
                    
                    # Save individual result
                    with open(f"{results_dir}/result_{index + 1}.json", "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=4)
                
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                continue
        
        # Save combined results
        if all_results:
            with open(f"{results_dir}/combined_results.json", "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=4)
            print(f"\nResults saved in {results_dir} directory")
        
        return all_results
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Process URLs from a CSV file')
    parser.add_argument('--csv', type=str, help='Path to CSV file containing URLs')
    parser.add_argument('--url', type=str, help='Single URL to process')
    
    args = parser.parse_args()
    
    if args.csv:
        print(f"Processing URLs from CSV file: {args.csv}")
        results = process_csv_urls(args.csv)
        if results:
            print("\nProcessing completed successfully")
    elif args.url:
        print(f"Processing single URL: {args.url}")
        try:
            result = crawl_and_generate_response(args.url)
            if result:
                print("\nLLM Response (JSON):\n")
                print(json.dumps(result, indent=4))
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Please provide either a CSV file path with --csv or a single URL with --url")
