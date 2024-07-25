import { useState } from "react";
import LogoIMG from '../../assets/imgs/easyParkLogo.svg';
import './StylesFormLogin.css';
//import { SignInButton } from "../SignInButton";

export function FormLogin() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    return (
        <div className='container-login'>
            <div className='wrap-login'>
                <form className='login-form'>
                    <span className='login-form-title'>
                        <img src={LogoIMG} alt="easyParkLogo" />
                    </span>
                    <span className="login-form-title">Bem-Vindo!</span>
                    <div className="login-form-subtitle">
                        <span className="text-subtitle1">Entre em nosso <strong>estacionamento</strong></span>
                    </div>
                    <div className="wrap-input">
                        <input
                            className={email !== "" ? 'has-val input' : 'input'}
                            type="email"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />
                        <span className="focus-input" data-placeholder='Usuário:'></span>
                    </div>
                    <div className="wrap-input">
                        <input
                            className={password !== "" ? 'has-val input' : 'input'}
                            type="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />
                        <span className="focus-input" data-placeholder='Senha:'></span>
                    </div>
                    <div className="container-login-form-btn">
                        <button className="login-form-btn">Entrar</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
