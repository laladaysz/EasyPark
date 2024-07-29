import styles from './Monitoramento.module.css'
import { Modal } from '../modal/Modal'
import { useEffect, useState } from 'react'
import axios from 'axios';

interface StatusData {
    spot_id: number;
    status: string;
  }

export function Monitoramento(){
    const [statusData, setStatusData] = useState<Record<number, StatusData[]>>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    const [openModal, setOpenModal] = useState(false);
    const [selectedSpot, setSelectedSpot] = useState<StatusData | null>(null);


    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await axios.get<StatusData[]>('http://127.0.0.1:8000/api/status');
            const data = response.data;
    
            // Organizar os dados por vaga (spot_id)
            const organizedData = data.reduce<Record<number, StatusData[]>>((acc, item) => {
              if (!acc[item.spot_id]) {
                acc[item.spot_id] = [];
              }
              acc[item.spot_id].push(item);
              return acc;
            }, {});
    
            setStatusData(organizedData);
            setLoading(false);
          } catch (error) {
            setError(error as Error);
            setLoading(false);
            console.log(`Erro: ${error}`)
          }
        };
    
        fetchData();
        const intervalId = setInterval(fetchData, 5000);

        // Cleanup do intervalo
        return () => clearInterval(intervalId);
      }, []);

      if (loading) {
        return <div>Carregando...</div>;
      }
    
      if (error) {
        return <div>Erro: {error.message}</div>;
      }

      const handleOpenModal = (spot: StatusData) => {
        if (spot.status === 'Occupied') {
          setSelectedSpot(spot);
          setOpenModal(true);
        }

      };
    

  return(
        <>
        <div className={styles.container}>
            <div className={styles.content}>
                <div className={styles.title}>
                   <p><b>Selecione</b> a vaga que deseja</p><p><b>visualizar</b></p> 
                </div>
                <div className={styles.vagas_container}>
                    <hr /> 
                </div>
                <div className={styles.grid_linhas}>
                    {Object.keys(statusData).map((spotId) => (
                        <div className={styles.linha_vertical} key={spotId}>
                            {statusData[Number(spotId)].map((item, index) => (
                                <div key={index} className={styles.vaga_container}>
                                <button
                                    onClick={() => handleOpenModal(item)}
                                    className={`${item.status === 'Occupied' ? styles.occupied : ''} ${styles.vaga}`}
                                ></button>
                                <p className={styles.vaga_marcacao}>{`Vaga ${spotId}`}</p>
                                {/* <p className={styles.vaga_status}>{`Status: ${item.status}`}</p> */}
                            </div>
                            ))}
                        </div>
                      ))}
                    </div>
                    <Modal isOpen={openModal} onClose={() => setOpenModal(false)} data={selectedSpot}/>
                </div> 
            </div>
        </>
    )
}