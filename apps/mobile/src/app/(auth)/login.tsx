import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { SafeAreaView } from "react-native-safe-area-context";
import { GoogleSignin, statusCodes } from "@react-native-google-signin/google-signin";

import { useAuthStore } from "@/store/auth-store";
import {
  HeritageColors,
  HeritageRadius,
} from "@/constants/theme";
import { env } from "@/config/env";



export default function LoginScreen() {
  const login = useAuthStore((state) => state.login);
  const loginWithGoogle = useAuthStore(
    (state) => state.loginWithGoogle,
  );

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit =
    email.trim().length > 0 && password.length > 0;


  const handleLogin = async () => {
    if (!canSubmit || isSubmitting) {
      return;
    }

    setError(null);
    setIsSubmitting(true);

    try {
      await login({
        email: email.trim(),
        password,
      });
    } catch {
      setError(
        "Unable to sign in. Check your credentials and try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGoogleLogin = async () => {
    if (isSubmitting) {
      return;
    }

    setError(null);
    setIsSubmitting(true);

    try {
      console.log("[GOOGLE AUTH] STARTING NATIVE GOOGLE LOGIN");

      await GoogleSignin.hasPlayServices({
        showPlayServicesUpdateDialog: true,
      });

      await GoogleSignin.configure({
        webClientId: env.googleWebClientId,
        offlineAccess: false,
      });

      const result = await GoogleSignin.signIn();

      console.log(
        "[GOOGLE AUTH] SIGN-IN RESULT RECEIVED",
      );

      if (result.type !== "success") {
        console.log(
          "[GOOGLE AUTH] SIGN-IN CANCELLED",
        );
        return;
      }

      const idToken = result.data?.idToken;

      console.log(
        "[GOOGLE AUTH] ID TOKEN:",
        idToken ? "RECEIVED" : "MISSING",
      );

      if (!idToken) {
        throw new Error(
          "Google did not return a valid identity token.",
        );
      }

      await loginWithGoogle(idToken);

      console.log(
        "[GOOGLE AUTH] BACKEND LOGIN SUCCESS",
      );
    } catch (googleError: any) {
      console.error(
        "[AUTH TRACE] Native Google authentication failed",
        googleError,
      );

      if (
        googleError?.code === statusCodes.SIGN_IN_CANCELLED
      ) {
        console.log(
          "[GOOGLE AUTH] USER CANCELLED SIGN-IN",
        );
        return;
      }

      if (
        googleError?.code === statusCodes.IN_PROGRESS
      ) {
        setError(
          "Google sign-in is already in progress.",
        );
        return;
      }

      if (
        googleError?.code === statusCodes.PLAY_SERVICES_NOT_AVAILABLE
      ) {
        setError(
          "Google Play Services is not available or needs an update.",
        );
        return;
      }

      setError(
        "Google sign-in failed. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.backgroundGlowTop} />
          <View style={styles.backgroundGlowBottom} />

          <View style={styles.content}>
            <View style={styles.brand}>
              <Text style={styles.brandText}>HERITAGEAI</Text>

              <View style={styles.brandDivider}>
                <View style={styles.dividerLine} />

                <Ionicons
                  name="sparkles"
                  size={13}
                  color={HeritageColors.goldLight}
                />

                <View style={styles.dividerLine} />
              </View>

              <Text style={styles.brandSubtitle}>
                CULTURAL HERITAGE INTELLIGENCE
              </Text>
            </View>

            <View style={styles.card}>
              <View style={styles.cardGlow} />

              <View style={styles.cardContent}>
                <Text style={styles.title}>Welcome back</Text>

                <Text style={styles.subtitle}>
                  Sign in securely to continue your HeritageAI
                  journey.
                </Text>

                <View style={styles.form}>
                  <View style={styles.field}>
                    <Text style={styles.label}>EMAIL</Text>

                    <View style={styles.inputContainer}>
                      <Ionicons
                        name="mail-outline"
                        size={18}
                        color={HeritageColors.muted}
                      />

                      <TextInput
                        autoCapitalize="none"
                        autoCorrect={false}
                        keyboardType="email-address"
                        autoComplete="email"
                        textContentType="emailAddress"
                        placeholder="Enter your email"
                        placeholderTextColor={
                          HeritageColors.mutedDark
                        }
                        value={email}
                        onChangeText={(value) => {
                          setEmail(value);

                          if (error) {
                            setError(null);
                          }
                        }}
                        style={styles.input}
                        editable={!isSubmitting}
                        returnKeyType="next"
                      />
                    </View>
                  </View>

                  <View style={styles.field}>
                    <Text style={styles.label}>PASSWORD</Text>

                    <View style={styles.inputContainer}>
                      <Ionicons
                        name="lock-closed-outline"
                        size={18}
                        color={HeritageColors.muted}
                      />

                      <TextInput
                        autoCapitalize="none"
                        autoCorrect={false}
                        autoComplete="password"
                        textContentType="password"
                        placeholder="Enter your password"
                        placeholderTextColor={
                          HeritageColors.mutedDark
                        }
                        value={password}
                        onChangeText={(value) => {
                          setPassword(value);

                          if (error) {
                            setError(null);
                          }
                        }}
                        secureTextEntry={!isPasswordVisible}
                        style={styles.input}
                        editable={!isSubmitting}
                        returnKeyType="done"
                        onSubmitEditing={handleLogin}
                      />

                      <Pressable
                        accessibilityRole="button"
                        accessibilityLabel={
                          isPasswordVisible
                            ? "Hide password"
                            : "Show password"
                        }
                        hitSlop={10}
                        onPress={() =>
                          setIsPasswordVisible(
                            (visible) => !visible,
                          )
                        }
                      >
                        <Ionicons
                          name={
                            isPasswordVisible
                              ? "eye-off-outline"
                              : "eye-outline"
                          }
                          size={19}
                          color={HeritageColors.muted}
                        />
                      </Pressable>
                    </View>
                  </View>

                  {error ? (
                    <View style={styles.errorContainer}>
                      <Ionicons
                        name="alert-circle-outline"
                        size={17}
                        color="#FCA5A5"
                      />

                      <Text style={styles.errorText}>
                        {error}
                      </Text>
                    </View>
                  ) : null}

                  <Pressable
                    accessibilityRole="button"
                    accessibilityState={{
                      disabled:
                        !canSubmit || isSubmitting,
                    }}
                    disabled={!canSubmit || isSubmitting}
                    onPress={handleLogin}
                    style={({ pressed }) => [
                      styles.signInButton,
                      !canSubmit || isSubmitting
                        ? styles.signInButtonDisabled
                        : null,
                      pressed && canSubmit
                        ? styles.signInButtonPressed
                        : null,
                    ]}
                  >
                    {isSubmitting ? (
                      <ActivityIndicator
                        size="small"
                        color={HeritageColors.black}
                      />
                    ) : (
                      <>
                        <Text style={styles.signInButtonText}>
                          SIGN IN
                        </Text>

                        <Ionicons
                          name="arrow-forward"
                          size={18}
                          color={HeritageColors.black}
                        />
                      </>
                    )}
                  </Pressable>

                  <View style={styles.orRow}>
                    <View style={styles.orLine} />
                    <Text style={styles.orText}>OR</Text>
                    <View style={styles.orLine} />
                  </View>

                  <Pressable
                    accessibilityRole="button"
                    accessibilityState={{
                      disabled:
                        isSubmitting,
                    }}
                    disabled={isSubmitting}
                    onPress={handleGoogleLogin}
                    style={({ pressed }) => [
                      styles.googleButton,
                      pressed
                        ? styles.googleButtonPressed
                        : null,
                    ]}
                  >
                    {isSubmitting ? (
                      <ActivityIndicator
                        size="small"
                        color={HeritageColors.ivory}
                      />
                    ) : (
                      <>
                        <View style={styles.googleMark}>
                          <Text style={styles.googleMarkText}>
                            G
                          </Text>
                        </View>

                        <Text style={styles.googleButtonText}>
                          Continue with Google
                        </Text>
                      </>
                    )}
                  </Pressable>
                </View>

                <Text style={styles.legalText}>
                  By continuing, you agree to use Google or your
                  HeritageAI credentials to authenticate your
                  account.
                </Text>
              </View>
            </View>

            <View style={styles.footer}>
              <Ionicons
                name="sparkles-outline"
                size={13}
                color={HeritageColors.mutedDark}
              />

              <Text style={styles.footerText}>
                DISCOVER Ãƒâ€šÃ‚Â· UNDERSTAND Ãƒâ€šÃ‚Â· PRESERVE
              </Text>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: HeritageColors.black,
  },

  flex: {
    flex: 1,
  },

  scrollContent: {
    flexGrow: 1,
    justifyContent: "center",
    paddingHorizontal: 20,
    paddingVertical: 28,
  },

  content: {
    width: "100%",
    maxWidth: 520,
    alignSelf: "center",
  },

  backgroundGlowTop: {
    position: "absolute",
    width: 280,
    height: 280,
    borderRadius: 140,
    backgroundColor: "rgba(212, 175, 90, 0.055)",
    top: -100,
    right: -110,
  },

  backgroundGlowBottom: {
    position: "absolute",
    width: 260,
    height: 260,
    borderRadius: 130,
    backgroundColor: "rgba(155, 117, 48, 0.045)",
    bottom: -90,
    left: -100,
  },

  brand: {
    alignItems: "center",
    marginBottom: 22,
  },

  brandText: {
    color: HeritageColors.ivory,
    fontSize: 14,
    fontWeight: "800",
    letterSpacing: 4.5,
  },

  brandDivider: {
    flexDirection: "row",
    alignItems: "center",
    gap: 9,
    marginTop: 10,
  },

  dividerLine: {
    width: 34,
    height: 1,
    backgroundColor: HeritageColors.borderStrong,
  },

  brandSubtitle: {
    marginTop: 8,
    color: HeritageColors.mutedDark,
    fontSize: 8,
    fontWeight: "700",
    letterSpacing: 2,
  },

  card: {
    position: "relative",
    overflow: "hidden",
    borderRadius: 30,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: "rgba(255, 255, 255, 0.045)",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 20,
    },
    shadowOpacity: 0.35,
    shadowRadius: 35,
    elevation: 12,
  },

  cardGlow: {
    position: "absolute",
    width: 220,
    height: 220,
    borderRadius: 110,
    backgroundColor: "rgba(212, 175, 90, 0.055)",
    top: -110,
    right: -100,
  },

  cardContent: {
    padding: 25,
  },

  title: {
    color: HeritageColors.ivory,
    fontSize: 30,
    fontWeight: "700",
    letterSpacing: -0.8,
  },

  subtitle: {
    marginTop: 9,
    color: HeritageColors.muted,
    fontSize: 14,
    lineHeight: 21,
  },

  form: {
    marginTop: 26,
    gap: 17,
  },

  field: {
    gap: 8,
  },

  label: {
    color: HeritageColors.goldLight,
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 1.8,
  },

  inputContainer: {
    minHeight: 52,
    flexDirection: "row",
    alignItems: "center",
    gap: 11,
    borderWidth: 1,
    borderColor: HeritageColors.border,
    borderRadius: HeritageRadius.lg,
    backgroundColor: "rgba(255, 255, 255, 0.025)",
    paddingHorizontal: 15,
  },

  input: {
    flex: 1,
    minHeight: 50,
    color: HeritageColors.ivory,
    fontSize: 15,
    paddingVertical: 0,
  },

  errorContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    borderWidth: 1,
    borderColor: "rgba(239, 68, 68, 0.22)",
    borderRadius: 13,
    backgroundColor: "rgba(239, 68, 68, 0.07)",
    paddingHorizontal: 12,
    paddingVertical: 10,
  },

  errorText: {
    flex: 1,
    color: "#FCA5A5",
    fontSize: 12,
    lineHeight: 18,
  },

  signInButton: {
    minHeight: 52,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 9,
    borderRadius: HeritageRadius.lg,
    backgroundColor: HeritageColors.gold,
    shadowColor: HeritageColors.gold,
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.16,
    shadowRadius: 16,
    elevation: 5,
  },

  signInButtonDisabled: {
    opacity: 0.42,
    shadowOpacity: 0,
    elevation: 0,
  },

  signInButtonPressed: {
    transform: [{ scale: 0.985 }],
    opacity: 0.9,
  },

  signInButtonText: {
    color: HeritageColors.black,
    fontSize: 12,
    fontWeight: "900",
    letterSpacing: 1.5,
  },

  orRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },

  orLine: {
    flex: 1,
    height: 1,
    backgroundColor: HeritageColors.border,
  },

  orText: {
    color: HeritageColors.mutedDark,
    fontSize: 9,
    fontWeight: "700",
    letterSpacing: 1.5,
  },

  googleButton: {
    minHeight: 52,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    borderRadius: HeritageRadius.lg,
    backgroundColor: "rgba(255, 255, 255, 0.035)",
  },

  googleButtonPressed: {
    backgroundColor: "rgba(255, 255, 255, 0.07)",
  },

  googleMark: {
    width: 25,
    height: 25,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 13,
    backgroundColor: HeritageColors.ivory,
  },

  googleMarkText: {
    color: "#4285F4",
    fontSize: 14,
    fontWeight: "900",
  },

  googleButtonText: {
    color: HeritageColors.ivory,
    fontSize: 14,
    fontWeight: "600",
  },

  legalText: {
    marginTop: 22,
    color: HeritageColors.mutedDark,
    fontSize: 10,
    lineHeight: 16,
    textAlign: "center",
  },

  footer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 7,
    marginTop: 20,
  },

  footerText: {
    color: HeritageColors.mutedDark,
    fontSize: 8,
    fontWeight: "700",
    letterSpacing: 1.4,
  },
});





