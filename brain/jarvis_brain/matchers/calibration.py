"""Turn each matcher's raw output into P(correct) so they can be compared at all.

Two different fits, because the matchers are different shapes:

* hassil has no scalar, so its "calibration" is a per-bucket prior from the audit log —
  the rate at which exact, fuzzy and unmatched-entity matches turned out correct (2.5).
* the retriever and the classifier produce scalars, fitted with isotonic regression.

Every fit is refitted from the audit log, including the satellite's on-device decisions
(review 2.4), which are the majority of turns once MultiNet is acting and are therefore
exactly the population the thresholds must be fitted on.
"""

from __future__ import annotations

from ..turn import Candidate, Source
from .hassil_tier0 import Bucket


class Calibrator:
    def calibrate(self, candidate: Candidate, bucket: Bucket | None = None) -> float:
        """Set and return ``candidate.calibrated``. The only score the guards may read."""
        raise NotImplementedError("build order step 3")

    def fit(self, source: Source) -> None:
        """Refit one matcher from the audit log."""
        raise NotImplementedError("build order step 5")

    def is_fitted(self, source: Source) -> bool:
        """False until real turns have been fitted.

        While False the guard chain refuses tiers B and C from that source. An unfitted
        threshold is not a conservative default; it is an unknown.
        """
        raise NotImplementedError("build order step 5")
