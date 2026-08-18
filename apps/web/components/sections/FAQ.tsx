"use client";

import { useAuth } from "@/providers/AuthProvider";

import { useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  ChevronDown,
  CircleHelp,
  MessageCircle,
  Sparkles,
} from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

const faqs = [
  {
    question: "What is HeritageAI?",
    answer:
      "HeritageAI is a heritage discovery and preservation platform that combines exploration, conversational AI and visual intelligence to help people understand cultural places and their stories.",
  },
  {
    question: "Can the AI identify every heritage site?",
    answer:
      "No. HeritageAI is designed to communicate uncertainty rather than force an identification when the available visual evidence is insufficient. An uncertain result should remain clearly marked as uncertain.",
  },
  {
    question: "Where does HeritageAI get its historical knowledge?",
    answer:
      "The AI experience is designed around available HeritageAI evidence and retrieval sources. Answers should stay within supported evidence rather than inventing historical facts or unsupported citations.",
  },
  {
    question: "Can I explore heritage places without using AI?",
    answer:
      "Yes. HeritageAI also provides a heritage exploration experience where you can browse places and learn about their historical and cultural context without needing to ask an AI question.",
  },
  {
    question: "Is HeritageAI only for historical monuments?",
    answer:
      "The broader goal is cultural heritage discovery. Monuments and architectural sites are an important part of the experience, while the platform can also support stories, locations, traditions and other forms of heritage knowledge.",
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);
  const reduceMotion = useReducedMotion();
  const { isAuthenticated, isLoading } = useAuth();


  return (
    <section
      id="faq"
      className="relative overflow-hidden py-24 sm:py-32"
    >
      <div className="pointer-events-none absolute right-0 top-1/4 h-72 w-72 rounded-full bg-[rgba(212,175,90,0.04)] blur-[110px]" />

      <div className="heritage-container relative">
        {/* ---------------------------------------------------------------- */}
        {/* Heading */}
        {/* ---------------------------------------------------------------- */}

        <motion.div
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 20,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.2,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.7,
            ease: EASE,
          }}
          className="mx-auto max-w-2xl text-center"
        >
          <div className="heritage-badge mx-auto w-fit">
            <CircleHelp
              className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            Frequently asked
          </div>

          <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.045em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
            Questions before you
            <span className="heritage-gold-gradient"> explore.</span>
          </h2>

          <p className="mx-auto mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
            Learn how HeritageAI approaches discovery, visual intelligence
            and evidence-grounded historical knowledge.
          </p>
        </motion.div>

        {/* ---------------------------------------------------------------- */}
        {/* FAQ layout */}
        {/* ---------------------------------------------------------------- */}

        <div className="mx-auto mt-12 max-w-4xl">
          <div className="space-y-3">
            {faqs.map((faq, index) => {
              const isOpen = openIndex === index;

              return (
                <motion.div
                  key={faq.question}
                  initial={{
                    opacity: 0,
                    y: reduceMotion ? 0 : 14,
                  }}
                  whileInView={{
                    opacity: 1,
                    y: 0,
                  }}
                  viewport={{
                    once: true,
                    amount: 0.08,
                  }}
                  transition={{
                    duration: reduceMotion ? 0 : 0.45,
                    delay: reduceMotion ? 0 : index * 0.035,
                    ease: EASE,
                  }}
                  className={`heritage-glass overflow-hidden rounded-[22px] transition-colors duration-300 ${
                    isOpen
                      ? "border-[var(--glass-border-strong)]"
                      : "hover:border-[var(--glass-border-strong)]"
                  }`}
                >
                  <button
                    type="button"
                    aria-expanded={isOpen}
                    aria-controls={`faq-answer-${index}`}
                    onClick={() =>
                      setOpenIndex((current) =>
                        current === index ? null : index,
                      )
                    }
                    className="flex min-h-16 w-full items-center gap-4 px-5 py-4 text-left sm:px-6"
                  >
                    <span
                      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border text-[10px] font-semibold transition-colors ${
                        isOpen
                          ? "border-[var(--glass-border-strong)] bg-[rgba(212,175,90,0.09)] text-[var(--heritage-gold-light)]"
                          : "border-[var(--glass-border)] bg-white/[0.02] text-[var(--heritage-bronze)]"
                      }`}
                    >
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <span
                      className={`flex-1 text-sm font-semibold transition-colors sm:text-base ${
                        isOpen
                          ? "text-[var(--heritage-ivory)]"
                          : "text-[var(--heritage-muted)]"
                      }`}
                    >
                      {faq.question}
                    </span>

                    <span
                      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-[var(--glass-border)] transition-transform duration-300 ${
                        isOpen
                          ? "rotate-180 bg-[rgba(212,175,90,0.07)]"
                          : "bg-white/[0.02]"
                      }`}
                    >
                      <ChevronDown
                        className="h-4 w-4 text-[var(--heritage-gold-light)]"
                        aria-hidden="true"
                      />
                    </span>
                  </button>

                  <AnimatePresence initial={false}>
                    {isOpen && (
                      <motion.div
                        id={`faq-answer-${index}`}
                        initial={
                          reduceMotion
                            ? false
                            : {
                                height: 0,
                                opacity: 0,
                              }
                        }
                        animate={{
                          height: "auto",
                          opacity: 1,
                        }}
                        exit={
                          reduceMotion
                            ? undefined
                            : {
                                height: 0,
                                opacity: 0,
                              }
                        }
                        transition={{
                          duration: reduceMotion ? 0 : 0.28,
                          ease: EASE,
                        }}
                        role="region"
                        aria-labelledby={`faq-question-${index}`}
                      >
                        <div className="border-t border-[var(--glass-border)] px-5 pb-5 pt-4 sm:px-6 sm:pb-6">
                          <div className="pl-12">
                            <p className="max-w-2xl text-sm leading-7 text-[var(--heritage-muted)]">
                              {faq.answer}
                            </p>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              );
            })}
          </div>
        </div>

        <div className="mt-8 flex items-center justify-center gap-2 text-[10px] uppercase tracking-[0.16em] text-[var(--heritage-bronze)]">
          <Sparkles className="h-3 w-3" aria-hidden="true" />
          Discover · Understand · Preserve
        </div>
      </div>
    </section>
  );
}
