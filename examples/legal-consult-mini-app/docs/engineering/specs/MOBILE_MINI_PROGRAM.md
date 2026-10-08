# Mobile / Mini Program Spec

status: APPROVED
owner: Engineering Owner

## Device Permissions
V1 requests no camera, microphone, location, or address-book permission. Any future permission needs a user-visible reason and denial path.

## Signing / Review
Release ownership, application/mini-program signing identity, platform review copy, privacy disclosures, and reviewer test account are release inputs. Store/mini-program review rejection is handled as a release blocker, not bypassed.

## Gray Release / Compatibility
Use provider-supported gray rollout when available. Backend remains compatible with the previous mini-program version during the observation window.

## Package Strategy
Keep the consult core in the main package; history/operations-only optional surfaces may use subpackages if package size requires it.

## Offline / Weak Network
Question submit uses a stable client request id, retry is idempotent, pending state is recoverable after restart, and cached content never exposes another account.
