import {
  RecordingPresets,
  requestRecordingPermissionsAsync,
  useAudioPlayer,
  useAudioPlayerStatus,
  useAudioRecorder,
} from "expo-audio";
import * as Speech from "expo-speech";
import { useRef, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Text,
  View,
} from "react-native";

import {
  processVoiceGuide,
  type VoiceGuideResponse,
} from "@/services/voice-guide";

export default function AIGuideScreen() {
  const recorder = useAudioRecorder(
    RecordingPresets.HIGH_QUALITY,
  );

  const player = useAudioPlayer(undefined, {
    updateInterval: 250,
  });

  const playerStatus = useAudioPlayerStatus(
    player,
  );

  const [isRecording, setIsRecording] =
    useState(false);

  const [recordingUri, setRecordingUri] =
    useState<string | null>(null);

  const [voiceGuide, setVoiceGuide] =
    useState<VoiceGuideResponse | null>(null);

  const [errorMessage, setErrorMessage] =
    useState<string | null>(null);

  const [isBusy, setIsBusy] = useState(false);

  const [isSpeechPlaying, setIsSpeechPlaying] = useState(false);

  // Each recording/question receives a unique session.
  // Old async callbacks are ignored after a new session starts.
  const voiceSessionRef = useRef(0);

  const startRecording = async () => {
    if (isBusy || isRecording) {
      return;
    }

    // Start a completely new Voice Guide session.
    voiceSessionRef.current += 1;

    const sessionId = voiceSessionRef.current;

    console.log(
      "[VOICE GUIDE TRACE] new voice session:",
      sessionId,
    );

    // Stop any speech from the previous question before
    // touching the recorder.
    try {
      await Speech.stop();
    } catch {
      // Ignore speech cleanup errors.
    }

    setIsSpeechPlaying(false);
    setErrorMessage(null);
    setRecordingUri(null);
    setVoiceGuide(null);
    setIsBusy(true);

    try {
      const permission =
        await requestRecordingPermissionsAsync();

      if (!permission.granted) {
        throw new Error(
          "Microphone permission is required.",
        );
      }

      await recorder.prepareToRecordAsync();

      // The user may have started another session while
      // permission/recorder preparation was pending.
      if (voiceSessionRef.current !== sessionId) {
        return;
      }

      recorder.record();

      setIsRecording(true);

      console.log(
        "[VOICE GUIDE TRACE] recording started:",
        sessionId,
      );
    } catch (error) {
      console.error(
        "[VOICE GUIDE TRACE] start recording failed:",
        error,
      );

      if (voiceSessionRef.current === sessionId) {
        setErrorMessage(
          error instanceof Error
            ? error.message
            : "Unable to start recording.",
        );
      }
    } finally {
      if (voiceSessionRef.current === sessionId) {
        setIsBusy(false);
      }
    }
  };

  const speakAnswer = async (
    answer: string,
    language: string | null,
    sessionId = voiceSessionRef.current,
  ) => {
    const text = answer.trim();

    if (!text) {
      throw new Error(
        "Voice Guide returned an empty answer.",
      );
    }

    // Never allow an old question to speak into a newer session.
    if (voiceSessionRef.current !== sessionId) {
      console.log(
        "[VOICE GUIDE TRACE] ignoring stale speech request:",
        sessionId,
      );

      return;
    }

    try {
      await Speech.stop();
    } catch {
      // Ignore stale speech cleanup errors.
    }

    if (voiceSessionRef.current !== sessionId) {
      return;
    }

    setIsSpeechPlaying(true);

    console.log(
      "[VOICE GUIDE TRACE] using device speech fallback:",
      sessionId,
    );

    Speech.speak(text, {
      language: language?.trim() || "en-US",
      rate: 0.95,
      pitch: 1.0,

      onStart: () => {
        if (voiceSessionRef.current !== sessionId) {
          return;
        }

        setIsSpeechPlaying(true);

        console.log(
          "[VOICE GUIDE TRACE] device speech started:",
          sessionId,
        );
      },

      onDone: () => {
        if (voiceSessionRef.current !== sessionId) {
          return;
        }

        setIsSpeechPlaying(false);

        console.log(
          "[VOICE GUIDE TRACE] device speech completed:",
          sessionId,
        );
      },

      onStopped: () => {
        if (voiceSessionRef.current !== sessionId) {
          return;
        }

        setIsSpeechPlaying(false);

        console.log(
          "[VOICE GUIDE TRACE] device speech stopped:",
          sessionId,
        );
      },

      onError: (error) => {
        // expo-speech on web can report an asynchronous
        // error after stop() / replacement. Do not allow
        // an old session to affect the current question.
        if (voiceSessionRef.current !== sessionId) {
          console.log(
            "[VOICE GUIDE TRACE] ignored stale speech error:",
            sessionId,
          );

          return;
        }

        setIsSpeechPlaying(false);

        console.error(
          "[VOICE GUIDE TRACE] device speech failed:",
          error,
        );
      },
    });
  };

  const processRecording = async (
    uri: string,
    sessionId: number,
  ) => {
    console.log(
      "[VOICE GUIDE TRACE] sending recording to Voice Guide:",
      JSON.stringify({
        sessionId,
        uri,
      }),
    );

    const result = await processVoiceGuide(uri);

    console.log(
      "[VOICE GUIDE TRACE] Voice Guide response:",
      JSON.stringify({
        sessionId,
        grounded: result.grounded,
        sourceCount: result.sources.length,
        audioUrl: result.audio_url,
        audioMimeType:
          result.audio_mime_type,
        audioSampleRate:
          result.audio_sample_rate,
      }),
    );

    // Ignore a response belonging to an older question.
    if (voiceSessionRef.current !== sessionId) {
      console.log(
        "[VOICE GUIDE TRACE] ignoring stale Voice Guide response:",
        sessionId,
      );

      return;
    }

    setVoiceGuide(result);

    if (result.audio_url) {
      console.log(
        "[VOICE GUIDE TRACE] Gemini TTS audio available:",
        sessionId,
      );

      player.replace(result.audio_url);

      console.log(
        "[VOICE GUIDE TRACE] audio source loaded:",
        sessionId,
      );

      player.play();

      console.log(
        "[VOICE GUIDE TRACE] audio playback started:",
        sessionId,
      );

      return;
    }

    console.log(
      "[VOICE GUIDE TRACE] Gemini TTS unavailable:",
      result.tts_fallback_reason,
    );

    await speakAnswer(
      result.answer,
      result.language,
      sessionId,
    );
  };

  const stopRecording = async () => {
    if (!isRecording || isBusy) {
      return;
    }

    const sessionId = voiceSessionRef.current;

    setIsBusy(true);
    setErrorMessage(null);

    try {
      // Ensure no previous speech is still active.
      try {
        await Speech.stop();
      } catch {
        // Ignore speech cleanup errors.
      }

      setIsSpeechPlaying(false);

      await recorder.stop();

      const uri = recorder.uri;

      setIsRecording(false);

      if (!uri) {
        throw new Error(
          "Recording stopped but no audio file was created.",
        );
      }

      setRecordingUri(uri);

      console.log(
        "[VOICE GUIDE TRACE] recording completed:",
        JSON.stringify({
          sessionId,
          uri,
        }),
      );

      // The session may have changed while stopping.
      if (voiceSessionRef.current !== sessionId) {
        console.log(
          "[VOICE GUIDE TRACE] ignoring stale recording:",
          sessionId,
        );

        return;
      }

      await processRecording(
        uri,
        sessionId,
      );
    } catch (error: any) {
      // Ignore errors from a session that has already been replaced.
      if (voiceSessionRef.current !== sessionId) {
        console.log(
          "[VOICE GUIDE TRACE] ignored stale recording error:",
          sessionId,
        );

        return;
      }

      console.error(
        "[VOICE GUIDE TRACE] voice analysis failed:",
        {
          status: error?.response?.status,
          detail: error?.response?.data?.detail,
          message:
            error?.response?.data?.message ||
            error?.message,
        },
      );

      const message =
        error?.response?.data?.detail?.message ||
        error?.response?.data?.message ||
        error?.message ||
        "Voice transcription failed.";

      setErrorMessage(message);
      setIsRecording(false);
    } finally {
      if (voiceSessionRef.current === sessionId) {
        setIsBusy(false);
      }
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        AI Heritage Guide
      </Text>

      <Text style={styles.subtitle}>
        Ask questions and explore history with
        HeritageAI.
      </Text>

      <View style={styles.card}>
        <Text style={styles.status}>
          {isRecording
            ? "Listening..."
            : isBusy
              ? "HeritageAI is thinking..."
              : playerStatus.playing ||
                  isSpeechPlaying
                ? "HeritageAI is speaking..."
                : voiceGuide
                  ? "Voice Guide ready"
                  : recordingUri
                    ? "Recording ready"
                    : "Ready to listen"}
        </Text>

        {isRecording ? (
          <Pressable
            style={[
              styles.button,
              styles.stopButton,
            ]}
            onPress={stopRecording}
            disabled={isBusy}
          >
            {isBusy ? (
              <ActivityIndicator />
            ) : (
              <Text style={styles.buttonText}>
                Stop Recording
              </Text>
            )}
          </Pressable>
        ) : (
          <Pressable
            style={styles.button}
            onPress={startRecording}
            disabled={isBusy}
          >
            {isBusy ? (
              <ActivityIndicator />
            ) : (
              <Text style={styles.buttonText}>
                Start Recording
              </Text>
            )}
          </Pressable>
        )}

        {isBusy && !isRecording ? (
          <Text style={styles.processing}>
            HeritageAI is processing your voice...
          </Text>
        ) : null}

        {voiceGuide ? (
          <View style={styles.resultCard}>
            <Text style={styles.voiceGuideTitle}>
              ?? HeritageAI Voice Guide
            </Text>

            <Text style={styles.voiceGuideStatus}>
              {playerStatus.playing
                ? "HeritageAI is speaking..."
                : "Voice response ready"}
            </Text>

            <View style={styles.voiceVisualizer}>
              <Text style={styles.voiceIcon}>
                {playerStatus.playing ||
                  isSpeechPlaying
                    ? "??"
                    : "???"}
              </Text>
            </View>

            <Text style={styles.metadata}>
              Grounded by {voiceGuide.sources.length}{" "}
              heritage sources
            </Text>

            <Text style={styles.metadata}>
              {voiceGuide.grounded
                ? "Verified heritage evidence"
                : "Evidence confidence limited"}
            </Text>

            <View style={styles.audioControls}>
              <Pressable
                  style={styles.audioButton}
                  onPress={async () => {
                    if (voiceGuide?.audio_url) {
                      if (playerStatus.playing) {
                        player.pause();
                      } else {
                        player.play();
                      }

                      return;
                    }

                    if (isSpeechPlaying) {
                      await Speech.stop();
                      setIsSpeechPlaying(false);
                    } else if (voiceGuide?.answer) {
                      await speakAnswer(
                        voiceGuide.answer,
                        voiceGuide.language,
                        voiceSessionRef.current,
                      );
                    }
                  }}
                >
                  <Text style={styles.buttonText}>
                    {playerStatus.playing ||
                    isSpeechPlaying
                      ? "Pause"
                      : "Play"}
                  </Text>
                </Pressable>

              <Pressable
                  style={styles.audioButton}
                  onPress={async () => {
                    if (voiceGuide?.audio_url) {
                      await player.seekTo(0);
                      player.play();
                      return;
                    }

                    if (voiceGuide?.answer) {
                      await speakAnswer(
                        voiceGuide.answer,
                        voiceGuide.language,
                      );
                    }
                  }}
                >
                  <Text style={styles.buttonText}>
                    Replay
                  </Text>
                </Pressable>
            </View>

            {playerStatus.duration > 0 ? (
              <Text style={styles.metadata}>
                {Math.floor(
                  playerStatus.currentTime,
                )}
                s /{" "}
                {Math.ceil(
                  playerStatus.duration,
                )}
                s
              </Text>
            ) : null}
          </View>
        ) : null}

        {recordingUri && !voiceGuide ? (
          <Text
            style={styles.uri}
            numberOfLines={3}
          >
            Recording URI:
            {"\n"}
            {recordingUri}
          </Text>
        ) : null}

        {errorMessage ? (
          <Text style={styles.error}>
            {errorMessage}
          </Text>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: "center",
    gap: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
  },
  subtitle: {
    fontSize: 16,
    lineHeight: 24,
  },
  card: {
    padding: 24,
    borderRadius: 20,
    gap: 16,
  },
  status: {
    fontSize: 18,
    fontWeight: "600",
  },
  button: {
    minHeight: 52,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 20,
  },
  stopButton: {
    opacity: 0.85,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: "700",
  },
  processing: {
    fontSize: 14,
  },
  voiceGuideTitle: {
    fontSize: 20,
    fontWeight: "700",
    textAlign: "center",
    marginBottom: 8,
  },

  voiceGuideStatus: {
    fontSize: 16,
    textAlign: "center",
    marginBottom: 18,
  },

  voiceVisualizer: {
    width: 96,
    height: 96,
    borderRadius: 48,
    alignItems: "center",
    justifyContent: "center",
    alignSelf: "center",
    marginBottom: 18,
  },

  voiceIcon: {
    fontSize: 42,
  },

  audioControls: {
    flexDirection: "row",
    gap: 12,
    marginTop: 16,
  },

  audioButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: "center",
    backgroundColor: "#1f2937",
  },

  resultCard: {
    padding: 18,
    borderRadius: 16,
    gap: 10,
  },
  resultLabel: {
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 1,
  },
  transcript: {
    fontSize: 17,
    lineHeight: 25,
  },
  metadata: {
    fontSize: 13,
  },
  uri: {
    fontSize: 12,
    lineHeight: 18,
  },
  error: {
    fontSize: 14,
  },
});