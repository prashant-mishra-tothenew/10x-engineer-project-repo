"""Seed the database with sample data for testing"""

import requests
import random

BASE_URL = "http://localhost:8000"

def generate_random_prompts(n, collection_ids):
    """
    Generates n random prompts. Each prompt is associated with a random collection.
    """
    titles = [
        "Code Review", "Bug Finder", "Generate Docstrings", "Blog Idea Generator", "Email Campaign Planner",
        "API Design Consultant", "Testing Strategy Advisor", "UX Improvement Analyst", "SEO Audit Guide", 
        "Data Analysis Request", "Startup Pitch Enhancer", "Algorithm Complexity Assessor", "Security Audit Planner",
        "DevOps Process Advisor", "Content Strategy Developer", "Project Plan Evaluator", "Software Release Notes Writer",
        "Customer Feedback Collector", "Technical Writing Coach", "Interview Preparation Guide"
    ]

    descriptions = [
        "AI-driven analysis and feedback.", "Insightful and comprehensive reviews.", 
        "Creative and thoughtful insights.", "Strategically crafted with attention to detail.",
        "Data-backed guidance and recommendations.", "Straightforward and actionable steps.",
        "A holistic approach to identifying improvement areas.", "Effective strategies for reaching goals.",
        "Expert advice to increase efficiency and results.", "Proven techniques for success."
    ]
    
    contents = [
        "Analyze the following {{topic}} and provide detailed insights:\n\n{{details}}",
        "Prepare a comprehensive report on:\n\n{{topic}}",
        "Draft an email responding to {{situation}} using {{tone}} tone.",
        "Summarize the key points of the following {{content}}:",
        "Identify potential improvements for the {{system}} based on the following information:\n\n{{details}}"
    ]
    
    prompts = []

    for i in range(n):
        title = random.choice(titles) + f" Example {i+1}"
        description = random.choice(descriptions)
        content = random.choice(contents)
        collection_id = random.choice(collection_ids) if collection_ids else None
        prompts.append({
            "title": title,
            "content": content,
            "description": description,
            "collection_id": collection_id
        })

    return prompts

def seed_data():
    # Create collections
    collections = [
        {
            "name": "Development",
            "description": "Prompts for software development tasks"
        },
        {
            "name": "Writing",
            "description": "Prompts for content creation"
        }
    ]

    created_collections = []
    for coll in collections:
        response = requests.post(f"{BASE_URL}/collections", json=coll)
        if response.status_code == 201:
            created_collections.append(response.json())

    # Generate 50 prompts
    prompts = generate_random_prompts(50, [coll["id"] for coll in created_collections])

    for prompt in prompts:
        response = requests.post(f"{BASE_URL}/prompts", json=prompt)
        if response.status_code == 201:
            print(f"✓ Created prompt: {prompt['title']}")
        else:
            print(f"✗ Failed to create prompt: {prompt['title']}")

    print(f"\n✅ Seeding complete! Created {len(created_collections)} collections and {len(prompts)} prompts.")

if __name__ == "__main__":
    try:
        seed_data()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running at http://localhost:8000")