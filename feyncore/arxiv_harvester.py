import urllib, urllib.request

def search_arxiv(query="electron", max_results=1):
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}'
    data = urllib.request.urlopen(url)
    return data.read().decode('utf-8')

if __name__ == '__main__':
    print(search_arxiv())
