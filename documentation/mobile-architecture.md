# HeritageAI Mobile Application Architecture

## 1. Product Position

HeritageAI Mobile is the primary consumer-facing HeritageAI application.

The existing web application remains the supporting web platform for:
- Public web discovery
- SEO
- Administrative workflows
- Web-based heritage exploration
- Documentation

The mobile application is not a direct visual copy of the website.

## 2. Mobile Application

Target workspace:

apps/mobile

Framework:

- React Native
- Expo
- TypeScript
- Expo Router

## 3. Core Application Areas

### Home
- Featured heritage
- Explore entry points
- Nearby heritage
- AI guide entry point

### Explore
- Heritage search
- Categories
- Countries
- Heritage cards
- Filters

### Heritage Detail
- Hero
- Quick facts
- About
- Historical timeline
- Sources and provenance
- Related heritage
- Location / map

### AI Heritage Guide
- Conversational heritage questions
- Historical explanations
- Story mode
- Future image understanding

### Map
- Nearby heritage
- Heritage location
- Map exploration

### Profile
- Authentication
- Saved heritage
- Preferences
- Account

## 4. Backend Integration

The mobile application uses the existing HeritageAI FastAPI backend.

Base backend:

apps/api

The mobile application must not directly connect to MySQL.

Architecture:

Mobile
→ API client
→ FastAPI
→ Application services
→ Database / AI infrastructure

## 5. State Management

Server state:

- TanStack Query

Client state:

- Zustand

Local persistence:

- Secure storage for authentication/session credentials
- Async local persistence for non-sensitive preferences/cache metadata

## 6. Navigation

Expo Router will provide file-based navigation.

Primary navigation:

- Home
- Explore
- Map
- AI Guide
- Profile

Nested routes will support:

/heritage/[siteId]

and future feature routes.

## 7. Design System

The mobile design system should inherit the HeritageAI visual identity while being designed specifically for touch interaction.

Design direction:

- Premium heritage aesthetic
- Dark-first interface
- Glass / translucent surfaces where appropriate
- Warm heritage accents
- Large readable typography
- Touch-friendly controls
- Subtle motion
- Accessible contrast

## 8. API Layer

Mobile API access must be centralized.

Recommended structure:

services/
  api/
  auth/
  heritage/

The UI must not construct raw API requests directly.

## 9. Feature Architecture

Mobile features should be organized by domain rather than by arbitrary UI component grouping.

Recommended:

src/
  app/
  components/
  features/
  services/
  store/
  hooks/
  lib/
  types/
  constants/

## 10. Security

Authentication credentials must never be hard-coded.

Sensitive session data must use secure device storage.

Environment-specific API configuration must not contain committed secrets.

## 11. Offline Strategy

Phase 1:
- Cache recently viewed heritage content
- Cache last successful API results where appropriate

Phase 2:
- Offline heritage detail access
- Offline maps / map metadata where technically appropriate

## 12. AI Boundary

The mobile application does not directly contain provider credentials.

AI requests flow through the HeritageAI backend.

Mobile
→ HeritageAI API
→ AI service provider

## 13. Media

Heritage media should be delivered through the backend/media infrastructure.

The mobile application should support:
- Remote image loading
- Caching
- Placeholder states
- Failure states

## 14. Maps

Map functionality should be isolated behind a map feature abstraction so the implementation can evolve without coupling the rest of the application to one map provider.

## 15. Testing

Required levels:

- Type checking
- Linting
- Unit tests for utilities/services
- Component tests for critical UI
- End-to-end testing for critical user journeys

## 16. Build Strategy

Development:

Expo development environment

Production:

Android and iOS application builds

## 17. Monorepo Integration

Mobile is an application workspace:

apps/mobile

Shared packages may be consumed where their contents are platform-safe.

Web-specific packages/components must not be imported into mobile.

## 18. Development Rule

Architecture first.

One feature at a time.

No unnecessary refactors.

No direct database access from mobile.

No hard-coded secrets.

Existing production web/API behavior must remain backward compatible.
