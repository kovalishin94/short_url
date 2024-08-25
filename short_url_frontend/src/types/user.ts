interface URL {
  id: number;
  orig_url: string;
  shorted_url: string;
}

export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  urls: Array<URL>;
}
