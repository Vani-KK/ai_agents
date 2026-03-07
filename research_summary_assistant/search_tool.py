from ddgs import DDGS

def search_web(query):

    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=5)

            for r in search_results:
                results.append({
                    "title": r["title"],
                    "link": r["href"]
                })

    except Exception as e:
        print("Search error:", e)

    return results