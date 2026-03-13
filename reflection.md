# PawPal+ Project Reflection

## 1. System Design
1) Core actions a user should perform

A user can add their pet and basic owner information.

A user can create and manage pet care tasks such as feeding, walking, or medication with duration and priority.

A user can generate a daily plan that schedules tasks based on time available and priority.

2) Main System Objects

The four classes are:
Owner
Pet
Task
Scheduler

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the user and manages the pets they own. The Pet class represents each pet and keeps track of the tasks related to caring for that pet. The Task class represents individual care activities like feeding or walking and stores information such as duration and priority. The Scheduler class is responsible for organizing tasks and generating a daily plan based on the available time and task priorities.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed slightly during implementation. Initially, I only planned for the scheduler to organize tasks, but during implementation I realized it should ignore completed tasks when generating the daily plan. I also adjusted how tasks are collected from each pet so the scheduler can easily access all tasks. This change made the scheduling logic simpler and more organized.

---

## 2. Scheduling Logic and Tradeoffs

Scheduler: Greedy priority selection
generate_daily_plan() uses a greedy algorithm : it sorts incomplete tasks by priority
(highest first) and picks each one in order as long as it fits within available_minutes.

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

generate_daily_plan() considers two constraints: priority (which tasks get picked first) and available time (tasks are skipped if they don't fit in the remaining minutes). That's it, no preferences, no pet-specific needs, no time-of-day windows.

Priority and time are the minimum viable pair for any scheduler without priority you have no ordering logic, and without a time budget you have no selection logic. Everything else (preferences, recurring frequency, conflict detection) is useful but layered on top. For a demo app the goal was to get a working, explainable schedule first, then add complexity only where it added clear value. That's why conflict detection and recurring tasks live as separate methods rather than being baked into the core scheduling loop, they can be added without rewriting the base algorithm.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a greedy algorithm, it picks the highest-priority task first and keeps going in order until time runs out. This means a single long, high-priority task can fill the budget and block several shorter tasks that would have fit and collectively covered more value.

Pet care tasks in a day-to-day app tend to be short and have clearly different priorities a vet visit outranks a grooming session without much debate. The edge case where greedy fails badly (one big task crowding out many small ones) is uncommon in this context. The alternative is a knapsack algorithm which would be provably optimal but significantly harder to read and maintain for what is essentially a personal planning tool. Readable and good enough beats optimal and complex for this scenario.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was used throughout the project for generating class stubs, filling in method implementations, debugging the st.session_state reset bug, and comparing algorithm approaches. It was most useful in describing a specific problem and asking for a targeted fix was faster than reading documentation cold. For the algorithmic phase, asking AI to suggest a more Pythonic version of generate_daily_plan() was valuable not to accept the suggestion blindly, but to make a deliberate readability decision by comparing both versions. The most effective prompts were specific and included existing code as context, such as "here is my current method, how could this be simplified?" Vague prompts like "write a scheduler" produced generic output that needed significant revision, while constrained prompts like "return a warning instead of crashing" shaped the implementation directly.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The clearest example was the AI's suggested rewrite of generate_daily_plan() using a walrus operator (:=) inside a list comprehension. The suggestion was technically correct and more compact, but it relied on a side effect inside an expression, mutating time_used while filtering, which makes the logic harder to follow at a glance. The original for loop was kept because it makes the accumulation explicit and reads like a sequence of steps rather than a clever one-liner. The evaluation was straightforward so both versions were read mentally and the question I asked was "would a student understand this without an explanation?" The comprehension version failed that test, so the more verbal but transparent version won.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the main behaviors of the system, such as adding pets to an owner, adding tasks to a pet, and generating a daily plan using the scheduler. I also tested that the scheduler prioritizes tasks correctly and respects the available time. These tests were important because they verify that the core features of the app work as expected and that the scheduling logic produces a correct plan.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence is fairly high for the basics which are priority ordering, time limits, and skipping completed tasks all have passing tests. The weak spot is conflict detection, which only catches tasks at the exact same time and misses overlaps where one task runs into another's start time.

If there were more time, the most useful cases to test next would be overlapping task durations, a pet with a large number of tasks where the greedy approach leaves obvious gaps, and bad inputs like negative durations or empty titles that currently pass through unchecked.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part I'm most satisfied with is the session state integration in app.py. It's a small fix, just a one-line if guard, but it solves a real bug that would have made the entire app useless. Understanding why Streamlit reruns the whole script on every click, and then knowing exactly where to intercept that to preserve data, felt like a genuine insight rather than just following instructions.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

The first thing to improve would be conflict detection, since right now it only catches tasks at the exact same time and misses overlaps entirely. Adding duration-aware checking would make the scheduler much more useful in practice. The second thing would be the owner setup in the UI, where changing the name input after the first load has no effect because the object is already created. A proper submit form would fix that and make the flow less confusing.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

An important thing I learned is that AI is a great collaborative tool, but it cannot be relied on entirely. Students still need to know their code.