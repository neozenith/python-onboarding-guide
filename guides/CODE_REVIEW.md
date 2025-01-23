# Code Review

There are **\*three types of Code Review** inspired by conference talks by Trisha Gee (Jetbrain Java Advocate)

- https://www.youtube.com/watch?v=a9_0UUUNt-Y
- https://www.youtube.com/watch?v=3pth05Rgr8U&t

## The Three Types

### Draft / Early Feedback 📝

Github has a feature to mark a Pull Request as a draft. Often this won't run CI checks as it is known that it is in a partial working state.

These are great to get early feedback about design decisions before sinking too much effort.

### Educational 📚

Sometimes the person creating the Pull Request is the Subject Matter Expect (SME). 

They have authority to just push the change through, but it is important for others to see and follow along what the change _**IS**_ and _**WHY**_.

### Goalkeeper 🥅

This is probably the more common one that people think of when it comes to code review. They are looking at quality control and trying to stop bugs getting through.

The key goals they need to ask themselves when reviewing code:

> Will this break production?
> Can someone else reasonably maintain this later?

Sometimes a solution isn't exactly how you would expect it to be solved, that is ok. As a reviewer you should be open to letting these through. This is to help avoid nitpicking.

**Nitpicking should never block code getting released**.

The regulating factor here is that if the code could not reasonably be maintained by someone else, then that is leaving tech debt and lowering the bar for the whole project.

## Before Code Review

Before requiring the valuable resource which is someone's attention there are some things you can do, (and yes your attention too is valuable, and I am grateful you have read this far 🫶).

- Run code formatters
- Run code linters
- Run test suite
- Add test coverage
- Read your own PR as though someone gave it to you for review
    - Does the code represent the pragmatically smallest amount of code changed to reach the outcome?
    - Can you squash some of the commits together to better tell a story? Eg 17 commits down to 3 commits?
    - Can you pre-emptively add comments on PRs to draw attention to the important parts?
    - Have you added appropriate documentation so the next person can self-service contribute?
