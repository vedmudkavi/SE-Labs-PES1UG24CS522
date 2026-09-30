# Lab 4 Lunar Lander

**Student:** Ved Mudkavi  
**SRN:** PES1UG24CS522

## Files

- `game.py`: updated game implementing Tasks 1 to 4.
- `README.md`: original assignment instructions and setup.
- `before.mov`: student-supplied recording before the changes.
- `after.mov`: student-supplied recording after the changes.
- `Chat-History.docx`: chronological user prompts and assistant replies, with screenshots.
- `Chat-Link.txt`: shareable conversation URL.

## Repositories and chat

- [Assigned repository](https://github.com/SETAPESU26/32_lunarLander)
- [Personal game fork and separate task commits](https://github.com/vedmudkavi/32_lunarLander)
- [Shared conversation](https://chatgpt.com/s/cx_6abcb1c898a08191acd4534e7f35c86b)

## Task commits

| Task | Change | Commit |
| --- | --- | --- |
| 1 | Check horizontal speed when validating landings | [b0ec23f](https://github.com/vedmudkavi/32_lunarLander/commit/b0ec23f) |
| 2 | Blend ship colour from pale to red as fuel falls | [d2b6027](https://github.com/vedmudkavi/32_lunarLander/commit/d2b6027) |
| 3 | Generate score-dependent landing chimes with audio fallback | [d89219e](https://github.com/vedmudkavi/32_lunarLander/commit/d89219e) |
| 4 | Set the bonus-life interval to 1500 points | [5ebdd10](https://github.com/vedmudkavi/32_lunarLander/commit/5ebdd10) |

## Verification

Direct checks covered landing speed and angle limits, pad placement, scoring and life loss; full, half and empty fuel colours and clamping; generated audio on a dummy audio backend and unavailable-audio handling; and milestone awards, duplicate prevention and reset tracking. The existing bonus-life check runs on the next active round after pressing Space. Speaker playback and the contents of the student-supplied recordings were not independently verified.
