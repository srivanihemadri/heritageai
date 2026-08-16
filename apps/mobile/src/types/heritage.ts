export type HeritageMediaType = "IMAGE" | "VIDEO";

export type HeritageSiteHistoricalEventDatePrecision =
  | "YEAR"
  | "MONTH"
  | "DAY"
  | "APPROXIMATE"
  | "PERIOD"
  | "UNKNOWN";

export type HeritageSiteSourceType =
  | "GOVERNMENT"
  | "UNESCO"
  | "ACADEMIC"
  | "BOOK"
  | "MUSEUM"
  | "ARCHIVE"
  | "WEBSITE"
  | "OTHER";

export interface APIResponse<T> {
  success: boolean;
  data: T;
  message: string;
}
export type HeritageRelationType =
  | "RELATED_TO"
  | "PART_OF"
  | "ASSOCIATED_WITH"
  | "LOCATED_NEAR"
  | "HISTORICALLY_CONNECTED";

export interface HeritageSite {
  id: string;
  name: string;
  slug: string;
  short_description: string | null;
  description: string | null;
  category: string;
  country: string;
  state: string | null;
  city: string | null;
  latitude: number | null;
  longitude: number | null;
  established_year: number | null;
  architectural_style: string | null;
  historical_period: string | null;
  significance: string | null;
  preservation_status: string | null;
  is_verified: boolean;
  is_active: boolean;
}

export interface HeritageSiteListResponse {
  sites: HeritageSite[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface HeritageSiteFilters {
  search?: string;
  category?: string;
  country?: string;
  state?: string;
  city?: string;
  page?: number;
  page_size?: number;
}

export interface HeritageSiteMedia {
  id: string;
  site_id: string;
  media_type: HeritageMediaType;
  storage_key: string;
  url: string;
  title: string | null;
  alt_text: string | null;
  display_order: number;
  is_primary: boolean;
  is_active: boolean;
}

export interface HeritageSiteMediaListResponse {
  media: HeritageSiteMedia[];
  total: number;
}

export interface HeritageSiteHistoricalEvent {
  id: string;
  site_id: string;
  title: string;
  description: string | null;
  event_date: string | null;
  date_label: string | null;
  date_precision: HeritageSiteHistoricalEventDatePrecision;
  significance: string | null;
  display_order: number;
  is_verified: boolean;
  is_active: boolean;
}

export interface HeritageSiteHistoricalEventListResponse {
  events: HeritageSiteHistoricalEvent[];
  total: number;
}

export interface HeritageSiteSource {
  id: string;
  site_id: string;
  source_type: HeritageSiteSourceType;
  title: string;
  author: string | null;
  organization: string | null;
  publisher: string | null;
  publication_date: string | null;
  url: string | null;
  citation_text: string | null;
  language: string;
  display_order: number;
  is_verified: boolean;
  is_active: boolean;
}

export interface HeritageSiteSourceListResponse {
  sources: HeritageSiteSource[];
  total: number;
}

export interface HeritageSiteRelation {
  id: string;
  source_site_id: string;
  target_site_id: string;
  relation_type: HeritageRelationType;
  description: string | null;
  display_order: number;
  is_verified: boolean;
  is_active: boolean;
}

export interface HeritageSiteRelationListResponse {
  relations: HeritageSiteRelation[];
  total: number;
}

export interface ResolvedHeritageSiteRelation {
  relation: HeritageSiteRelation;
  site: HeritageSite;
}
