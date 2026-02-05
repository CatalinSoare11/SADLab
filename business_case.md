# Board Briefing: Selecting the Most Successful Genre for the Next Film Release

## Executive Summary
This briefing outlines a data-driven approach to determine the most commercially successful genre for our next release. It defines the decision criteria, the evidence required, and the analysis framework to evaluate the **most recent 1,000 movies** by release date. The final recommendation will be issued once the dataset is provided or external data access is enabled.

## Decision Question
**Which genre should we prioritize for our next release to maximize profitability and strategic fit?**

## What We Need to Make a Defensible Call (Evidence Requirements)
To answer the question rigorously, we need a dataset of the **last 1,000 theatrical or wide-release films** with:
- **Release date** (to verify recency)
- **Genres** (primary + secondary)
- **Production budget**
- **Worldwide gross / box office**
- **Audience signals** (ratings + vote counts)
- **Distribution type** (theatrical/streaming hybrid)

## Analysis Method (Planned)
1. **Filter** to the most recent 1,000 films by release date.
2. **Normalize performance** using:
   - ROI (gross ÷ budget)
   - Audience-weighted score (rating × log10(votes+1))
3. **Aggregate by genre** to compute:
   - Average ROI
   - Median ROI
   - Average audience-weighted score
   - Consistency (variance / downside risk)
4. **Rank genres** by a composite score (ROI + audience engagement + risk-adjusted return).

## Visualization (Placeholder)
Once the dataset is provided, we will generate and present a bar chart similar to the following:

```
Avg Success Score by Genre (Most Recent 1,000 Movies)

Action        | ████████████████
Adventure     | █████████████
Horror        | ██████████████████
Comedy        | ███████████
Drama         | ██████████
Animation     | ███████████████
```

This chart will be replaced by an actual visualization populated with the computed results.

## Preliminary Strategic Hypotheses (To Validate with Data)
- **Horror/Thriller** often shows strong ROI due to low budgets and consistent audience demand.
- **Action/Adventure** can deliver high gross but with higher capital risk and franchise dependence.
- **Animation/Family** provides durable long-term value and merchandising upside but requires longer production timelines.

## Risks of Deciding Without Data
- Misalignment with current audience demand.
- Overexposure to high-budget risk in competitive release windows.
- Underestimation of streaming-driven performance vs theatrical performance.

## Next Steps (Immediate)
1. Provide the dataset (last 1,000 films with budgets, grosses, genres, and ratings).
2. Run the analysis pipeline and generate the final chart.
3. Issue a board-ready recommendation with quantified evidence.

---

## Appendix: Data Intake Template
Please provide a CSV with the following columns:
- `title`
- `release_date`
- `genres` (comma-separated)
- `production_budget_usd`
- `worldwide_gross_usd`
- `average_rating`
- `vote_count`
- `distribution_type`
