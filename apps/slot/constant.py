class ErrorMessages:
    """
    Constants for defining errors.
    """

    OVERLAPPING_SCHEDULE = "This cinema is already booked during this time slot."
    DURATION_TOO_SHORT = "The slot duration is shorter than the actual movie running time."
    BEFORE_RELEASE_DATE = "Cannot schedule a showtime before the movie's official release date."
    INVALID_LANGUAGE = "The selected language is not supported for this specific movie."
    PAST_START_TIME = "Showtimes cannot be scheduled in the past."
