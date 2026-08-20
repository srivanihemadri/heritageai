import {
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

import {
  HeritageColors,
  HeritageRadius,
  HeritageSpacing,
  HeritageTypography,
} from "@/constants/theme";
import { useAuthStore } from "@/store/auth-store";

export default function ProfileScreen() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  const displayName =
    user?.full_name?.trim() || "HeritageAI User";

  const email = user?.email?.trim() || "No email available";

  const initial =
    displayName.charAt(0).toUpperCase() || "H";

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >
        <View style={styles.header}>
          <View>
            <Text style={styles.eyebrow}>
              HERITAGEAI
            </Text>

            <Text style={styles.title}>
              Profile
            </Text>

            <Text style={styles.subtitle}>
              Your HeritageAI identity
            </Text>
          </View>

          <View style={styles.headerIcon}>
            <Ionicons
              name="person-outline"
              size={20}
              color={HeritageColors.goldLight}
            />
          </View>
        </View>

        <View style={styles.profileCard}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {initial}
            </Text>
          </View>

          <Text style={styles.name}>
            {displayName}
          </Text>

          <Text style={styles.email}>
            {email}
          </Text>

          <View style={styles.roleBadge}>
            <View style={styles.roleDot} />

            <Text style={styles.roleText}>
              HERITAGE EXPLORER
            </Text>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionLabel}>
            YOUR IDENTITY
          </Text>

          <View style={styles.identityCard}>
            <View style={styles.identityIcon}>
              <Ionicons
                name="sparkles-outline"
                size={20}
                color={HeritageColors.goldLight}
              />
            </View>

            <View style={styles.identityCopy}>
              <Text style={styles.identityTitle}>
                Explore India's heritage
              </Text>

              <Text style={styles.identityDescription}>
                Discover monuments, history, architecture,
                culture, and the stories behind the places
                you explore.
              </Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionLabel}>
            ACCOUNT
          </Text>

          <View style={styles.infoCard}>
            <View style={styles.infoRow}>
              <View style={styles.infoIcon}>
                <Ionicons
                  name="person-outline"
                  size={18}
                  color={HeritageColors.goldLight}
                />
              </View>

              <View style={styles.infoCopy}>
                <Text style={styles.infoLabel}>
                  NAME
                </Text>

                <Text
                  style={styles.infoValue}
                  numberOfLines={1}
                >
                  {displayName}
                </Text>
              </View>
            </View>

            <View style={styles.rowDivider} />

            <View style={styles.infoRow}>
              <View style={styles.infoIcon}>
                <Ionicons
                  name="mail-outline"
                  size={18}
                  color={HeritageColors.goldLight}
                />
              </View>

              <View style={styles.infoCopy}>
                <Text style={styles.infoLabel}>
                  EMAIL
                </Text>

                <Text
                  style={styles.infoValue}
                  numberOfLines={1}
                >
                  {email}
                </Text>
              </View>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionLabel}>
            SESSION
          </Text>

          <Pressable
            onPress={() => {
              void logout();
            }}
            style={({ pressed }) => [
              styles.logoutButton,
              pressed && styles.logoutPressed,
            ]}
          >
            <View style={styles.logoutIcon}>
              <Ionicons
                name="log-out-outline"
                size={20}
                color={HeritageColors.danger}
              />
            </View>

            <Text style={styles.logoutText}>
              Sign out
            </Text>

            <Ionicons
              name="chevron-forward"
              size={18}
              color={HeritageColors.mutedDark}
            />
          </Pressable>
        </View>

        <Text style={styles.footer}>
          HeritageAI · Discover. Understand. Preserve.
        </Text>
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
    paddingHorizontal: HeritageSpacing.xl,
    paddingTop: HeritageSpacing.lg,
    paddingBottom: 110,
  },

  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 26,
  },

  eyebrow: {
    color: HeritageColors.goldLight,
    fontSize: HeritageTypography.caption,
    fontWeight: "900",
    letterSpacing: 2.2,
  },

  title: {
    marginTop: 5,
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.display,
    lineHeight: 40,
    fontWeight: "900",
    letterSpacing: -1,
  },

  subtitle: {
    marginTop: 4,
    color: HeritageColors.muted,
    fontSize: HeritageTypography.body,
  },

  headerIcon: {
    width: 46,
    height: 46,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: HeritageRadius.md,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: HeritageColors.surfaceSoft,
  },

  profileCard: {
    alignItems: "center",
    paddingHorizontal: HeritageSpacing.xl,
    paddingVertical: 28,
    borderRadius: HeritageRadius.glass,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: HeritageColors.surface,
  },

  avatar: {
    width: 78,
    height: 78,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 39,
    borderWidth: 1,
    borderColor: HeritageColors.gold,
    backgroundColor: "rgba(212,175,90,0.12)",
  },

  avatarText: {
    color: HeritageColors.goldLight,
    fontSize: 30,
    fontWeight: "900",
  },

  name: {
    maxWidth: "90%",
    marginTop: 16,
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.heading,
    fontWeight: "900",
    textAlign: "center",
  },

  email: {
    maxWidth: "90%",
    marginTop: 5,
    color: HeritageColors.muted,
    fontSize: HeritageTypography.small,
    textAlign: "center",
  },

  roleBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 7,
    marginTop: 14,
    paddingHorizontal: 11,
    paddingVertical: 7,
    borderRadius: HeritageRadius.pill,
    borderWidth: 1,
    borderColor: HeritageColors.border,
    backgroundColor: HeritageColors.surfaceSoft,
  },

  roleDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: HeritageColors.goldLight,
  },

  roleText: {
    color: HeritageColors.goldLight,
    fontSize: 9,
    fontWeight: "900",
    letterSpacing: 1.3,
  },

  section: {
    marginTop: HeritageSpacing.section,
  },

  sectionLabel: {
    marginBottom: 10,
    color: HeritageColors.mutedDark,
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 1.8,
  },

  identityCard: {
    flexDirection: "row",
    padding: HeritageSpacing.lg,
    borderRadius: HeritageRadius.lg,
    borderWidth: 1,
    borderColor: HeritageColors.border,
    backgroundColor: HeritageColors.surfaceSoft,
  },

  identityIcon: {
    width: 42,
    height: 42,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
    borderRadius: HeritageRadius.md,
    backgroundColor: "rgba(212,175,90,0.10)",
  },

  identityCopy: {
    flex: 1,
  },

  identityTitle: {
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.body,
    fontWeight: "800",
  },

  identityDescription: {
    marginTop: 5,
    color: HeritageColors.muted,
    fontSize: HeritageTypography.small,
    lineHeight: 19,
  },

  infoCard: {
    overflow: "hidden",
    borderRadius: HeritageRadius.lg,
    borderWidth: 1,
    borderColor: HeritageColors.border,
    backgroundColor: HeritageColors.surfaceSoft,
  },

  infoRow: {
    minHeight: 70,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: HeritageSpacing.lg,
  },

  infoIcon: {
    width: 40,
    height: 40,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
    borderRadius: HeritageRadius.md,
    backgroundColor: "rgba(212,175,90,0.08)",
  },

  infoCopy: {
    flex: 1,
  },

  infoLabel: {
    color: HeritageColors.mutedDark,
    fontSize: 9,
    fontWeight: "900",
    letterSpacing: 1.4,
  },

  infoValue: {
    marginTop: 4,
    color: HeritageColors.ivory,
    fontSize: HeritageTypography.small,
    fontWeight: "700",
  },

  rowDivider: {
    height: 1,
    marginLeft: 68,
    backgroundColor: HeritageColors.border,
  },

  logoutButton: {
    minHeight: 58,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: HeritageSpacing.lg,
    borderRadius: HeritageRadius.lg,
    borderWidth: 1,
    borderColor: "rgba(184,107,99,0.28)",
    backgroundColor: "rgba(184,107,99,0.055)",
  },

  logoutPressed: {
    opacity: 0.7,
    transform: [{ scale: 0.985 }],
  },

  logoutIcon: {
    width: 38,
    height: 38,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
    borderRadius: HeritageRadius.md,
    backgroundColor: "rgba(184,107,99,0.08)",
  },

  logoutText: {
    flex: 1,
    color: HeritageColors.danger,
    fontSize: HeritageTypography.body,
    fontWeight: "800",
  },

  footer: {
    marginTop: 32,
    color: HeritageColors.mutedDark,
    fontSize: 10,
    fontWeight: "700",
    letterSpacing: 0.8,
    textAlign: "center",
  },
});
