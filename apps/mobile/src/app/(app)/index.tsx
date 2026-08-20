import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";

import {
  HeritageColors,
  HeritageRadius,
  HeritageSpacing,
  HeritageTypography,
} from "@/constants/theme";
import {
  getHeritageSiteMedia,
  getHeritageSites,
} from "@/services/heritage";
import { resolveMediaUrl } from "@/lib/media-url";
import { useAuthStore } from "@/store/auth-store";
import type { HeritageSite } from "@/types/heritage";

interface FeaturedSite {
  site: HeritageSite;
  mediaUrl: string | null;
}

export default function HomeScreen() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);

  const [featuredSites, setFeaturedSites] = useState<FeaturedSite[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

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
          setError(
            "Unable to load heritage sites right now.",
          );
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

  const firstName =
    user?.full_name?.trim().split(" ")[0] || "Explorer";

  const openSearch = () => {
    router.push({
      pathname: "/(app)/explore",
      params: search.trim()
        ? { search: search.trim() }
        : undefined,
    });
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={["top"]}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >
        {/* HEADER */}
        <View style={styles.header}>
          <View style={styles.brandRow}>
            <View style={styles.logoMark}>
              <Ionicons
                name="sparkles"
                size={18}
                color={HeritageColors.goldLight}
              />
            </View>

            <View>
              <Text style={styles.brand}>HERITAGEAI</Text>
              <Text style={styles.brandCaption}>
                PRESERVE · DISCOVER · EXPERIENCE
              </Text>
            </View>
          </View>

          <Pressable
            style={styles.profileButton}
            onPress={() => router.push("/(app)/profile")}
          >
            <Ionicons
              name="person-outline"
              size={20}
              color={HeritageColors.ivory}
            />
          </Pressable>
        </View>

        {/* GREETING */}
        <View style={styles.greeting}>
          <Text style={styles.greetingSmall}>
            WELCOME BACK
          </Text>

          <Text style={styles.greetingTitle}>
            Discover, {firstName}.
          </Text>

          <Text style={styles.greetingSubtitle}>
            Step into the stories that shaped our world.
          </Text>
        </View>

        {/* SEARCH */}
        <Pressable
          style={styles.searchContainer}
          onPress={openSearch}
        >
          <Ionicons
            name="search-outline"
            size={21}
            color={HeritageColors.muted}
          />

          <TextInput
            value={search}
            onChangeText={setSearch}
            onSubmitEditing={openSearch}
            placeholder="Search heritage, places, history..."
            placeholderTextColor={HeritageColors.mutedDark}
            style={styles.searchInput}
            returnKeyType="search"
          />

          <Ionicons
            name="options-outline"
            size={19}
            color={HeritageColors.goldLight}
          />
        </Pressable>

        {/* DISCOVER HERO */}
        <Pressable
          style={styles.heroCard}
          onPress={() => router.push("/(app)/explore")}
        >
          <View style={styles.heroGlow} />

          <View style={styles.heroContent}>
            <View style={styles.heroBadge}>
              <Ionicons
                name="sparkles"
                size={13}
                color={HeritageColors.goldLight}
              />
              <Text style={styles.heroBadgeText}>
                YOUR HERITAGE JOURNEY
              </Text>
            </View>

            <Text style={styles.heroTitle}>
              Discover the past.
              {"\n"}
              Experience the story.
            </Text>

            <Text style={styles.heroDescription}>
              Explore remarkable places, uncover forgotten
              stories, and connect with history through AI.
            </Text>

            <View style={styles.heroButton}>
              <Text style={styles.heroButtonText}>
                Start Exploring
              </Text>

              <Ionicons
                name="arrow-forward"
                size={17}
                color={HeritageColors.black}
              />
            </View>
          </View>
        </Pressable>

        {/* FEATURED */}
        <View style={styles.sectionHeader}>
          <View>
            <Text style={styles.sectionEyebrow}>
              CURATED FOR YOU
            </Text>
            <Text style={styles.sectionTitle}>
              Featured Heritage
            </Text>
          </View>

          <Pressable
            onPress={() => router.push("/(app)/explore")}
          >
            <Text style={styles.seeAll}>See all</Text>
          </Pressable>
        </View>

        {isLoading ? (
          <View style={styles.loading}>
            <ActivityIndicator
              color={HeritageColors.goldLight}
            />
            <Text style={styles.loadingText}>
              Discovering heritage...
            </Text>
          </View>
        ) : error ? (
          <View style={styles.errorCard}>
            <Ionicons
              name="alert-circle-outline"
              size={22}
              color={HeritageColors.danger}
            />
            <Text style={styles.errorText}>{error}</Text>
          </View>
        ) : (
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.featuredList}
          >
            {featuredSites.map(({ site, mediaUrl }) => (
              <Pressable
                key={site.id}
                style={styles.featuredCard}
                onPress={() =>
                  router.push({
                    pathname:
                      "/(app)/heritage/[siteId]",
                    params: { siteId: site.id },
                  })
                }
              >
                <View style={styles.featuredImage}>
                  {mediaUrl ? (
                    <Image
                      source={{ uri: mediaUrl }}
                      style={styles.image}
                      accessibilityLabel={site.name}
                    />
                  ) : (
                    <View style={styles.imageFallback}>
                      <Ionicons
                        name="business-outline"
                        size={32}
                        color={HeritageColors.goldDark}
                      />
                    </View>
                  )}

                  <View style={styles.imageOverlay} />

                  {site.is_verified && (
                    <View style={styles.verified}>
                      <Ionicons
                        name="checkmark-circle"
                        size={14}
                        color={HeritageColors.goldLight}
                      />
                      <Text style={styles.verifiedText}>
                        VERIFIED
                      </Text>
                    </View>
                  )}
                </View>

                <View style={styles.featuredBody}>
                  <Text
                    style={styles.featuredTitle}
                    numberOfLines={2}
                  >
                    {site.name}
                  </Text>

                  <View style={styles.locationRow}>
                    <Ionicons
                      name="location-outline"
                      size={13}
                      color={HeritageColors.gold}
                    />

                    <Text
                      style={styles.location}
                      numberOfLines={1}
                    >
                      {[site.city, site.state, site.country]
                        .filter(Boolean)
                        .join(", ")}
                    </Text>
                  </View>

                  <Text style={styles.category}>
                    {site.category}
                  </Text>
                </View>
              </Pressable>
            ))}
          </ScrollView>
        )}

        {/* AI ACTIONS */}
        <View style={styles.sectionHeader}>
          <View>
            <Text style={styles.sectionEyebrow}>
              POWERED BY AI
            </Text>
            <Text style={styles.sectionTitle}>
              What would you like to do?
            </Text>
          </View>
        </View>

        <View style={styles.actionsGrid}>
          <Pressable
            style={[
              styles.actionCard,
              styles.actionCardLarge,
            ]}
            onPress={() =>
              router.push("/(app)/ai-scanner")
            }
          >
            <View
              style={[
                styles.actionIcon,
                styles.scannerIcon,
              ]}
            >
              <Ionicons
                name="scan-outline"
                size={27}
                color={HeritageColors.goldLight}
              />
            </View>

            <View style={styles.actionTextBlock}>
              <Text style={styles.actionLabel}>
                AI SCANNER
              </Text>

              <Text style={styles.actionTitle}>
                Identify Heritage
              </Text>

              <Text style={styles.actionDescription}>
                Point your camera at a monument or artifact
                and let AI reveal its story.
              </Text>
            </View>

            <Ionicons
              name="arrow-forward-circle"
              size={28}
              color={HeritageColors.gold}
            />
          </Pressable>

          <Pressable
            style={styles.actionCard}
            onPress={() => router.push("/(app)/ai")}
          >
            <View
              style={[
                styles.actionIcon,
                styles.aiIcon,
              ]}
            >
              <Ionicons
                name="chatbubbles-outline"
                size={23}
                color="#C58CFF"
              />
            </View>

            <Text style={styles.actionLabel}>
              CHAT WITH AI
            </Text>

            <Text style={styles.actionTitleSmall}>
              Ask anything
            </Text>

            <Text style={styles.actionDescription}>
              Talk with your heritage companion.
            </Text>
          </Pressable>

          <Pressable
            style={styles.actionCard}
            onPress={() =>
              router.push("/(app)/explore")
            }
          >
            <View
              style={[
                styles.actionIcon,
                styles.exploreIcon,
              ]}
            >
              <Ionicons
                name="compass-outline"
                size={23}
                color={HeritageColors.goldLight}
              />
            </View>

            <Text style={styles.actionLabel}>
              EXPLORE
            </Text>

            <Text style={styles.actionTitleSmall}>
              Find places
            </Text>

            <Text style={styles.actionDescription}>
              Browse heritage across the world.
            </Text>
          </Pressable>
        </View>

        {/* RECENTLY EXPLORED */}
        <View style={styles.sectionHeader}>
          <View>
            <Text style={styles.sectionEyebrow}>
              YOUR JOURNEY
            </Text>
            <Text style={styles.sectionTitle}>
              Recently Explored
            </Text>
          </View>
        </View>

        <View style={styles.emptyRecent}>
          <View style={styles.emptyRecentIcon}>
            <Ionicons
              name="time-outline"
              size={25}
              color={HeritageColors.gold}
            />
          </View>

          <View style={styles.emptyRecentContent}>
            <Text style={styles.emptyRecentTitle}>
              Your journey starts here
            </Text>

            <Text style={styles.emptyRecentText}>
              Explore heritage sites and they will appear
              here for quick access.
            </Text>
          </View>
        </View>

        <View style={styles.bottomSpacer} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: HeritageColors.background,
  },

  content: {
    paddingHorizontal: HeritageSpacing.lg,
    paddingTop: HeritageSpacing.md,
    paddingBottom: 110,
    gap: HeritageSpacing.xl,
  },

  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  brandRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: HeritageSpacing.sm,
  },

  logoMark: {
    width: 40,
    height: 40,
    borderRadius: HeritageRadius.md,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: HeritageColors.surfaceStrong,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  brand: {
    color: HeritageColors.ivory,
    fontSize: 16,
    fontWeight: "900",
    letterSpacing: 2.2,
  },

  brandCaption: {
    color: HeritageColors.mutedDark,
    fontSize: 7,
    fontWeight: "700",
    letterSpacing: 1.1,
    marginTop: 2,
  },

  profileButton: {
    width: 42,
    height: 42,
    borderRadius: 21,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  greeting: {
    gap: 5,
  },

  greetingSmall: {
    color: HeritageColors.gold,
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 2,
  },

  greetingTitle: {
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.display,
    fontWeight: "800",
    lineHeight: 40,
  },

  greetingSubtitle: {
    color: HeritageColors.muted,
    fontSize: HeritageTypography.body,
    lineHeight: 22,
  },

  searchContainer: {
    minHeight: 54,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    gap: 10,
    borderRadius: HeritageRadius.lg,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  searchInput: {
    flex: 1,
    color: HeritageColors.ivory,
    fontSize: 14,
    paddingVertical: 14,
  },

  heroCard: {
    minHeight: 290,
    overflow: "hidden",
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surfaceStrong,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    position: "relative",
  },

  heroGlow: {
    position: "absolute",
    width: 230,
    height: 230,
    borderRadius: 115,
    right: -90,
    top: -80,
    backgroundColor: "rgba(212, 175, 90, 0.12)",
  },

  heroContent: {
    flex: 1,
    padding: 24,
    justifyContent: "flex-end",
    gap: 13,
  },

  heroBadge: {
    alignSelf: "flex-start",
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: HeritageRadius.pill,
    backgroundColor: HeritageColors.surfaceSoft,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  heroBadgeText: {
    color: HeritageColors.goldLight,
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 1.2,
  },

  heroTitle: {
    color: HeritageColors.ivory,
    fontSize: 29,
    lineHeight: 34,
    fontWeight: "800",
  },

  heroDescription: {
    maxWidth: 330,
    color: HeritageColors.muted,
    fontSize: 13,
    lineHeight: 20,
  },

  heroButton: {
    alignSelf: "flex-start",
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 11,
    borderRadius: HeritageRadius.pill,
    backgroundColor: HeritageColors.goldLight,
  },

  heroButtonText: {
    color: HeritageColors.black,
    fontSize: 12,
    fontWeight: "800",
  },

  sectionHeader: {
    flexDirection: "row",
    alignItems: "flex-end",
    justifyContent: "space-between",
  },

  sectionEyebrow: {
    color: HeritageColors.gold,
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 1.5,
    marginBottom: 4,
  },

  sectionTitle: {
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.heading,
    fontWeight: "800",
  },

  seeAll: {
    color: HeritageColors.goldLight,
    fontSize: 12,
    fontWeight: "800",
    paddingBottom: 2,
  },

  featuredList: {
    gap: 14,
  },

  featuredCard: {
    width: 265,
    overflow: "hidden",
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  featuredImage: {
    height: 170,
    backgroundColor: HeritageColors.backgroundElevated,
    position: "relative",
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

  imageOverlay: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    height: 70,
    backgroundColor: "rgba(0,0,0,0.20)",
  },

  verified: {
    position: "absolute",
    top: 10,
    left: 10,
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 5,
    borderRadius: HeritageRadius.pill,
    backgroundColor: "rgba(11,9,7,0.78)",
  },

  verifiedText: {
    color: HeritageColors.ivory,
    fontSize: 8,
    fontWeight: "800",
    letterSpacing: 0.8,
  },

  featuredBody: {
    padding: 14,
    gap: 6,
  },

  featuredTitle: {
    color: HeritageColors.ivory,
    fontSize: 17,
    fontWeight: "800",
    lineHeight: 21,
  },

  locationRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
  },

  location: {
    flex: 1,
    color: HeritageColors.muted,
    fontSize: 11,
  },

  category: {
    color: HeritageColors.gold,
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 1,
    textTransform: "uppercase",
  },

  loading: {
    minHeight: 180,
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },

  loadingText: {
    color: HeritageColors.muted,
    fontSize: 12,
  },

  errorCard: {
    minHeight: 120,
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    padding: 20,
    borderRadius: HeritageRadius.lg,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: "rgba(184,107,99,0.30)",
  },

  errorText: {
    color: HeritageColors.danger,
    textAlign: "center",
    fontSize: 12,
  },

  actionsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 12,
  },

  actionCard: {
    width: "47.5%",
    minHeight: 180,
    padding: 16,
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  actionCardLarge: {
    width: "100%",
    minHeight: 150,
    flexDirection: "row",
    alignItems: "center",
    gap: 14,
  },

  actionIcon: {
    width: 48,
    height: 48,
    borderRadius: HeritageRadius.md,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
  },

  scannerIcon: {
    backgroundColor: "rgba(212,175,90,0.12)",
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  aiIcon: {
    backgroundColor: "rgba(197,140,255,0.10)",
    borderWidth: 1,
    borderColor: "rgba(197,140,255,0.22)",
  },

  exploreIcon: {
    backgroundColor: "rgba(240,207,122,0.09)",
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  actionTextBlock: {
    flex: 1,
  },

  actionLabel: {
    color: HeritageColors.gold,
    fontSize: 9,
    fontWeight: "900",
    letterSpacing: 1.3,
    marginBottom: 5,
  },

  actionTitle: {
    color: HeritageColors.ivory,
    fontSize: 19,
    fontWeight: "800",
    marginBottom: 5,
  },

  actionTitleSmall: {
    color: HeritageColors.ivory,
    fontSize: 16,
    fontWeight: "800",
    marginBottom: 6,
  },

  actionDescription: {
    color: HeritageColors.muted,
    fontSize: 11,
    lineHeight: 17,
  },

  emptyRecent: {
    flexDirection: "row",
    alignItems: "center",
    gap: 14,
    padding: 17,
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  emptyRecentIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(212,175,90,0.10)",
  },

  emptyRecentContent: {
    flex: 1,
    gap: 4,
  },

  emptyRecentTitle: {
    color: HeritageColors.ivory,
    fontSize: 14,
    fontWeight: "800",
  },

  emptyRecentText: {
    color: HeritageColors.muted,
    fontSize: 11,
    lineHeight: 17,
  },

  bottomSpacer: {
    height: 10,
  },
});
