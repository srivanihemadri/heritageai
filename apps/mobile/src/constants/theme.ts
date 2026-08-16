import { Platform } from "react-native";

export const HeritageColors = {
  background: "#0B0907",
  backgroundElevated: "#14110E",
  surface: "rgba(31, 26, 20, 0.78)",
  surfaceStrong: "rgba(38, 31, 23, 0.92)",
  surfaceSoft: "rgba(255, 255, 255, 0.055)",

  ivory: "#F7F1E6",
  muted: "#B8AD9C",
  mutedDark: "#806F57",

  gold: "#D4AF5A",
  goldLight: "#F0CF7A",
  goldDark: "#9B7530",

  border: "rgba(212, 175, 90, 0.20)",
  borderStrong: "rgba(212, 175, 90, 0.38)",
  highlight: "rgba(255, 244, 214, 0.08)",

  success: "#7FA67C",
  warning: "#C89B5A",
  danger: "#B86B63",

  black: "#0B0907",
  white: "#FFFFFF",
} as const;

export const HeritageSpacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  xxxl: 32,
  section: 40,
} as const;

export const Spacing = {
  half: 2,
  one: 4,
  two: 8,
  three: 12,
  four: 16,
  five: 20,
  six: 24,
  seven: 28,
  eight: 32,
  ten: 40,
} as const;

export const HeritageRadius = {
  sm: 10,
  md: 14,
  lg: 18,
  xl: 22,
  glass: 26,
  pill: 999,
} as const;

export const HeritageTypography = {
  display: 34,
  title: 28,
  heading: 22,
  subheading: 18,
  body: 15,
  small: 13,
  caption: 11,
} as const;

export const Colors = {
  light: {
    text: HeritageColors.black,
    background: "#F7F1E6",
    backgroundElement: "#EFE7D9",
    backgroundSelected: "#E4D8C5",
    textSecondary: "#6E6558",
  },
  dark: {
    text: HeritageColors.ivory,
    background: HeritageColors.background,
    backgroundElement: HeritageColors.surfaceStrong,
    backgroundSelected: HeritageColors.surfaceSoft,
    textSecondary: HeritageColors.muted,
  },
} as const;

export type ThemeColor =
  keyof typeof Colors.light & keyof typeof Colors.dark;

export const Fonts = Platform.select({
  ios: {
    sans: "system-ui",
    serif: "ui-serif",
    rounded: "ui-rounded",
    mono: "ui-monospace",
  },
  default: {
    sans: "normal",
    serif: "serif",
    rounded: "normal",
    mono: "monospace",
  },
  web: {
    sans: "var(--font-display)",
    serif: "var(--font-serif)",
    rounded: "var(--font-rounded)",
    mono: "var(--font-mono)",
  },
});

export const BottomTabInset =
  Platform.select({
    ios: 50,
    android: 80,
  }) ?? 0;

export const MaxContentWidth = 800;
