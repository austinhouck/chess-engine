import { index, route } from "@react-router/dev/routes"

export default [
  // Landing ('/')
  index('@/features/landing/Landing.tsx'),

  // Gameplay
  route('play', "@/features/gameplay/menu/Menu.tsx"),
  route('play/:matchId', "@/features/gameplay/match/Match.tsx"),
  route('play/:matchId/review', "@/features/gameplay/review/Review.tsx"),
]
