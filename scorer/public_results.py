"""Public submission records contain only the documented leaderboard measures."""
METADATA = {'issue', 'user', 'set', 'display_name', 'role', 'tools', 'minutes',
            'submitted_utc', 'status'}
AGGREGATES = {'net_score', 'silent_errors', 'precision', 'coverage',
              'duplicate_ids_found', 'structural_changes_found'}
PRACTICE = {'records', 'correct', 'wrong', 'unsure_or_blank', 'matched_rows'}


def public_entry(entry):
    allowed = METADATA | AGGREGATES
    if entry.get('set') == 'practice':
        allowed |= PRACTICE
    return {key: value for key, value in entry.items() if key in allowed}
