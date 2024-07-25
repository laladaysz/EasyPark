import { Header } from "../components/header/Header";
import { StatusContainers } from "../components/container_status/StatusContainers";
import { Monitoramento } from "../components/monitoramento/Monitoramento";

export function Home(){
    return(
        <>
        <Header/>
        <StatusContainers/>
        <Monitoramento/>
        </>
    )
}