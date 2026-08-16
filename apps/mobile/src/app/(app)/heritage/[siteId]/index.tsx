import { useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { Stack, useLocalSearchParams, useRouter } from "expo-router";

import { resolveMediaUrl } from "@/lib/media-url";
import {
  getHeritageSite,
  getHeritageSiteHistoricalEvents,
  getHeritageSiteMedia,
  getHeritageSiteRelations,
  getHeritageSiteSources,
} from "@/services/heritage";
import type {
  HeritageSite,
  HeritageSiteHistoricalEvent,
  HeritageSiteMedia,
  HeritageSiteRelation,
  HeritageSiteSource,
} from "@/types/heritage";

interface RelatedSite {
  relation: HeritageSiteRelation;
  site: HeritageSite;
}

export default function HeritageDetailScreen() {
  const router = useRouter();

  const { siteId } = useLocalSearchParams<{
    siteId: string;
  }>();

  const [site, setSite] = useState<HeritageSite | null>(null);
  const [media, setMedia] = useState<HeritageSiteMedia | null>(null);
  const [events, setEvents] = useState<HeritageSiteHistoricalEvent[]>([]);
  const [sources, setSources] = useState<HeritageSiteSource[]>([]);
  const [relatedSites, setRelatedSites] = useState<RelatedSite[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const loadDetail = async () => {
      if (!siteId) {
        setError("Heritage site was not specified.");
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);

        const [
          siteResult,
          mediaResult,
          eventsResult,
          sourcesResult,
          relationsResult,
        ] = await Promise.all([
          getHeritageSite(siteId),
          getHeritageSiteMedia(siteId),
          getHeritageSiteHistoricalEvents(siteId),
          getHeritageSiteSources(siteId),
          getHeritageSiteRelations(siteId),
        ]);

        const primaryMedia =
          mediaResult.media.find(
            (item) => item.is_active && item.is_primary,
          ) ??
          mediaResult.media.find(
            (item) => item.is_active,
          ) ??
          null;

        const activeEvents = eventsResult.events
          .filter((event) => event.is_active)
          .sort((a, b) => {
            if (a.is_verified !== b.is_verified) {
              return a.is_verified ? -1 : 1;
            }

            return a.display_order - b.display_order;
          });

        const activeSources = sourcesResult.sources
          .filter((source) => source.is_active)
          .sort((a, b) => {
            if (a.is_verified !== b.is_verified) {
              return a.is_verified ? -1 : 1;
            }

            return a.display_order - b.display_order;
          });

        const activeRelations = relationsResult.relations
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
              const related = await getHeritageSite(
                relation.target_site_id,
              );

              return {
                relation,
                site: related,
              };
            } catch {
              return null;
            }
          }),
        );

        if (cancelled) {
          return;
        }

        setSite(siteResult);
        setMedia(primaryMedia);
        setEvents(activeEvents);
        setSources(activeSources);
        setRelatedSites(
          resolvedRelations.filter(
            (item): item is RelatedSite =>
              item !== null,
          ),
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load this heritage site right now.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    };

    void loadDetail();

    return () => {
      cancelled = true;
    };
  }, [siteId]);

  const mediaUrl = useMemo(
    () => (media ? resolveMediaUrl(media.url) : null),
    [media],
  );

  return (
    <>
      <Stack.Screen
        options={{
          title: site?.name ?? "Heritage",
        }}
      />

      {isLoading ? (
        <View style={styles.center}>
          <ActivityIndicator />
          <Text style={styles.muted}>
            Loading heritage details...
          </Text>
        </View>
      ) : error || !site ? (
        <View style={styles.center}>
          <Text style={styles.error}>
            {error ?? "Heritage site not found."}
          </Text>

          <Pressable
            style={styles.retryButton}
            onPress={() => router.back()}
          >
            <Text style={styles.retryText}>
              Go Back
            </Text>
          </Pressable>
        </View>
      ) : (
        <ScrollView
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.hero}>
            {mediaUrl ? (
              <Image
                source={{ uri: mediaUrl }}
                accessibilityLabel={
                  media?.alt_text ?? site.name
                }
                style={styles.heroImage}
              />
            ) : (
              <View style={styles.heroFallback}>
                <Text style={styles.heroFallbackText}>
                  {site.name}
                </Text>
              </View>
            )}

            <View style={styles.heroOverlay}>
              <Text style={styles.category}>
                {site.category}
              </Text>

              <Text style={styles.heroTitle}>
                {site.name}
              </Text>

              <Text style={styles.location}>
                {[site.city, site.state, site.country]
                  .filter(Boolean)
                  .join(", ")}
              </Text>

              {site.is_verified ? (
                <View style={styles.verifiedBadge}>
                  <Text style={styles.verifiedText}>
                    VERIFIED HERITAGE SITE
                  </Text>
                </View>
              ) : null}
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionLabel}>
              OVERVIEW
            </Text>

            <Text style={styles.description}>
              {site.description ??
                site.short_description ??
                "No description is currently available."}
            </Text>
          </View>

          <View style={styles.factsGrid}>
            <Fact
              label="Established"
              value={
                site.established_year
                  ? String(site.established_year)
                  : "Unknown"
              }
            />

            <Fact
              label="Historical Period"
              value={
                site.historical_period ?? "Unknown"
              }
            />

            <Fact
              label="Architecture"
              value={
                site.architectural_style ?? "Unknown"
              }
            />

            <Fact
              label="Preservation"
              value={
                site.preservation_status ?? "Unknown"
              }
            />
          </View>

          {site.significance ? (
            <View style={styles.sectionCard}>
              <Text style={styles.sectionLabel}>
                SIGNIFICANCE
              </Text>

              <Text style={styles.bodyText}>
                {site.significance}
              </Text>
            </View>
          ) : null}

          <View style={styles.sectionCard}>
            <Text style={styles.sectionTitle}>
              Historical Timeline
            </Text>

            {events.length === 0 ? (
              <Text style={styles.muted}>
                No historical events are currently
                available.
              </Text>
            ) : (
              <View style={styles.timeline}>
                {events.map((event, index) => (
                  <View
                    key={event.id}
                    style={styles.timelineItem}
                  >
                    <View style={styles.timelineRail}>
                      <View style={styles.timelineDot} />

                      {index < events.length - 1 ? (
                        <View
                          style={styles.timelineLine}
                        />
                      ) : null}
                    </View>

                    <View style={styles.timelineBody}>
                      <Text
                        style={styles.timelineDate}
                      >
                        {event.date_label ??
                          event.event_date ??
                          "Date unavailable"}
                      </Text>

                      <Text
                        style={styles.timelineTitle}
                      >
                        {event.title}
                      </Text>

                      {event.description ? (
                        <Text
                          style={styles.timelineDescription}
                        >
                          {event.description}
                        </Text>
                      ) : null}

                      {event.significance ? (
                        <Text
                          style={styles.timelineSignificance}
                        >
                          {event.significance}
                        </Text>
                      ) : null}
                    </View>
                  </View>
                ))}
              </View>
            )}
          </View>

          {relatedSites.length > 0 ? (
            <View style={styles.sectionCard}>
              <View style={styles.sectionHeader}>
                <Text style={styles.sectionTitle}>
                  Related Heritage
                </Text>

                <Text style={styles.muted}>
                  {relatedSites.length}
                </Text>
              </View>

              <View style={styles.relatedList}>
                {relatedSites.map(({ relation, site: related }) => (
                  <Pressable
                    key={relation.id}
                    style={styles.relatedCard}
                    onPress={() =>
                      router.push({
                        pathname:
                          "/(app)/heritage/[siteId]",
                        params: {
                          siteId: related.id,
                        },
                      })
                    }
                  >
                    <Text style={styles.relatedTitle}>
                      {related.name}
                    </Text>

                    <Text style={styles.relatedLocation}>
                      {[
                        related.city,
                        related.country,
                      ]
                        .filter(Boolean)
                        .join(", ")}
                    </Text>

                    <Text style={styles.relatedType}>
                      {relation.relation_type}
                    </Text>
                  </Pressable>
                ))}
              </View>
            </View>
          ) : null}

          {sources.length > 0 ? (
            <View style={styles.sectionCard}>
              <Text style={styles.sectionTitle}>
                Sources & Provenance
              </Text>

              <View style={styles.relatedList}>
                {sources.map((source) => (
                  <View
                    key={source.id}
                    style={styles.sourceCard}
                  >
                    <Text style={styles.sourceType}>
                      {source.source_type}
                    </Text>

                    <Text style={styles.sourceTitle}>
                      {source.title}
                    </Text>

                    {source.author ? (
                      <Text style={styles.muted}>
                        {source.author}
                      </Text>
                    ) : null}

                    {source.organization ? (
                      <Text style={styles.muted}>
                        {source.organization}
                      </Text>
                    ) : null}

                    {source.citation_text ? (
                      <Text style={styles.sourceCitation}>
                        {source.citation_text}
                      </Text>
                    ) : null}
                  </View>
                ))}
              </View>
            </View>
          ) : null}
        </ScrollView>
      )}
    </>
  );
}

