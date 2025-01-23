# Code Review

There are **\*three types of Code Review** inspired by conference talks by Trisha Gee (Jetbrain Java Advocate)

- https://www.youtube.com/watch?v=a9_0UUUNt-Y
- https://www.youtube.com/watch?v=3pth05Rgr8U&t

## Draft / Early Feedback

Github has a feature to mark a Pull Request as a draft. Often this won't run CI checks as it is known that it is in a partial working state.

These are great to get early feedback about design decisions before sinking too much effort.

## Educational

Sometimes the person creating the Pull Request is the Subject Matter Expect (SME) like a @newwwie/core-maintainers. They have authority to just push the change through, but it is important for others to see and follow along what the change _**IS**_ and _**WHY**_.

## Goalkeeper

This is probably the more common one that people think of when it comes to code review. They are looking at quality control and trying to stop bugs getting through.

The key goals they need to ask themselves when reviewing code:

> Will this break production?
> Can someone else reasonably maintain this later?

Sometimes a solution isn't exactly how you would expect it to be solved, that is ok. As a reviewer you should be open to letting these through. This is to help avoid nitpicking.

**Nitpicking should never block code getting released**.

The regulating factor here is that if the code could not reasonably be maintained by someone else, then that is leaving tech debt and lowering the bar for the whole project.
