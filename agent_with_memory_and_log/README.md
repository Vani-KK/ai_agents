## Agent Memory & Debugging

The agent maintains in-loop memory for each iteration, storing:
- generated summaries
- evaluation results
- feedback
- quality scores

This allows:
- debugging agent behavior
- tracking refinement progress
- returning the best candidate when limits are reached

This design mirrors real-world agent observability practices.
