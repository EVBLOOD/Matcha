from typing import Optional

class Profile:
    def __init__(
        self,
        user_id: int,
        gender: str = None,
        sexual_preference: str = None,
        biography: str = None,
        location_set_by_user: bool = False
    ):
        self.user_id = user_id
        self.gender = gender
        self.sexual_preference = sexual_preference
        self.biography = biography
        self.location_set_by_user = location_set_by_user