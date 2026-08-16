import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

import {
  HeritageColors,
  HeritageRadius,
  HeritageSpacing,
  HeritageTypography,
} from "@/constants/theme";

type AIFeature = {
  icon: keyof typeof Ionicons.glyphMap;
  eyebrow: string;
  title: string;
  description: string;
  route: string;
};

const features: AIFeature[] = [
  {
    icon: "scan-outline",
    eyebrow: "DISCOVER",
    title: "AI Heritage Scanner",
    description:
      "Scan a monument and let HeritageAI uncover its history, significance, architecture, and context.",
    route: "/(app)/ai-scanner",
  },
  {
    icon: "mic-outline",
    eyebrow: "CONVERSE",
    title: "AI Voice Guide",
    description:
      "Ask questions naturally with your voice and explore heritage through an intelligent guide.",
    route: "/(app)/ai-guide",
  },
  {
    icon: "sparkles-outline",
    eyebrow: "RESTORE",
    title: "Image Enhancement",
    description:
      "Improve the quality of low-resolution heritage photographs while preserving their visual character.",
    route: "/(app)/ai-enhance",
  },
];

export default function AIScreen() {
  const router = useRouter();

  return (
    <View style={styles.screen}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >
        <View style={styles.header}>
          <View style={styles.aiBadge}>
            <Ionicons
              name="sparkles"
              size={16}
              color={HeritageColors.goldLight}
            />
            <Text style={styles.aiBadgeText}>HERITAGE INTELLIGENCE</Text>
          </View>

          <Text style={styles.title}>
            Explore heritage{"\n"}
            with AI.
          </Text>

          <Text style={styles.subtitle}>
            Three intelligent experiences designed to help you
            discover, understand, and preserve cultural heritage.
          </Text>
        </View>

        <View style={styles.featureList}>
          {features.map((feature, index) => (
            <Pressable
              key={feature.title}
              style={({ pressed }) => [
                styles.featureCard,
                pressed && styles.featureCardPressed,
              ]}
              onPress={() => router.push(feature.route as never)}
            >
              <View style={styles.cardTop}>
                <View style={styles.iconContainer}>
                  <Ionicons
                    name={feature.icon}
                    size={25}
                    color={HeritageColors.goldLight}
                  />
                </View>

                <Text style={styles.index}>
                  0{index + 1}
                </Text>
              </View>

              <Text style={styles.eyebrow}>
                {feature.eyebrow}
              </Text>

              <Text style={styles.featureTitle}>
                {feature.title}
              </Text>

              <Text style={styles.featureDescription}>
                {feature.description}
              </Text>

              <View style={styles.actionRow}>
                <Text style={styles.actionText}>
                  Open experience
                </Text>

                <Ionicons
                  name="arrow-forward"
                  size={17}
                  color={HeritageColors.gold}
                />
              </View>
            </Pressable>
          ))}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: HeritageColors.background,
  },

  content: {
    paddingHorizontal: HeritageSpacing.xl,
    paddingTop: 30,
    paddingBottom: 130,
  },

  header: {
    marginBottom: HeritageSpacing.xxxl,
  },

  aiBadge: {
    alignSelf: "flex-start",
    flexDirection: "row",
    alignItems: "center",
    gap: 7,
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: HeritageRadius.pill,
    backgroundColor: HeritageColors.surfaceSoft,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  aiBadgeText: {
    color: HeritageColors.goldLight,
    fontSize: HeritageTypography.caption,
    fontWeight: "800",
    letterSpacing: 1.5,
  },

  title: {
    marginTop: 20,
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.display,
    lineHeight: 40,
    fontWeight: "800",
    letterSpacing: -1,
  },

  subtitle: {
    marginTop: 14,
    maxWidth: 360,
    color: HeritageColors.muted,
    fontSize: HeritageTypography.body,
    lineHeight: 23,
  },

  featureList: {
    gap: HeritageSpacing.lg,
  },

  featureCard: {
    padding: HeritageSpacing.xxl,
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 16,
    },
    shadowOpacity: 0.24,
    shadowRadius: 30,
    elevation: 8,
  },

  featureCardPressed: {
    backgroundColor: HeritageColors.surfaceStrong,
    borderColor: HeritageColors.borderStrong,
    transform: [{ scale: 0.985 }],
  },

  cardTop: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  iconContainer: {
    width: 52,
    height: 52,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 17,
    backgroundColor: HeritageColors.surfaceSoft,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  index: {
    color: HeritageColors.mutedDark,
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 1,
  },

  eyebrow: {
    marginTop: 24,
    color: HeritageColors.gold,
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 2,
  },

  featureTitle: {
    marginTop: 7,
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.heading,
    fontWeight: "800",
  },

  featureDescription: {
    marginTop: 8,
    color: HeritageColors.muted,
    fontSize: HeritageTypography.body,
    lineHeight: 22,
  },

  actionRow: {
    marginTop: 22,
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },

  actionText: {
    color: HeritageColors.goldLight,
    fontSize: 13,
    fontWeight: "700",
  },
});
