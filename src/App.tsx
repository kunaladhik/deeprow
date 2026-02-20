import { Routes, Route } from 'react-router-dom'
import Homepage from './pages/Homepage'
import Layout from './components/Layout'
import Login from './pages/Login'
import FileUpload from './pages/FileUpload'
import Analytics from './pages/Analytics'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/login" element={<Login />} />
      <Route element={<Layout />}>
        <Route path="/upload" element={<FileUpload />} />
        <Route path="/analytics" element={<Analytics />} />
      </Route>
    </Routes>
  )
}

export default App
