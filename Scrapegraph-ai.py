from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "model": "ollama/mistral",
        "temperature": 0,
        "format": "json",  # Ollama 需要显式指定格式
        "base_url": "http://localhost:11434",  # 设置 Ollama URL
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",  # 设置 Ollama URL
    },
    "verbose": True,
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me the mp4 url in the video tag",
    # 也接受已下载的 HTML 代码的字符串
    source="https://fyptt.to/16961/beautiful-slim-brunette-with-sexy-tan-lines-spreading-her-pussy-on-tiktok/",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)