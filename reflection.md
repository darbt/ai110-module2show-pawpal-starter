# PawPal+ Project Reflection

## 1. System Design

A user should be able to: 
        Add a pet
        Add a task
        Edit tasks

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
OWNER: 
Pets (list)
email (string)
name (string) 
addPet(): Should be able to add pets
editTask(): should be able to edit tasks

PET: 
name (string)
age (number) 
tasks (lists) 
addTask()

TASK: 
Title (string) 
Description (string)
dueDate (date) 
priority (string)

SCHEDULER:
generatePlan(List Task)
filterPrirority(List Task) 
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
        The design definitley changed after implementation. One really noticable change was the Scheduler class. The scheduler gained a lot of new methods, some of which were necessary for sorting and filtering
--- 

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler consideres time, priority, and which pet the task belongs to
- How did you decide which constraints mattered most?

I just imagined what would be the most important to me if I were to use this application. Which constraint would make or break the program. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler filters out the complete tasks before planning. This is reasonable beacause this way a user won't be confused and run a task twice just because the plan does not initially move out tasks that are already completed. The task may be marked as completed, but because it stays where it is in the list, it's not absurd to think that the mark can be missed. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I utilized AI tools mainly for design and brainstorming. AI tools were very useful when filling in spots that I didn't even think of. 

- What kinds of prompts or questions were most helpful?

I think the most helpful prompts were anything that had to do with testing. For example, "What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?". This was important to make sure even the smallest features worked the way they were supposed to. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When it came to the streamlit. The AI suggested only the duration for tasks, which I did not accept.  

- How did you evaluate or verify what the AI suggested?
Just using duration is not as specific as we need it to be. We need dates as well and times so that not only is it more detailed but it is best to see if there are any scheduling conflicts
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested all sorting methods, conflicts, and filtering. 
- Why were these tests important?
These test are important because they are essential to a scheduler. A user needs to be able to list their task by whatever filter that they need. It makes it a lot more organized. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
I would give my confidence level a 4. Its not a perfect score because we have to leave 1 point for anything we could've potentially missed. 

- What edge cases would you test next if you had more time?
I think i would test more of conflicts. I feel like the conflict checks can be fleshed out a bit more
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am really satisfied with the UI and the filtering. I feel like it looks like and works like a proper scheduler. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would design a way to edit task. Especially if there are scheduling conflicts, I want a user to be able to edit the task right there.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I feel that when working with different aspects of a system, example testing, design, UI, etc , it really helps to have utilize different chat sessions with AI to make things more organized. I feel like putting everything in one chat makes it harder to go back and may cause confusion. 

What I learned about being the "lead architect" when working with the AI tools is that having a good structured workflow is essential. Its great when you know what aspect to be working on in the moment and have a steady flow rather than jumping from component to component and confusing not only myself but the AI as well. 