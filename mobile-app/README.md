# Career Finder Mobile (Expo)

A new Expo-managed companion app for iOS and Android that reuses the Supabase data and workflows from the Django web/CLI stack. Capture companies on the go, inspect roles, and keep application statuses in sync.

## Quick start
1. Copy `.env.example` to `.env` and fill in `SUPABASE_URL` and `SUPABASE_ANON_KEY` (the same values used by the Django app/CLI).
2. Install dependencies (Codespaces users can run this in a separate terminal):
   ```bash
   cd mobile-app
   npm install
   ```
3. Launch Expo:
   ```bash
   npm run start
   ```
   - Press `w` for the web preview or scan the QR code with Expo Go on a device.
4. Use the tabs:
   - **Dashboard** shows counts pulled directly from Supabase.
   - **Opportunities** lists companies with their roles and lets you update statuses inline.
   - **Capture** inserts new companies (name is the only required field).

## Shipping to the App Store / Play Store
- When you are ready to submit, run `npx expo prebuild` and follow Expo's build docs for EAS or native builds.
- The app pulls Supabase credentials from the compiled manifest (via `app.config.js`), so set production keys in your CI/CD secrets before building.
- Supabase RLS rules must allow the anon key to read/write the `companies` table and read from `roles`. Keep `status` and `notes` updateable for status tracking.

## Project structure
- `App.tsx` wires up bottom tabs for Dashboard, Opportunities, Capture, and Settings.
- `src/lib` contains Supabase initialization and theme tokens.
- `src/screens` contains the individual feature screens.
- `src/components` exposes reusable UI like the company card.

## Supabase tables expected
- `companies`: `id`, `company_name`, `url`, `career_page_url`, `notes`, `status`, `user_rank` (optional), plus any other metadata.
- `roles`: `id`, `company_id`, `role_title`, `role_link`, `salary`, `score`.
