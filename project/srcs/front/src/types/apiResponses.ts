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
    email?: string;
    location?: string;
    birthdate?: string;
}


export interface UserProfileInteractionsResponse {
    is_same: boolean;
    likes_count: number;
    views_count: number;
    is_connected?: number;
    interaction_status?: string;
    conversation_id?: number;
}

export interface UserProfileResponse {
  interactions: UserProfileInteractionsResponse;
  interests: string[];
  pictures: UserProfilePicturesResponse[];
  profile: UserProfileInfosResponse;
  user: UserProfileAttrsResponse
}

export interface NotificationsResponse {
    created_at: string;
    is_read: boolean;
    notification_id: number;
    picture_url: UserProfilePicturesResponse[];
    sourse_user_id: number;
    type: string;
    user_id: number;
    username: string;
}

export interface MessagesResponse {
    content: string;
    id: number;
    is_read: boolean;
    sender_id: number;
    sent_at: string;
}

export interface ConversationsResponse {
    conversation_id: number;
    last_active_at: string;
    first_name: string;
    last_name: string;
    last_online: string;
    peer_id: number;
    profile_picture_url: UserProfilePicturesResponse[];
    username: string;
    messages_list?: MessagesResponse[];
}

export interface SuggestionsResponse {
    user_id: number;
    fame_rating: number;
    age: string;
    last_name: string;
    first_name: string;
    username: string;
    location: string;
    profile_picture_url: UserProfilePicturesResponse[];
}


export interface UserLocation {
    id: number;
    username: string;
    latitude: number;
    longitude: number;
    profile_picture_url: UserProfilePicturesResponse[];

}

export interface Location {
    latitude: number,
    longitude: number
}

export interface BlocksResponse {
    blocked_id: number,
    username: string,
    first_name: string,
    last_name: string,
    profile_picture_url: UserProfilePicturesResponse[]
    unblock?: boolean
}

export interface LikesResponse {
    liked_id: number,
    username: string,
    first_name: string,
    last_name: string,
    profile_picture_url: UserProfilePicturesResponse[],
    unlike?: boolean
}

export interface ViewsListResponse {
    viewer_id: number,
    username: string,
    first_name: string,
    last_name: string,
    profile_picture_url: UserProfilePicturesResponse[],
    viewed_at: any
}
// export interface UserProfile extends User {
//     bio: string;
//     interests: string[];
//     photos: string[];
// }