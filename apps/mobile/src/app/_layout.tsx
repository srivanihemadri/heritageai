import { Stack, useSegments, useRouter } from "expo-router";
import { useEffect } from "react";

import { useAuthStore } from "@/store/auth-store";

export default function RootLayout() {
  const status = useAuthStore((state) => state.status);
  const initialize = useAuthStore((state) => state.initialize);

  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    void initialize();
  }, [initialize]);

  useEffect(() => {
    if (status === "loading") {
      return;
    }

    const firstSegment = segments[0];

    const inAuthGroup = firstSegment === "(auth)";
    const inAppGroup = firstSegment === "(app)";

    if (status === "unauthenticated" && !inAuthGroup) {
      router.replace("/(auth)/login");
      return;
    }

    if (status === "authenticated" && !inAppGroup) {
      router.replace("/(app)");
    }
  }, [status, segments, router]);

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(auth)" />
      <Stack.Screen name="(app)" />
    </Stack>
  );
}
