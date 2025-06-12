def format_result_to_english(question: str, result: list[dict]) -> str:
    if not result:
        return "Sorry, I couldn't find any relevant data."

    # Basic examples - extend these with more rules as needed
    question_lower = question.lower()

    # Example 1: Department of an employee
    if "which department" in question_lower and "belong" in question_lower:
        name = question.split(" ")[-1].rstrip("?")
        dept = result[0].get("name", "")
        return f"{name} belongs to the {dept} department."

    # Example 2: List of employees
    if "employees" in question_lower:
        names = [row.get("name") for row in result]
        return f"The employees are: {', '.join(names)}."

    # Example 3: Laptops in department
    if "laptop" in question_lower:
        assets = [row.get("name") or row.get("asset_tag") for row in result]
        return f"Laptops found: {', '.join(assets)}."

    # Fallback: just dump rows nicely
    response_lines = []
    for row in result:
        line = ", ".join(f"{key}: {val}" for key, val in row.items())
        response_lines.append(line)
    return "\n".join(response_lines)
