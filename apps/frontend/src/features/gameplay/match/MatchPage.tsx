import MatchChessBoard from '@/features/gameplay/match/components/MatchChessBoard'
import MatchControls from '@/features/gameplay/match/components/MatchControls'
import MatchMoveList from '@/features/gameplay/match/components/MatchMoveList'
import { useParams } from 'react-router'
import styled from 'styled-components'

enum evaluator {
  SHANNON = 'shannon',
  PLACEHOLDER = 'placeholder',
}

enum algorithm {
  MINIMAX = 'minimax',
  ALPHA_BETA = 'alpha-beta',
  MONTE_CARLO = 'monte-carlo',
  NEURAL_NETWORK = 'neural-network',
}

const Match = () => {
  const matchId = useParams().matchId

  return (
    <MatchContainer>
      <TechnicalInfoMatchItem>
        <div>
          <h2>Evaluator</h2>
          <ul>
            {Object.values(evaluator).map((evalOption) => (
              <li key={evalOption}>{evalOption}</li>
            ))}
          </ul>
        </div>
        <div>
          <h2>Algorithm</h2>
          <ul>
            {Object.values(algorithm).map((algoOption) => (
              <li key={algoOption}>{algoOption}</li>
            ))}
          </ul>
        </div>
      </TechnicalInfoMatchItem>
      <ChessBoardMatchItem>
        <MatchChessBoard />
      </ChessBoardMatchItem>
      <MatchControlsMatchItem>
        <MatchMoveList />
        <MatchControls />
      </MatchControlsMatchItem>
    </MatchContainer>
  )
}

export default Match

const MatchContainer = styled.div`
  display: flex;
  height: 100%;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 32px;
`

const MatchItem = styled.div`
  display: flex;
  height: 100%;
  padding: 18px 24px;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  background-color: #2c2c2c33;
  border-radius: 8px;
  border: 1px solid #2c2c2ccc;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
`

const TechnicalInfoMatchItem = styled(MatchItem)`
  flex: 1;
`

const ChessBoardMatchItem = styled(MatchItem)`
  max-height: calc(100vh - 112px);
  align-items: center;
  justify-content: center;
`

const MatchControlsMatchItem = styled(MatchItem)`
  flex: 2;
  align-items: center;
  justify-content: space-between;
`
