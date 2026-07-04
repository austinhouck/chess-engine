
import "@/index.css"
import { BrowserRouter, Outlet } from 'react-router'

export function App() {
  return (
    <BrowserRouter>
      <Outlet />
    </BrowserRouter>
  )
}

export default App
