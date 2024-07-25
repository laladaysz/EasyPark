import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Login } from './pages/Login';
import { Home } from './pages/Home';

function Routers(){
    return(
      <BrowserRouter>
        <Routes>
            <Route path='/' element={<Login/>}/>
            <Route path='/home' element={<Home/>}/>
            <Route path='*' element={<h1>Not Found</h1>}/>
        </Routes>
      </BrowserRouter>
    );
}

export default Routers;