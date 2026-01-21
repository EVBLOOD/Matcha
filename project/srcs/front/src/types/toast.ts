export type ToastType =
    | 'error'
    | 'warning'
    | 'success'
    | 'info'
    | 'message'
    | 'like'
    | 'view'

export interface ToastItem {
    id: number
    type: ToastType
    title: string
    description: string;
    avatar: null |string;
    id_user: null | number;
    username: null | string;
}
