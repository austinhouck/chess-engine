import '@/index.css'
import { CERoutes } from '@/Routes'
import { BrowserRouter } from 'react-router'

export function App() {
  return (
    <BrowserRouter>
      <CERoutes />
    </BrowserRouter>
  )
}

export default App
