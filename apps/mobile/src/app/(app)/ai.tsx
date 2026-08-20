import { useMemo, useRef, useState } from "react";
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
import * as Speech from "expo-speech";
import {
  RecordingPresets,
  requestRecordingPermissionsAsync,
  useAudioRecorder,
} from "expo-audio";
import { SafeAreaView } from "react-native-safe-area-context";

import {
  HeritageColors,
  HeritageRadius,
} from "@/constants/theme";
import { askHeritageAI } from "@/services/ai-chat";
import { transcribeVoice } from "@/services/voice-transcription";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  text: string;
  grounded?: boolean;
  sourceCount?: number;
};

const INITIAL_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  text:
    "Namaste. I am HeritageAI. Ask me anything about India's heritage, monuments, history, architecture, culture, or the stories behind the places you discover.",
};

export default function AIChatScreen() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    INITIAL_MESSAGE,
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingUri, setRecordingUri] = useState<string | null>(null);
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);

  const scrollViewRef = useRef<ScrollView>(null);

  const canSend = useMemo(
    () => input.trim().length > 0 && !isSending,
    [input, isSending],
  );

  const scrollToBottom = () => {
    requestAnimationFrame(() => {
      scrollViewRef.current?.scrollToEnd({
        animated: true,
      });
    });
  };

  const speakAIResponse = async (
    text: string,
  ) => {
    const normalizedText = text.trim();

    if (!normalizedText) {
      return;
    }

    try {
      await Speech.stop();

      setIsSpeaking(true);

      console.log(
        "[CHAT VOICE TRACE] speaking AI response",
      );

      Speech.speak(normalizedText, {
        language: "en-IN",
        rate: 0.95,
        pitch: 1.0,
        onDone: () => {
          setIsSpeaking(false);

          console.log(
            "[CHAT VOICE TRACE] AI speech completed",
          );
        },
        onStopped: () => {
          setIsSpeaking(false);

          console.log(
            "[CHAT VOICE TRACE] AI speech stopped",
          );
        },
        onError: (error) => {
          setIsSpeaking(false);

          console.error(
            "[CHAT VOICE TRACE] AI speech failed:",
            error,
          );
        },
      });
    } catch (error) {
      setIsSpeaking(false);

      console.error(
        "[CHAT VOICE TRACE] unable to start AI speech:",
        error,
      );
    }
  };
  const handleVoicePress = async () => {
    if (isSending) {
      return;
    }

    if (isRecording) {
      try {
        await recorder.stop();

        const uri = recorder.uri;

        setIsRecording(false);
        setRecordingUri(uri ?? null);

        console.log(
          "[CHAT VOICE TRACE] recording completed:",
          JSON.stringify({
            uri,
          }),
        );

        if (!uri) {
          setErrorMessage(
            "Recording stopped but no audio file was created.",
          );
          return;
        }

        setIsSending(true);

        try {
          console.log(
            "[CHAT VOICE TRACE] starting transcription",
          );

          const result = await transcribeVoice(uri);

          const transcript =
            result.transcript.trim();

          console.log(
            "[CHAT VOICE TRACE] transcript:",
            transcript,
          );

          if (!transcript) {
            throw new Error(
              "No speech was detected in the recording.",
            );
          }

          setInput((current) =>
            current.trim()
              ? `${current.trim()} ${transcript}`
              : transcript,
          );
        } catch (error) {
          console.error(
            "[CHAT VOICE TRACE] transcription failed:",
            error,
          );

          setErrorMessage(
            error instanceof Error
              ? error.message
              : "Voice transcription failed.",
          );
        } finally {
          setIsSending(false);
        }
      } catch (error) {
        console.error(
          "[CHAT VOICE TRACE] stop recording failed:",
          error,
        );

        setIsRecording(false);
        setErrorMessage("Unable to stop voice recording.");
      }

      return;
    }

    try {
      setErrorMessage(null);

      const permission =
        await requestRecordingPermissionsAsync();

      if (!permission.granted) {
        setErrorMessage(
          "Microphone permission is required for voice input.",
        );
        return;
      }

      setRecordingUri(null);

      await recorder.prepareToRecordAsync();

      recorder.record();

      setIsRecording(true);

      console.log(
        "[CHAT VOICE TRACE] recording started",
      );
    } catch (error) {
      console.error(
        "[CHAT VOICE TRACE] start recording failed:",
        error,
      );

      setIsRecording(false);
      setErrorMessage("Unable to start voice recording.");
    }
  };
  const handleSend = async () => {
    const question = input.trim();

    if (!question || isSending) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      text: question,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);
    setInput("");
    setIsSending(true);

    scrollToBottom();

    try {
      const result = await askHeritageAI(question);

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        text: result.answer,
        grounded: result.grounded,
        sourceCount: result.sources?.length ?? 0,
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);
      void speakAIResponse(result.answer);

      scrollToBottom();
    } catch (error) {
      console.error(
        "[AI CHAT TRACE] request failed",
        error,
      );

      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        role: "assistant",
        text:
          "I couldn't reach HeritageAI right now. Please check your connection and try again.",
      };

      setMessages((current) => [
        ...current,
        errorMessage,
      ]);

      scrollToBottom();

    } finally {
      setIsSending(false);
    }
  };

  return (
    <SafeAreaView
      style={styles.safeArea}
      edges={["top", "bottom"]}
    >
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <View style={styles.header}>
          <View>
            <Text style={styles.eyebrow}>
              HERITAGEAI
            </Text>

            <Text style={styles.title}>HeritageAI</Text>
          </View>

          <View style={styles.status}>
            <View style={styles.statusDot} />
            <Text style={styles.statusText}>
              ONLINE
            </Text>
          </View>
        </View>

        <ScrollView
          ref={scrollViewRef}
          style={styles.messages}
          contentContainerStyle={styles.messagesContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
          onContentSizeChange={scrollToBottom}
        >
          {messages.map((message) => {
            const isUser = message.role === "user";

            return (
              <View
                key={message.id}
                style={[
                  styles.messageRow,
                  isUser
                    ? styles.userRow
                    : styles.assistantRow,
                ]}
              >
                {!isUser && (
                  <View style={styles.aiAvatar}>
                    <Ionicons
                      name="sparkles"
                      size={17}
                      color={HeritageColors.goldLight}
                    />
                  </View>
                )}

                <View
                  style={[
                    styles.messageBubble,
                    isUser
                      ? styles.userBubble
                      : styles.assistantBubble,
                  ]}
                >
                  <Text
                    style={[
                      styles.messageText,
                      isUser
                        ? styles.userText
                        : styles.assistantText,
                    ]}
                  >
                    {message.text}
                  </Text>
                  {!isUser && message.id !== "welcome" && (
                    <Pressable
                      accessibilityRole="button"
                      accessibilityLabel={
                        isSpeaking
                          ? "Stop AI voice"
                          : "Listen to AI response"
                      }
                      onPress={() => {
                        if (isSpeaking) {
                          void Speech.stop();
                          return;
                        }

                        void speakAIResponse(message.text);
                      }}
                      style={({ pressed }) => [
                        styles.voicePlaybackButton,
                        pressed &&
                          styles.voicePlaybackButtonPressed,
                      ]}
                    >
                      <Ionicons
                        name={
                          isSpeaking
                            ? "stop"
                            : "volume-high-outline"
                        }
                        size={15}
                        color={HeritageColors.goldLight}
                      />

                      <Text style={styles.voicePlaybackText}>
                        {isSpeaking ? "Stop" : "Listen"}
                      </Text>
                    </Pressable>
                  )}

                  {!isUser &&
                    message.sourceCount !== undefined &&
                    message.sourceCount > 0 && (
                      <View style={styles.groundingBadge}>
                        <Ionicons
                          name="shield-checkmark-outline"
                          size={13}
                          color={HeritageColors.goldLight}
                        />

                        <Text style={styles.groundingText}>
                          {message.grounded
                            ? `Grounded · ${message.sourceCount} sources`
                            : `${message.sourceCount} sources`}
                        </Text>
                      </View>
                    )}
                </View>
              </View>
            );
          })}

          {isSending && (
            <View
              style={[
                styles.messageRow,
                styles.assistantRow,
              ]}
            >
              <View style={styles.aiAvatar}>
                <Ionicons
                  name="sparkles"
                  size={17}
                  color={HeritageColors.goldLight}
                />
              </View>

              <View
                style={[
                  styles.messageBubble,
                  styles.assistantBubble,
                  styles.loadingBubble,
                ]}
              >
                <ActivityIndicator
                  size="small"
                  color={HeritageColors.goldLight}
                />

                <Text style={styles.loadingText}>
                  HeritageAI is thinking…
                </Text>
              </View>
            </View>
          )}
        </ScrollView>

                <View style={styles.composerShell}>
          <Pressable
            disabled={isSending}
            style={({ pressed }) => [
              styles.composerActionButton,
              pressed && styles.composerActionPressed,
            ]}
          >
            <Ionicons
              name="add"
              size={24}
              color={HeritageColors.muted}
            />
          </Pressable>

          <TextInput
            value={input}
            onChangeText={setInput}
            placeholder="Ask anything"
            placeholderTextColor={HeritageColors.mutedDark}
            style={styles.input}
            multiline
            maxLength={2000}
            editable={!isSending}
            onSubmitEditing={() => {
              if (Platform.OS === "ios" && canSend) {
                void handleSend();
              }
            }}
          />

          <Pressable
            disabled={isSending}
            style={({ pressed }) => [
              styles.thinkButton,
              pressed && styles.composerActionPressed,
            ]}
          >
            <Ionicons
              name="sparkles-outline"
              size={17}
              color={HeritageColors.muted}
            />
            <Text style={styles.thinkButtonText}>Think</Text>
          </Pressable>

          <Pressable
            disabled={isSending}
            onPress={() => {
              if (isSpeaking) {
                void Speech.stop();
                return;
              }

              void handleVoicePress();
            }}
            style={({ pressed }) => [
              styles.voiceButton,
              isRecording && styles.voiceButtonRecording,
              pressed && styles.composerActionPressed,
            ]}
          >
            <Ionicons
              name={isRecording ? "stop" : "mic-outline"}
              size={21}
              color={
                isRecording
                  ? HeritageColors.goldLight
                  : HeritageColors.muted
              }
            />
          </Pressable>

          <Pressable
            disabled={!canSend}
            onPress={() => void handleSend()}
            style={({ pressed }) => [
              styles.sendButton,
              !canSend && styles.sendButtonDisabled,
              pressed && canSend && styles.sendButtonPressed,
            ]}
          >
            <Ionicons
              name="arrow-up"
              size={21}
              color={HeritageColors.black}
            />
          </Pressable>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: HeritageColors.black,
  },

  container: {
    flex: 1,
    backgroundColor: HeritageColors.black,
  },

  header: {
    paddingHorizontal: 18,
    paddingTop: 10,
    paddingBottom: 12,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderBottomWidth: 1,
    borderBottomColor: HeritageColors.border,
  },

  eyebrow: {
    color: HeritageColors.goldLight,
    fontSize: 10,
    fontWeight: "900",
    letterSpacing: 2,
  },

  title: {
    marginTop: 3,
    color: HeritageColors.white,
    fontSize: 22,
    fontWeight: "900",
  },

  status: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 7,
    borderRadius: HeritageRadius.pill,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: "rgba(255,255,255,0.04)",
  },

  statusDot: {
    width: 7,
    height: 7,
    borderRadius: 7,
    backgroundColor: HeritageColors.goldLight,
  },

  statusText: {
    color: HeritageColors.muted,
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 1,
  },

  messages: {
    flex: 1,
  },

  messagesContent: {
    paddingHorizontal: 16,
    paddingTop: 18,
    paddingBottom: 24,
    gap: 14,
  },

  messageRow: {
    width: "100%",
    flexDirection: "row",
    alignItems: "flex-end",
  },

  assistantRow: {
    justifyContent: "flex-start",
  },

  userRow: {
    justifyContent: "flex-end",
  },

  aiAvatar: {
    width: 34,
    height: 34,
    borderRadius: 17,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 8,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: "rgba(197,140,255,0.10)",
  },

  messageBubble: {
    maxWidth: "82%",
    paddingHorizontal: 15,
    paddingVertical: 12,
    borderRadius: HeritageRadius.lg,
  },

  assistantBubble: {
    backgroundColor: "rgba(255,255,255,0.055)",
    borderWidth: 1,
    borderColor: HeritageColors.border,
    borderBottomLeftRadius: 5,
  },

  userBubble: {
    backgroundColor: HeritageColors.goldLight,
    borderBottomRightRadius: 5,
  },

  messageText: {
    fontSize: 15,
    lineHeight: 22,
  },

  assistantText: {
    color: HeritageColors.white,
  },
  voicePlaybackButton: {
    alignSelf: "flex-start",
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginTop: 10,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: HeritageRadius.pill,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: "rgba(197,140,255,0.08)",
  },

  voicePlaybackButtonPressed: {
    opacity: 0.65,
    transform: [{ scale: 0.97 }],
  },

  voicePlaybackText: {
    color: HeritageColors.goldLight,
    fontSize: 11,
    fontWeight: "700",
  },

  userText: {
    color: HeritageColors.black,
    fontWeight: "600",
  },

  groundingBadge: {
    marginTop: 10,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: HeritageColors.border,
    flexDirection: "row",
    alignItems: "center",
    gap: 5,
  },

  groundingText: {
    color: HeritageColors.goldLight,
    fontSize: 10,
    fontWeight: "800",
  },

  loadingBubble: {
    minWidth: 145,
    flexDirection: "row",
    alignItems: "center",
    gap: 9,
  },

  loadingText: {
    color: HeritageColors.muted,
    fontSize: 12,
    fontWeight: "600",
  },

  composerShell: {
    marginHorizontal: 12,
    marginBottom: 92,
    paddingHorizontal: 8,
    paddingVertical: 7,
    minHeight: 58,
    maxHeight: 140,
    flexDirection: "row",
    alignItems: "center",
    borderRadius: HeritageRadius.pill,
    borderWidth: 1,
    borderColor: HeritageColors.borderStrong,
    backgroundColor: "rgba(23,20,17,0.94)",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.22,
    shadowRadius: 18,
    elevation: 8,
  },

  composerActionButton: {
    width: 38,
    height: 38,
    borderRadius: 19,
    alignItems: "center",
    justifyContent: "center",
  },

  composerActionPressed: {
    transform: [{ scale: 0.92 }],
    opacity: 0.72,
  },

  thinkButton: {
    height: 36,
    paddingHorizontal: 8,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 4,
    borderRadius: HeritageRadius.pill,
  },

  thinkButtonText: {
    color: HeritageColors.muted,
    fontSize: 12,
    fontWeight: "700",
  },

  voiceButtonRecording: {
    backgroundColor: "rgba(197,140,255,0.16)",
    borderWidth: 1,
    borderColor: "rgba(197,140,255,0.45)",
  },
  voiceButton: {
    width: 38,
    height: 38,
    borderRadius: 19,
    alignItems: "center",
    justifyContent: "center",
  },

  input: {
    flex: 1,
    minHeight: 42,
    maxHeight: 110,
    paddingHorizontal: 10,
    paddingTop: 10,
    paddingBottom: 9,
    color: HeritageColors.white,
    fontSize: 15,
    lineHeight: 21,
    textAlignVertical: "top",
  },

  sendButton: {
    width: 42,
    height: 42,
    marginLeft: 6,
    borderRadius: 21,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: HeritageColors.goldLight,
  },

  sendButtonDisabled: {
    opacity: 0.3,
  },

  sendButtonPressed: {
    transform: [{ scale: 0.94 }],
  },
});












