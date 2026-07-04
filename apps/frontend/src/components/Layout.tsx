import { NavBar } from '@/components/NavBar'
import { Outlet } from 'react-router'
import styled from 'styled-components'

export const Layout = () => {
  return (
    <LayoutContainer>
      <NavBar />
      <ContentContainer>
        <Outlet />
      </ContentContainer>
    </LayoutContainer>
  )
}

const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`

const ContentContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
`
