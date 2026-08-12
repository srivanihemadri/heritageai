"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

const questions = [
  {
    question: "What is HeritageAI?",
    answer:
      "HeritageAI is an AI-powered platform designed to help people discover, understand and preserve cultural and historical heritage through digital tools.",
  },
  {
    question: "What can HeritageAI analyze?",
    answer:
      "The platform is designed to work with heritage imagery, historical artifacts, inscriptions and visible structural conditions to support exploration and preservation workflows.",
  },
  {
    question: "Can HeritageAI restore historical photographs?",
    answer:
      "HeritageAI is designed to provide AI-assisted restoration capabilities that can help enhance damaged historical photographs while keeping preservation context in mind.",
  },
  {
    question: "Can I explore historical places?",
    answer:
      "Yes. HeritageAI is being designed around heritage discovery, allowing users to explore monuments, landmarks, architecture and historical context through an accessible digital experience.",
  },
  {
    question: "Is HeritageAI intended to replace heritage experts?",
    answer:
      "No. AI should support researchers, historians, conservation teams and the public rather than replace expert judgment. Heritage preservation ultimately depends on appropriate human interpretation and validation.",
  },
  {
    question: "Will HeritageAI be free to use?",
    answer:
      "The project is being designed with the goal of making its core heritage experience accessible without unnecessary cost barriers.",
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section
      id="faq"
      className="relative mx-auto w-full max-w-5xl px-6 py-24 md:px-8 md:py-32"
    >
      <div className="mx-auto max-w-3xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
          Frequently Asked
        </p>

        <h2 className="mt-4 text-3xl font-semibold tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
          Questions about HeritageAI.
        </h2>

        <p className="mt-5 text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
          A quick look at the platform, its purpose and how AI fits into the
          preservation experience.
        </p>
      </div>

      <div className="mt-12 space-y-3">
        {questions.map((item, index) => {
          const isOpen = openIndex === index;

          return (
            <div
              key={item.question}
              className="heritage-glass overflow-hidden rounded-[var(--radius-card)] transition-colors duration-300 hover:border-[var(--glass-border-strong)]"
            >
              <button
                type="button"
                aria-expanded={isOpen}
                onClick={() =>
                  setOpenIndex(isOpen ? null : index)
                }
                className="flex w-full items-center justify-between gap-6 px-5 py-5 text-left md:px-6"
              >
                <span className="text-sm font-semibold text-[var(--heritage-ivory)] md:text-base">
                  {item.question}
                </span>

                <ChevronDown
                  className={`h-5 w-5 shrink-0 text-[var(--heritage-gold)] transition-transform duration-300 ${
                    isOpen ? "rotate-180" : ""
                  }`}
                />
              </button>

              <div
                className={`grid transition-[grid-template-rows,opacity] duration-300 ${
                  isOpen
                    ? "grid-rows-[1fr] opacity-100"
                    : "grid-rows-[0fr] opacity-0"
                }`}
              >
                <div className="overflow-hidden">
                  <p className="border-t border-[var(--glass-border)] px-5 pb-5 pt-4 text-sm leading-7 text-[var(--heritage-muted)] md:px-6">
                    {item.answer}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}