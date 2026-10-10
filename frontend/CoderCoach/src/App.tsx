import '@stylesheets/App.css'
import { HashRouter, Routes, Route } from 'react-router';
import Home from './pages/home.tsx' 
import ResponsePage from './pages/responsepage.tsx'

export default function App() {
  return (
        <HashRouter>
            <Routes>
                <Route path='/' element={<Home/>}/>
                <Route path='/response' element={<ResponsePage/>}/>
            </Routes>
        </HashRouter>
    )
}
