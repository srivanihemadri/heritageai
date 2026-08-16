import apiClient from "@/lib/api-client";
import type {
  APIResponse,
  HeritageSite,
  HeritageSiteFilters,
  HeritageSiteHistoricalEventListResponse,
  HeritageSiteListResponse,
  HeritageSiteMediaListResponse,
  HeritageSiteRelationListResponse,
  HeritageSiteSourceListResponse,
  ResolvedHeritageSiteRelation,
} from "@/types/heritage";

export async function getHeritageSites(
  filters: HeritageSiteFilters = {},
): Promise<HeritageSiteListResponse> {
  const response = await apiClient.get<
    APIResponse<HeritageSiteListResponse>
  >("/heritage-sites", {
    params: {
      search: filters.search,
      category: filters.category,
      country: filters.country,
      state: filters.state,
      city: filters.city,
      page: filters.page ?? 1,
      page_size: filters.page_size ?? 12,
    },
  });

  return response.data.data;
}

export async function getHeritageSite(
  siteId: string,
): Promise<HeritageSite> {
  const response = await apiClient.get<APIResponse<HeritageSite>>(
    `/heritage-sites/${encodeURIComponent(siteId)}`,
  );

  return response.data.data;
}

export async function getHeritageSiteMedia(
  siteId: string,
): Promise<HeritageSiteMediaListResponse> {
  const response = await apiClient.get<
    APIResponse<HeritageSiteMediaListResponse>
  >(`/heritage-sites/${encodeURIComponent(siteId)}/media`);

  return response.data.data;
}

export async function getHeritageSiteHistoricalEvents(
  siteId: string,
): Promise<HeritageSiteHistoricalEventListResponse> {
  const response = await apiClient.get<
    APIResponse<HeritageSiteHistoricalEventListResponse>
  >(`/heritage-sites/${encodeURIComponent(siteId)}/historical-events`);

  return response.data.data;
}

export async function getHeritageSiteSources(
  siteId: string,
): Promise<HeritageSiteSourceListResponse> {
  const response = await apiClient.get<
    APIResponse<HeritageSiteSourceListResponse>
  >(`/heritage-sites/${encodeURIComponent(siteId)}/sources`);

  return response.data.data;
}

export async function getHeritageSiteRelations(
  siteId: string,
): Promise<HeritageSiteRelationListResponse> {
  const response = await apiClient.get<
    APIResponse<HeritageSiteRelationListResponse>
  >(`/heritage-sites/${encodeURIComponent(siteId)}/relations`);

  return response.data.data;
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
        const site = await getHeritageSite(relation.target_site_id);

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
    (item): item is ResolvedHeritageSiteRelation =>
      item !== null,
  );
}
