# AI-Engineer-Assignments
# Pain Point to Solution Agent

This project contains a prototype for the "Pain Point to Solution Agent," designed to meet the requirements of the AI Engineer assignment. The agent takes a user's described business pain point and suggests relevant Filum.ai features that can help address it.

## Project Structure

- `main.md`: The detailed design document outlining the agent's architecture, input/output formats, and knowledge base structure.
- `agent.py`: The core Python script for the prototype. It contains the logic for loading the knowledge base, processing input, and matching pain points to solutions.
- `filum_features.json`: The knowledge base for the agent, containing a list of Filum.ai features, their descriptions, and associated keywords.
- `input.json`: A sample input file used for demonstrating how to run the agent.
- `README.md`: This file, providing setup and usage instructions.

## Setup

This prototype is written in standard Python 3 and does not require any external libraries. You only need a working Python 3 interpreter.

## How to Run the Agent

The agent is designed to be run from the command line, reading a JSON object from standard input.

1.  **Prepare the Input**: Create a JSON file (e.g., `input.json`) with the pain point and any relevant context. The structure should be as follows:

    ```json
    {
      "pain_point": "A description of the business pain point.",
      "context": {
        "industry": "e.g., retail",
        "business_size": "e.g., medium"
      }
    }
    ```

2.  **Execute the Script**: Use a pipe (`|`) to send the contents of your input file to the `agent.py` script.

    On Windows (Command Prompt):
    ```sh
    type input.json | python agent.py
    ```

    On macOS/Linux (or Windows PowerShell):
    ```sh
    cat input.json | python agent.py
    ```

## Example

Here is a complete example of running the agent.

### 1. Example Input (`input.json`)

```json
{
  "pain_point": "It's difficult to get a single view of a customer's interaction history when they contact us",
  "context": {
    "industry": "retail",
    "business_size": "medium"
  }
}
```

### 2. Command

```sh
type input.json | python agent.py
```

### 3. Corresponding Output

The agent will produce the following JSON output, suggesting the most relevant solution:

```json
{
  "pain_point_summary": "It's difficult to get a single view of a customer's interaction history when they contact us",
  "suggested_solutions": [
    {
      "feature_name": "Customer Profile with Interaction History",
      "categories": [
        "Customer 360 - Customers & AI Inbox"
      ],
      "description": "Provides a unified view of customer interactions across channels.",
      "how_it_helps": "To address the issue of 'it's difficult to get a single view of a customer's interaction history when they contact us', this feature provides a unified view of customer interactions across channels.",
      "relevance_score": 0.47,
      "more_info_link": "https://filum.ai/docs/customer-360"
    }
  ]
}