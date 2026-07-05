import styled from 'styled-components'

const MatchControls = () => {
  return (
    <ControlsContainer>
      <ControlButton>{`❘⏴`}</ControlButton>
      <ControlButton>{`⏴`}</ControlButton>
      <ControlButton>{`⏵`}</ControlButton>
      <ControlButton>{`⏵❘`}</ControlButton>
    </ControlsContainer>
  )
}

export default MatchControls

const ControlsContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
`

const ControlButton = styled.button`
  color: #ffffff;
  font-size: 16px;
  font-weight: bold;
  background-color: #2c2c2c33;
  border: 1px solid #2c2c2ccc;
  border-radius: 8px;
  padding: 8px 16px;
  cursor: pointer;
  &:hover {
    background-color: #2c2c2c55;
  }
`
