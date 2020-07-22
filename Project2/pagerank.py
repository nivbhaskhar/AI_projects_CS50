import os
import random
import re
import sys
from collections import defaultdict
import numpy as np


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_of_next_page = {}
    links_from_page = corpus[page]
    no_of_links_from_page = len(links_from_page)
    no_of_pages = len(corpus)

    scaling_factor = 1
    if links_from_page:
        scaling_factor = 1-damping_factor
        
    for filename in corpus:
            probability_of_next_page[filename] = scaling_factor/no_of_pages
            
    for neighbor in links_from_page:
         probability_of_next_page[neighbor] += damping_factor/no_of_links_from_page
        
    return probability_of_next_page
    
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    freq_of_visits = defaultdict(int)
    list_of_pages = list(sorted(corpus.keys()))
    no_of_pages = len(list_of_pages)
    current_page = random.choice(list_of_pages)
    
    for counter in range(n):
        freq_of_visits[current_page] += 1
        transition_probabilities = transition_model(corpus, current_page, damping_factor)
        next_page_number = None
        p = 0
        pseudo_random_number = random.random()
        for page_number in range(no_of_pages):
            p += transition_probabilities[list_of_pages[page_number]]
            next_page_number = page_number
            if pseudo_random_number < p:
                break

        if next_page_number is None:
            current_page = random.choice(list_of_pages)
        else:
            current_page = list_of_pages[next_page_number]

    for page in freq_of_visits:
        freq_of_visits[page]/= n
    return freq_of_visits
            
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    no_of_pages = len(corpus)
    
    index = {} 
    scaled_out_going_links = {}
    for i, page in enumerate(sorted(corpus.keys())):
        if len(corpus[page])>0:
            scaled_out_going_links[page] = damping_factor/len(corpus[page])
        else:
            scaled_out_going_links[page] = damping_factor/no_of_pages
        index[page] = i

    #Transition matrix T[i,j] = scaled_outgoing_links[j] if j->i, 0 otherwise
    transition_matrix = np.zeros((no_of_pages, no_of_pages), dtype=float)
    for page in index:
        j = index[page]
        if corpus[page]:
            for linkedpage in corpus[page]:
                i = index[linkedpage]
                transition_matrix[i,j] = scaled_out_going_links[page]
        else:
            for i in range(no_of_pages):
                 transition_matrix[i,j] = scaled_out_going_links[page]
   

                        
    page_rank_col = np.array([1/no_of_pages]*no_of_pages)
    no_of_negligible_differences = 0
    
    while(no_of_negligible_differences < 100):
        updated_page_rank_col = np.dot(transition_matrix, page_rank_col) + ((1-damping_factor)/no_of_pages)
        if all(map(lambda x: (abs(x) <= 0.001), page_rank_col - updated_page_rank_col)):
            no_of_negligible_differences += 1
        page_rank_col = updated_page_rank_col


    page_rank = {}
    for page in corpus:
        page_rank[page] = page_rank_col[index[page]].item()
    return page_rank


if __name__ == "__main__":
    main()
