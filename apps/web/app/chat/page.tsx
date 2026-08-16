"use client";

import {
  FormEvent,
  useEffect,
  useRef,
  useState,
} from "react";
import { useRouter } from "next/navigation";
import {
  ArrowUp,
  BookOpen,
  CheckCircle2,
  Loader2,
  Mic,
  MicOff,
  Pause,
  Play,
  ShieldCheck,
  Sparkles,
  Volume2,
  VolumeX,
} from "lucide-react";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useAuth } from "@/providers/AuthProvider";
import apiClient from "@/lib/api-client";
import {
  askHeritageAI,
  type GroundedAnswerResponse,
} from "@/services/ai";

interface VoiceResponse {
  success: boolean;
  transcript: string;
  language: string;
  confidence: number;
}

const suggestions = [
  "Tell me about the history of Brihadeeswarar Temple.",
  "What makes a heritage site historically significant?",
  "How can cultural heritage be preserved?",
];

export default function ChatPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] =
    useState<GroundedAnswerResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [voiceLoading, setVoiceLoading] = useState(false);
  const [error, setError] = useState("");

  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);

  const [isSpeaking, setIsSpeaking] = useState(false);

  const mediaRecorderRef =
    useRef<MediaRecorder | null>(null);

  const mediaStreamRef =
    useRef<MediaStream | null>(null);

  const audioChunksRef =
    useRef<Blob[]>([]);

  const recordingTimerRef =
    useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    return () => {
      mediaStreamRef.current
        ?.getTracks()
        .forEach((track) => track.stop());

      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current);
      }

      window.speechSynthesis?.cancel();
    };
  }, []);

  if (!authLoading && !isAuthenticated) {
    router.replace("/login");
    return null;
  }

  async function submitQuestion(
    event?: FormEvent<HTMLFormElement>,
  ) {
    event?.preventDefault();

    const trimmed = question.trim();

    if (!trimmed || loading || voiceLoading) {
      return;
    }

    setLoading(true);
    setError("");
    setAnswer(null);

    try {
      const result = await askHeritageAI(trimmed);
      setAnswer(result);
    } catch {
      setError(
        "HeritageAI could not generate an answer right now. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function processVoiceBlob(blob: Blob) {
    setVoiceLoading(true);
    setError("");

    try {
      const formData = new FormData();

      const extension =
        blob.type.includes("webm")
          ? "webm"
          : blob.type.includes("mp4")
            ? "mp4"
            : "webm";

      formData.append(
        "file",
        new File(
          [blob],
          `heritage-voice.${extension}`,
          {
            type: blob.type || "audio/webm",
          },
        ),
      );

      const response =
        await apiClient.post<VoiceResponse>(
          "/ai/voice",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          },
        );

      const transcript =
        response.data.transcript?.trim();

      if (!transcript) {
        throw new Error(
          "No speech was detected.",
        );
      }

      setQuestion(transcript);

      setLoading(true);

      const answerResult =
        await askHeritageAI(transcript);

      setAnswer(answerResult);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "";

      setError(
        message ||
          "Voice input could not be processed. Please try again.",
      );
    } finally {
      setVoiceLoading(false);
      setLoading(false);
    }
  }

  async function startRecording() {
    if (
      typeof window === "undefined" ||
      !navigator.mediaDevices?.getUserMedia
    ) {
      setError(
        "Voice input is not supported in this browser.",
      );
      return;
    }

    if (
      !("MediaRecorder" in window)
    ) {
      setError(
        "Audio recording is not supported in this browser.",
      );
      return;
    }

    try {
      setError("");

      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      mediaStreamRef.current = stream;

      const preferredMimeTypes = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/mp4",
      ];

      const supportedMimeType =
        preferredMimeTypes.find(
          (type) =>
            MediaRecorder.isTypeSupported(
              type,
            ),
        );

      const recorder =
        supportedMimeType
          ? new MediaRecorder(
              stream,
              {
                mimeType:
                  supportedMimeType,
              },
            )
          : new MediaRecorder(stream);

      audioChunksRef.current = [];

      recorder.ondataavailable = (
        event,
      ) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(
            event.data,
          );
        }
      };

      recorder.onstop = async () => {
        const blob = new Blob(
          audioChunksRef.current,
          {
            type:
              recorder.mimeType ||
              "audio/webm",
          },
        );

        stream
          .getTracks()
          .forEach((track) =>
            track.stop(),
          );

        mediaStreamRef.current = null;

        await processVoiceBlob(blob);
      };

      mediaRecorderRef.current =
        recorder;

      recorder.start();

      setRecordingSeconds(0);
      setIsRecording(true);

      recordingTimerRef.current =
        setInterval(() => {
          setRecordingSeconds(
            (seconds) => seconds + 1,
          );
        }, 1000);
    } catch {
      setError(
        "Microphone access was denied or unavailable.",
      );
    }
  }

  function stopRecording() {
    const recorder =
      mediaRecorderRef.current;

    if (
      recorder &&
      recorder.state !== "inactive"
    ) {
      recorder.stop();
    }

    setIsRecording(false);

    if (recordingTimerRef.current) {
      clearInterval(
        recordingTimerRef.current,
      );

      recordingTimerRef.current = null;
    }
  }

  function toggleRecording() {
    if (isRecording) {
      stopRecording();
    } else {
      void startRecording();
    }
  }

  function toggleSpeech() {
    if (!answer?.answer) {
      return;
    }

    if (
      !("speechSynthesis" in window)
    ) {
      setError(
        "Voice playback is not supported in this browser.",
      );
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance =
      new SpeechSynthesisUtterance(
        answer.answer,
      );

    utterance.onstart = () =>
      setIsSpeaking(true);

    utterance.onend = () =>
      setIsSpeaking(false);

    utterance.onerror = () =>
      setIsSpeaking(false);

    window.speechSynthesis.speak(
      utterance,
    );
  }

  function formatTime(seconds: number) {
    const minutes = Math.floor(
      seconds / 60,
    );

    const remaining =
      seconds % 60;

    return `${minutes}:${remaining
      .toString()
      .padStart(2, "0")}`;
  }

  return (
    <>
      <Navbar />

      <main className="mx-auto min-h-[calc(100vh-100px)] max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
        <section className="mx-auto max-w-3xl text-center">
          <div className="heritage-gold-glow mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-[var(--glass-border-strong)] bg-[var(--glass-bg-strong)]">
            <Sparkles className="h-6 w-6 text-[var(--heritage-gold-light)]" />
          </div>

          <p className="mt-6 text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold)]">
            HeritageAI Guide
          </p>

          <h1 className="mt-3 text-4xl font-semibold tracking-tight text-[var(--heritage-ivory)] sm:text-5xl">
            Ask history.
            <span className="heritage-gold-gradient">
              {" "}
              Get grounded answers.
            </span>
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-[var(--heritage-muted)]">
            Ask by typing or speaking.
            HeritageAI connects your
            question to grounded heritage
            knowledge and clearly presents
            its evidence.
          </p>
        </section>

        <section className="mt-10">
          <div className="heritage-glass-strong rounded-[28px] p-4 sm:p-6">
            <form
              onSubmit={submitQuestion}
            >
              <label
                htmlFor="heritage-question"
                className="sr-only"
              >
                Ask a heritage question
              </label>

              <textarea
                id="heritage-question"
                value={question}
                onChange={(event) =>
                  setQuestion(
                    event.target.value,
                  )
                }
                maxLength={2000}
                rows={5}
                placeholder="Ask about a monument, historical period, cultural tradition..."
                disabled={
                  isRecording ||
                  voiceLoading
                }
                className="w-full resize-none rounded-2xl border border-[var(--glass-border)] bg-black/20 p-4 text-sm leading-7 text-[var(--heritage-ivory)] outline-none placeholder:text-[var(--heritage-muted)] focus:border-[var(--glass-border-strong)] disabled:opacity-60"
              />

              <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-xs text-[var(--heritage-muted)]">
                    {question.length}/2000
                  </span>

                  {isRecording && (
                    <span className="inline-flex items-center gap-2 text-xs text-[var(--heritage-gold-light)]">
                      <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--heritage-gold)]" />
                      Recording{" "}
                      {formatTime(
                        recordingSeconds,
                      )}
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={
                      toggleRecording
                    }
                    disabled={
                      loading ||
                      voiceLoading
                    }
                    aria-label={
                      isRecording
                        ? "Stop recording"
                        : "Start voice input"
                    }
                    aria-pressed={
                      isRecording
                    }
                    className={`inline-flex h-11 items-center gap-2 rounded-xl border px-4 text-sm font-medium transition-all ${
                      isRecording
                        ? "border-[var(--heritage-gold)] bg-[var(--heritage-gold)]/15 text-[var(--heritage-gold-light)]"
                        : "border-[var(--glass-border)] text-[var(--heritage-ivory)] hover:border-[var(--glass-border-strong)] hover:bg-white/5"
                    } disabled:cursor-not-allowed disabled:opacity-50`}
                  >
                    {isRecording ? (
                      <>
                        <MicOff className="h-4 w-4" />
                        Stop
                      </>
                    ) : (
                      <>
                        <Mic className="h-4 w-4" />
                        Speak
                      </>
                    )}
                  </button>

                  <button
                    type="submit"
                    disabled={
                      !question.trim() ||
                      loading ||
                      voiceLoading ||
                      isRecording
                    }
                    className="heritage-gold-glow inline-flex h-11 items-center gap-2 rounded-xl bg-[var(--heritage-gold)] px-5 text-sm font-semibold text-[var(--heritage-black)] transition-all hover:bg-[var(--heritage-gold-light)] disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Researching
                      </>
                    ) : (
                      <>
                        Ask
                        <ArrowUp className="h-4 w-4" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </form>
          </div>

          {!answer &&
            !loading &&
            !voiceLoading && (
              <div className="mt-5 grid gap-3 md:grid-cols-3">
                {suggestions.map(
                  (suggestion) => (
                    <button
                      key={suggestion}
                      type="button"
                      onClick={() =>
                        setQuestion(
                          suggestion,
                        )
                      }
                      className="heritage-glass rounded-2xl p-4 text-left text-sm leading-6 text-[var(--heritage-muted)] transition-all hover:-translate-y-0.5 hover:border-[var(--glass-border-strong)] hover:text-[var(--heritage-ivory)]"
                    >
                      {suggestion}
                    </button>
                  ),
                )}
              </div>
            )}

          {voiceLoading && (
            <div className="heritage-glass mt-6 flex items-center gap-3 rounded-2xl p-4 text-sm text-[var(--heritage-muted)]">
              <Loader2 className="h-4 w-4 animate-spin text-[var(--heritage-gold)]" />
              Transcribing your voice and
              preparing the heritage answer...
            </div>
          )}

          {error && (
            <div
              role="alert"
              className="mt-6 rounded-2xl border border-red-400/20 bg-red-400/5 p-4 text-sm text-red-200"
            >
              {error}
            </div>
          )}

          {answer && (
            <article className="heritage-glass-strong mt-8 overflow-hidden rounded-[28px]">
              <div className="border-b border-[var(--glass-border)] p-6">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="inline-flex items-center gap-1.5 rounded-full border border-[var(--glass-border)] bg-white/5 px-3 py-1 text-xs text-[var(--heritage-muted)]">
                    <ShieldCheck className="h-3.5 w-3.5 text-[var(--heritage-gold)]" />
                    {answer.grounded
                      ? "Grounded answer"
                      : "Insufficient evidence"}
                  </span>

                  <button
                    type="button"
                    onClick={
                      toggleSpeech
                    }
                    className="inline-flex items-center gap-2 rounded-xl border border-[var(--glass-border)] px-3 py-2 text-xs text-[var(--heritage-muted)] transition-colors hover:border-[var(--glass-border-strong)] hover:text-[var(--heritage-ivory)]"
                    aria-label={
                      isSpeaking
                        ? "Stop reading answer"
                        : "Read answer aloud"
                    }
                  >
                    {isSpeaking ? (
                      <>
                        <VolumeX className="h-4 w-4" />
                        Stop
                      </>
                    ) : (
                      <>
                        <Volume2 className="h-4 w-4" />
                        Listen
                      </>
                    )}
                  </button>
                </div>

                <p className="mt-4 text-sm text-[var(--heritage-muted)]">
                  {answer.query}
                </p>
              </div>

              <div className="p-6">
                <div className="flex gap-3">
                  <Sparkles className="mt-1 h-5 w-5 shrink-0 text-[var(--heritage-gold)]" />

                  <p className="whitespace-pre-wrap text-[15px] leading-8 text-[var(--heritage-ivory)]">
                    {answer.answer}
                  </p>
                </div>

                {answer.sources.length > 0 && (
                  <div className="mt-8 border-t border-[var(--glass-border)] pt-6">
                    <div className="flex items-center gap-2">
                      <BookOpen className="h-4 w-4 text-[var(--heritage-gold)]" />
                      <h2 className="text-sm font-semibold text-[var(--heritage-ivory)]">
                        Evidence & Sources
                      </h2>
                    </div>

                    <div className="mt-4 grid gap-3">
                      {answer.sources.map(
                        (source) => (
                          <div
                            key={`${source.document_id}-${source.chunk_id}`}
                            className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.025] p-4"
                          >
                            <div className="flex flex-wrap items-center justify-between gap-2">
                              <p className="text-sm font-medium text-[var(--heritage-ivory)]">
                                {source.title}
                              </p>

                              {source.is_verified && (
                                <span className="inline-flex items-center gap-1 text-xs text-[var(--heritage-gold-light)]">
                                  <CheckCircle2 className="h-3.5 w-3.5" />
                                  Verified
                                </span>
                              )}
                            </div>

                            <p className="mt-2 text-xs text-[var(--heritage-muted)]">
                              {source.provenance_level}
                            </p>
                          </div>
                        ),
                      )}
                    </div>
                  </div>
                )}
              </div>
            </article>
          )}
        </section>
      </main>

      <Footer />
    </>
  );
}
