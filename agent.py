import json
import sys
import string
from typing import List, Dict, Set

# --- Constants for configuration ---
KNOWLEDGE_BASE_FILE = "filum_features.json"
STOPWORDS = {"a", "an", "the", "to", "is", "it", "of", "in", "for", "on", "with", "as", "by", "at", "that", "this", "was", "were", "be", "are", "from", "or", "and", "we're", "our", "we", "they", "us"}
RELEVANCE_THRESHOLD = 0.1  # Lowered threshold to allow more potential matches
CONTEXT_BOOST = 0.15

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculates the Jaccard similarity between two sets."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def preprocess_text(text: str) -> Set[str]:
    """Converts text to lowercase, removes punctuation and stopwords, and returns a set of keywords."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return {word for word in words if word not in STOPWORDS}

def load_knowledge_base(file_path: str) -> List[Dict]:
    """Loads the feature knowledge base from a JSON file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Knowledge base file not found at '{file_path}'.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'. Check for syntax errors.", file=sys.stderr)
        sys.exit(1)

def suggest_solutions(input_data: Dict, features: List[Dict]) -> Dict:
    """Analyzes a pain point and suggests solutions from the knowledge base."""
    pain_point = input_data.get("pain_point")
    if not pain_point:
        return {"error": "Input JSON must contain a 'pain_point' field."}

    context = input_data.get("context", {})
    pain_keywords = preprocess_text(pain_point)
    
    suggestions = []
    for feature in features:
        # Combine all relevant text fields from the feature for a richer keyword set
        feature_text = ' '.join(
            feature.get("keywords", []) +
            feature.get("pain_points_addressed", []) +
            [feature.get("feature_name", ""), feature.get("description", "")]
        )
        feature_keywords = preprocess_text(feature_text)
        
        score = jaccard_similarity(pain_keywords, feature_keywords)
        
        # Boost score if context (e.g., industry) is relevant
        if "industry" in context and context["industry"] in ' '.join(feature.get("categories", [])).lower():
            score += CONTEXT_BOOST
        score = min(score, 1.0)  # Cap score at 1.0
        
        if score >= RELEVANCE_THRESHOLD:
            # Create a more dynamic "how_it_helps" message
            description = feature.get('description', 'provides a solution').rstrip('. ')
            # Make the description fit grammatically into the sentence.
            desc_text = description[0].lower() + description[1:] if description else ""
            how_it_helps = (
                f"To address the issue of '{pain_point.lower()}', this feature "
                f"{desc_text}."
            )
            
            suggestions.append({
                "feature_name": feature["feature_name"],
                "categories": feature["categories"],
                "description": feature["description"],
                "how_it_helps": how_it_helps,
                "relevance_score": round(score, 2),
                "more_info_link": feature["more_info_link"]
            })
    
    suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    output = {
        "pain_point_summary": pain_point,
        "suggested_solutions": suggestions
    }
    if not suggestions:
        output["no_match_reason"] = "No matching Filum.ai features were found for this specific pain point."
    
    return output

def main():
    """Main function to run the agent from command line input."""
    try:
        input_json = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input provided.", file=sys.stderr)
        sys.exit(1)

    features = load_knowledge_base(KNOWLEDGE_BASE_FILE)
    result = suggest_solutions(input_json, features)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
