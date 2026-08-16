import { Tabs } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import {
  HeritageColors,
  HeritageRadius,
} from "@/constants/theme";

export default function AppLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,

        tabBarActiveTintColor: HeritageColors.goldLight,
        tabBarInactiveTintColor: HeritageColors.mutedDark,

        tabBarStyle: {
          position: "absolute",
          left: 16,
          right: 16,
          bottom: 14,
          height: 68,
          borderRadius: HeritageRadius.glass,
          borderTopWidth: 1,
          borderWidth: 1,
          borderColor: HeritageColors.borderStrong,
          backgroundColor: "rgba(23, 20, 17, 0.94)",
          shadowColor: "#000000",
          shadowOffset: {
            width: 0,
            height: 12,
          },
          shadowOpacity: 0.32,
          shadowRadius: 24,
          elevation: 16,
        },

        tabBarLabelStyle: {
          fontSize: 10,
          fontWeight: "700",
          marginBottom: 5,
        },

        tabBarIconStyle: {
          marginTop: 4,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color, size }) => (
            <Ionicons
              name="home-outline"
              color={color}
              size={size}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="explore"
        options={{
          title: "Explore",
          tabBarIcon: ({ color, size }) => (
            <Ionicons
              name="compass-outline"
              color={color}
              size={size}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="ai"
        options={{
          title: "AI",
          tabBarIcon: ({ color, size }) => (
            <Ionicons
              name="sparkles-outline"
              color={color}
              size={size}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ color, size }) => (
            <Ionicons
              name="person-outline"
              color={color}
              size={size}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="map"
        options={{
          href: null,
        }}
      />

      <Tabs.Screen
        name="ai-guide"
        options={{
          href: null,
        }}
      />

      <Tabs.Screen
        name="ai-scanner"
        options={{
          href: null,
        }}
      />
    </Tabs>
  );
}
