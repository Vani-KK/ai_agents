from search_tool import search_web
from reader_tool import read_article
from summarizer import summarize_text, synthesize_research

def research_agent(topic):
    

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

    print("\nReading articles...\n")

    # Collect up to 3 working articles
    articles = []

    for result in results:
        if len(articles) >= 3:  # stop after 3 successful reads
            break

        link = result["link"]
        print(f"Trying: {link}")

        text = read_article(link)

        if text and len(text) > 500:
            articles.append({"url": link, "text": text})
            print(f"✅ Extracted successfully ({len(text)} chars)\n")
        else:
            print("❌ Failed to extract useful text.\n")

    if len(articles) == 0:
        print("Could not extract text from any link.")
        return

    print(f"\nSuccessfully read {len(articles)} articles. Synthesizing...\n")

    # Synthesize all articles together
    final_report = synthesize_research(articles, topic)

    return final_report

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    result=research_agent(topic)
    print(result)