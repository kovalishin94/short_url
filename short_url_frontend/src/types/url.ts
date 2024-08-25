interface User {
    id: number;
    username: string;
    last_name: string;
    first_name: string;
}
export interface URL {
    id: number;
    orig_url: string;
    shorted_url: string;
    click_stat: number;
    created_at: string;
    user: User;
}