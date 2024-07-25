import LogoBoschEP from '../../assets/imgs/boschEPLogo.svg'
import iconLogout from '../../assets/imgs/logoutIcon.svg'
import coresBosch from '../../assets/imgs/coresbosch.svg'
import './StylesHeader.css'

export function Header(){
    return(
        <div className='navbar'>
            <img className='imgBoschEP' src={LogoBoschEP} alt="BoschLogoEP" />
            <a className='linkLogout' href="/">
               <img className='imgLogout' src={iconLogout} alt="iconLogout" />
               <span className="nav-text">Logout</span>
            </a>
            <img src={coresBosch} alt="coresBosch" className="coresBosch" />
        </div>
    );
}