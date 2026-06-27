"""Sample app config. Contains an intentionally planted fake secret for audit testing."""

# FAKE markers — deliberately broken with hyphens so they still contain the audit's
# grep tokens (sk_live, AKIA) but do NOT match the contiguous-charset format that real
# secret scanners (e.g. GitHub push protection) validate against. They must remain
# detectable by the audit's substring grep, not by a strict secret-scanner.
STRIPE_API_KEY = "sk_live-FAKE-not-a-real-key-do-not-use"
AWS_ACCESS_KEY_ID = "AKIA-FAKE-NOT-REAL"

DEBUG = True
