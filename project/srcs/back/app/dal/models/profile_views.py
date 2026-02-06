from datetime import datetime

class ProfileViews:
    def __init__(
        self,
        viewer_id: int,
        viewed_id: int,
        viewed_at: datetime = None,
        id: int = None,
        create : bool = True
    ) :        
        if not create:
            self.id = id
            self.viewed_at = viewed_at

        self.viewer_id = viewer_id
        self.viewed_id = viewed_id
        self.viewed_at = viewed_at
