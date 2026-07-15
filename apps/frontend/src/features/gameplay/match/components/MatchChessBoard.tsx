import { Chessboard, type PieceDropHandlerArgs } from 'react-chessboard'

const MatchChessBoard = () => {
  return (
    <Chessboard
      options={{
        // Styling for the chessboard
        boardStyle: {
          borderRadius: '8px',
          justifyContent: 'center',
          alignItems: 'center',
          aspectRatio: '1 / 1',
        },
        squareStyle: { borderRadius: '8px' },
        lightSquareStyle: { backgroundColor: '#eeeeee' },
        lightSquareNotationStyle: { color: '#2c2c2c' },
        darkSquareStyle: { backgroundColor: '#2c2c2c00' },
        darkSquareNotationStyle: { color: '#eeeeee' },

        // Game data and behavior
        boardOrientation: 'black',
        allowDragging: true,
        onPieceDrop: (event: PieceDropHandlerArgs) => {
          const pieceSide = event.piece.pieceType.at(0)
          const pieceType = event.piece.pieceType.slice(1)

          console.log(
            `Piece ${pieceType} of side ${pieceSide} moved from ${event.sourceSquare} to ${event.targetSquare}`
          )

          return true
        },
      }}
    />
  )
}

export default MatchChessBoard
