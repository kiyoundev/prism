import re
import tldextract
from typing import List, Dict, Any, Optional

# Suspicious TLDs often used in scams
SUSPICIOUS_TLDS = {
    'xyz', 'top', 'vip', 'info', 'club', 'live', 'shop', 'site', 'work', 
    'click', 'link', 'icu', 'buzz', 'best', 'online', 'art', 'pro', 'cc'
}

# Common URL shorteners
SHORTENERS = {
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'buff.ly', 
    'adf.ly', 'bit.do', 'mcaf.ee', 'su.pr', 'ow.ly', 'rb.gy'
}

class URLChecker:
    def __init__(self, brands_config: Dict[str, Any] = None):
        """
        Initialize with optional brand configuration for allowlist checking.
        brands_config structure: { "category": [ { "slug": "brand", "domains": ["valid.com"] } ] }
        """
        self.brand_domains = self._build_brand_map(brands_config) if brands_config else {}
        self.ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

    def _build_brand_map(self, config: Dict[str, Any]) -> Dict[str, List[str]]:
        """Flatten brand config into a map of slug -> list of valid domains."""
        brand_map = {}
        for category, brands in config.items():
            for brand in brands:
                if 'domains' in brand:
                    brand_map[brand['slug']] = brand['domains']
        return brand_map

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text using regex."""
        # Simple regex for URL extraction
        return re.findall(r'https?://[^\s]+', text)

    def analyze_url(self, url: str, matched_brand_slug: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a single URL for risk signals.
        If matched_brand_slug is provided, checks against that brand's allowlist.
        """
        report = {
            "url": url,
            "risk_score": 0.0,
            "signals": [],
            "details": {}
        }

        # 1. Parse URL
        try:
            parsed = tldextract.extract(url)
            domain = f"{parsed.domain}.{parsed.suffix}"
            subdomain = parsed.subdomain
            fqdn = f"{subdomain}.{domain}" if subdomain else domain
            
            # Helper for full domain check (e.g. tracking.purolator.com)
            registered_domain = f"{parsed.domain}.{parsed.suffix}"
        except Exception:
            report["risk_score"] = 0.5
            report["signals"].append("MALFORMED_URL")
            return report

        # 2. Check for IP address usage (high risk)
        if self.ip_pattern.match(parsed.domain):
            report["risk_score"] = 1.0
            report["signals"].append("IP_ADDRESS_URL")
            # Usually strict scam
            return report

        # 3. Check Shorteners
        if registered_domain in SHORTENERS:
            report["risk_score"] += 0.4
            report["signals"].append("URL_SHORTENER")
        
        # 4. Check Suspicious TLDs
        if parsed.suffix in SUSPICIOUS_TLDS:
            report["risk_score"] += 0.3
            report["signals"].append(f"SUSPICIOUS_TLD_{parsed.suffix.upper()}")

        # 5. Brand Verification (if brand context exists)
        if matched_brand_slug:
            valid_domains = self.brand_domains.get(matched_brand_slug, [])
            if valid_domains:
                # Check if the registered domain is in the allowlist
                if registered_domain in valid_domains:
                    report["risk_score"] = 0.0
                    report["signals"].append("OFFICIAL_DOMAIN_MATCH")
                    report["is_safe"] = True
                else:
                    # Brand is mentioned but domain doesn't match -> High probability of Typosquatting/Phishing
                    report["risk_score"] += 0.6  # Boost significantly
                    report["signals"].append("BRAND_DOMAIN_MISMATCH")
                    
                    # Check for brand name in the domain (Typosquatting/Subdomain abuse)
                    # e.g. brand="purolator", domain="purolator-delivery.com" or "purolator.badsite.com"
                    clean_brand = matched_brand_slug.replace("-", "")
                    if clean_brand in fqdn.replace("-", ""):
                        report["risk_score"] += 0.3
                        report["signals"].append("TYPOSQUATTING_SUSPICION")

        return report

# Example usage for quick testing
if __name__ == "__main__":
    # Mock config
    mock_config = {
        "delivery": [
            {"slug": "purolator", "domains": ["purolator.com", "purolator.ca"]}
        ]
    }
    checker = URLChecker(mock_config)
    
    test_urls = [
        ("https://purolator.com/track", "purolator"),
        ("https://purolator-delivery.com/track", "purolator"),
        ("http://192.168.1.1/login", None),
        ("https://bit.ly/claim-prize", None),
        ("https://netflix.vip/login", None)
    ]
    
    for url, brand in test_urls:
        print(f"Analyzing {url} (Brand: {brand}):")
        print(checker.analyze_url(url, brand))
        print("-" * 20)