import logo from './logo.svg';
import './index.css'
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import Login from './pages/loginPage/Login';
import { Route, Routes, BrowserRouter } from 'react-router-dom'
import Home from './pages/homePage/Home';
import { Accommodations } from './pages/accommodationsPage/Accommodations';
function App() {
  return (
    <>
      <BrowserRouter>

        <NavBar />
        <div className="pages">
          <Routes>

            <Route path='/' element={<Home />} />
            <Route path='/login' element={<Login />} />
            <Route path='/accommodations' element={<Accommodations/>}/>
      </Routes>
        </div>
      </BrowserRouter>
      <Footer />
    </>
  );
}

export default App;
