import '@/index.css'
import CERoutes from '@/Routes'
import { MotionConfig } from 'motion/react'
import { BrowserRouter } from 'react-router'

const App = () => {
  return (
    <MotionConfig>
      <BrowserRouter>
        <CERoutes />
      </BrowserRouter>
    </MotionConfig>
  )
}

export default App
