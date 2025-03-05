from agent import run_agent


def test_task_a():
    question = (
        "Find a floral skirt under $40 in size S. "
        "Is it in stock, and can I apply a discount code 'SAVE10'?"
    )
    print("\nRunning Task A: Basic Item Search + Price Constraint")
    result = run_agent(question)
    print_results(result)


def test_task_b():
    question = (
        "I need white sneakers (size 8) for under $70 that can arrive by Friday."
    )
    print("\nRunning Task B: Shipping Deadline")
    result = run_agent(question)
    print_results(result)


def test_task_c():
    question = (
        "I found a 'casual denim jacket' at $80 on SiteA. Any better deals?"
    )
    print("\nRunning Task C: Competitor Price Comparison")
    result = run_agent(question)
    print_results(result)


def test_task_d():
    question = (
        "I want to buy a cocktail dress from SiteB, "
        "but only if returns are hassle-free. Do they accept returns?"
    )
    print("\nRunning Task D: Returns & Policies")
    result = run_agent(question)
    print_results(result)


def test_task_e():
    question = (
        "Find a waterproof hiking backpack under $100 with free shipping, "
        "check if I can use the code 'HIKER20', "
        "and compare prices across sites."
    )
    print("\nRunning Task E: Multi-Tool Reasoning")
    result = run_agent(question)
    print_results(result)


def print_results(result):
    print("\nFinal Answer:", result["answer"])
    print("Self-Critique:", result["critique"])
    print("Auto-Evaluation:", result["evaluation"])