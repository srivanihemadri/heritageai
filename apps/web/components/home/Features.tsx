"use client";

import { motion, useReducedMotion } from "framer-motion";
import {
  BookOpen,
  Camera,
  Globe2,
  Map,
  MessageCircle,
  Sparkles,
} from "lucide-react";

const features = [
  {
    icon: Globe2,
    title: "Discover",
    description:
      "Explore remarkable heritage places, cultures and stories from around the world.",
  },
  {
    icon: Camera,
    title: "Identify",
    description:
      "Use visual intelligence to understand heritage architecture and landmarks.",
  },
  {
    icon: MessageCircle,
    title: "Ask",
    description:
      "Ask natural-language questions and receive answers grounded in available evidence.",
  },
  {
    icon: BookOpen,
    title: "Understand",
    description:
      "Go deeper into historical context, architecture and cultural significance.",
  },
  {
    icon: Map,
    title: "Explore",
    description:
      "Move from individual sites to a broader picture of cultural heritage.",
  },
  {
    icon: Sparkles,
    title: "Preserve",
    description:
      "Use technology to make heritage knowledge more accessible and engaging.",
  },
];

export default function Features() {
  const reduceMotion = useReducedMotion();

  return (
    <section className="relative py-24 sm:py-32">
      <div className="heritage-container">
        <div className="max-w-2xl">
          <div className="heritage-badge w-fit">
            <Sparkles
              className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            Heritage intelligence
          </div>

          <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.04em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
            Everything you need to
            <span className="heritage-gold-gradient"> explore heritage.</span>
          </h2>

          <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
            HeritageAI brings discovery, visual understanding and grounded
            historical knowledge together in one experience.
          </p>
        </div>

        <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => {
            const Icon = feature.icon;

            return (
              <motion.article
                key={feature.title}
                initial={{
                  opacity: 0,
                  y: reduceMotion ? 0 : 18,
                }}
                whileInView={{
                  opacity: 1,
                  y: 0,
                }}
                viewport={{
                  once: true,
                  amount: 0.15,
                }}
                transition={{
                  duration: reduceMotion ? 0 : 0.55,
                  delay: reduceMotion ? 0 : index * 0.06,
                }}
                whileHover={
                  reduceMotion
                    ? undefined
                    : {
                        y: -4,
                      }
                }
                className="heritage-glass rounded-[22px] p-5 transition-colors duration-300 hover:border-[var(--glass-border-strong)]"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.07)]">
                  <Icon
                    className="h-4 w-4 text-[var(--heritage-gold-light)]"
                    aria-hidden="true"
                  />
                </div>

                <h3 className="mt-5 text-base font-semibold text-[var(--heritage-ivory)]">
                  {feature.title}
                </h3>

                <p className="mt-2 text-sm leading-6 text-[var(--heritage-muted)]">
                  {feature.description}
                </p>
              </motion.article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