function Fact({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <View style={styles.fact}>
      <Text style={styles.factLabel}>{label}</Text>
      <Text style={styles.factValue} numberOfLines={3}>
        {value}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  content: {
    paddingBottom: 40,
    backgroundColor: "#F7F3EC",
  },
  hero: {
    minHeight: 420,
    backgroundColor: "#E5DCCF",
    position: "relative",
  },
  heroImage: {
    width: "100%",
    height: 420,
  },
  heroFallback: {
    height: 420,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 28,
  },
  heroFallbackText: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: "800",
    color: "#70542E",
    textAlign: "center",
  },
  heroShade: {
    ...StyleSheet.absoluteFill,
    backgroundColor: "rgba(0,0,0,0.26)",
  },
  heroOverlay: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    paddingHorizontal: 22,
    paddingTop: 34,
    paddingBottom: 26,
    backgroundColor: "rgba(0,0,0,0.34)",
    gap: 8,
  },
  heroMetaRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  categoryPill: {
    alignSelf: "flex-start",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
    backgroundColor: "rgba(24,24,24,0.62)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.18)",
  },
  category: {
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1.3,
    color: "#F3D9A1",
  },
  heroTitle: {
    fontSize: 32,
    lineHeight: 37,
    fontWeight: "900",
    color: "#FFFFFF",
  },
  location: {
    fontSize: 14,
    color: "#F1ECE3",
  },
  verifiedBadge: {
    alignSelf: "flex-start",
    marginTop: 6,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 6,
    backgroundColor: "#D7E7DB",
  },
  verifiedText: {
    fontSize: 9,
    fontWeight: "900",
    color: "#31563A",
    letterSpacing: 0.8,
  },
  section: {
    paddingHorizontal: 20,
    paddingTop: 24,
    gap: 10,
  },
  sectionCard: {
    marginHorizontal: 20,
    marginTop: 20,
    padding: 20,
    borderRadius: 20,
    backgroundColor: "#FFFFFF",
    gap: 14,
  },
  sectionEyebrowRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  sectionAccent: {
    width: 20,
    height: 3,
    borderRadius: 999,
    backgroundColor: "#B27C38",
  },
  sectionLabel: {
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1.5,
    color: "#97703F",
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  sectionHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  description: {
    fontSize: 17,
    lineHeight: 27,
    color: "#353535",
  },
  bodyText: {
    fontSize: 15,
    lineHeight: 23,
    color: "#444444",
  },
  factsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 12,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  fact: {
    width: "47%",
    padding: 15,
    borderRadius: 16,
    backgroundColor: "#EEE7DC",
    gap: 6,
  },
  factLabel: {
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1,
    color: "#8A7350",
    textTransform: "uppercase",
  },
  factValue: {
    fontSize: 15,
    lineHeight: 20,
    fontWeight: "700",
    color: "#262626",
  },
  timeline: {
    gap: 4,
  },
  timelineItem: {
    flexDirection: "row",
  },
  timelineRail: {
    width: 28,
    alignItems: "center",
  },
  timelineDot: {
    width: 12,
    height: 12,
    marginTop: 3,
    borderRadius: 999,
    backgroundColor: "#B27C38",
  },
  timelineLine: {
    flex: 1,
    width: 2,
    marginTop: 4,
    backgroundColor: "#DCCDB6",
  },
  timelineBody: {
    flex: 1,
    paddingBottom: 22,
    paddingLeft: 8,
    gap: 5,
  },
  timelineDate: {
    fontSize: 11,
    fontWeight: "900",
    color: "#A57839",
    letterSpacing: 0.6,
  },
  timelineTitle: {
    fontSize: 16,
    lineHeight: 21,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  timelineDescription: {
    fontSize: 14,
    lineHeight: 21,
    color: "#555555",
  },
  timelineSignificance: {
    fontSize: 13,
    lineHeight: 19,
    color: "#7A6244",
    fontStyle: "italic",
  },
  relatedList: {
    gap: 10,
  },
  relatedCard: {
    padding: 15,
    borderRadius: 14,
    backgroundColor: "#F5F0E7",
    gap: 4,
  },
  relatedTitle: {
    fontSize: 16,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  relatedLocation: {
    fontSize: 13,
    color: "#6A6A6A",
  },
  relatedType: {
    fontSize: 10,
    fontWeight: "800",
    color: "#A57839",
    letterSpacing: 0.8,
  },
  sourceCard: {
    padding: 15,
    borderRadius: 14,
    backgroundColor: "#F5F0E7",
    gap: 5,
  },
  sourceType: {
    fontSize: 10,
    fontWeight: "900",
    color: "#A57839",
    letterSpacing: 1,
  },
  sourceTitle: {
    fontSize: 16,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  sourceCitation: {
    fontSize: 13,
    lineHeight: 19,
    color: "#5F5F5F",
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
    padding: 24,
    backgroundColor: "#F7F3EC",
  },
  muted: {
    fontSize: 13,
    color: "#727272",
  },
  error: {
    fontSize: 15,
    color: "#8A3D3D",
    textAlign: "center",
  },
  retryButton: {
    paddingHorizontal: 20,
    paddingVertical: 11,
    borderRadius: 12,
    backgroundColor: "#1C1C1C",
  },
  retryText: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
});
