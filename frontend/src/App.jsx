import './index.css'
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import Login from './pages/loginPage/Login';
import VerificationPage from './pages/verificationPage/VerificationPage';
import { Route, Routes, BrowserRouter } from 'react-router-dom'
import Home from './pages/homePage/Home';
import Accommodation from './pages/individualAcc/Accommodation';
import BacklogView from './pages/verificationBacklog/BacklogView';
import { Accommodations } from './pages/accommodationsPage/Accommodations';
function App() {
  return (
    <>
      <BrowserRouter>

        <NavBar />
        <div className="pages">
          <Routes>
            <Route path='/verifications' element={<BacklogView />} />
            <Route path='/accommodation/:id' element={<Accommodation />} />
            <Route path='/' element={<Home />} />
            <Route path='/login' element={<Login />} />
            <Route path='/accommodations' element={<Accommodations/>}/>
            <Route path='/verification/:id' element={<VerificationPage />} />
      </Routes>
        </div>
      </BrowserRouter>
      <Footer />
    </>
  );
}

export default App;
