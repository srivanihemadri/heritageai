import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Image,
  Pressable,
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useRouter } from "expo-router";

import {
  getHeritageSiteMedia,
  getHeritageSites,
} from "@/services/heritage";
import { resolveMediaUrl } from "@/lib/media-url";
import type {
  HeritageSite,
  HeritageSiteMedia,
} from "@/types/heritage";

interface ExploreItem {
  site: HeritageSite;
  media: HeritageSiteMedia | null;
}

export default function ExploreScreen() {
  const router = useRouter();

  const [items, setItems] = useState<ExploreItem[]>([]);
  const [search, setSearch] = useState("");
  const [appliedSearch, setAppliedSearch] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    let cancelled = false;

    const loadInitialSites = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const result = await getHeritageSites({
          search: appliedSearch || undefined,
          page: 1,
          page_size: 20,
        });

        const enriched = await Promise.all(
          result.sites.map(async (site) => {
            try {
              const mediaResult =
                await getHeritageSiteMedia(site.id);

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
                media: primary,
              };
            } catch {
              return {
                site,
                media: null,
              };
            }
          }),
        );

        if (!cancelled) {
          setItems(enriched);
        }
      } catch {
        if (!cancelled) {
          setError("Unable to load heritage sites.");
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    };

    void loadInitialSites();

    return () => {
      cancelled = true;
    };
  }, [appliedSearch, refreshKey]);

  const handleSearch = () => {
    setAppliedSearch(search.trim());
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.eyebrow}>DISCOVER</Text>

        <Text style={styles.title}>Explore Heritage</Text>

        <Text style={styles.subtitle}>
          Discover remarkable places and their stories.
        </Text>
      </View>

      <View style={styles.searchRow}>
        <TextInput
          value={search}
          onChangeText={setSearch}
          placeholder="Search heritage sites"
          placeholderTextColor="#8C8C8C"
          style={styles.searchInput}
          returnKeyType="search"
          onSubmitEditing={handleSearch}
          autoCapitalize="none"
          autoCorrect={false}
        />

        <Pressable
          style={styles.searchButton}
          onPress={handleSearch}
        >
          <Text style={styles.searchButtonText}>Search</Text>
        </Pressable>
      </View>

      {isLoading ? (
        <View style={styles.state}>
          <ActivityIndicator />
          <Text style={styles.stateText}>Loading heritage...</Text>
        </View>
      ) : error ? (
        <View style={styles.state}>
          <Text style={styles.error}>{error}</Text>

          <Pressable
            onPress={() => setRefreshKey((value) => value + 1)}
            style={styles.retryButton}
          >
            <Text style={styles.retryText}>Retry</Text>
          </Pressable>
        </View>
      ) : (
        <ScrollView
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl
              refreshing={isRefreshing}
              onRefresh={() => setRefreshKey((value) => value + 1)}
            />
          }
          contentContainerStyle={styles.list}
        >
          {items.length === 0 ? (
            <View style={styles.empty}>
              <Text style={styles.emptyTitle}>
                No heritage sites found
              </Text>

              <Text style={styles.emptyText}>
                Try a different search.
              </Text>
            </View>
          ) : (
            items.map(({ site, media }) => (
              <Pressable
                key={site.id}
                style={styles.card}
                onPress={() =>
                  router.push({
                    pathname: "/(app)/heritage/[siteId]",
                    params: {
                      siteId: site.id,
                    },
                  })
                }
              >
                <View style={styles.imageContainer}>
                  {media ? (
                    <Image
                      source={{
                        uri: resolveMediaUrl(media.url),
                      }}
                      accessibilityLabel={
                        media.alt_text ?? site.name
                      }
                      style={styles.image}
                    />
                  ) : (
                    <View style={styles.imageFallback}>
                      <Text style={styles.imageFallbackText}>
                        HeritageAI
                      </Text>
                    </View>
                  )}
                </View>

                <View style={styles.body}>
                  <Text style={styles.cardTitle} numberOfLines={2}>
                    {site.name}
                  </Text>

                  <Text
                    style={styles.location}
                    numberOfLines={1}
                  >
                    {[site.city, site.country]
                      .filter(Boolean)
                      .join(", ")}
                  </Text>

                  <View style={styles.metaRow}>
                    <Text style={styles.category}>
                      {site.category}
                    </Text>

                    {site.is_verified ? (
                      <Text style={styles.verified}>
                        VERIFIED
                      </Text>
                    ) : null}
                  </View>
                </View>
              </Pressable>
            ))
          )}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F7F3EC",
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 28,
    gap: 6,
  },
  eyebrow: {
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 2,
    color: "#B07D38",
  },
  title: {
    fontSize: 30,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  subtitle: {
    fontSize: 15,
    lineHeight: 22,
    color: "#6E6E6E",
  },
  searchRow: {
    flexDirection: "row",
    gap: 10,
    paddingHorizontal: 20,
    paddingVertical: 18,
  },
  searchInput: {
    flex: 1,
    height: 48,
    borderRadius: 14,
    paddingHorizontal: 15,
    backgroundColor: "#FFFFFF",
    color: "#1C1C1C",
    borderWidth: 1,
    borderColor: "#E5DED1",
  },
  searchButton: {
    minWidth: 76,
    height: 48,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#1C1C1C",
  },
  searchButtonText: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
  list: {
    paddingHorizontal: 20,
    paddingBottom: 36,
    gap: 16,
  },
  card: {
    overflow: "hidden",
    borderRadius: 20,
    backgroundColor: "#FFFFFF",
  },
  imageContainer: {
    height: 200,
    backgroundColor: "#E9E1D4",
  },
  image: {
    width: "100%",
    height: "100%",
  },
  imageFallback: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  imageFallbackText: {
    fontSize: 18,
    fontWeight: "800",
    color: "#967243",
  },
  body: {
    padding: 16,
    gap: 7,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: "800",
    color: "#1C1C1C",
  },
  location: {
    fontSize: 14,
    color: "#6B6B6B",
  },
  metaRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    marginTop: 3,
  },
  category: {
    fontSize: 12,
    fontWeight: "700",
    color: "#A2763C",
    textTransform: "uppercase",
  },
  verified: {
    fontSize: 10,
    fontWeight: "800",
    color: "#3B6949",
  },
  state: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
    paddingHorizontal: 24,
  },
  stateText: {
    color: "#6B6B6B",
  },
  error: {
    color: "#8A3D3D",
    textAlign: "center",
  },
  retryButton: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 12,
    backgroundColor: "#1C1C1C",
  },
  retryText: {
    color: "#FFFFFF",
    fontWeight: "700",
  },
  empty: {
    alignItems: "center",
    paddingVertical: 80,
    gap: 8,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: "800",
  },
  emptyText: {
    color: "#6B6B6B",
  },
});
