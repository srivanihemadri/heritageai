import { Ionicons } from "@expo/vector-icons";
import * as ImageManipulator from "expo-image-manipulator";
import * as ImagePicker from "expo-image-picker";
import { useRouter } from "expo-router";
import { useState } from "react";
import {
  ActivityIndicator,
  Image,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

import apiClient from "@/lib/api-client";
import {
  HeritageColors,
  HeritageRadius,
  HeritageSpacing,
  HeritageTypography,
} from "@/constants/theme";

type IdentificationStatus =
  | "IDENTIFIED"
  | "POSSIBLE_MATCH"
  | "INSUFFICIENT_EVIDENCE"
  | "NOT_HERITAGE"
  | "AMBIGUOUS";

type ConfidenceLevel = "LOW" | "MEDIUM" | "HIGH";

type HeritageScanResult = {
  scan_id?: string;
  identified_name?: string | null;
  identification_status?: IdentificationStatus;
  evidence_quality?: string;
  category?: string | null;
  location?: string | null;
  country?: string | null;
  confidence?: number | null;
  confidence_level?: ConfidenceLevel | null;
  description?: string | null;
  architectural_style?: string | null;
  historical_period?: string | null;
  historical_significance?: string | null;
  visual_evidence?: string[];
  alternative_matches?: string[];
  grounding_status?: string | null;
};

type SelectedImage = {
  uri: string;
  name: string;
  type: string;
};

function getStatusLabel(status?: IdentificationStatus) {
  switch (status) {
    case "IDENTIFIED":
      return "IDENTIFIED";
    case "POSSIBLE_MATCH":
      return "POSSIBLE MATCH";
    case "INSUFFICIENT_EVIDENCE":
      return "INSUFFICIENT EVIDENCE";
    case "NOT_HERITAGE":
      return "NOT HERITAGE";
    case "AMBIGUOUS":
      return "AMBIGUOUS";
    default:
      return "ANALYZED";
  }
}

function getStatusIcon(
  status?: IdentificationStatus,
): keyof typeof Ionicons.glyphMap {
  switch (status) {
    case "IDENTIFIED":
      return "checkmark-circle";
    case "POSSIBLE_MATCH":
    case "AMBIGUOUS":
      return "help-circle";
    case "INSUFFICIENT_EVIDENCE":
      return "information-circle";
    case "NOT_HERITAGE":
      return "close-circle";
    default:
      return "sparkles";
  }
}

function getFileType(uri: string) {
  const extension = uri.split(".").pop()?.toLowerCase();

  if (extension === "png") {
    return "image/png";
  }

  if (extension === "webp") {
    return "image/webp";
  }

  return "image/jpeg";
}

function getFileName(uri: string) {
  const cleanUri = uri.split("?")[0];
  const value = cleanUri.split("/").pop();

  return value || `heritage-scan-${Date.now()}.jpg`;
}

export default function AIHeritageScanner() {
  const router = useRouter();

  const [selectedImage, setSelectedImage] =
    useState<SelectedImage | null>(null);

  const [result, setResult] =
    useState<HeritageScanResult | null>(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState("");

  async function selectFromGallery() {
    setError("");

    const permission =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permission.granted) {
      setError(
        "Photo library permission is required to choose a heritage image.",
      );
      return;
    }

    const response =
      await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ["images"],
        allowsEditing: false,
        quality: 1,
      });

    if (response.canceled || !response.assets.length) {
      return;
    }

    const asset = response.assets[0];

    setSelectedImage({
      uri: asset.uri,
      name: asset.fileName || getFileName(asset.uri),
      type: asset.mimeType || getFileType(asset.uri),
    });

    setResult(null);
  }

  async function captureImage() {
    setError("");

    const permission =
      await ImagePicker.requestCameraPermissionsAsync();

    if (!permission.granted) {
      setError(
        "Camera permission is required to scan a monument.",
      );
      return;
    }

    const response =
      await ImagePicker.launchCameraAsync({
        mediaTypes: ["images"],
        allowsEditing: false,
        quality: 1,
      });

    if (response.canceled || !response.assets.length) {
      return;
    }

    const asset = response.assets[0];

    setSelectedImage({
      uri: asset.uri,
      name: asset.fileName || `heritage-scan-${Date.now()}.jpg`,
      type: asset.mimeType || "image/jpeg",
    });

    setResult(null);
  }

  async function analyzeHeritage() {
    if (!selectedImage || isAnalyzing) {
      return;
    }

    setIsAnalyzing(true);
    setError("");
    setResult(null);

    try {
      const normalizedImage =
        await ImageManipulator.manipulateAsync(
          selectedImage.uri,
          [],
          {
            compress: 0.9,
            format: ImageManipulator.SaveFormat.JPEG,
          },
        );

      console.log(
        "[SCANNER TRACE] normalized image:",
        JSON.stringify({
          uri: normalizedImage.uri,
          width: normalizedImage.width,
          height: normalizedImage.height,
          format: "image/jpeg",
        }),
      );

      const formData = new FormData();

      if (Platform.OS === "web") {
        const imageResponse = await fetch(
          normalizedImage.uri,
        );

        if (!imageResponse.ok) {
          throw new Error(
            "Unable to read the normalized image.",
          );
        }

        const imageBlob = await imageResponse.blob();

        console.log(
          "[SCANNER TRACE] normalized web image:",
          JSON.stringify({
            blobType: imageBlob.type,
            blobSize: imageBlob.size,
          }),
        );

        formData.append(
          "file",
          imageBlob,
          "heritage-scan.jpg",
        );
      } else {
        formData.append(
          "file",
          {
            uri: normalizedImage.uri,
            name: "heritage-scan.jpg",
            type: "image/jpeg",
          } as unknown as Blob,
        );
      }

      const response =
        await apiClient.post<{
          success: boolean;
          scan_id: string;
          result: HeritageScanResult;
        }>(
          "/ai/scan",
          formData,
          {
            timeout: 60000,
          },
        );

      console.log(
        "[SCANNER TRACE] API result received:",
        JSON.stringify(response.data),
      );

      setResult(response.data.result);
    } catch (requestError: any) {
      const detail = requestError?.response?.data?.detail;

      const message =
        typeof detail === "string"
          ? detail
          : detail?.message ||
            requestError?.response?.data?.message ||
            requestError?.message ||
            "Heritage analysis failed. Please try again.";

      console.error("[SCANNER TRACE] analysis failed:", {
        status: requestError?.response?.status,
        detail,
        message,
      });

      setError(message);
    } finally {
      setIsAnalyzing(false);
    }
  }

  function resetScanner() {
    setSelectedImage(null);
    setResult(null);
    setError("");
  }

  return (
    <View style={styles.screen}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >
        <View style={styles.header}>
          <View style={styles.headerTopRow}>
            <Pressable
              onPress={() => router.back()}
              style={({ pressed }) => [
                styles.backButton,
                pressed && styles.headerButtonPressed,
              ]}
              accessibilityLabel="Go back"
            >
              <Ionicons
                name="arrow-back"
                size={22}
                color={HeritageColors.ivory}
              />
            </Pressable>

            <View style={styles.brandLockup}>
              <Text style={styles.brandText}>
                HeritageAI
              </Text>

              <View style={styles.brandDivider} />
            </View>

            <Pressable
              onPress={captureImage}
              style={({ pressed }) => [
                styles.cameraHeaderButton,
                pressed && styles.headerButtonPressed,
              ]}
              accessibilityLabel="Open camera"
            >
              <Ionicons
                name="camera-outline"
                size={21}
                color={HeritageColors.goldLight}
              />
            </Pressable>
          </View>

          <View style={styles.headerText}>
            <Text style={styles.eyebrow}>
              AI HERITAGE INTELLIGENCE
            </Text>

            <Text style={styles.title}>
              Scan a monument.
            </Text>

            <Text style={styles.subtitle}>
              Let HeritageAI identify what you see and uncover
              its historical story.
            </Text>
          </View>
        </View>

        {!selectedImage && (
          <View style={styles.capturePanel}>
            <View style={styles.scanVisual}>
              <View style={styles.scanCornerTopLeft} />
              <View style={styles.scanCornerTopRight} />
              <View style={styles.scanCornerBottomLeft} />
              <View style={styles.scanCornerBottomRight} />

              <View style={styles.scannerIcon}>
                <Ionicons
                  name="scan-outline"
                  size={38}
                  color={HeritageColors.goldLight}
                />
              </View>

              <View style={styles.scanHint}>
                <View style={styles.scanHintDot} />
                <Text style={styles.scanHintText}>
                  READY TO SCAN
                </Text>
              </View>
            </View>

            <Text style={styles.panelTitle}>
              Discover the story behind a place.
            </Text>

            <Text style={styles.panelDescription}>
              Capture a monument or choose an existing photograph.
              HeritageAI will analyze the visual evidence and
              return a structured heritage interpretation.
            </Text>

            <View style={styles.actionGroup}>
              <Pressable
                style={({ pressed }) => [
                  styles.primaryButton,
                  pressed && styles.buttonPressed,
                ]}
                onPress={captureImage}
              >
                <Ionicons
                  name="camera-outline"
                  size={20}
                  color={HeritageColors.black}
                />
                <Text style={styles.primaryButtonText}>
                  Open Camera
                </Text>
              </Pressable>

              <Pressable
                style={({ pressed }) => [
                  styles.secondaryButton,
                  pressed && styles.buttonPressed,
                ]}
                onPress={selectFromGallery}
              >
                <Ionicons
                  name="images-outline"
                  size={20}
                  color={HeritageColors.goldLight}
                />
                <Text style={styles.secondaryButtonText}>
                  Choose Image
                </Text>
              </Pressable>
            </View>
          </View>
        )}

        {selectedImage && !result && (
          <View style={styles.previewPanel}>
            <View style={styles.imageFrame}>
              <Image
                source={{ uri: selectedImage.uri }}
                style={styles.previewImage}
                resizeMode="cover"
              />
            </View>

            <View style={styles.previewHeader}>
              <View>
                <Text style={styles.eyebrow}>
                  SELECTED IMAGE
                </Text>
                <Text
                  style={styles.fileName}
                  numberOfLines={1}
                >
                  {selectedImage.name}
                </Text>
              </View>

              <Pressable
                onPress={resetScanner}
                style={styles.closeButton}
                accessibilityLabel="Remove selected image"
              >
                <Ionicons
                  name="close"
                  size={19}
                  color={HeritageColors.ivory}
                />
              </Pressable>
            </View>

            {error ? (
              <View style={styles.errorBox}>
                <Ionicons
                  name="alert-circle-outline"
                  size={19}
                  color={HeritageColors.danger}
                />
                <Text style={styles.errorText}>
                  {error}
                </Text>
              </View>
            ) : null}

            <Pressable
              style={({ pressed }) => [
                styles.primaryButton,
                styles.analyzeButton,
                pressed && styles.buttonPressed,
                isAnalyzing && styles.disabledButton,
              ]}
              onPress={analyzeHeritage}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? (
                <>
                  <ActivityIndicator
                    size="small"
                    color={HeritageColors.black}
                  />
                  <Text style={styles.primaryButtonText}>
                    Analyzing Heritage...
                  </Text>
                </>
              ) : (
                <>
                  <Ionicons
                    name="sparkles"
                    size={20}
                    color={HeritageColors.black}
                  />
                  <Text style={styles.primaryButtonText}>
                    Analyze Heritage
                  </Text>
                </>
              )}
            </Pressable>

            <Text style={styles.disclaimer}>
              AI results may be uncertain. HeritageAI will
              communicate confidence and evidence quality rather
              than presenting guesses as facts.
            </Text>
          </View>
        )}

        {result && selectedImage && (
          <View style={styles.resultSection}>
            <View style={styles.resultImageFrame}>
              <Image
                source={{ uri: selectedImage.uri }}
                style={styles.resultImage}
                resizeMode="cover"
              />
            </View>

            <View style={styles.resultCard}>
              <View style={styles.statusRow}>
                <View style={styles.statusBadge}>
                  <Ionicons
                    name={getStatusIcon(
                      result.identification_status,
                    )}
                    size={15}
                    color={HeritageColors.goldLight}
                  />
                  <Text style={styles.statusText}>
                    {getStatusLabel(
                      result.identification_status,
                    )}
                  </Text>
                </View>

                {result.confidence_level ? (
                  <Text style={styles.confidenceLevel}>
                    {result.confidence_level}
                  </Text>
                ) : null}
              </View>

              <Text style={styles.resultTitle}>
                {result.identified_name ||
                  "Heritage site analysis"}
              </Text>

              {result.location || result.country ? (
                <View style={styles.locationRow}>
                  <Ionicons
                    name="location-outline"
                    size={16}
                    color={HeritageColors.gold}
                  />
                  <Text style={styles.locationText}>
                    {[result.location, result.country]
                      .filter(Boolean)
                      .join(" ï¿½ ")}
                  </Text>
                </View>
              ) : null}

              {typeof result.confidence === "number" ? (
                <View style={styles.confidenceBlock}>
                  <View style={styles.confidenceHeader}>
                    <Text style={styles.label}>
                      Confidence
                    </Text>
                    <Text style={styles.confidenceValue}>
                      {Math.round(result.confidence * 100)}%
                    </Text>
                  </View>

                  <View style={styles.confidenceTrack}>
                    <View
                      style={[
                        styles.confidenceFill,
                        {
                          width: `${Math.max(
                            0,
                            Math.min(
                              100,
                              result.confidence * 100,
                            ),
                          )}%`,
                        },
                      ]}
                    />
                  </View>
                </View>
              ) : null}

              <ResultSection
                title="About this place"
                value={result.description}
              />

              <ResultSection
                title="Historical significance"
                value={result.historical_significance}
              />

              <ResultSection
                title="Architecture"
                value={result.architectural_style}
              />

              <ResultSection
                title="Historical period"
                value={result.historical_period}
              />

              {result.visual_evidence?.length ? (
                <View style={styles.resultBlock}>
                  <Text style={styles.label}>
                    Visual evidence
                  </Text>

                  {result.visual_evidence.map(
                    (evidence, index) => (
                      <View
                        key={`${evidence}-${index}`}
                        style={styles.bulletRow}
                      >
                        <View style={styles.bullet} />
                        <Text style={styles.bodyText}>
                          {evidence}
                        </Text>
                      </View>
                    ),
                  )}
                </View>
              ) : null}

              {result.alternative_matches?.length ? (
                <View style={styles.resultBlock}>
                  <Text style={styles.label}>
                    Alternative possibilities
                  </Text>

                  {result.alternative_matches.map(
                    (match, index) => (
                      <View
                        key={`${match}-${index}`}
                        style={styles.bulletRow}
                      >
                        <View style={styles.bullet} />
                        <Text style={styles.bodyText}>
                          {match}
                        </Text>
                      </View>
                    ),
                  )}
                </View>
              ) : null}

              {result.grounding_status ? (
                <View style={styles.groundingBox}>
                  <Ionicons
                    name="shield-checkmark-outline"
                    size={18}
                    color={HeritageColors.success}
                  />

                  <View style={styles.groundingContent}>
                    <Text style={styles.groundingTitle}>
                      Evidence status
                    </Text>
                    <Text style={styles.groundingText}>
                      {result.grounding_status}
                    </Text>
                  </View>
                </View>
              ) : null}
            </View>

            <Pressable
              style={({ pressed }) => [
                styles.secondaryButton,
                pressed && styles.buttonPressed,
              ]}
              onPress={resetScanner}
            >
              <Ionicons
                name="scan-outline"
                size={19}
                color={HeritageColors.goldLight}
              />
              <Text style={styles.secondaryButtonText}>
                Scan Another Monument
              </Text>
            </Pressable>
          </View>
        )}

        {error && !selectedImage ? (
          <View style={styles.errorBox}>
            <Ionicons
              name="alert-circle-outline"
              size={19}
              color={HeritageColors.danger}
            />
            <Text style={styles.errorText}>{error}</Text>
          </View>
        ) : null}
      </ScrollView>
    </View>
  );
}

