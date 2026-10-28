# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
look normal, like expected
- List at least two concrete bugs you noticed at the start  
   1. allowing improper input (parse guess function in app.py)
   2. hints are wrong (line 37-40 of app.py)
   3. difficulty ranges are wrong
  (for example: "the hints were backwards").


  after testing:
- new game button does not work

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used claude. One AI suggestion that was correct was when I asked it to refactor each of the core logic functions from app.py to logic_utils.py, it did that correctly. ONe example where I did not accept a suggestion was when it started fixing all the issues. Instead I stopped it remprompted to only fix one so both I and the AI could only focus on one and also add documentation about the fix which it missed the first time.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I did a quick glimpse of the logic and comments to make sure it made sense to me. Then I tested by running the app and using the same tests I did when I started. One was just inputting proper input, and I noticed that the hints were correct this time, and so werethe difficulty ranges. As I tested, I noticed a new bug which was the new game button does not work.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every click makes streamlit run app.py again from top to bottom. Anything store in st.session_state survives between runs, this is where the game's memory is stored. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I documentation strategy is something I want to reuse, because although I just followed it as good practice, it came in handy when I had to refactor and needed a reminder of what AI fixed
- What is one thing you would do differently next time you work with AI on a coding task?
 - before getting into debugging I would try to understand the main logic, especially in the form of an logical tree because it made it difficult for me to try to understand the new game button bug 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - im realizing how easy it is get lost if you do not understand the code base, and every more confusing if you do not understand what changes your ai made
