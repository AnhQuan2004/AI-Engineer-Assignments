# Pain Point to Solution Agent Design Document

## 1. Agent's Input Definition

### Proposed Structure and Format
The agent's input should be structured as a JSON object to ensure clarity, parsability, and extensibility. This format allows for easy integration into APIs, scripts, or user interfaces while preventing ambiguity in free-form text. The proposed schema is:

```json
{
  "pain_point": "string",
  "context": {
    "industry": "string",
    "business_size": "string",
    "current_tools": ["string"],
    "priority_aspects": ["string"]
  }
}
```

If no context is provided, the agent defaults to general assumptions (e.g., mid-sized business in a generic service industry).

### Rationale
- **Clarity and Structure**: JSON enforces a consistent format, reducing errors in interpretation compared to plain text. For example, plain text might mix pain points with context, leading to parsing issues.
- **Extensibility**: The optional "context" object allows for future enhancements without breaking existing inputs.
- **Effectiveness**: The core "pain_point" captures the user's issue succinctly, while context enables more personalized matching (e.g., prioritizing AI-driven solutions for large-scale businesses). This is beneficial for understanding nuances, such as whether the pain point involves high-volume interactions or specific integrations.
- **Guidelines for Users**: Instruct users to keep the pain_point concise (under 100 words) and factual, focusing on customer experience or service issues.

For the given pain point example ("It's difficult to get a single view of a customer's interaction history when they contact us"), a sample input JSON would be:
```json
{
  "pain_point": "It's difficult to get a single view of a customer's interaction history when they contact us",
  "context": {
    "industry": "retail",
    "business_size": "medium"
  }
}
```

## 2. Agent's Output Definition

### Proposed Structure and Format
The agent's output should be a JSON object for machine-readability and easy rendering in UIs or further processing. It includes a list of suggested solutions sorted by relevance. The schema is:

```json
{
  "pain_point_summary": "string",
  "suggested_solutions": [
    {
      "feature_name": "string",
      "categories": ["string"],
      "description": "string",
      "how_it_helps": "string",
      "relevance_score": 0.95,
      "more_info_link": "string"
    }
  ],
  "no_match_reason": "string"
}
```

If no solutions match, "suggested_solutions" is an empty array, and "no_match_reason" is populated.

### Rationale
- **Actionable and Understandable**: Each solution includes essential details: name for identification, description for context, how_it_helps for direct relevance, and a link for deeper exploration. The relevance_score helps users prioritize.
- **Structure Benefits**: JSON arrays allow easy iteration in code or display in tables/lists. Sorting by score ensures the best matches appear first.
- **User-Friendliness**: The pain_point_summary confirms understanding, building trust. This format is versatile for outputs like console prints, web responses, or emails.
- **Completeness**: Includes edge cases (no matches) to avoid silent failures.

For the example pain point, a sample output might be:
```json
{
  "pain_point_summary": "Difficulty accessing a unified view of customer interaction history during support interactions.",
  "suggested_solutions": [
    {
      "feature_name": "Customer Profile with Interaction History",
      "categories": ["Customer 360", "Customers & AI Inbox"],
      "description": "A centralized profile that aggregates all customer data and interactions.",
      "how_it_helps": "Consolidates all touchpoints and past interactions for a comprehensive view, enabling faster and more informed support responses.",
      "relevance_score": 0.95,
      "more_info_link": "https://filum.ai/docs/customer-360"
    }
  ]
}
```

## 3. Feature Knowledge Base Structure

### Proposed Data Structure
Use a JSON file for simplicity, portability, and ease of loading in Python. The schema is an array of feature objects:

```json
[
  {
    "feature_name": "string",
    "categories": ["string"],
    "description": "string",
    "keywords": ["string"],
    "pain_points_addressed": ["string"],
    "more_info_link": "string"
  }
]
```

Sample knowledge base based on provided Filum.ai examples (filum_features.json):

