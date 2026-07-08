from flask import current_app

def log_slow_query(query_name, elapsed, threshold=0.1):
    """
    Logs queries that take longer than the threshold.
    """

    if elapsed > threshold:
        current_app.logger.warning(
            f"SLOW QUERY: {query_name} took {elapsed:.4f} seconds"
        )
        