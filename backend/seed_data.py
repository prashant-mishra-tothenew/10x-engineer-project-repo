"""Seed the database with sample data for testing"""

import random

import requests

BASE_URL = "http://localhost:8000"

# Tag definitions
TAGS = [
    {"name": "python"},
    {"name": "javascript"},
    {"name": "ai"},
    {"name": "web"},
    {"name": "api"},
    {"name": "database"},
    {"name": "testing"},
    {"name": "devops"},
    {"name": "security"},
    {"name": "documentation"},
]


def generate_random_prompts(n, collection_ids, tag_names):
    """
    Generates n random prompts. Each prompt is associated with a random collection and 1-3 tags.
    """
    titles = [
        "Code Review",
        "Bug Finder",
        "Generate Docstrings",
        "Blog Idea Generator",
        "Email Campaign Planner",
        "API Design Consultant",
        "Testing Strategy Advisor",
        "UX Improvement Analyst",
        "SEO Audit Guide",
        "Data Analysis Request",
        "Startup Pitch Enhancer",
        "Algorithm Complexity Assessor",
        "Security Audit Planner",
        "DevOps Process Advisor",
        "Content Strategy Developer",
        "Project Plan Evaluator",
        "Software Release Notes Writer",
        "Customer Feedback Collector",
        "Technical Writing Coach",
        "Interview Preparation Guide",
    ]

    descriptions = [
        "AI-driven analysis and feedback.",
        "Insightful and comprehensive reviews.",
        "Creative and thoughtful insights.",
        "Strategically crafted with attention to detail.",
        "Data-backed guidance and recommendations.",
        "Straightforward and actionable steps.",
        "A holistic approach to identifying improvement areas.",
        "Effective strategies for reaching goals.",
        "Expert advice to increase efficiency and results.",
        "Proven techniques for success.",
    ]

    contents = [
        "Analyze the following {{topic}} and provide detailed insights:\n\n{{details}}",
        "Prepare a comprehensive report on:\n\n{{topic}}",
        "Draft an email responding to {{situation}} using {{tone}} tone.",
        "Summarize the key points of the following {{content}}:",
        "Identify potential improvements for the {{system}} based on the following information:\n\n{{details}}",
    ]

    prompts = []

    for i in range(n):
        title = random.choice(titles) + f" Example {i+1}"
        description = random.choice(descriptions)
        content = random.choice(contents)
        collection_id = random.choice(collection_ids) if collection_ids else None

        # Assign 1-3 random tags to each prompt (if tags available)
        tags = []
        if tag_names:
            num_tags = random.randint(1, min(3, len(tag_names)))
            tags = random.sample(tag_names, num_tags)

        prompts.append(
            {"title": title, "content": content, "description": description, "collection_id": collection_id, "tags": tags}
        )

    return prompts


def seed_data():
    print("🌱 Starting database seeding...\n")

    # Step 1: Create tags
    print("📌 Creating tags...")
    created_tags = []
    for tag in TAGS:
        try:
            response = requests.post(f"{BASE_URL}/tags", json=tag)
            if response.status_code in [200, 201]:
                created_tag = response.json()
                created_tags.append(created_tag)
                print(f"  ✓ Created tag: {tag['name']}")
            else:
                print(f"  ✗ Failed to create tag: {tag['name']} (Status: {response.status_code})")
                print(f"     Response: {response.text}")
        except Exception as e:
            print(f"  ✗ Error creating tag {tag['name']}: {str(e)}")

    print(f"\n✅ Created {len(created_tags)} tags\n")

    # Step 2: Create collections
    print("📁 Creating collections...")
    collections = [
        {"name": "Development", "description": "Prompts for software development tasks"},
        {"name": "Writing", "description": "Prompts for content creation"},
        {"name": "AI & Machine Learning", "description": "Prompts for AI and ML tasks"},
    ]

    created_collections = []
    for coll in collections:
        response = requests.post(f"{BASE_URL}/collections", json=coll)
        if response.status_code == 201:
            created_collections.append(response.json())
            print(f"  ✓ Created collection: {coll['name']}")
        else:
            print(f"  ✗ Failed to create collection: {coll['name']}")

    print(f"\n✅ Created {len(created_collections)} collections\n")

    # Step 3: Generate and create prompts with tags
    print("💬 Creating prompts...")
    tag_names = [tag["name"] for tag in created_tags]

    # Only generate prompts if we have tags
    if not tag_names:
        print("  ⚠️  No tags available, creating prompts without tags")
        tag_names = []  # Empty list for prompts without tags

    prompts = generate_random_prompts(50, [coll["id"] for coll in created_collections], tag_names)

    created_prompts = 0
    for prompt in prompts:
        response = requests.post(f"{BASE_URL}/prompts", json=prompt)
        if response.status_code == 201:
            created_prompts += 1
            tags_str = ", ".join(prompt["tags"])
            print(f"  ✓ Created prompt: {prompt['title']} [tags: {tags_str}]")
        else:
            print(f"  ✗ Failed to create prompt: {prompt['title']}")

    print(f"\n✅ Seeding complete!")
    print(f"   - {len(created_tags)} tags")
    print(f"   - {len(created_collections)} collections")
    print(f"   - {created_prompts} prompts")


if __name__ == "__main__":
    try:
        seed_data()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running at http://localhost:8000")
