export type CompanyStatus = 'wishlist' | 'applied' | 'interviewing' | 'offer' | 'rejected' | null;

export interface Company {
  id: number;
  company_name: string;
  url?: string | null;
  career_page_url?: string | null;
  careers?: string | null;
  notes?: string | null;
  status?: CompanyStatus;
  user_rank?: number | null;
}

export interface Role {
  id: number;
  company_id: number;
  role_title: string;
  role_link?: string | null;
  salary?: string | null;
  score?: number | null;
}
