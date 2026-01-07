// export type UserRole = 'admin' | 'user' | 'moderator';

export interface UserRegister {
    username: string;
    email: string;
    password: string;
    first_name: string;
    last_name: string;
}






export interface UserProfilePicturesResponse {
    is_profile_picture: boolean;
    url: string;
}

export interface UserProfileInfosResponse {
    biography: string;
    fame_rating: number;
}

export interface UserProfileAttrsResponse {
    first_name: string;
    gender: string;
    last_name: string;
    sexual_preference: string;
    user_id: number;
    username: string;
    email?: string
}


export interface UserProfileInteractionsResponse {
    is_same: boolean;
    likes_count: number;
    views_count: number;
    is_connected?: number;
    interaction_status?: string;
}

export interface UserProfileResponse {
  interactions: UserProfileInteractionsResponse;
  interests: string[];
  pictures: UserProfilePicturesResponse[];
  profile: UserProfileInfosResponse;
  user: UserProfileAttrsResponse
}

export interface NotificationsResponse {
    create_at: string;
    is_read: boolean;
    notification_id: number;
    picture_url: UserProfilePicturesResponse[];
    sourse_user_id: number;
    type: string;
    user_id: number;
    username: string;
}



// export interface UserProfile extends User {
//     bio: string;
//     interests: string[];
//     photos: string[];
// }