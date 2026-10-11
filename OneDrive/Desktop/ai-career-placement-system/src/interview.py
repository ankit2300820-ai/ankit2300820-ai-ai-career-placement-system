"""Interview preparation: technical question bank (question, hint) + HR questions."""
from .career import ROLES

BANK = {
    "Python": [("What is the difference between a list and a tuple?", "Mutability, performance, use-cases"), ("Explain decorators and generators.", "Closures, yield, lazy evaluation")],
    "Java": [("Explain JVM, JRE and JDK.", "Compilation to bytecode, runtime"), ("Difference between abstract class and interface?", "Multiple inheritance, default methods")],
    "SQL": [("Difference between INNER, LEFT and FULL JOIN?", "Draw two tables, show unmatched rows"), ("Write a query for the 2nd highest salary.", "LIMIT/OFFSET, subquery or DENSE_RANK")],
    "DBMS": [("Explain normalization up to 3NF.", "Redundancy, anomalies, dependencies"), ("What are ACID properties?", "Atomicity, Consistency, Isolation, Durability")],
    "Data Structures": [("Array vs Linked List - when to use which?", "Access time, insert/delete cost"), ("How does a HashMap work internally?", "Hashing, collisions, load factor")],
    "Algorithms": [("Explain binary search and its complexity.", "O(log n), sorted input"), ("Dynamic programming vs greedy?", "Overlapping subproblems, optimal substructure")],
    "OOP": [("Explain the four pillars of OOP with examples.", "Encapsulation, abstraction, inheritance, polymorphism"), ("Overloading vs overriding?", "Compile-time vs runtime polymorphism")],
    "Operating Systems": [("Process vs thread?", "Memory sharing, context switch"), ("What is deadlock and how to prevent it?", "4 Coffman conditions")],
    "Computer Networks": [("What happens when you type a URL in the browser?", "DNS, TCP, TLS, HTTP, rendering"), ("TCP vs UDP?", "Reliability, ordering, use-cases")],
    "Machine Learning": [("Explain overfitting and how to reduce it.", "Regularization, CV, more data"), ("Precision vs recall - when does each matter?", "Spam vs cancer detection")],
    "Statistics": [("What is a p-value?", "Probability under null hypothesis"), ("Mean vs median - when to use which?", "Outliers, skewness")],
    "Pandas": [("loc vs iloc?", "Label vs position"), ("How do you handle missing values?", "Drop, impute, indicators")],
    "Git": [("Merge vs rebase?", "History shape, conflicts"), ("What does git stash do?", "Temporarily shelve changes")],
    "Docker": [("Image vs container?", "Template vs running instance"), ("What is a Dockerfile?", "Layers, build steps")],
    "JavaScript": [("Explain closures and the event loop.", "Scope, call stack, microtasks"), ("var vs let vs const?", "Scope, hoisting, reassignment")],
    "React": [("What are hooks? Explain useState and useEffect.", "State, side effects, dependency array"), ("Virtual DOM - why?", "Diffing, reconciliation")],
    "REST APIs": [("What are the HTTP methods and status codes you know?", "GET/POST/PUT/DELETE, 200/201/400/404/500"), ("What makes an API RESTful?", "Stateless, resources, uniform interface")],
    "Linux": [("How do you check running processes and kill one?", "ps, top, kill -9"), ("Explain chmod 755.", "rwx for owner, rx for group/others")],
    "Cybersecurity": [("Explain SQL injection and prevention.", "Parameterised queries"), ("What is the CIA triad?", "Confidentiality, Integrity, Availability")],
}
HR = [("Tell me about yourself.", "60-90 sec: education, skills, one project, goal"), ("Why should we hire you?", "Match skills to the role with evidence"),
      ("Describe a project you are proud of.", "Use STAR: Situation, Task, Action, Result"), ("Tell me about a failure and what you learned.", "Be honest, focus on learning"),
      ("Where do you see yourself in 5 years?", "Growth with the company, skills to be built"), ("How do you handle tight deadlines or conflict in a team?", "Real example, communication, prioritisation")]

def questions(role, skills, per_skill=2):
    order = [s for s in ROLES[role] if s in skills] + [s for s in ROLES[role] if s not in skills]   # strengths first
    out = [(s, q, h) for s in order if s in BANK for q, h in BANK[s][:per_skill]]
    return out, [("HR", q, h) for q, h in HR]