function ResultSection({
  title,
  value,
}: {
  title: string;
  value?: string | null;
}) {
  if (!value) {
    return null;
  }

  return (
    <View style={styles.resultBlock}>
      <Text style={styles.label}>{title}</Text>
      <Text style={styles.bodyText}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: HeritageColors.background,
  },

  content: {
    paddingHorizontal: 18,
    paddingTop: 22,
    paddingBottom: 130,
  },

  header: {
    marginBottom: 24,
  },

  headerTopRow: {
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 22,
  },

  backButton: {
    width: 48,
    height: 48,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 17,
    backgroundColor: "rgba(255,255,255,0.045)",
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
  },

  cameraHeaderButton: {
    width: 48,
    height: 48,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 17,
    backgroundColor: "rgba(197,140,255,0.10)",
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
  },

  headerButtonPressed: {
    opacity: 0.68,
    transform: [{ scale: 0.94 }],
  },

  brandLockup: {
    alignItems: "center",
    justifyContent: "center",
  },

  brandText: {
    color: HeritageColors.goldLight,
    fontSize: 21,
    fontWeight: "800",
    letterSpacing: -0.3,
  },

  brandDivider: {
    width: 34,
    height: 1,
    marginTop: 6,
    backgroundColor: HeritageColors.gold,
  },

  headerText: {
    alignItems: "flex-start",
  },

  eyebrow: {
    color: HeritageColors.goldLight,
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 2.2,
  },

  title: {
    marginTop: 6,
    color: HeritageColors.ivory,
    fontSize: 31,
    lineHeight: 36,
    fontWeight: "900",
    letterSpacing: -0.9,
  },

  subtitle: {
    marginTop: 8,
    color: HeritageColors.muted,
    fontSize: 15,
    lineHeight: 22,
  },

  capturePanel: {
    paddingHorizontal: 20,
    paddingTop: 26,
    paddingBottom: 20,
    alignItems: "center",
    borderRadius: 28,
    backgroundColor: "rgba(255,255,255,0.045)",
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 12,
    },
    shadowOpacity: 0.22,
    shadowRadius: 24,
    elevation: 8,
  },

  scanVisual: {
    width: "100%",
    height: 178,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 18,
    borderRadius: HeritageRadius.lg,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.10)",
    backgroundColor: "rgba(255,255,255,0.025)",
    overflow: "hidden",
    position: "relative",
  },

  scanCornerTopLeft: {
    position: "absolute",
    top: 20,
    left: 20,
    width: 30,
    height: 30,
    borderTopWidth: 2,
    borderLeftWidth: 2,
    borderColor: HeritageColors.goldLight,
    borderTopLeftRadius: 8,
  },

  scanCornerTopRight: {
    position: "absolute",
    top: 20,
    right: 20,
    width: 30,
    height: 30,
    borderTopWidth: 2,
    borderRightWidth: 2,
    borderColor: HeritageColors.goldLight,
    borderTopRightRadius: 8,
  },

  scanCornerBottomLeft: {
    position: "absolute",
    bottom: 20,
    left: 20,
    width: 30,
    height: 30,
    borderBottomWidth: 2,
    borderLeftWidth: 2,
    borderColor: HeritageColors.goldLight,
    borderBottomLeftRadius: 8,
  },

  scanCornerBottomRight: {
    position: "absolute",
    bottom: 20,
    right: 20,
    width: 30,
    height: 30,
    borderBottomWidth: 2,
    borderRightWidth: 2,
    borderColor: HeritageColors.goldLight,
    borderBottomRightRadius: 8,
  },

  scannerIcon: {
    width: 96,
    height: 96,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 32,
    backgroundColor: "rgba(197,140,255,0.055)",
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    shadowColor: "#C58CFF",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 0.12,
    shadowRadius: 18,
    elevation: 5,
  },

  scanHint: {
    position: "absolute",
    bottom: 14,
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: HeritageRadius.pill,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: "rgba(23,20,17,0.72)",
  },

  scanHintDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: HeritageColors.goldLight,
  },

  scanHintText: {
    color: HeritageColors.muted,
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 1.2,
  },

  panelTitle: {
    marginTop: 20,
    color: HeritageColors.ivory,
    textAlign: "center",
    fontSize: 22,
    lineHeight: 28,
    fontWeight: "900",
    letterSpacing: -0.35,
  },

  panelDescription: {
    marginTop: 10,
    paddingHorizontal: 4,
    color: HeritageColors.muted,
    textAlign: "center",
    fontSize: 14,
    lineHeight: 21,
  },

  actionGroup: {
    width: "100%",
    gap: 11,
    marginTop: 26,
  },

  primaryButton: {
    minHeight: 54,
    paddingHorizontal: 20,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 9,
    borderRadius: 17,
    backgroundColor: HeritageColors.gold,
  },

  primaryButtonText: {
    color: HeritageColors.black,
    fontSize: 14,
    fontWeight: "800",
  },

  secondaryButton: {
    minHeight: 54,
    paddingHorizontal: 20,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 9,
    borderRadius: 17,
    backgroundColor: HeritageColors.surfaceSoft,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
  },

  secondaryButtonText: {
    color: HeritageColors.goldLight,
    fontSize: 14,
    fontWeight: "800",
  },

  buttonPressed: {
    opacity: 0.78,
    transform: [{ scale: 0.985 }],
  },

  previewPanel: {
    gap: 16,
  },

  imageFrame: {
    height: 340,
    overflow: "hidden",
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surfaceStrong,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  previewImage: {
    width: "100%",
    height: "100%",
  },

  previewHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  fileName: {
    maxWidth: 270,
    marginTop: 5,
    color: HeritageColors.ivory,
    fontSize: 14,
    fontWeight: "700",
  },

  closeButton: {
    width: 40,
    height: 40,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 13,
    backgroundColor: HeritageColors.surfaceSoft,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  analyzeButton: {
    marginTop: 4,
  },

  disabledButton: {
    opacity: 0.65,
  },

  disclaimer: {
    color: HeritageColors.mutedDark,
    textAlign: "center",
    fontSize: 11,
    lineHeight: 17,
  },

  errorBox: {
    marginTop: 14,
    padding: 14,
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 9,
    borderRadius: 15,
    backgroundColor: "rgba(184, 107, 99, 0.09)",
    borderWidth: 1,
    borderColor: "rgba(184, 107, 99, 0.25)",
  },

  errorText: {
    flex: 1,
    color: HeritageColors.ivory,
    fontSize: 13,
    lineHeight: 20,
  },

  resultSection: {
    gap: 16,
  },

  resultImageFrame: {
    height: 260,
    overflow: "hidden",
    borderRadius: HeritageRadius.glass,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  resultImage: {
    width: "100%",
    height: "100%",
  },

  resultCard: {
    padding: HeritageSpacing.xxl,
    borderRadius: HeritageRadius.glass,
    backgroundColor: HeritageColors.surface,
    borderWidth: 1,
    borderColor: HeritageColors.border,
  },

  statusRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  statusBadge: {
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

  statusText: {
    color: HeritageColors.goldLight,
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1,
  },

  confidenceLevel: {
    color: HeritageColors.muted,
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 1,
  },

  resultTitle: {
    marginTop: 18,
    color: HeritageColors.ivory,
    fontSize: 26,
    lineHeight: 32,
    fontWeight: "800",
    letterSpacing: -0.5,
  },

  locationRow: {
    marginTop: 9,
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },

  locationText: {
    flex: 1,
    color: HeritageColors.muted,
    fontSize: 13,
  },

  confidenceBlock: {
    marginTop: 22,
  },

  confidenceHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  label: {
    color: HeritageColors.gold,
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1.5,
    textTransform: "uppercase",
  },

  confidenceValue: {
    color: HeritageColors.ivory,
    fontSize: 13,
    fontWeight: "800",
  },

  confidenceTrack: {
    height: 5,
    marginTop: 8,
    overflow: "hidden",
    borderRadius: 999,
    backgroundColor: HeritageColors.surfaceSoft,
  },

  confidenceFill: {
    height: "100%",
    borderRadius: 999,
    backgroundColor: HeritageColors.gold,
  },

  resultBlock: {
    marginTop: 24,
  },

  bodyText: {
    marginTop: 8,
    color: HeritageColors.muted,
    fontSize: 14,
    lineHeight: 22,
  },

  bulletRow: {
    marginTop: 9,
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 9,
  },

  bullet: {
    width: 5,
    height: 5,
    marginTop: 8,
    borderRadius: 999,
    backgroundColor: HeritageColors.gold,
  },

  groundingBox: {
    marginTop: 24,
    padding: 14,
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 10,
    borderRadius: 15,
    backgroundColor: "rgba(127, 166, 124, 0.08)",
    borderWidth: 1,
    borderColor: "rgba(127, 166, 124, 0.20)",
  },

  groundingContent: {
    flex: 1,
  },

  groundingTitle: {
    color: HeritageColors.ivory,
    fontSize: 12,
    fontWeight: "800",
  },

  groundingText: {
    marginTop: 3,
    color: HeritageColors.muted,
    fontSize: 12,
    lineHeight: 18,
  },
});



