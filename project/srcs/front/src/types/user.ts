// export type UserRole = 'admin' | 'user' | 'moderator';

export interface UserRegister {
    username: string;
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    birhdate: any;
}


// export interface UserProfile extends User {
//     bio: string;
//     interests: string[];
//     photos: string[];
// }