```json
[
  {
    "feature_name": "Automated Post-Purchase Surveys",
    "categories": ["VoC - Surveys"],
    "description": "Automatically sends surveys via email or SMS after transactions.",
    "keywords": ["customer feedback", "post-purchase", "surveys", "consistent collection"],
    "pain_points_addressed": ["Struggling to collect customer feedback consistently after a purchase."],
    "more_info_link": "https://filum.ai/docs/voc-surveys"
  },
  {
    "feature_name": "AI Agent for FAQ & First Response",
    "categories": ["AI Customer Service - AI Inbox"],
    "description": "Handles common queries with instant AI responses.",
    "keywords": ["repetitive questions", "support overload", "FAQ deflection"],
    "pain_points_addressed": ["Support agents overwhelmed by high volume of repetitive questions."],
    "more_info_link": "https://filum.ai/docs/ai-inbox"
  },
  {
    "feature_name": "Customer Journey Experience Analysis",
    "categories": ["Insights - Experience"],
    "description": "Analyzes feedback and data to identify friction in customer journeys.",
    "keywords": ["touchpoint frustration", "journey analysis", "friction points"],
    "pain_points_addressed": ["No clear idea which customer touchpoints are causing the most frustration."],
    "more_info_link": "https://filum.ai/docs/insights-experience"
  },
  {
    "feature_name": "Customer Profile with Interaction History",
    "categories": ["Customer 360 - Customers & AI Inbox"],
    "description": "Provides a unified view of customer interactions across channels.",
    "keywords": ["single view", "interaction history", "customer profile", "consolidated touchpoints"],
    "pain_points_addressed": ["Difficult to get a single view of a customer's interaction history when they contact us."],
    "more_info_link": "https://filum.ai/docs/customer-360"
  },
  {
    "feature_name": "AI-Powered Topic & Sentiment Analysis for VoC",
    "categories": ["VoC - Conversations/Surveys", "Insights - Experience"],
    "description": "Automatically analyzes text feedback for themes and emotions.",
    "keywords": ["open-ended responses", "theme analysis", "sentiment extraction", "time-consuming manual review"],
    "pain_points_addressed": ["Manually analyzing thousands of open-ended survey responses for common themes is too time-consuming."],
    "more_info_link": "https://filum.ai/docs/voc-analysis"
  }
]
```

### Rationale
- **Essential Attributes**: Keywords and pain_points_addressed enable effective matching (e.g., via string similarity or embedding). Categories aid in grouping, description/how_it_helps derive from it, and links provide actionability.
- **Why JSON?**: Lightweight, human-readable, and natively supported in Python (via json module). Scalable to databases if needed later.
- **Matching Relevance**: Attributes like keywords allow for fuzzy matching against pain points, improving accuracy over exact strings.
- **Filum.ai Alignment**: Structure is informed by examples, focusing on customer experience features like VoC, AI Inbox, and Insights.

## 4. Agent's Core Logic & Matching Approach

### Outline
1. **Load Knowledge Base**: Read the JSON file into memory as a list of dicts.
2. **Parse Input**: Load JSON input, extract pain_point and context.
3. **Preprocess Pain Point**: Lowercase, remove stopwords (using simple list or NLTK if available), extract key phrases.
4. **Matching Algorithm**:
   - For each feature, compute relevance_score using keyword overlap (e.g., Jaccard similarity: intersection/union of pain_point keywords and feature keywords/pain_points_addressed).
   - Threshold: Only include features with score > 0.5.
   - Incorporate context: Boost score if context matches (e.g., +0.1 for industry alignment, if KB extended with industry tags).
   - Sort suggestions descending by score.
5. **Generate Output**: Construct JSON with summaries and solutions. Derive how_it_helps dynamically (e.g., template: "This feature [description] by [specific benefit based on match]").
6. **Edge Cases**: If no matches, provide no_match_reason (e.g., "No direct Filum.ai feature matches; consider custom integration.").

### Justifications
- **Simplicity for Prototype**: Jaccard similarity is lightweight, no ML needed (uses set operations in Python). Scalable to cosine similarity with TF-IDF if vectors added (using numpy/scipy).
- **Accuracy**: Keyword-based matching leverages explicit attributes, reducing false positives. Context boosts personalization.
- **Efficiency**: O(n) for n features; suitable for small KB. For larger, index with FAISS or embeddings.
- **Rationale for Approach**: Focuses on semantic relevance without overcomplicating (e.g., no full NLP model required). Justified by examples where pain points directly map to features via keywords like "interaction history".
## 5. (Optional) Prototype

A lightweight Python prototype was implemented to validate this logic. It uses Jaccard similarity for keyword-based matching. See `agent.py` in the repository for details.
