import { env } from "@/config/env";

console.log("===== RUNTIME GOOGLE CONFIG =====");
console.log(
  "WEB:",
  env.googleWebClientId
    ? `PRESENT (${env.googleWebClientId.length} chars)`
    : "MISSING",
);
console.log(
  "ANDROID:",
  env.googleAndroidClientId
    ? `PRESENT (${env.googleAndroidClientId.length} chars)`
    : "MISSING",
);
console.log(
  "IOS:",
  env.googleIosClientId
    ? `PRESENT (${env.googleIosClientId.length} chars)`
    : "MISSING",
);
