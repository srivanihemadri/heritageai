import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useRouter } from "expo-router";

import { getHeritageSiteMedia, getHeritageSites } from "@/services/heritage";
import { resolveMediaUrl } from "@/lib/media-url";
import { useAuthStore } from "@/store/auth-store";
import type { HeritageSite } from "@/types/heritage";

export default function HomeScreen() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);

  interface FeaturedSite {
    site: HeritageSite;
    mediaUrl: string | null;
  }

  const [featuredSites, setFeaturedSites] = useState<FeaturedSite[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const loadFeaturedSites = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const result = await getHeritageSites({
          page: 1,
          page_size: 6,
        });

        const featured = await Promise.all(
          result.sites.map(async (site) => {
            try {
              const mediaResult = await getHeritageSiteMedia(site.id);

              const primary =
                mediaResult.media.find(
                  (media) =>
                    media.is_active && media.is_primary,
                ) ??
                mediaResult.media.find(
                  (media) => media.is_active,
                ) ??
                null;

              return {
                site,
                mediaUrl: primary
                  ? resolveMediaUrl(primary.url)
                  : null,
              };
            } catch {
              return {
                site,
                mediaUrl: null,
              };
            }
          }),
        );

        if (!cancelled) {
          setFeaturedSites(featured);
        }
      } catch {
        if (!cancelled) {
          setError("Unable to load heritage sites right now.");
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    };

    void loadFeaturedSites();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <ScrollView
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.hero}>
        <Text style={styles.eyebrow}>HERITAGEAI</Text>

        <Text style={styles.title}>
          Welcome{user?.full_name ? `, ${user.full_name}` : ""}
        </Text>

        <Text style={styles.subtitle}>
          Explore the stories, places, and people that shaped our world.
        </Text>
      </View>

      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Featured Heritage</Text>

        <Pressable onPress={() => router.push("/(app)/explore")}>
          <Text style={styles.link}>See all</Text>
        </Pressable>
      </View>

      {isLoading ? (
        <View style={styles.stateContainer}>
          <ActivityIndicator />
          <Text style={styles.stateText}>Discovering heritage...</Text>
        </View>
      ) : error ? (
        <View style={styles.stateContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      ) : (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.horizontalList}
        >
          {featuredSites.map(({ site, mediaUrl }) => (
            <Pressable
              key={site.id}
              style={styles.card}
              onPress={() =>
                router.push({
                  pathname: "/(app)/heritage/[siteId]",
                  params: { siteId: site.id },
                })
              }
            >
              <View style={styles.imagePlaceholder}>
                {mediaUrl ? (
                  <Image
                    source={{ uri: mediaUrl }}
                    accessibilityLabel={site.name}
                    style={styles.image}
                  />
                ) : (
                  <View style={styles.imageFallback}>
                    <Text style={styles.imageFallbackText}>
                      {site.name}
                    </Text>
                  </View>
                )}
              </View>

              <View style={styles.cardBody}>
                <Text style={styles.cardTitle} numberOfLines={2}>
                  {site.name}
                </Text>

                <Text style={styles.cardLocation} numberOfLines={1}>
                  {[site.city, site.country]
                    .filter(Boolean)
                    .join(", ")}
                </Text>

                {site.category ? (
                  <Text style={styles.cardCategory}>
                    {site.category}
                  </Text>
                ) : null}
              </View>
            </Pressable>
          ))}
        </ScrollView>
      )}

      <View style={styles.quickActions}>
        <Pressable
          style={styles.actionCard}
          onPress={() => router.push("/(app)/explore")}
        >
          <Text style={styles.actionTitle}>Explore Heritage</Text>
          <Text style={styles.actionText}>
            Browse heritage sites by place and category.
          </Text>
        </Pressable>

        <Pressable
          style={styles.actionCard}
          onPress={() => router.push("/(app)/ai-guide")}
        >
          <Text style={styles.actionTitle}>Ask the AI Guide</Text>
          <Text style={styles.actionText}>
            Learn about history through conversation.
          </Text>
        </Pressable>

        <Pressable
          style={styles.actionCard}
          onPress={() => router.push("/(app)/map")}
        >
          <Text style={styles.actionTitle}>Discover Nearby</Text>
          <Text style={styles.actionText}>
            Find heritage places around you.
          </Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: 20,
    paddingTop: 28,
    paddingBottom: 40,
    gap: 24,
  },
  hero: {
    gap: 8,
  },
  eyebrow: {
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 2,
    color: "#C89B5A",
  },
  title: {
    fontSize: 34,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  subtitle: {
    fontSize: 16,
    lineHeight: 24,
    color: "#666666",
  },
  sectionHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  link: {
    fontSize: 14,
    fontWeight: "700",
    color: "#A5793B",
  },
  horizontalList: {
    gap: 16,
  },
  card: {
    width: 280,
    overflow: "hidden",
    borderRadius: 20,
    backgroundColor: "#FFFFFF",
  },
  imagePlaceholder: {
    height: 180,
    backgroundColor: "#E9E2D7",
  },
  image: {
    width: "100%",
    height: "100%",
  },  imageFallback: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 20,
    backgroundColor: "#E9E2D7",
  },
  imageFallbackText: {
    fontSize: 16,
    fontWeight: "700",
    color: "#967243",
    textAlign: "center",
  },
  cardBody: {
    gap: 6,
    padding: 16,
  },
  cardTitle: {
    fontSize: 19,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  cardLocation: {
    fontSize: 14,
    color: "#666666",
  },
  cardCategory: {
    fontSize: 12,
    fontWeight: "700",
    color: "#A5793B",
    textTransform: "uppercase",
  },
  stateContainer: {
    minHeight: 180,
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },
  stateText: {
    color: "#666666",
  },
  errorText: {
    color: "#8A3D3D",
    textAlign: "center",
  },
  quickActions: {
    gap: 12,
  },
  actionCard: {
    padding: 18,
    borderRadius: 18,
    backgroundColor: "#F4EFE7",
    gap: 6,
  },
  actionTitle: {
    fontSize: 17,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  actionText: {
    fontSize: 14,
    lineHeight: 20,
    color: "#666666",
  },
});
