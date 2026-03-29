from search_tool import search_web
from reader_tool import read_article
from summarizer import summarize_text


def research_agent():

    topic = input("Enter research topic: ")

    print("\nSearching the web...\n")

    results = search_web(topic)

    if len(results) == 0:
        print("No search results found.")
        return

    # Print search results
    for i, r in enumerate(results):
        print(f"{i+1}. {r['title']}")
        print(r["link"])
        print()

    print("\nReading article...\n")

    article_text = None

    # Try reading multiple links until one works
    for result in results:
        link = result["link"]
        print(f"Trying: {link}")

        text = read_article(link)

        if text and len(text) > 500:
            article_text = text
            print("Article extracted successfully.\n")
            break
        else:
            print("Failed to extract useful text.\n")

    if article_text is None:
        print("Could not extract article text from any link.")
        return

    print("\nSummarizing...\n")

    summary = summarize_text(article_text,topic,link)

    print("\nFINAL SUMMARY:\n")
    print(summary)


if __name__ == "__main__":
    research_agent()