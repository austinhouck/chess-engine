import { Link } from 'react-router'
import styled from 'styled-components'

export const NavBar = () => {
  return (
    <NavBarContainer>
      <Link to="/">Home</Link>
      <span>|</span>
      <Link to="/play">Play Chess!</Link>
    </NavBarContainer>
  )
}

const NavBarContainer = styled.div`
  width: 100%;
  min-height: 48px;
  max-height: 48px;
  background-color: #2e2e2e;
  color: white;
  padding: 16px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 16px;

  a {
    font-size: 16px;
    font-weight: bold;
    color: inherit;
    text-decoration: none;
  }

  span {
    color: #ababad;
  }
`

const NavLink = styled(Link)`
  font-size: 16px;
  font-weight: bold;
  color: inherit;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  &:hover {
    border-bottom: 2px solid white;
  }
  &:active {
    border-bottom: 2px solid white;
  }
`
