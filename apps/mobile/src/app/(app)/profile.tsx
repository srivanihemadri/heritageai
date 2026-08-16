import { Button, StyleSheet, Text, View } from "react-native";

import { useAuthStore } from "@/store/auth-store";

export default function ProfileScreen() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Profile</Text>

      <Text>{user?.full_name ?? "HeritageAI User"}</Text>
      <Text>{user?.email ?? ""}</Text>

      <Button
        title="Sign out"
        onPress={() => {
          void logout();
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    gap: 12,
    padding: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
  },
});
