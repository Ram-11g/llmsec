import json
import logging
from datetime import datetime
from pentest.scrapers import (
    ArxivScraper,
    OWASPScraper,
    MITREScraper,
    SecurityBlogScraper
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_advanced_attacks():
    """Scrape advanced attack vectors from multiple sources."""
    # Initialize scrapers
    arxiv_scraper = ArxivScraper()
    owasp_scraper = OWASPScraper()
    mitre_scraper = MITREScraper()
    security_blog_scraper = SecurityBlogScraper()

    # Advanced keywords for searching
    advanced_keywords = [
        "LLM security",
        "LLM vulnerabilities",
        "LLM attacks",
        "LLM prompt injection",
        "LLM jailbreak",
        "LLM adversarial attacks",
        "LLM model extraction",
        "LLM data leakage",
        "LLM code injection",
        "LLM prompt manipulation",
        "LLM system prompt extraction",
        "LLM role playing attacks",
        "LLM token smuggling",
        "LLM prompt leaking",
        "LLM prompt engineering attacks"
    ]

    # Collect data from all sources
    all_data = []

    # 1. Collect from arXiv
    logger.info("Collecting data from arXiv...")
    arxiv_data = arxiv_scraper.collect_data(advanced_keywords, max_results=20)
    all_data.extend(arxiv_data)

    # 2. Collect from OWASP
    logger.info("Collecting data from OWASP...")
    owasp_data = owasp_scraper.collect_data()
    all_data.extend(owasp_data)

    # 3. Collect from MITRE
    logger.info("Collecting data from MITRE...")
    mitre_data = mitre_scraper.collect_data()
    all_data.extend(mitre_data)

    # 4. Collect from Security Blogs
    logger.info("Collecting data from Security Blogs...")
    blog_data = security_blog_scraper.collect_data(advanced_keywords)
    all_data.extend(blog_data)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"advanced_attack_vectors_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(all_data)} advanced attack vectors to {output_file}")
    return all_data

if __name__ == "__main__":
    scrape_advanced_attacks() 