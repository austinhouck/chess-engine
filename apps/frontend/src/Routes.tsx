import { Route } from 'react-router'
import { Match } from './features/gameplay/match/MatchPage'
import { Menu } from './features/gameplay/menu/MenuPage'
import { Review } from './features/gameplay/review/ReviewPage'
import { Landing } from './features/landing/LandingPage'

export function Routes() {
  return (
    <>
      <Route index element={<Landing />} />
      <Route path="play" element={<Menu />} />
      <Route path="play/:matchId" element={<Match />} />
      <Route path="play/:matchId/review" element={<Review />} />
    </>
  );
}