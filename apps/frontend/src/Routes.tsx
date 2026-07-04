import { Layout } from '@/components/Layout'
import { Route, Routes } from 'react-router'
import { Match } from './features/gameplay/match/MatchPage'
import { Menu } from './features/gameplay/menu/MenuPage'
import { Review } from './features/gameplay/review/ReviewPage'
import { Landing } from './features/landing/LandingPage'

export const CERoutes = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Landing />} />
        <Route path="play" element={<Menu />} />
        <Route path="play/:matchId" element={<Match />} />
        <Route path="play/:matchId/review" element={<Review />} />
      </Route>
    </Routes>
  )
}
