# Model selection — measured local Docker lab

## The question
Predict whether a customer will churn so a retention team can prioritize outreach. A false positive wastes outreach cost; a false negative misses someone who might leave. This is a teaching dataset, not evidence of a production-ready retention system.

## Reproducible comparison
Data: `data/churn_v1.csv`, 1,200 rows. Stratified 80/20 train/holdout split, seed 42, 240 holdout rows, probability threshold >0.5. Preprocessing is fitted on training data only: standardized numeric columns plus unknown-tolerant one-hot encoding. All three candidates use exactly the same split and full SHA-256 file hash. Batch: `lab3-measured-v2`. Training commit: `b9b500e` (full SHA recorded in each run's git_sha tag).

| Candidate | Why tried | AUC | F1 | Lowest contract F1 | p95 ms | Size KB | Run ID |
|---|---|---:|---:|---:|---:|---:|---|
| logreg | Regularized, interpretable linear baseline (C=0.7). | 0.7981 | 0.5000 | 0.2500 | 12.34 | 3.55 | `1550f4c0b68b41c69579cee6eea05015` |
| random_forest | Bagged nonlinear trees; depth 7 and leaf size 3 limit overfitting. | 0.7738 | 0.4396 | 0.0000 | 62.51 | 1595.60 | `34907aa2a07e480897e677b792e18d83` |
| gradient_boosting | Shallow boosted trees; 80 stages and learning rate 0.05. | 0.7827 | 0.4186 | 0.0000 | 16.34 | 72.13 | `73eacaa8b00f4e2b9b14a151df1304fa` |

### Contract slices (holdout)

| Candidate | Month-to-month (n=140) | One-year (n=47) | Two-year (n=53) |
|---|---:|---:|---:|
| logreg | 0.5500 | 0.2500 | 0.2500 |
| random_forest | 0.5195 | 0.0000 | 0.0000 |
| gradient_boosting | 0.4789 | 0.0000 | 0.2500 |

## The champion
**Logistic regression** wins overall F1 (0.5000), AUC (0.7981), weakest slice F1 (0.2500), p95 latency (12.34 ms) and size (3.55 KB). It is registered as `churn-model`, version 1, alias `champion`. Gradient boosting fits the latency budget but has lower overall F1 (0.4186) and zero F1 for one-year contracts. Random forest has F1 0.4396 and fails the 30 ms budget (62.51 ms).

No measured metric favors a challenger in this comparison. The trade-off I accept is lower model flexibility and still-poor absolute performance: F1 0.25 on both fixed-term slices and 0.50 overall leave many mistakes. I do not hide this behind the champion label. A more complex model may work better with more data or tuning, but these measured candidates do not justify its cost. This model is suitable for the lab demonstration; deployment alone does not establish business suitability.

## Promotion rules
- **p95 <= 30 ms** for one-row `predict_proba`: the measured champion has approximately 2.4x headroom; 200 sequential predictions after warmup, excluding network/HTTP overhead. This permits interactive scoring while allowing some CI scheduling variation. Runners vary; if a runner fails this budget, inspect its actual measurements rather than bypassing the gate.
- **Absolute F1 improvement >= 0.01** over the committed champion: avoid replacing the model for a tiny score change. A 0.0099 gain or equal score blocks; 0.0100 passes provided latency is eligible. This is a practical policy, not a statistical significance test.
- Only finished runs in the selected batch are eligible. The highest eligible overall F1 wins. With no champion, bootstrap the best eligible candidate. Subsequent candidates compare against `artifacts/champion.json` from the PR base branch; blocked runs return exit 1 before registry/model files change.
- Slice F1 and model size are reviewed here; they are **not additional automatic gate constraints** in this lab. A future gate could require a minimum slice score, with sufficient sample counts and a documented trade-off.
- F1 is retained at logged precision in champion.json, avoiding comparisons against a rounded three-decimal baseline.

## Evidence and limitations
`evidence/runs.json` and CSV contain actual metrics, parameters and full data hashes; `evidence/MLmodel` has the signature. `evidence/blocked.log` records the deliberately weak C=0.00001 logistic candidate and unchanged champion artifacts. A real failed GitHub Actions PR must still be produced on the student's account; local logs do not claim to be hosted workflow results.

F1 depends on the fixed classification threshold and class distribution. The small fixed-term slices need confusion matrices, positive-class counts and confidence intervals before real use. Keep an untouched test set: repeated model selection on the same holdout can overfit it. Next checks: temporal/independent test data, drift, calibration and a retention-cost-informed threshold. Reported p95 comes from shared execution hardware and is not an end-to-end service SLA.
