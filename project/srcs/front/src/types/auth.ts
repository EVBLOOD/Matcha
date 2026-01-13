export interface Login {
    username: string;
    password: string;
}


export interface RecoverPassword {
    email: string;
}

export interface RecoverPasswordIn {
    new_password: string;
    token: string;
}
