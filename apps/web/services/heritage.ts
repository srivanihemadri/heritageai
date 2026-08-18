const API_BASE_URL =
  `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/v1`;

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

export type HeritageMediaType = "IMAGE" | "VIDEO";
export type HeritageSiteHistoricalEventDatePrecision =
  | "YEAR"
  | "MONTH"
  | "DAY"
  | "APPROXIMATE"
  | "PERIOD"
  | "UNKNOWN";

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

interface HeritageSiteHistoricalEventApiResponse {
  success: boolean;
  data: HeritageSiteHistoricalEventListResponse;
  message: string;
}


export type HeritageSiteSourceType =
  | "GOVERNMENT"
  | "UNESCO"
  | "ACADEMIC"
  | "BOOK"
  | "MUSEUM"
  | "ARCHIVE"
  | "WEBSITE"
  | "OTHER";

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

interface HeritageSiteSourceApiResponse {
  success: boolean;
  data: HeritageSiteSourceListResponse;
  message: string;
}
export type HeritageRelationType =
  | "RELATED_TO"
  | "PART_OF"
  | "ASSOCIATED_WITH"
  | "LOCATED_NEAR"
  | "HISTORICALLY_CONNECTED";

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

interface HeritageSiteRelationApiResponse {
  success: boolean;
  data: HeritageSiteRelationListResponse;
  message: string;
}

export function resolveHeritageMediaUrl(
  url: string,
): string {
  if (!url) {
    return url;
  }

  if (
    url.startsWith("/") ||
    url.startsWith("data:") ||
    url.startsWith("blob:")
  ) {
    return url;
  }

  try {
    const parsedUrl = new URL(url);

    const apiUrl = new URL(API_BASE_URL);

    if (
      parsedUrl.hostname === "localhost" ||
      parsedUrl.hostname === "127.0.0.1" ||
      parsedUrl.hostname === "::1"
    ) {
      return `${apiUrl.origin}${parsedUrl.pathname}${parsedUrl.search}`;
    }

    return url;
  } catch {
    return url;
  }
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

interface HeritageSiteMediaApiResponse {
  success: boolean;
  data: HeritageSiteMediaListResponse;
  message: string;
}

export interface HeritageSiteListResponse {
  sites: HeritageSite[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

interface HeritageApiResponse {
  success: boolean;
  data: HeritageSiteListResponse;
  message: string;
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

export async function getHeritageSiteHistoricalEvents(
  siteId: string,
): Promise<HeritageSiteHistoricalEventListResponse> {
  const response = await fetch(
    `${API_BASE_URL}/heritage-sites/${encodeURIComponent(siteId)}/historical-events`,
    {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch heritage site historical events: ${response.status}`,
    );
  }

  const payload =
    (await response.json()) as HeritageSiteHistoricalEventApiResponse;

  if (!payload.success) {
    throw new Error(
      payload.message ||
        "Failed to fetch heritage site historical events",
    );
  }

  return payload.data;
}
export async function getHeritageSite(
  siteId: string,
): Promise<HeritageSite> {
  const response = await fetch(
    `${API_BASE_URL}/heritage-sites/${encodeURIComponent(siteId)}`,
    {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch heritage site: ${response.status}`,
    );
  }

  const payload = (await response.json()) as {
    success: boolean;
    data: HeritageSite;
    message: string;
  };

  if (!payload.success) {
    throw new Error(
      payload.message || "Failed to fetch heritage site",
    );
  }

  return payload.data;
}

export async function getHeritageSiteSources(
  siteId: string,
): Promise<HeritageSiteSourceListResponse> {
  const response = await fetch(
    `${API_BASE_URL}/heritage-sites/${encodeURIComponent(siteId)}/sources`,
    {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch heritage site sources: ${response.status}`,
    );
  }

  const payload =
    (await response.json()) as HeritageSiteSourceApiResponse;

  if (!payload.success) {
    throw new Error(
      payload.message || "Failed to fetch heritage site sources",
    );
  }

  return payload.data;
}
export async function getHeritageSiteRelations(
  siteId: string,
): Promise<HeritageSiteRelationListResponse> {
  const response = await fetch(
    `${API_BASE_URL}/heritage-sites/${encodeURIComponent(siteId)}/relations`,
    {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch heritage site relations: ${response.status}`,
    );
  }

  const payload =
    (await response.json()) as HeritageSiteRelationApiResponse;

  if (!payload.success) {
    throw new Error(
      payload.message || "Failed to fetch heritage site relations",
    );
  }

  return payload.data;
}

export interface ResolvedHeritageSiteRelation {
  relation: HeritageSiteRelation;
  site: HeritageSite;
}

export async function getResolvedHeritageSiteRelations(
  siteId: string,
): Promise<ResolvedHeritageSiteRelation[]> {
  const { relations } = await getHeritageSiteRelations(siteId);

  const activeRelations = relations
    .filter((relation) => relation.is_active)
    .sort((a, b) => {
      if (a.is_verified !== b.is_verified) {
        return a.is_verified ? -1 : 1;
      }

      return a.display_order - b.display_order;
    });

  const resolvedRelations = await Promise.all(
    activeRelations.map(async (relation) => {
      try {
        const site = await getHeritageSite(
          relation.target_site_id,
        );

        return {
          relation,
          site,
        };
      } catch {
        return null;
      }
    }),
  );

  return resolvedRelations.filter(
    (
      item,
    ): item is ResolvedHeritageSiteRelation =>
      item !== null,
  );
}
export async function getHeritageSiteMedia(
  siteId: string,
): Promise<HeritageSiteMediaListResponse> {
  const response = await fetch(
    `${API_BASE_URL}/heritage-sites/${encodeURIComponent(siteId)}/media`,
    {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch heritage site media: ${response.status}`,
    );
  }

  const payload =
    (await response.json()) as HeritageSiteMediaApiResponse;

  if (!payload.success) {
    throw new Error(
      payload.message || "Failed to fetch heritage site media",
    );
  }

  return {
    ...payload.data,
    media: payload.data.media.map((media) => ({
      ...media,
      url: resolveHeritageMediaUrl(media.url),
    })),
  };
}

export async function getHeritageSites(
  filters: HeritageSiteFilters = {},
): Promise<HeritageSiteListResponse> {
  const params = new URLSearchParams();

  if (filters.search) {
    params.set("search", filters.search);
  }

  if (filters.category) {
    params.set("category", filters.category);
  }

  if (filters.country) {
    params.set("country", filters.country);
  }

  if (filters.state) {
    params.set("state", filters.state);
  }

  if (filters.city) {
    params.set("city", filters.city);
  }

  params.set("page", String(filters.page ?? 1));
  params.set("page_size", String(filters.page_size ?? 12));

  const response = await fetch(
    `${API_BASE_URL}/heritage-sites?${params.toString()}`,
    {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch heritage sites: ${response.status}`,
    );
  }

  const payload =
    (await response.json()) as HeritageApiResponse;

  if (!payload.success) {
    throw new Error(
      payload.message || "Failed to fetch heritage sites",
    );
  }

  return payload.data;
}
