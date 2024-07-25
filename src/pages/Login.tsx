import LogoBoschEP from '../assets/imgs/boschEPLogo.svg';
import { FormLogin } from "../components/form_login/FormLogin";

export function Login(){
    return(
        <div className='container'>
            <div className='navbar'>
                <img className='imgBoschEP' src={LogoBoschEP} alt="BoschLogoEP" />
            </div>
               <FormLogin/>
        </div>
    )
}